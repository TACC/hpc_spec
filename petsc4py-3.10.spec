#
# Spec file for Petsc4py
#

Summary: Petsc4py install

# Give the package a base name
%define pkg_base_name petsc4py
%define MODULE_VAR    PETSC4PY

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 10

%define pkg_version %{major_version}.%{minor_version}
%define wgetversion 3.10.1

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include python-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home2.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 2%{?dist}
License: GPL
Vendor: Lisandro Dalcin
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
URL: https://bitbucket.org/petsc/petsc4py/
Source0: %{pkg_base_name}-%{wgetversion}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Petsc4py local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Petsc4py local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
PETSC4PY is the python interface to petsc
%description %{MODULEFILE}
PETSC4PY is the python interface to petsc

%prep 

%setup -n petsc4py-%{wgetversion}

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
%include python-defines.inc

%include compiler-load.inc
%include mpi-load.inc
%include python-load.inc

echo %{PYTHON_INSTALL_DIR}
if [ -z "%{PYTHON_INSTALL_DIR}" ] ; then
  echo "No PYTHON INSTALL DIR defined"
  exit 1
fi

module avail petsc

export PETSC4PY_DIR=`pwd`
rm -rf $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}

# same as in petsc
export dynamiccc="i64 debug i64debug complexi64 complexi64debug uni unidebug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

for ext in \
  single "" \
  ${dynamiccc} ${dynamiccxx} ; do

module list
module avail petsc
export architecture=skylake
if [ -z "${ext}" ] ; then
  module load petsc/%{version}
else
  module load petsc/%{version}-${ext}
  export architecture=${architecture}-${ext}
fi

pwd
python setup.py build
python setup.py install --prefix=${RPM_BUILD_DIR}/%{PYTHON_INSTALL_DIR}

module unload petsc

## Module files for petsc4py

mkdir -p %{PYTHON_MODULE_DIR}

if [ -z "${ext}" ] ; then
  export moduleversion=%{version}
else
  export moduleversion=%{version}-${ext}
fi

echo "writing module file for python ${TACC_PYTHON_VER}, petsc ${moduleversion}"

cat > $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/${moduleversion}.lua << EOF
help( [[
The PETSC4PY modulefile defines the following environment variables:
TACC_PETSC4PY_DIR
for the location of the PETSC4PY %{version} distribution;
it also updates PYTHONPATH.

Version ${moduleversion}
]] )

whatis( "Name: Petsc4py" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${moduleversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://bitbucket.org/petsc/petsc4py/" )
whatis( "Description: python interface to PETSc" )

local             petsc_arch =    "${architecture}"
local             petsc4py_dir =     "%{PYTHON_INSTALL_DIR}"

prepend_path("PYTHONPATH", pathJoin(petsc4py_dir,"lib","python${TACC_PYTHON_VER}","site-packages") )

setenv(          "TACC_PETSC4PY_DIR",        petsc4py_dir)

prereq("petsc/${moduleversion}")
EOF

cat > $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/.version.${moduleversion} << EOF
#%Module1.0##################################################
##
## version file for petsc4py
##
 
set     ModulesVersion      "${moduleversion}"
EOF

###%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{modulefileroot}/${moduleversion}.lua

done

#cp -r %{PYTHON_INSTALL_DIR}            $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/
echo %{PYTHON_INSTALL_DIR}
cp -r demo docs src test *.rst  $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/

%files %{PACKAGE}
  %defattr(755,root,install)
  %{PYTHON_INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(755,root,install)
  %{PYTHON_MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 06 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: using new python infrastructure
* Mon Nov 19 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial build
