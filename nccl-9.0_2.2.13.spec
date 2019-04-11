#
# W. Cyrus Proctor
# 2016-08-07
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
%define pkg_base_name nccl
%define MODULE_VAR    NCCL

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2
%define patch_version 13
%define cuda_version  9.0
%define cuda_fam_ver  cuda9_0

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-cuda.inc
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

Release:   1%{?dist}
License:   NVIDIA Proprietary
Group:     Development/Tools
URL:       https://developer.nvidia.com/nccl
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Requires:  cuda = %{cuda_version}

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
The NVIDIA Collective Communications Library (NCCL) implements multi-GPU and
multi-node collective communication primitives that are performance optimized
for NVIDIA GPUs. NCCL provides routines such as all-gather, all-reduce,
broadcast, reduce, reduce-scatter, that are optimized to achieve high bandwidth
over PCIe and NVLink high-speed interconnect.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
The NVIDIA Collective Communications Library (NCCL) implements multi-GPU and
multi-node collective communication primitives that are performance optimized
for NVIDIA GPUs. NCCL provides routines such as all-gather, all-reduce,
broadcast, reduce, reduce-scatter, that are optimized to achieve high bandwidth
over PCIe and NVLink high-speed interconnect.

%description
The NVIDIA Collective Communications Library (NCCL) implements multi-GPU and
multi-node collective communication primitives that are performance optimized
for NVIDIA GPUs. NCCL provides routines such as all-gather, all-reduce,
broadcast, reduce, reduce-scatter, that are optimized to achieve high bandwidth
over PCIe and NVLink high-speed interconnect.


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
module purge
# Load Compiler
#%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

# Insert further module commands

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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib64
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
  
  tar xvf %{_sourcedir}/nccl_%{pkg_version}*+cuda%{cuda_version}_x86_64.txz
  cd nccl_%{pkg_version}*+cuda%{cuda_version}_x86_64
  # Copy everything from tarball over to the installation directory
  cp -rp * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
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
The NVIDIA Collective Communications Library (NCCL) implements multi-GPU and
multi-node collective communication primitives that are performance optimized
for NVIDIA GPUs. NCCL provides routines such as all-gather, all-reduce,
broadcast, reduce, reduce-scatter, that are optimized to achieve high bandwidth
over PCIe and NVLink high-speed interconnect.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and 
for the location of the %{MODULE_VAR} distribution, libraries,
include files, and libraries respectively.

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: %{pkg_base_name}")
-- Create environment variables.
local base_dir           = "%{INSTALL_DIR}"

family("%{pkg_base_name}")
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(base_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_DIR",                base_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(base_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(base_dir, "lib"))
add_property("arch","gpu")
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

