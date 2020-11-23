#
# Joe Allen
# 2017-09-04
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

%define shortsummary AutoDock Vina is an open-source program for doing molecular docking
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name autodock_vina
%define MODULE_VAR    AUTODOCK_VINA

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 1
%define patch_version 2

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
#%include system-defines.inc
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
%include name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
########################################

Release:   1
License:   Apache License 2.0
Group:     Applications/Life Sciences
URL:       http://vina.scripps.edu/
Packager:  TACC - wallen@tacc.utexas.edu
Source:    %{pkg_base_name}_%{major_version}_%{minor_version}_%{patch_version}.tgz
Patch1:    autodock_vina-1.1.2.patch

%package %{PACKAGE}
Summary: %{shortsummary}
Group:   Applications/Life Sciences
%description package
%{pkg_base_name}: %{shortsummary}

%package %{MODULEFILE}
Summary: The modulefile RPM
Group:   Lmod/Modulefiles
%description modulefile
Module file for %{pkg_base_name}

%description
%{pkg_base_name}: %{shortsummary}

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Comment this out if pulling from git
%setup -n %{pkg_base_name}_%{major_version}_%{minor_version}_%{patch_version}
# If using multiple sources. Make sure that the "-n" names match.
#%setup -T -D -a 1 -n %{pkg_base_name}-%{pkg_version}
%patch1 -p1

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
##################################
# If using build_rpm
##################################
%include compiler-load.inc
#%include mpi-load.inc
#%include mpi-env-vars.inc
##################################
# Manually load modules
##################################
# module load
module load boost/1.64
##################################

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

cd build/linux/release/

make GPP=g++ \
     BASE=$TACC_BOOST_DIR \
     BOOST_VERSION=1_64 \
     LDFLAGS="-L$TACC_BOOST_LIB" \
     LIBS="-lboost_system -lboost_thread -lboost_serialization -lboost_filesystem -lboost_program_options" \
     C_PLATFORM=""
     #CFLAGS="%{TACC_OPT}" \

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp ./vina ./vina_split $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
#chmod -R a+rx $RPM_BUILD_ROOT%{INSTALL_DIR}/bin

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
The %{pkg_base_name} module file defines the following environment variables:

 - TACC_%{MODULE_VAR}_DIR
 - TACC_%{MODULE_VAR}_BIN

for the location of the %{pkg_base_name} distribution.

Documentation: %{url}

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Computational Biology, Chemistry, Structural Biology, Docking, Small Molecule, Protein")
whatis("Description: %{shortsummary}")
whatis("URL: %{url}")

prepend_path("PATH",		"%{INSTALL_DIR}/bin")

setenv("TACC_%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_BIN",	"%{INSTALL_DIR}/bin")

prereq("boost/1.64")
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
