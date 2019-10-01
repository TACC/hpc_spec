#
# Si Liu
# 2019-9-24
#

# Give the package a base name
%define pkg_base_name mcr
%define MODULE_VAR    MCR

# Create some macros (spec file variables)
%define major_version 9
%define minor_version 7
%define pkg_version %{major_version}.%{minor_version}

Summary: Matlab Compiler Runtime (MCR)
Release: 1%{?dist}
License: Mathworks License
Vendor: Mathworks
Group: Utility
Source: %{name}-%{version}.tar.gz
Packager:  TACC - siliu@tacc.utexas.edu

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%define APPS /home1/apps/
%define MODULES modulefiles

%package %{PACKAGE}
Summary: The package RPM
Group: Matlab 
%description package
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile

%description



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
  mkdir -p %{INSTALL_DIR}
##  mount -t tmpfs tmpfs %{INSTALL_DIR}
  
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

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

Version v9.7
]]
)

whatis("Name: MCR")
whatis("Version: v9.7")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab v9.7 Compiler Runtime from MathWorks")

append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.7/bin/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.7/runtime/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.7/sys/os/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.7/sys/java/jre/glnxa64/jre/lib/amd64/server")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.7/sys/java/jre/glnxa64/jre/lib/amd64")

setenv ("TACC_MCR_DIR", "/home1/apps/mcr/9.7")

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
