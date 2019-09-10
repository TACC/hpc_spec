#
# Joe Garcia
# 2019-02-07
# changing lib version to 2018.4.0.574913 bc update 4 has a patch that should 
# with the problems users and Mccalpin have been experiencing #2019-02-07 
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
%define pkg_base_name vtune 
%define MODULE_VAR    VTUNE

# Create some macros (spec file variables)
%define major_version 18
%define minor_version 0
%define micro_version 2

%define lib_version 2018.4.0.574913 

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
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

Release:   2%{?dist}
License:   proprietary
Group:     PROFILER
URL:       https://software.intel.com/en-us/intel-vtune-amplifier-xe
Packager:  TACC - jgarcia@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
This is specifically an rpm for the Intel vtune modulefile
used on Stampede2.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
This is specifically an rpm for the Intel vtune modulefile
used on Stampede2.

%description
This is specifically an rpm for the Intel vtune modulefile
used on Stampede2.

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
local vtune_dir   = "/opt/intel/vtune_amplifier_%{lib_version}"

whatis( "Name: vtune" )
whatis( "Version: %{version}" )
whatis( "Category: performance analysis" )
whatis( "Keywords: System, Utility, Tools" )
whatis( "Description: Intel VTune Amplifier" )
whatis( "URL: https://software.intel.com/en-us/intel-vtune-amplifier-xe" )

prepend_path(     "PATH", pathJoin( vtune_dir, "bin64"   )   )

setenv( "TACC_VTUNE_DIR", vtune_dir                          )
setenv( "TACC_VTUNE_BIN", pathJoin( vtune_dir, "bin64"   )   )
setenv( "TACC_VTUNE_LIB", pathJoin( vtune_dir, "lib64"   )   )
setenv( "TACC_VTUNE_INC", pathJoin( vtune_dir, "include" )   )

--setenv("VTUNE_AMPLIFIER_2019_DIR","/opt/intel/vtune_amplifier_2019.4.0.597835")
--setenv("VT_ADD_LIBS","-ldwarf -lelf -lvtunwind -lm -lpthread")
--setenv("VT_ARCH","intel64")
--setenv("VT_LIB_DIR","/opt/intel/itac/2019.4.036/intel64/lib")
--setenv("VT_MPI","impi4")
--setenv("VT_ROOT","/opt/intel/itac/2019.4.036")
--setenv("VT_SLIB_DIR","/opt/intel/itac/2019.4.036/intel64/slib")

help(
[[

VTune is Intel's signature performance profiling tool.

For detailed info, consult the extensive documentation in
$TACC_VTUNE_DIR/documentation or online at
software.intel.com/en-us/intel-vtune-amplifier-xe.

COLLECTION
**********

First, compile with "-g".

To collect data on an executable named main.exe,
using a collection named "hotspots", execute the following
command on a compute node:

   amplxe-cl -collect hotspots -- main.exe

Note the "--" followed by a space.

This will generate a directory with a name like 'r000hs' or 'r000ah'
("hs" means "hotspots";  "ah" means "advanced-hotspots").
It will also print a brief summary report to stdout.

You can reduce the sampling rate to use less memory,
reduce collection time,  and generate smaller database files.
To reduce the sampling rate to 15ms (default is 1-4ms):

   amplxe-cl -collect hotspots -knob sampling-interval=15 -- main.exe

ANALYSIS AND REPORTING
**********************

Assuming a collection directory named "r000hs".
From a login or compute node with X11:

   amplxe-gui r000hs

There are also text-based command-line analysis and report utilities.

ENVIRONMENT VARIABLES
*********************

This modulefile defines TACC_VTUNE_DIR, TACC_VTUNE_BIN, TACC_VTUNE_LIB,
and TACC_VTUNE_INC in the usual way.  It also preprends VTune's bin64
directory to $PATH.

To see the exact effect of loading the module, execute "module show vtune".

Version %{version}
]]
)

EOF
 
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
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

