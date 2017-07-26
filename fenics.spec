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
URL: http://fenics.sandia.gov/
Vendor: Sandia National Labs
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Fenics is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Fenics is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
The Fenics Project is an effort to develop algorithms and enabling
technologies within an object-oriented software framework for the
solution of large-scale, complex multi-physics engineering and
scientific problems. A unique design feature of Fenics is its focus
on packages.

Each Fenics package is a self-contained, independent piece of
software with its own set of requirements, its own development team
and group of users. Because of this, Fenics itself is designed to
respect the autonomy of packages. Fenics offers a variety of ways
for a particular package to interact with other Fenics packages. It
also offers a set of tools that can assist package developers with
builds across multiple platforms, generating documentation and
regression testing across a set of target platforms. At the same time,
what a package must do to be called a Fenics package is minimal, and
varies with each package.
%description %{MODULEFILE}
The Fenics Project is an effort to develop algorithms and enabling
technologies within an object-oriented software framework for the
solution of large-scale, complex multi-physics engineering and
scientific problems. A unique design feature of Fenics is its focus
on packages.

Each Fenics package is a self-contained, independent piece of
software with its own set of requirements, its own development team
and group of users. Because of this, Fenics itself is designed to
respect the autonomy of packages. Fenics offers a variety of ways
for a particular package to interact with other Fenics packages. It
also offers a set of tools that can assist package developers with
builds across multiple platforms, generating documentation and
regression testing across a set of target platforms. At the same time,
what a package must do to be called a Fenics package is minimal, and
varies with each package.

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

module load cmake boost python3

export LOG_DIR=%{_topdir}/SPECS
export FENICS_DIR=%{INSTALL_DIR}
export PYTHON_EXTRA_PATHS=

rm -f ${LOG_DIR}/fenics_install.log
. %{_topdir}/SPECS/fenics.install

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The fenics module defines the following environment variables:
TACC_FENICS_DIR, TACC_FENICS_BIN, and
TACC_FENICS_LIB for the location
of the Fenics distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Fenics" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/fenics/fenics-as/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             fenics_arch =    "${architecture}"
local             fenics_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(fenics_dir,fenics_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,fenics_arch,"lib") )

setenv("FENICS_ARCH",            fenics_arch)
setenv("FENICS_DIR",             fenics_dir)
setenv("TACC_FENICS_DIR",        fenics_dir)
setenv("TACC_FENICS_BIN",        pathJoin(fenics_dir,fenics_arch,"bin") )
setenv("TACC_FENICS_INC",        pathJoin(fenics_dir,fenics_arch,"include") )
setenv("TACC_FENICS_LIB",        pathJoin(fenics_dir,fenics_arch,"lib") )
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

module unload python
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Fri Jun 30 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: fix broken stuff that trips up dealII
* Fri May 12 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
