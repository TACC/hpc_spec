Summary: P4est install

# Give the package a base name
%define pkg_base_name p4est
%define MODULE_VAR    P4EST

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 1%{?dist}
License: GPL
Vendor: https://github.com/cburstedde/p4est
#Source1: p4est-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{major_version}.%{minor_version}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: P4est local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: P4est local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
P4EST is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description %{MODULEFILE}
P4EST is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.

%prep

%setup -n p4est-%{version}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
%include mpi-defines.inc
module purge
%include compiler-load.inc
%include mpi-load.inc

export P4EST_DIR=`pwd`

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#### from http://p4est.github.io/api/index.html :
# A typical development configure line looks as follows:
# relative/path/to/configure CFLAGS="-Wall -O0 -g" --enable-mpi --enable-debug
# A typical production configure line looks as follows:
# relative/path/to/configure CFLAGS="-Wall -O2" --enable-mpi

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
# cp -r * %{INSTALL_DIR}
# pushd %{INSTALL_DIR}

%if "%{comp_fam}" == "gcc"
  module load mkl
#  export MKLROOT=/opt/intel/compilers_and_libraries_2017.2.174/linux/mkl
  #VLE complaint about .a not being portable. I haven't tried this .so version yet.
  export BLASOPTIONS="-Wl,--start-group $MKLROOT/lib/intel64/libmkl_intel_lp64.so $MKLROOT/lib/intel64/libmkl_sequential.so $MKLROOT/lib/intel64/libmkl_core.so -Wl,--end-group -lpthread -lm"
  export BLASFLAG=
%else
  export BLASOPTIONS=
  export BLASFLAG=-mkl
%endif
mpicc -show
./configure \
    --prefix=%{INSTALL_DIR}/ \
    CC=mpicc CFLAGS="%{TACC_OPT} -g ${BLASFLAG}" \
    CXX=mpicxx CXXFLAGS="%{TACC_OPT} -g ${BLASFLAG}" \
    FC=mpif90 FCLAGS="-O2 -g ${BLASFLAG}" \
    F77=mpif77 FFLAGS="-O2 -g ${BLASFLAG}" \
    LIBS="${BLASOPTIONS}" \
    --enable-mpi \
    && make && make install

echo "after installation:"
ls %{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r doc example src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/
# popd

umount %{INSTALL_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The P4EST modulefile defines the following environment variables:
TACC_P4EST_DIR, TACC_P4EST_LIB, and TACC_P4EST_INC 
for the location of the P4EST %{version} distribution, 
libraries, and include files, respectively.\n

Version %{p4estversion}
]] )

whatis( "Name: P4est 'p4-est of octrees'" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${p4estversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://github.com/cburstedde/p4est" )
whatis( "Description: octree support for dealii" )

local             p4est_dir =     "%{INSTALL_DIR}"

prepend_path("LD_LIBRARY_PATH", pathJoin(p4est_dir,"lib") )
prepend_path("PATH", pathJoin(p4est_dir,"bin") )

setenv(          "P4EST_DIR",             p4est_dir)
setenv(          "TACC_P4EST_DIR",        p4est_dir)
setenv(          "TACC_P4EST_BIN",        pathJoin(p4est_dir,"bin"))
setenv(          "TACC_P4EST_INC",        pathJoin(p4est_dir,"include"))
setenv(          "TACC_P4EST_LIB",        pathJoin(p4est_dir,"lib"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${version} << EOF
#%Module1.0#################################################
##
## version file for P4est %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jun 03 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
