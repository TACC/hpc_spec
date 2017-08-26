Summary: Fenics install

# Give the package a base name
%define pkg_base_name fenics
%define MODULE_VAR    FENICS

# Create some macros (spec file variables)
%define major_version 2017july
#%define minor_version 10
#%define micro_version 1

%define pkg_version %{major_version}
#.%{minor_version}.%{micro_version}

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

Release: 2%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tgz
URL: https://fenicsproject.org/
Vendor: Fenics project
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: FEniCS is a popular open-source (LGPLv3) computing platform for solving partial differential equations (PDEs). 
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: FEniCS is a popular open-source (LGPLv3) computing platform for solving partial differential equations (PDEs). 
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
FEniCS is a popular open-source (LGPLv3) computing platform for
solving partial differential equations (PDEs). 
FEniCS enables users to
quickly translate scientific models into efficient finite element
code. With the high-level Python and C++ interfaces to FEniCS, it is
easy to get started, but FEniCS offers also powerful capabilities for
more experienced programmers. FEniCS runs on a multitude of platforms
ranging from laptops to high-performance clusters.

%description %{MODULEFILE}
FEniCS is a popular open-source (LGPLv3) computing platform for
solving partial differential equations (PDEs). FEniCS enables users to
quickly translate scientific models into efficient finite element
code. With the high-level Python and C++ interfaces to FEniCS, it is
easy to get started, but FEniCS offers also powerful capabilities for
more experienced programmers. FEniCS runs on a multitude of platforms
ranging from laptops to high-performance clusters.

%prep

%setup -n fenics
#-%{version}

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

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

module load cmake boost python3 swig
module load gsl petsc phdf5
# trilinos : gives problems with the STKdoc_tests

%if "%{comp_fam}" == "gcc"
FENICS_C_COMPILER=gcc
FENICS_X_COMPILER=g++
%else
FENICS_C_COMPILER=icc
FENICS_X_COMPILER=icpc
%endif

export LOG_DIR=%{_topdir}/SPECS
export SRC_DIR=%{_topdir}/BUILD/fenics
export BUILD_DIR=%{_topdir}/BUILD/fenics
export FENICS_DIR=%{INSTALL_DIR}
export PYTHON_EXTRA_PATHS=

rm -f ${LOG_DIR}/fenics_install.log
. %{_topdir}/SPECS/fenics.install

cp -r %{INSTALL_DIR}/{fiat,instant,dijitso,ufl,ffc,eigen,dolfin,mshr} ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
cp -r %{INSTALL_DIR}/python ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The fenics module defines the environment variables:
TACC_FENICS_DIR for the location of the Fenics distribution, 
and PYTHONPATH. Fenics requires python3.

Version %{version}
]] )

whatis( "Name: Fenics" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://fenicsproject.org/" )
whatis( "Description: Fenics, finite element package" )

local             fenics_dir =     "%{INSTALL_DIR}/"
local             python_dir =     "${PYTHON_EXTRA_PATHS}"

prepend_path("PYTHONPATH",      python_dir )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"ufl","bin" )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"python","bin" )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"mshr","bin" )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"instant","bin" )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"fiat","bin" )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"ffc","bin" )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"dolfin","bin" )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenicsdir,"dijitso","bin" )
setenv("TACC_FENICS_DIR",        fenics_dir)
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Fenics %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Fri Aug 25 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: much LD_LIBRARY_PATH
* Fri Jul 28 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
