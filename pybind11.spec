#
# Spec file for PYBIND11:
# interface generator utility 
# which is always too old for trilinos
#
# Victor Eijkhout, 2017
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

Summary:    Set of tools for manipulating geographic and Cartesian data sets

# Give the package a base name
%define pkg_base_name pybind11
%define MODULE_VAR    PYBIND11

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2
%define micro_version 4

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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

Release:   1%{?dist}
License:   GNU
Group:     Development/Tools
Vendor:     Pybind11
Group:      Libraries/maps
Source:	    pybind11-%{version}.tar.gz
URL:	    https://pybind1111.readthedocs.io/en/latest/
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: PYBIND11 install
Group: System Environment/Base
%description package
PYBIND11 exposes C++11 functionality to Python


%package %{MODULEFILE}
Summary: PYBIND11 install
Group: System Environment/Base
%description modulefile
PYBIND11 exposes C++11 functionality to Python

%description
PYBIND11 exposes C++11 functionality to Python

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
# Load Compiler
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

module load cmake python3

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
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
  
SPEC_DIR=`pwd`/../SPECS

#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}


#wget -nc --quiet https://github.com/pybind11/pybind1111/archive/v%{version}.tar.gz

find . -name pybind11\*cmake

####
#### pybind1111
####
PYBIND11_SRC=`pwd`
PYBIND11_INSTALL=%{INSTALL_DIR}
PYBIND11_BUILD=/tmp/pybind11-build
rm -rf ${PYBIND11_BUILD}
mkdir -p ${PYBIND11_BUILD}
pushd ${PYBIND11_BUILD}

( \
cmake \
    -D CMAKE_INSTALL_PREFIX=${PYBIND11_INSTALL} \
    -D PYTHON_EXECUTABLE=`which python3` \
    -D PYBIND11_INSTALL=ON \
    -D PYBIND11_TEST=OFF \
    -D OLD_CONFIG_FILES=0 \
   ${PYBIND11_SRC} \
&& make \
&& find . -name pybind11\*cmake \
&& sed -i \
       -e '/cmake_install.cmake/s/\/opt/-\/opt/' \
       Makefile \
&& make install || /bin/true \
) || /bin/true
echo "really done make install" \

# export nomake="\
#     -D PYBIND11_MASTER_PROJECT=ON \
#     -D PYBIND11_EXPORT_NAME=OFF \
#     "

popd

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

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
Python bindings to C++11. This module provides variables
TACC_PYBIND11_DIR, TACC_PYBIND11_INC, and TACC_PYBIND11_SHARE.
It also update the CMAKE_PREFIX_PATH.

Version %{version}
]] )

whatis( "Python bindings for C++11" )
whatis( "Version: %{version}" )
whatis( "Category: Development/Tools" )
whatis( "Description: PYBIND11 exposes C++11 functionality to Python" )
whatis( "URL: https://pybind1111.readthedocs.io/en/latest/" )

local pybind11_dir = "%{INSTALL_DIR}"

setenv("TACC_PYBIND11_DIR", pybind11_dir )
setenv("TACC_PYBIND11_INC", pathJoin(pybind11_dir,"include" ) )
setenv("TACC_PYBIND11_SHARE", pathJoin(pybind11_dir,"share" ) )
append_path( "CMAKE_PREFIX_PATH", pathJoin( pybind11_dir,"share","cmake","pybind11" ) )
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
* Mon Jun 10 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
