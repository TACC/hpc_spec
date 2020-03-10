#
# Spec file for TRNG:
# C++ linear algebra library
#
# Victor Eijkhout, 2019
# based on:
#
# Bar.spec, 
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary:    Tina's Random Number Generator

# Give the package a base name
%define pkg_base_name trng
%define MODULE_VAR    TRNG

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 21
# %define micro_version 4

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc
#%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   2%{?dist}
License:   GNU
Group:     Development/Tools
Vendor:     Tuxfamily
Group:      Development/Numerical-Libraries
Source:	    trng-%{version}.tar.gz
URL:	    https://numbercrunch.de/trng/
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Trng is a C++ library for random number generation.
Group:      Development/Numerical-Libraries
%description package
Tina's Random Number Generator

%package %{MODULEFILE}
Summary: Trng is Tina's Random Number Generator
Group:      Development/Numerical-Libraries
%description modulefile
Tina's Random Number Generator

%description 
Tina's Random Number Generator


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------



#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
module purge
# Load Compiler
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

# Insert further module commands
# module load boost 

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
export TRNG_SRC_DIR=`pwd`
export TRNG_INSTALL_DIR=%{INSTALL_DIR}

#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
./configure --prefix=${TRNG_INSTALL_DIR}
make
make install

cp -r doc examples ${TRNG_INSTALL_DIR}
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
umount tmpfs

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
Tina's Random Number Generator Library.

Module %{name} loads environmental variables defining
the location of TRNG directory, libraries, and binaries:
TACC_TRNG_DIR 
TACC_TRNG_INC TACC_TRNG_LIB
TACC_TRNG_SHARE

Version: %{version}
]] )

whatis( "TRNG" )
whatis( "Version: %{version}" )
whatis( "Category: system, development" )
whatis( "Keywords: Random number generation, C++" )
whatis( "Description: C++ template library for random number generation" )
whatis( "URL: https://numbercrunch.de/trng/" )

local version =  "%{version}"
local trng_dir =  "%{INSTALL_DIR}"

setenv("TACC_TRNG_DIR",trng_dir)
setenv("TACC_TRNG_INC",pathJoin( trng_dir,"include" ) )
setenv("TACC_TRNG_LIB",pathJoin( trng_dir,"lib" ) )
setenv("TACC_TRNG_SHARE",pathJoin( trng_dir,"share" ) )

prepend_path ("PATH",pathJoin( trng_dir,"share" ) )
prepend_path ("LD_LIBRARY_PATH",pathJoin( trng_dir,"lib" ) )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for %{name} version %{version}
##
set ModulesVersion "%version"
EOF

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Mar 05 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: better description in module help, remove bin definition
* Thu May 16 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
