#
# Si Liu
# 2019-08-11
#

Summary:ls-dyna - Local TACC Build

# Give the package a base name
%define pkg_base_name ls-dyna
%define MODULE_VAR    LSDYNA

# Create some macros (spec file variables)
%define major_version 11
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
License:   Oasys
Group:     Applications/Finite Element
URL:       https://www.oasys-software.com/dyna/software/ls-dyna/
Packager:  TACC - siliu@tacc.utexas.edu
Source:    %{pkg_base_name}-%{major_version}.%{minor_version}.%{micro_version}-%{year_stamp}.%{month_stamp}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: The package RPM
Group: Applications/Geoscience
%description package
LS-DYNA is a general-purpose finite element program capable of simulating complex real world problems. It is used by the automobile, aerospace, construction, military, manufacturing, and bioengineering industries. LS-DYNA is optimized for shared and distributed memory Unix, Linux, and Windows based, platforms, and it is fully QA'd by LSTC. The code's origins lie in highly nonlinear, transient dynamic finite element analysis using explicit time integration.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
LS-DYNA is a general-purpose finite element program capable of simulating complex real world problems. It is used by the automobile, aerospace, construction, military, manufacturing, and bioengineering industries. LS-DYNA is optimized for shared and distributed memory Unix, Linux, and Windows based, platforms, and it is fully QA'd by LSTC. The code's origins lie in highly nonlinear, transient dynamic finite element analysis using explicit time integration.

%description
LS-DYNA is a general-purpose finite element program capable of simulating complex real world problems. It is used by the automobile, aerospace, construction, military, manufacturing, and bioengineering industries. LS-DYNA is optimized for shared and distributed memory Unix, Linux, and Windows based, platforms, and it is fully QA'd by LSTC. The code's origins lie in highly nonlinear, transient dynamic finite element analysis using explicit time integration.

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
module load intel/18.0.2
module load intel/18.0.2
module list

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

LS-DYNA, developed by Livermore Software Technology Corporation (LSTC),
is a multi purpose explicit and implicit finite element and multiphysics program used to analyse the nonlinear response of structures.

Its fully automated contact analysis and wide range of material models enable users worldwide to solve complex, real world problems.

The %{MODULE_VAR} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN for
the location of the %{name} distribution and excutables,respectively.
 also appends the path to the executables
to the PATH environment variable.

The excutables of %{MODULE_VAR} in this version include:
        lsdyna_d and lsdyna_s

A license is required to run LS-DYNA on TACC systems. 
Please submit a ticket via the DesignSafe web portal for license request. 
Our administrator team will work with LSTC to verify your license.
https://portal.tacc.utexas.edu/tacc-consulting

Version %{pkg_version}
]]

help(help_msg)

whatis("LS_DYN: a general-purpose finite element program capable of simulating complex real world problems")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: application, finite element")
whatis("URL: https://www.oasys-software.com/dyna/software/ls-dyna/")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.

family("lsdyna")
prepend_path(    "PATH",               "/work/projects/wma_apps/stampede2/ls-dyna/ls-dyna_11.0.0/bin")
setenv( "TACC_%{MODULE_VAR}_DIR",      "/work/projects/wma_apps/stampede2/ls-dyna/ls-dyna_11.0.0")
setenv( "TACC_%{MODULE_VAR}_BIN",      "/work/projects/wma_apps/stampede2/ls-dyna/ls-dyna_11.0.0/bin")
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

