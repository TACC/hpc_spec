#
# W. Cyrus Proctor
# 2015-11-12
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
%define pkg_base_name mathematica 
%define MODULE_VAR    MATHEMATICA

# Create some macros (spec file variables)
%define major_version 12
%define minor_version 1

%define pkg_version %{major_version}.%{minor_version}
%define underscore_version %{major_version}_%{minor_version}

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

Release:   1%{?dist}
License:   proprietary
Group:     system library
URL:       https://www.wolfram.com/mathematica
Packager:  TACC - vtrueheart@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
Wolfram Mathematica (usually termed Mathematica) is a modern technical
computing system spanning most areas of technical computing - including neural
networks, machine learning, image processing, geometry, data science,
visualizations, and others.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Wolfram Mathematica (usually termed Mathematica) is a modern technical
computing system spanning most areas of technical computing - including neural
networks, machine learning, image processing, geometry, data science,
visualizations, and others.


%description
Wolfram Mathematica (usually termed Mathematica) is a modern technical
computing system spanning most areas of technical computing - including neural
networks, machine learning, image processing, geometry, data science,
visualizations, and others.

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

  # Nothing to do here 

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
local help_msg=[[
Wolfram Mathematica (usually termed Mathematica) is a modern technical
computing system spanning most areas of technical computing - including neural
networks, machine learning, image processing, geometry, data science,
visualizations, and others.

Please do not run mathematica on a login node.

To run Mathematica interactively, use idev to get a compute node,
then execute one of these commands:

$ math          # command-line (text-based) interface
$ mathematica   # graphical interface (requires X11 or equivalent)

Documentation is available at wolfram.com/mathematica.

The %{MODULE_VAR} module also defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BASE, and TACC_%{MODULE_VAR}_BIN 
for the location of the %{MODULE_VAR} distribution, binaries, and tools respectively.
The module also prepends TACC_%{MODULE_VAR}_BIN to PATH.

Version %{version}
]]

help(help_msg)

-- Create environment variables.
local mathematica_base = "/home1/apps/mathematica"
local version          = "%{version}"

local mathematica_dir  = pathJoin( mathematica_base, version      )
local mathematica_bin  = pathJoin( mathematica_dir, "Executables" )

whatis( "Name: Mathematica" )
whatis( "Version: "..version )
whatis( "Category: mathematics" )
whatis( "Keywords: Mathematics, Symbolic, Tools" )
whatis( "Description: commercial technical computing system" )
whatis( "URL: wolfram.com/mathematica" )

setenv( "MATHEMATICA_BASE",     mathematica_base )
setenv( "TACC_MATHEMATICA_DIR", mathematica_dir  )
setenv( "TACC_MATHEMATICA_BIN", mathematica_bin  )

prepend_path( "PATH",           mathematica_bin  )

EOF

 
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{pkg_base_name}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  ### don't check the hidden one!
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

