#
# Stephen Lien Harrell
# 2019-05-15
#

# Give the package a base name
%define pkg_base_name abaqus
%define MODULE_VAR    ABAQUS

# Create some macros (spec file variables)
%define major_version 2019

%define pkg_version %{major_version}

Summary: Abaqus spec file
Release: 1%{?dist}
License: Abaqus License
Vendor: Simulia
Group: Utility
Source: %{name}-%{version}.tar.gz
Packager:  TACC - sharrell@tacc.utexas.edu

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
Summary: Abaqus package RPM
Group: Applications
%description package
Abaqus is a software suite for finite element analysis and computer-aided engineering.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Abaqus is a software suite for finite element analysis and computer-aided engineering.

%description
Abaqus is a software suite for finite element analysis and computer-aided engineering.

%define HOME1 /home1/apps
%define OPT /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{HOME1}/%{pkg_base_name}/%{version}
%define MODULE_DIR  %{OPT}/%{MODULES}/%{pkg_base_name}

%define ABAQUS_GROUP "G-813612"

%define BUILD_ROOT ${RPM_BUILD_ROOT}
# Make sure only certain users can access this

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# %setup -n %{pkg_base_name}_%{pkg_version}
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



%build
echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------


  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


# This module expects all 5 Abaqus 2019 golden file under /tmp, they are identified in the Dassault Systems website as:
# SIMULIA Abaqus Extended Products (Abaqus, Isight, Tosca & fe-safe and Documentation) - Abaqus 2019 Golden - AllOS

# example SCP from staff.frontera as root
# scp /scratch1/01623/sharrell/2019* build:/rpms-sdb1/jail-7.6-3.10.0-957.27.2/tmp/


rm -rf /tmp/DSY*
cd /tmp
for f in /tmp/2019.AM_SIM_Abaqus_Extend.AllOS*.tar; do tar xfv "$f"; done


rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/*
export RPM_BUILD_ROOT=$RPM_BUILD_ROOT
RPM_BUILD_ROOT=$RPM_BUILD_ROOT echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
" > config_options

/tmp/AM_SIM_Abaqus_Extend.AllOS/4/SIMULIA_EstablishedProducts/Linux64/1/StartTUI.sh --silent ./config_options

#printf "*****************************************************************\n\n\n\nInstall directory (copy and paste): $RPM_BUILD_ROOT/%{INSTALL_DIR}\n\nLicense Server: 27000@license02.tacc.utexas.edu\n\n\n\n*****************************************************************"



rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/commands/*
ln -s %{INSTALL_DIR}/linux_a64/code/bin/ABQLauncher  $RPM_BUILD_ROOT/%{INSTALL_DIR}/commands/abq2019
ln -s %{INSTALL_DIR}/commands/abq2019 $RPM_BUILD_ROOT/%{INSTALL_DIR}/commands/abaqus


rm -rf /tmp/AM_SIM_Abaqus_Extend.AllOS
rm -rf /tmp/DSY*

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------




# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  # rm -rf  $RPM_BUILD_ROOT/%MODULE_DIR
  mkdir -p $RPM_BUILD_ROOT/%MODULE_DIR
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
  
# Write out the modulefile associated with the application

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message=[[
The TACC ABAQUS module appends the path to the abaqus executables
to the PATH environment variable.  Also TACC_ABAQUS_DIR, and
TACC_ABAQUS_BIN are set to ABAQUS home and command directories.

In order to use ABAQUS on TACC resources, UT Austin users will need to submit a ticket requesting to be added to the "ABAQUS" group.

Information on running ABAQUS and using other license servers can be found at:
https://portal.tacc.utexas.edu/software/abaqus

This the ABAQUS 2019 release.

Version %{version}
]]


whatis("Version: %{pkg_version}")
whatis("Category: application, engineering")
whatis("Keywords: finite element analysis, computer-aided engineering")
whatis("URL: https://www.3ds.com/")
whatis("Description: Abaqus is a software suite for finite element analysis and computer-aided engineering.")
help(help_message,"\n")


local group = %{ABAQUS_GROUP}
found = userInGroup(group)


local err_message = [[
You do not have access to ABAQUS!

In order to use ABAQUS on TACC resources, UT Austin users will need to submit a ticket requesting to be added to the "ABAQUS" group.

Information on running ABAQUS can be found at:
https://portal.tacc.utexas.edu/software/abaqus
]]


if (found) then
local abaqus_dir="%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(abaqus_dir, "commands"))
prepend_path(    "LD_PRELOAD",          "/home1/apps/tacc-patches/getcwd-patch.so")
setenv( "TACC_%{MODULE_VAR}_DIR",       abaqus_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(abaqus_dir, "commands"))

else
  LmodError(err_message,"\n")
end

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

  %defattr(640, root, %{ABAQUS_GROUP}, 750)
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

