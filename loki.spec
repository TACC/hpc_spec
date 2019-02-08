#
# Spec file for LOKI:
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
%define pkg_base_name loki
%define MODULE_VAR    LOKI

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 1
%define micro_version 7

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
Vendor:    Loki
Group:      Development/tools
Source:	    loki-%{version}.tar.gz
URL:	    http://loki.com/
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: LOKI install
Group: System Environment/Base
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: LOKI install
Group: System Environment/Base
%description modulefile
This is the long description for the modulefile RPM...

%description
LOKI offers C++11 functionality to environments that don't have that. Yeah right.

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
  
module load cmake 

if [ "${TACC_FAMILY_COMPILER}" = "intel" ] ; then
  export CC="icc -qopenmp -DYADE_OPENMP"
  export CXX="icpc -qopenmp -DYADE_OPENMP -std=c++98"
  export FC="ifort -qopenmp -DYADE_OPENMP"
else
  export CC="gcc -fopenmp -DYADE_OPENMP"
  export CXX="g++ -fopenmp -DYADE_OPENMP -std=c++98"
  export FC="gfortran -fopenmp -DYADE_OPENMP"
fi

cp %{SPEC_DIR}/victor_scripts/loki.makefile.common.${TACC_FAMILY_COMPILER} Makefile.common
make

cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
Simplified Wrapper and Interface Generator
This module loads loki.
The command directory is added to PATH.
The include directory is added to INCLUDE.
The lib     directory is added to LD_LIBRARY_PATH.

Version %{version}
]] )

whatis( "Simplified Wrapper and Interface Generator" )
whatis( "Version: %{version}" )
whatis( "Category: Development/Tools" )
whatis( "Description: LOKI is a software development tool that provides C++11 functionality" )
whatis( "URL: http://www.loki.org" )

local loki_dir = "%{INSTALL_DIR}"

prepend_path( "PATH", pathJoin( loki_dir,"bin" ) )
setenv("TACC_LOKI_DIR", loki_dir )
setenv("TACC_LOKI_BIN", pathJoin(loki_dir,"bin" ) )
setenv("TACC_LOKI_INC", pathJoin(loki_dir,"include" ) )
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
* Fri Dec 28 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
