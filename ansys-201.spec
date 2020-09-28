#
# Si Liu
# 2020-07-13
#

# Give the package a base name
%define pkg_base_name ansys
%define MODULE_VAR    ANSYS

# Create some macros (spec file variables)
%define major_version 20.1

%define pkg_version %{major_version}

Summary: ANSYS spec file
Release: 1%{?dist}
License: ANSYS License
Vendor: ANSYS
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

%package %{PACKAGE}
Summary: ANSYS package RPM
Group: Applications
%description package
Ansys Software Solutions Provide Fast, Accurate Results Across Every Area Of Physics. 

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Ansys Software Solutions Provide Fast, Accurate Results Across Every Area Of Physics. 

%description
Ansys Software Solutions Provide Fast, Accurate Results Across Every Area Of Physics. 

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
# mount -t tmpfs tmpfs %{INSTALL_DIR}
  
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
TACC’s current ANSYS license allows TACC users to access ANSYS for non-commercial, academic use. 
If you would like access to ANSYS, please submit a help desk ticket through the TACC portal. 
https://portal.tacc.utexas.edu/

This license is for ACAMEDIC USE ONLY!

ANSYS has been installed under /home1/apps/ANSYS on Frontera and Stampede2.
including the main components: "Structures", "Fluids" and "Electronics".
All packages are installed under the default locations based on the ANSYS name convention.
You should be able to find ANSYS binaries and shared libraries under the following directories.

/home1/apps/ANSYS/v201
/home1/apps/ANSYS/AnsysEM20.1

For more information about using ANSYS on TACC systems, please read:
https://portal.tacc.utexas.edu/software/ansys

For scientific or technical questions, please contact the ANSYS support:.
https://support.ansys.com/portal/site/AnsysCustomerPortal

Version 2020R1 (20.1)
]]
)

whatis("Name: ANSYS")
whatis("Version: 20.1")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Physics")
whatis("URL: https://www.ansys.com/")
whatis("Description: ANSYS 20.1")

setenv ("TACC_ANSYS_DIR", "/home1/apps/ANSYS")
setenv ("ANSYS_DIR","/home1/apps/ANSYS")

--License file
local UserHome=os.getenv("HOME")
setenv("ANSYSLMD_LICENSE_FILE", pathJoin(UserHome,".tacc_ansys_license") ) 

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
