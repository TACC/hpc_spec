#
# Si Liu
# 08-15-2019
#

# Give the package a base name
%define pkg_base_name sanitytool
%define MODULE_VAR    SANITYTOOL

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 6
%define pkg_version %{major_version}.%{minor_version}

Summary: SanityTool
Release: 1%{?dist}
License: TACC
Vendor: TACC
Group: TACC-HPC-TOOL
Source: %{name}-%{version}.tar.gz
Packager:  TACC - siliu@tacc.utexas.edu

%include rpm-dir.inc
%include name-defines-noreloc.inc

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
Group: TACC-HPC-TOOL
%description package
SanityTool 1.6 by Si Liu and Robert McLay
Texas Advanced Computing Center

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

  cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT/%{INSTALL_DIR} 
 
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
The module loads TACC SanityTool for you.
Version: 1.6

You can run the command "sanitycheck" to examine your current environment settings on Stampede2.
If you encounter any problems, please send an email to siliu@tacc.utexas.edu with your user id and error messages.
Please also contact siliu@tacc.utexas.edu, if you have any other concerns or require additional tests.


]]
)

whatis("Name: SanityTool")
whatis("Version: 1.6")
whatis("Category: TACC HPC Tools")

local sanitypath = "/opt/apps/sanitytool/1.6"
append_path("PATH",sanitypath)
setenv("TACC_SANITYTOOL_DIR", "/opt/apps/sanitytool/1.6")

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
