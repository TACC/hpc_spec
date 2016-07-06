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

# Give the package a base name
%define pkg_base_name wgrib2
%define MODULE_VAR    wgrib2
%define SOURCE_NAME   grib2

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 0
%define micro_version 4

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc
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
License:   BSD
Group:     applications/io
Source:    %{SOURCE_NAME}.tgz
Patch1:    wgrib_makefile.patch
URL:       www.cpc.ncep.noaa.gov/products/wesley/wgrib2/
Distribution: Source
Vendor:    NOAA
Packager:  TACC - cazes@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Modulefile for wgrib2.

%description
wgrib2 is a program to manipulate, inventory and decode GRIB files.  It can also:
*  inventory and read grib2 files
*  create subsets
*  create regional subsets by cookie cutter or projections
*  export to ieee, text, binary and CSV
*  export to netcdf and mysql
*  write grib2 fields like averages, accumulations, max/min values
*  convert grid-relative to earth relative winds
*  convert U and V to wind speed, direction
*  write new grib2 fields

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{SOURCE_NAME}
#cd grib2
%patch1 -p0 


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
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc


# Insert further module commands
module load netcdf/3.6.3

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  # Create temporary directory for the install.  We need this to
  mkdir -p             %{INSTALL_DIR}
#  mount -t tmpfs tmpfs %{INSTALL_DIR}
  #tacctmpfs --mount %{INSTALL_DIR}

  
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
  
  %if "%{is_intel}" == "1" || "%{is_intel13}" == "1" || "%{is_intel16}" == "1"
  
  	# environment used for configure with intel compiler
          export CFLAGS="-O3"
          export FFLAGS="-O3"
          export CXXFLAGS="-O3"
  %endif
  

  pwd
#No configure for this package
#  ./configure --prefix=%{INSTALL_DIR} 
#Although, we must patch the makefile
#Build the software
  make 


  # Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
  # place for the rest of the RPM.  Then, unmount the tmpfs.
  #Make a bin directory for wgrib2
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  cp wgrib2/wgrib2 $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
#  umount %{INSTALL_DIR}
  #tacctmpfs --umount %{INSTALL_DIR}

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
--netcdf

local help_message = [[
The %{pkg_base_name} module file defines the following environment variables:

TACC_WGRIB2_DIR 
TACC_WGRIB2_BIN

for the location of the wgrib2 binary.  The TACC_WGRIB2_BIN directory will be added to your path.

Version %{version}

]]

help(help_message,"\n")


whatis("wgrib2")
whatis("Version: %{version}")
whatis("Category: tool,I/O")
whatis("Keywords: I/O, tool")
whatis("Description: Application manage and convert grib files.")
whatis(" URL: www.cpc.ncep.noaa.gov/products/wesley/wgrib2 ")

--Prepend paths
prepend_path("PATH",           "%{INSTALL_DIR}/bin")

--Env variables 
setenv("TACC_WGRIB2_DIR", "%{INSTALL_DIR}")
setenv("TACC_WGRIB2_BIN", "%{INSTALL_DIR}/bin")

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
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

