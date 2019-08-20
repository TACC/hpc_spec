#
# W. Cyrus Proctor
# 2015-11-07
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
%define pkg_base_name ucx
%define MODULE_VAR    UCX

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 6
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define knem_install  /opt/knem-1.1.3.90mlnx1

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

Release:   6%{?dist}
License:   BSD3
Group:     System Environment/Libraries
URL:       https://github.com/openucx/ucx
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
Unified Communication X (UCX) provides an optimized communication layer for
Message Passing (MPI), PGAS/OpenSHMEM libraries and RPC/data-centric
applications.  UCX utilizes high-speed networks for inter-node communication,
and shared memory mechanisms for efficient intra-node communication.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...  OpenFabrics Interfaces
Unified Communication X (UCX) provides an optimized communication layer for
Message Passing (MPI), PGAS/OpenSHMEM libraries and RPC/data-centric
applications.  UCX utilizes high-speed networks for inter-node communication,
and shared memory mechanisms for efficient intra-node communication.

%description
Unified Communication X (UCX) provides an optimized communication layer for
Message Passing (MPI), PGAS/OpenSHMEM libraries and RPC/data-centric
applications.  UCX utilizes high-speed networks for inter-node communication,
and shared memory mechanisms for efficient intra-node communication.

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

%setup -n %{pkg_base_name}-%{pkg_version}


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
 
export CC=gcc
export CXX=g++

export ncores=48

#./configure             \
#--prefix=%{INSTALL_DIR} \
#--enable-logging        \
#--enable-debug          \
#--enable-debug-data     \
#--enable-profiling      \
#--enable-stats          \
#--enable-assertions     \
#--enable-params-check   \
#--enable-static=yes     \
#--enable-shared=yes     

export ncores=48

./configure             \
--prefix=%{INSTALL_DIR} \
--enable-compiler-opt=3 \
--enable-optimizations  \
--disable-logging       \
--disable-debug         \
--disable-assertions    \
--disable-params-check  \
--with-mcpu             \
--with-march            \
--with-rc               \
--with-ud               \
--with-dc               \
--with-cm               \
--with-mlx5-dv          \
--with-ib-hw-tm         \
--with-dm               \
--with-knem=%{knem_install} \
--enable-static=yes     \
--enable-shared=yes     


make V=1 -j ${ncores}
make DESTDIR=$RPM_BUILD_ROOT install -j ${ncores}
  
  
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
Unified Communication X (UCX) provides an optimized communication layer for
Message Passing (MPI), PGAS/OpenSHMEM libraries and RPC/data-centric
applications.  UCX utilizes high-speed networks for inter-node communication,
and shared memory mechanisms for efficient intra-node communication.

This module defines the environmental variables TACC_%{MODULE_VAR}_DIR,
TACC_%{MODULE_VAR}_BIN, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_INC
for the location of the main libfabric directory, binaries, libraries,
and include files respectively.

The location of the binary files is also added to your PATH.
The location of the library files is also added to your LD_LIBRARY_PATH.
Documentation is also added to your MANPATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: system, environment libaries")
whatis("Keywords: System, Environment Libraries")
whatis("Description: Fabric communication services")
whatis("URL: https://github.com/openucx/ucx")

-- Export environmental variables
local ucx_dir="%{INSTALL_DIR}"
local ucx_bin=pathJoin(ucx_dir,"bin")
local ucx_lib=pathJoin(ucx_dir,"lib")
local ucx_inc=pathJoin(ucx_dir,"include")
setenv("TACC_%{MODULE_VAR}_DIR",ucx_dir)
setenv("TACC_%{MODULE_VAR}_BIN",ucx_bin)
setenv("TACC_%{MODULE_VAR}_LIB",ucx_lib)
setenv("TACC_%{MODULE_VAR}_INC",ucx_inc)

-- Prepend the ucx directories to the adequate PATH variables
prepend_path("PATH",ucx_bin)
prepend_path("LD_LIBRARY_PATH",ucx_lib)
prepend_path("MANPATH", pathJoin(ucx_dir, "share/man"))

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

