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
%define pkg_base_name libfabric
%define MODULE_VAR    LIBFABRIC

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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
License:   GPLv2 or BSD
Group:     System Environment/Libraries
URL:       http://www.github.com/ofiwg/libfabric
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
penFabrics Interfaces (OFI) is a framework focused on exporting fabric
communication services to applications. OFI is best described as a collection
of libraries and applications used to export fabric services. The key
components of OFI are: application interfaces, provider libraries, kernel
services, daemons, and test applications.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...  OpenFabrics Interfaces
(OFI) is a framework focused on exporting fabric communication services to
applications. OFI is best described as a collection of libraries and
applications used to export fabric services. The key components of OFI are:
application interfaces, provider libraries, kernel services, daemons, and test
applications.

%description
OpenFabrics Interfaces (OFI) is a framework focused on exporting fabric
communication services to applications. OFI is best described as a collection
of libraries and applications used to export fabric services. The key
components of OFI are: application interfaces, provider libraries, kernel
services, daemons, and test applications.

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
  mount -t tmpfs tmpfs %{INSTALL_DIR}
  
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
  export ncores=8
  # DO NOT preppend $RPM_BUILD_ROOT in prefix
  ./configure \
  --prefix=%{INSTALL_DIR}
  make -j ${ncores}
  make install -j ${ncores}
  
  if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  fi
  cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}
  
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
OpenFabrics Interfaces (OFI) is a framework focused on exporting fabric
communication services to applications. OFI is best described as a collection
of libraries and applications used to export fabric services. The key
components of OFI are: application interfaces, provider libraries, kernel
services, daemons, and test applications.

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
whatis("URL: http://www.github.com/ofiwg/libfabric")

-- Export environmental variables
local libfabric_dir="%{INSTALL_DIR}"
local libfabric_bin=pathJoin(libfabric_dir,"bin")
local libfabric_lib=pathJoin(libfabric_dir,"lib")
local libfabric_inc=pathJoin(libfabric_dir,"include")
setenv("TACC_LIBFABRIC_DIR",libfabric_dir)
setenv("TACC_LIBFABRIC_BIN",libfabric_bin)
setenv("TACC_LIBFABRIC_LIB",libfabric_lib)
setenv("TACC_LIBFABRIC_INC",libfabric_inc)

-- Prepend the libfabric directories to the adequate PATH variables
prepend_path("PATH",libfabric_bin)
prepend_path("LD_LIBRARY_PATH",libfabric_lib)
prepend_path("MANPATH", pathJoin(libfabric_dir, "share/man"))

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

