#
# $Id: mpiP.spec 385 2015-12-01 08:35:03Z agomez $
#

Summary: MPI Profiling Library

# Give the package a base name
%define pkg_base_name mpiP
%define MODULE_VAR    MPIP

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 4
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################


Release: 1
License: GPL
Group: System Environment/Base
Source: mpiP-%{version}.tar.gz
Packager: agomez@tacc.utexas.edu
Buildroot: /tmp/rpm/%{name}-%{version}-buildroot
%define _topdir /admin/build/rpms/

# %define APPS /opt/apps
# %define MODULES modulefiles

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: mpiP
Group: Profiler
%description package
This is the long description.

%package %{MODULEFILE}
Summary: mpiP modulefile
Group: Profiler
%description modulefile
This is the ong description

%description

mpiP: Lightweight, Scalable MPI Profiling

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


%build

%install

%include system-load.inc
#%include compiler-load.inc
#%include mpi-load.inc

module purge

module load taccswitch
source taccswitch
module load intel
module load cmpich

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

export ARCH=x86_64
export CC=mpicc
export F77=mpif90
export PATH=/opt/apps/tacc/bin/:$PATH
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
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

 ./configure CFLAGS="-g" --enable-demangling --disable-bfd --disable-libunwind --prefix=%{INSTALL_DIR} 
  
  make
  make shared
  make DESTDIR=$RPM_BUILD_ROOT install

  
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
The mpiP modulefile defines the following environment variables:
TACC_MPIP_DIR, TACC_MPIP_LIB for the location of the
mpiP %{version} distribution and libraries respectively.

To use the mpiP library, relink your MPI code with the following option:
        -L\$TACC_MPIP_LIB -lmpiP

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: mpiP")
whatis("Version: %{version}")
whatis("Category: library, profiling")
whatis("Keywords: Profiling, Library")
whatis("URL: http://mpip.sourceforge.net")
whatis("Description: Lightweight, Scalable MPI Profiling")

--
-- Create environment variables.
--

local mpip_lib   = "%{INSTALL_DIR}/lib"

setenv("TACC_MPIP_DIR", "%{INSTALL_DIR}")
setenv("TACC_MPIP_LIB", "%{INSTALL_DIR}/lib")

-- Add mpiP to the LD_LIBRARY_PATH

prepend_path("LD_LIBRARY_PATH", mpip_lib)
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for mpip
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
  %{INSTALL_DIR}/bin

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
