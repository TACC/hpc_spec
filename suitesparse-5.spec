Summary: Suitesparse install

# Give the package a base name
%define pkg_base_name suitesparse
%define MODULE_VAR    SUITESPARSE

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 8
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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
Vendor: https://github.com/cburstedde/suitesparse
#Source1: suitesparse-setup.sh
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{pkg_version}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Suitesparse local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Suitesparse local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
%description %{MODULEFILE}

%prep

%setup -n suitesparse-%{version}

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
%if "%{comp_fam}" == "gcc"
    module load mkl
%endif

export SUITESPARSE_DIR=`pwd`

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
cp -r * %{INSTALL_DIR}
pushd %{INSTALL_DIR}

export SUITESPARSE_SRC=`pwd`
################
cp %{_topdir}/SOURCES/SuiteSparse_config.mk SuiteSparse_config/
%if "%{comp_fam}" == "intel"
    export CC="icc -qopenmp -fPIC"
    export CXX="icpc -qopenmp -fPIC"
    export FC="ifort -qopenmp -fPIC"
%else
    export CC=gcc; export CXX=g++; export FC=gfortran
%endif

echo && echo "%%%% metis %%%%" && echo
( cd metis-5.1.0 && \
  make config prefix=../lib && make && make install && \
  cp build/lib/lib/libmetis* ../lib/
)

# problems: SLIP_LU
for d in SuiteSparse_config \
    AMD BTF CAMD CCOLAMD COLAMD CHOLMOD \
    CSparse CXSparse LDL Mongoose RBio  SPQR \
    ; do
  echo "%%%% Installing package $d %%%%"
  ( cd $d && make AUTOCC="yes" ARCHIVE="ar cr" ) ;
done
################

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
# cp -r doc example src test $RPM_BUILD_ROOT/%{INSTALL_DIR}/
popd
umount %{INSTALL_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The SUITESPARSE modulefile defines the following environment variables:
TACC_SUITESPARSE_DIR, TACC_SUITESPARSE_LIB, and TACC_SUITESPARSE_INC 
for the location of the SUITESPARSE %{version} distribution, 
libraries, and include files, respectively.\n

Version %{suitesparseversion}
]] )

whatis( "Name: Suitesparse 'p4-est of octrees'" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${suitesparseversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://github.com/DrTimothyAldenDavis/SuiteSparse" )
whatis( "Description: suite of sparse solvers" )

local             suitesparse_dir =     "%{INSTALL_DIR}"

prepend_path("LD_LIBRARY_PATH", pathJoin(suitesparse_dir,"lib") )
prepend_path("PATH", pathJoin(suitesparse_dir,"bin") )

setenv(          "SUITESPARSE_DIR",             suitesparse_dir)
setenv(          "TACC_SUITESPARSE_DIR",        suitesparse_dir)
setenv(          "TACC_SUITESPARSE_BIN",        pathJoin(suitesparse_dir,"bin"))
setenv(          "TACC_SUITESPARSE_INC",        pathJoin(suitesparse_dir,"include"))
setenv(          "TACC_SUITESPARSE_LIB",        pathJoin(suitesparse_dir,"lib"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${version} << EOF
#%Module1.0#################################################
##
## version file for Suitesparse %version
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
* Mon Jan 04 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
