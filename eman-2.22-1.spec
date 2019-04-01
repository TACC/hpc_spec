#
# Joe Allen
# 2019-03-11
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

Summary: EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM

# Give the package a base name
%define pkg_base_name eman
%define MODULE_VAR    EMAN

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 22
#%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
#%include python-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc
#%include name-defines-noreloc-python.inc
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

Release:   1
License:   GPLv2
Group:     Applications/Life Sciences
URL:       http://blake.bcm.tmc.edu/EMAN2/
Packager:  TACC - wallen@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Applications/Life Sciences
%description package
EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM

%package %{PACKAGE}-python
Summary: The package RPM
Group: Applications/Life Sciences
%description package-python
EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM

%package %{PACKAGE}-mkllibs
Summary: The package RPM
Group: Applications/Life Sciences
%description package-mkllibs
EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM

%description
EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#%setup -n %{pkg_base_name}-%{pkg_version}

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
#%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc
# Load Python Library
#%include python-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  #mkdir -p $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
  
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
  
  module purge
  module load TACC
  module unload python2

  # And/or create some dummy directories and files for fun
  echo "TACC_OPT %{TACC_OPT}"
  echo "MODULE_DIR %{MODULE_DIR}"
  echo "INSTALL_DIR %{INSTALL_DIR}"
  echo "RPM_BUILD_ROOT $RPM_BUILD_ROOT"

  wget https://cryoem.bcm.edu/cryoem/static/software/release-2.22/eman2.22.linux64.sh
  #bash eman2.22.linux64.sh -b -f -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

  bash eman2.22.linux64.sh -b -f -p /opt/apps/eman/2.22
  mv /opt/apps/eman/2.22/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/envs
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/examples
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/man
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/mkspecs
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/pkgs
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/recipes
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/test
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/utils
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/var


  
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  #mkdir -p $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

# Modulefile Help Message
HELP_MSG=$(cat << EOM
This module file defines the following environment variables:

 - TACC_%{MODULE_VAR}_DIR
 - TACC_%{MODULE_VAR}_BIN

for the location of the EMAN2 distribution.

To use all of the features of e2display.py, you may need to connect through a
VNC session as described in the Lonestar5 user guide:

https://portal.tacc.utexas.edu/user-guides/lonestar5

Documentation: %{url}

Version %{version}
EOM
)

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << EOF
help([[${HELP_MSG}]])

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: computational biology, chemistry")
whatis("Keywords: Computational Biology, Chemistry, Structural Biology, Image Processing, Image Reconstruction, CryoEM")
whatis("Description: EMAN2 is a scientific image processing suite for single particle reconstruction from cryoEM")
whatis("URL: %{url}")

setenv("TACC_%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_BIN",     "%{INSTALL_DIR}/bin")
prepend_path("PATH", "%{INSTALL_DIR}/bin")

EOF

  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module3.1.1#################################################
##
## version file for %{pkg_base_name}%{version}
##
set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
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
  %exclude %{INSTALL_DIR}/lib/python2.7 
  %exclude %{INSTALL_DIR}/lib/libmkl*

%files package-python

  %defattr(-,root,install,)
  %{INSTALL_DIR}/lib/python2.7

%files package-mkllibs

  %defattr(-,root,install,)
  %{INSTALL_DIR}/lib/libmkl*

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

