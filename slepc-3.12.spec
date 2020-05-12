#
# Spec file for SLEPc
#

Summary: Slepc install

# Give the package a base name
%define pkg_base_name slepc
%define MODULE_VAR    SLEPC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 12
%define micro_version 0
%define versionpatch 3.12.0

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
Vendor: Universitat Politecnica De Valencia http://www.grycap.upv.es/slepc/
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{versionpatch}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

#---------------------------------------
%package %{PACKAGE}
#---------------------------------------
Summary: Slepc local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Slepc local binary install
Group: System Environment/Base

#---------------------------------------
%description
#---------------------------------------
%description %{PACKAGE}
SLEPC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description %{MODULEFILE}
SLEPC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.

#---------------------------------------
%prep 
#---------------------------------------

#---------------------------------------
%setup -n slepc-%{versionpatch}
#---------------------------------------

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

%include compiler-load.inc
%include mpi-load.inc

module avail petsc

export SLEPC_DIR=`pwd`
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
cp -r * %{INSTALL_DIR}
pushd %{INSTALL_DIR}
export SLEPC_DIR=`pwd`

# same as in petsc
export dynamiccc="i64 debug i64debug complex complexdebug complexi64 complexi64debug uni unidebug"
export dynamiccxx="cxx cxxdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

for ext in \
  single "" \
  ${dynamiccc} ; do

export architecture=clx
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

mkdir -p %{MODULE_DIR}

if [ -z "${ext}" ] ; then
  export moduleversion=%{version}
else
  export moduleversion=%{version}-${ext}
fi

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${moduleversion}.lua << EOF
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

whatis( "Name: SLEPc" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${moduleversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www.grycap.upv.es/slepc/" )
whatis( "Description: Scalable Library for Eigen Problem Computations, Library of eigensolvers" )

local             petsc_arch =    "${architecture}"
local             slepc_dir =     "%{INSTALL_DIR}"

prepend_path("LD_LIBRARY_PATH", pathJoin(slepc_dir,petsc_arch,"lib") )

setenv(          "SLEPC_DIR",             slepc_dir)
setenv(          "TACC_SLEPC_DIR",        slepc_dir)
setenv(          "TACC_SLEPC_LIB",        pathJoin(slepc_dir,petsc_arch,"lib"))
setenv(          "TACC_SLEPC_INC",        pathJoin(slepc_dir,petsc_arch,"include"))
setenv(          "SLEPC_VERSION",         "${moduleversion}")
setenv(          "TACC_SLEPC_VERSION",    "${moduleversion}")

depends_on("petsc/${moduleversion}")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${moduleversion} << EOF
#%Module1.0##################################################
##
## version file for slepc
##
 
set     ModulesVersion      "${moduleversion}"
EOF

###%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{modulefileroot}/${moduleversion}.lua

done ## end of for ext loop

cp -r docs include lib src \
    $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r clx* \
    $RPM_BUILD_ROOT/%{INSTALL_DIR}

popd
umount %{INSTALL_DIR}

echo "Directory to package up: $RPM_BUILD_ROOT/%{INSTALL_DIR}"
echo "listing:"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

%files %{PACKAGE}
  %defattr(755,root,install)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(755,root,install)
  %{MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Oct 05 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial build
