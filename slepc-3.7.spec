#
# Spec file for SLEPc
#
%define slepcversion 3.7
%define patchlevel .2

Summary: Slepc local binary install
Name: slepc
Version: %{slepcversion}
Release: 1
License: GPL
Vendor: http://www.grycap.upv.es/slepc/
Group: Universitat Politecnica De Valencia
Source: slepc-%{version}%{patchlevel}.tar.gz
Packager: eijkhout@tacc.utexas.edu 

%define debug_package %{nil}
%global _python_bytecompile_errors_terminate_build 0

%define APPS /opt/apps
%define HOMEAPPS /home1/apps
%define MODULES modulefiles

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define slepc_install_dir %{HOMEAPPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define modulefileroot  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%package -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-modulefiles
Summary: SLEPc local binary install
Group: Numerical library

%package -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-software
Summary: SLEPc local binary install
Group: Numerical library

%description
%description -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-modulefiles
SLEPC is a package of eigensolvers, built on top of petsc
%description -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-software
SLEPC is a package of eigensolvers, built on top of petsc

%prep 
rm -rf $RPM_BUILD_ROOT/%{slepc_install_dir}
mkdir -p $RPM_BUILD_ROOT/%{slepc_install_dir}

%setup -n slepc-%{version}%{patchlevel}

%build

%install

%include compiler-load.inc
%include mpi-load.inc

#module load python cmake
module unload python
module load cmake

#
# configure/install loop; also modulefiles
#
export SLEPC_DIR=`pwd`
mkdir -p $RPM_BUILD_ROOT/%{slepc_install_dir}
mkdir -p $RPM_BUILD_ROOT/%{modulefileroot}

# # we no longer provide static versions. 
# # leaving these definitions just in case
# export static="cxxstatic cxxstaticdebug static staticdebug "
# export nostatic="complexstatic complexstaticdebug cxxcomplexstatic cxxcomplexstaticdebug"

# export dynamic="debug cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug"
# export nodynamic="complex complexdebug cxxcomplexshared cxxcomplexshareddebug"

# same as in petsc
export dynamiccc="debug uni unidebug i64 i64debug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

%if "%{is_intel12}" == "1"
# not yet built for pgi
module load mkl/10.3 arpack
export arpackline="--with-arpack=1 --with-arpack-dir=${TACC_ARPACK_LIB} \
    --with-arpack-flags=\"-lparpack,-larpack\""
%else
export arpackline=
%endif

for ext in \
  single "" \
  ${dynamiccc} ${dynamiccxx} ; do

export architecture=sandybridge
if [ -z "${ext}" ] ; then
  module load petsc/%{version}
else
  module load petsc/%{version}-${ext}
  export architecture=${architecture}-${ext}
fi

pwd
python config/configure.py ${arpackline}
make || /bin/true

module unload petsc

## Module files for slepc

mkdir -p $RPM_BUILD_ROOT/%{modulefileroot}

if [ -z "${ext}" ] ; then
  export moduleversion=%{version}
else
  export moduleversion=%{version}-${ext}
fi

cat > $RPM_BUILD_ROOT/%{modulefileroot}/${moduleversion}.lua << EOF
help( [[
The SLEPC modulefile defines the following environment variables:
TACC_SLEPC_DIR, TACC_SLEPC_LIB, and TACC_SLEPC_INC 
for the location of the SLEPC %{version} distribution, 
libraries, and include files, respectively.\n

Usage:
    include \$(SLEPC_DIR)/conf/slepc_common
(Alternatively:
    include \$(SLEPC_DIR)/conf/slepc_variables
    include \$(SLEPC_DIR)/conf/slepc_rules
) in your makefile, then compile
    \$(CC) -c yourfile.c \$(PETSC_INCLUDE)
and link with
    \$(CLINKER) -o yourprog yourfile.o \$(SLEPC_LIB)

Version ${moduleversion}
]] )

whatis( "Name: Scalable Library for Eigen Problem Computations (SLEPc)" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${moduleversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www.grycap.upv.es/slepc/" )
whatis( "Description: Library of eigensolvers" )

local             petsc_arch =    "${architecture}"
local             slepc_dir =     "%{slepc_install_dir}"

prepend_path("LD_LIBRARY_PATH", pathJoin(slepc_dir,petsc_arch,"lib") )

setenv(          "SLEPC_DIR",             slepc_dir)
setenv(          "TACC_SLEPC_DIR",        slepc_dir)
setenv(          "TACC_SLEPC_LIB",        pathJoin(slepc_dir,petsc_arch,"lib"))
setenv(          "TACC_SLEPC_INC",        pathJoin(slepc_dir,petsc_arch,"include"))
setenv(          "SLEPC_VERSION",         "${moduleversion}")
setenv(          "TACC_SLEPC_VERSION",    "${moduleversion}")

prereq("petsc/${moduleversion}")
EOF

cat > $RPM_BUILD_ROOT/%{modulefileroot}/.version.${moduleversion} << EOF
#%Module1.0##################################################
##
## version file for slepc
##
 
set     ModulesVersion      "${moduleversion}"
EOF

###%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{modulefileroot}/${moduleversion}.lua

done


mkdir -p $RPM_BUILD_ROOT/%{slepc_install_dir}

cp -r sandybridge*          $RPM_BUILD_ROOT/%{slepc_install_dir}/
cp -r docs include lib src $RPM_BUILD_ROOT/%{slepc_install_dir}/

%files -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-software
%defattr(755,root,install)
%{slepc_install_dir}

%files -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-modulefiles
%defattr(755,root,install)
%{modulefileroot}

%post
%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jul 20 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial build
