#
# W. Cyrus Proctor
# 2015-11-07
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

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name cmake
%define MODULE_VAR    CMAKE

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 13
%define micro_version 4

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   BSD
Group:     System/Utils
URL:       http://www.cmake.org
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
CMake  is an extensible, open-source system that manages the build process in
an operating system and in a compiler-independent manner. Unlike many cross-
platform systems, CMake is designed to be used in conjunction with the native
build environment. Simple configuration files placed in each source directory
(called CMakeLists.txt files) are used to generate standard build files (e.g.,
makefiles on Unix and projects/workspaces in Windows MSVC) which are used in
the usual way.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
CMake  is an extensible, open-source system that manages the build process in
an operating system and in a compiler-independent manner. Unlike many cross-
platform systems, CMake is designed to be used in conjunction with the native
build environment. Simple configuration files placed in each source directory
(called CMakeLists.txt files) are used to generate standard build files (e.g.,
makefiles on Unix and projects/workspaces in Windows MSVC) which are used in
the usual way.

%description
CMake  is an extensible, open-source system that manages the build process in
an operating system and in a compiler-independent manner. Unlike many cross-
platform systems, CMake is designed to be used in conjunction with the native
build environment. Simple configuration files placed in each source directory
(called CMakeLists.txt files) are used to generate standard build files (e.g.,
makefiles on Unix and projects/workspaces in Windows MSVC) which are used in
the usual way.


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

%setup -n %{pkg_base_name}-%{pkg_version}


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

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
 
  export CC=gcc
  export ncores=24
  export CFLAGS="-mtune=generic"
  #export LDFLAGS="-Wl,-rpath,${GCC_LIB} -march=core-avx -mtune=core-avx2" # Location of correct libstdc++.so.6
  export LDFLAGS="-mtune=generic" # Location of correct libstdc++.so.6
  echo ${LD_LIBRARY_PATH}
  echo ${LDFLAGS}
  # DO NOT preppend $RPM_BUILD_ROOT in prefix
  ./bootstrap --prefix=%{INSTALL_DIR}
  make -j ${ncores}
  make DESTDIR=$RPM_BUILD_ROOT install -j ${ncores}
  
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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message = [[
CMake is an open-source, cross-platform family of tools designed to build, test
and package software. CMake is used to control the software compilation process
using simple platform and compiler independent configuration files, and
generate native makefiles and workspaces that can be used in the compiler
environment of your choice. 

This module defines the environmental variables TACC_%{MODULE_VAR}_BIN
and TACC_%{MODULE_VAR}_DIR for the location of the main CMake directory
and the binaries.

The location of the binary files is also added to your PATH.

Extended documentation on CMake can be found under $TACC_%{MODULE_VAR}_DIR/doc.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: system, utilities")
whatis("Keywords: System, Utility")
whatis("Description: tool for generation of files from source")
whatis("URL: http://www.cmake.org")

-- Export environmental variables
local cmake_dir="%{INSTALL_DIR}"
local cmake_bin=pathJoin(cmake_dir,"bin")
setenv("TACC_CMAKE_DIR",cmake_dir)
setenv("TACC_CMAKE_BIN",cmake_bin)

-- Prepend the cmake directories to the adequate PATH variables
prepend_path("PATH",cmake_bin)

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

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

