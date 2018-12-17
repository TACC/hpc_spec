#
# Ian Wangl, Si Liu
# 2018-11-05
#
# PROGRAMMING_MODE should be changed to build all three different
# versions of OpenSees.

Summary: OpenSees - Local TACC Build

# Give the package a base name
%define pkg_base_name opensees
%define MODULE_VAR    OPENSEES

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
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

Release:   1%{?dist}
License:   LGPL
Group:     Applications/Geoscience
URL:       http://opensees.berkeley.edu/
Packager:  TACC - iwang@tacc.utexas.edu, siliu@tacc.utexas.edu
Source:    %{pkg_base_name}-%{major_version}.%{minor_version}.%{micro_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Applications/Geoscience
%description package
This is the long description for the package RPM...
This package is a software framework for developing applications 
to simulate the performance of structural and geotechnical 
systems subjected to earthquakes. 

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
This package is a software framework for developing applications 
to simulate the performance of structural and geotechnical 
systems subjected to earthquakes. 

%description
This package is a software framework for developing applications 
to simulate the performance of structural and geotechnical 
systems subjected to earthquakes. 


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

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------


rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}

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
local help_msg=[[
The %{MODULE_VAR} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_BIN for
the location of the %{name} distribution, 
libraries, and excutables,respectively. 
It also appends the path to the executables
to the PATH environment variable.

The %{year_stamp}.%{month_stamp} is appended to the 
version number due to the rapid development on going.
We use the date to distinguish the version for now.

The excutables of %{MODULE_VAR} include:

OpenSees	Sequential version
OpenSeesSP	Parallel version in master-worker mode
OpenSeesMP	Parallel version for parameter studies

Version %{pkg_version}
]]

--help(help_msg)
help(help_msg)

whatis("OpenSees: Open System for Earthquake Engineering Simulation")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: application, geoscience")
whatis("Keywords: Earthquake, Simulation")
whatis("Description: Software framework for developing applications to simulate the performance of structural and geotechnical systems subjected to earthquakes")
whatis("URL: http://opensees.berkeley.edu/")
prereq("petsc/3.10")


%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local opensees_dir           = "/work/projects/wma_apps/lonestar5/opensees/opensees-3.0.0"

family("opensees")
prepend_path(    "PATH",                pathJoin(opensees_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_DIR",                opensees_dir)
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(opensees_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(opensees_dir, "bin"))
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

