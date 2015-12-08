#
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

Summary: A Nice little relocatable skeleton spec file example.

# Notes - this modulefile is based on the cray provided RPM 
#         cray-libhugetlbfs-2.16-1.0502.9469.5.1
#         CRF 2015.12.03

# Give the package a base name
%define pkg_base_name craytools
%define MODULE_VAR    craytools

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0
%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc                  
%include name-defines.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:  1
License:  GPL
Group:    System
URL:      https://www.tacc.utexas.edu
Packager: TACC - carlos@tacc.utexas.edu
Source:   %{pkg_base_name}-%{pkg_version}.tar.gz
NoSource: 0

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%define BUILD_PACKAGE 0

%package %{PACKAGE}
Summary: Cray tools associated to ALPS
Group: System
%description package
Cray tools associated to ALPS

%package %{MODULEFILE}
Summary: Modulefile for Cray tools associated to ALPS
Group: Lmod/Modulefiles
%description modulefile
Modulefile for Cray tools associated to ALPS

%description
Cray tools associated to ALPS

#---------------------------------------
%prep
#---------------------------------------

%if %{?BUILD_PACKAGE}
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n %{pkg_base_name}-%{pkg_version}
%endif # BUILD_PACKAGE |

%if %{?BUILD_MODULEFILE}
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif # BUILD_MODULEFILE |


#---------------------------------------
%build
#---------------------------------------

#---------------------------------------
%install
#---------------------------------------

# Setup modules
module purge
%include system-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  ##### Create TACC Canary Files ########
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  ##### Create TACC Canary Files ########
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local helpMsg=[[
 This module provides the functionallity tipically associated to the 
 alps cray module. The following commands will be available from any 
 service or compute node:

   xtnodestat
   xtnodeadmin

 Version 1.0
]]

help(helpMsg)

whatis("Name: Cray ALPS tools ")
whatis("Version: 1.0 ")
whatis("Category: System ")
whatis("Description: Cray ALPS tools ")

prepend_path("PATH","/opt/cray/eslogin/eswrap/1.1.0-1.020200.1231.0/bin")
prepend_path("PATH","/opt/cray/alps/5.2.3-2.0502.9295.14.14.ari/bin")
prepend_path("PATH","/opt/cray/alps/5.2.3-2.0502.9295.14.14.ari/sbin")
prepend_path("LD_LIBRARY_PATH","/opt/cray/alps/5.2.3-2.0502.9295.14.14.ari/lib64")
prepend_path("CRAY_LD_LIBRARY_PATH","/opt/cray/alps/5.2.3-2.0502.9295.14.14.ari/lib64")

family("craytools")
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

%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}
  %{INSTALL_DIR}/bin

%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
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

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

