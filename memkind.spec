#
# Antonio Gomez-Iglesias
# 2016-10-04
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#

Summary: Memkind spec file (https://github.com/memkind/memkind)

# Give the package a base name
%define pkg_base_name memkind
%define MODULE_VAR    MEMKIND

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

%define mpi_fam none

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
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
License:   GPL
Group:     Utility
URL:       https://github.com/memkind/memkind
Packager:  TACC - agomez@tacc.utexas.edu
Source:    memkind_%{major_version}.%{minor_version}.%{micro_version}.tar.gz
# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Memkind RPM
Group: Development/System Environment
%description package
Memkind library provides the possibility to use HBW memory from your code (C/C++/Fortran).

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Module RPM for Memkind

%description

The memkind library is a user extensible heap manager built on top of jemalloc which enables
control of memory characteristics and a partitioning of the heap between kinds of memory. 
The kinds of memory are defined by operating system memory policies that have been applied to
virtual address ranges. Memory characteristics supported by memkind without user extension
include control of NUMA and page size features. The jemalloc non-standard interface has been
extended to enable specialized arenas to make requests for virtual memory from the operating
system through the memkind partition interface. Through the other memkind interfaces the user
can control and extend memory partition features and allocate memory while selecting enabled
features.


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#setup -n %{pkg_base_name}-%{pkg_version}
%setup -n memkind_%{major_version}.%{minor_version}.%{micro_version}  %{name}-%{version}
#%setup -n memkind_%{major_version}_%{minor_version}_%{micro_version}  -T -D -a 1

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
#%include compiler-defines.inc
module purge
#%include compiler-load.inc

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

#  git clone https://github.com/memkind/memkind
#  cd memkind
#  git checkout v1.3.0
  ./build_jemalloc.sh
  ./autogen.sh
  ./configure --prefix=%{INSTALL_DIR}
  make -j 68
  make install

  mkdir -p              $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..



  if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  	mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  fi

  cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}

#---------------------- - 
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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
The memkind module file defines the following environment variables:"
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN, TACC_%{MODULE_VAR}_LIB,
and TACC_%{MODULE_VAR}_INC for the location of the memkind distribution."

Version %{version}"
]])

whatis("Name: memkind")
whatis("Version: %{version}")
whatis("Category: %{group}")
whatis("Keywords: System, Library, C, C++, Fortran")
whatis("URL: https://github.com/memkind/memkind")
whatis("Description: Memkind provides functionality to use HBW memory.")


setenv("TACC_%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
setenv("TACC_%{MODULE_VAR}_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_%{MODULE_VAR}_INC","%{INSTALL_DIR}/include")

-- Add memkind to PATH and LD_LIBRARY_PATH

prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{MODULE_VAR}%{version}
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

