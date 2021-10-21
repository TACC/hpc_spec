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
%define pkg_base_name pmix
%define MODULE_VAR    PMIX

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 2
%define micro_version 3

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

Release:   7%{?dist}
License:   BSD3
Group:     System Environment/Libraries
URL:       https://github.com/pmix/pmix
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.bz2

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
The Process Management Interface (PMI) has been used for quite some time as a
means of exchanging wireup information needed for interprocess communication.
Two versions (PMI-1 and PMI-2) have been released as part of the MPICH effort.
While PMI-2 demonstrates better scaling properties than its PMI-1 predecessor,
attaining rapid launch and wireup of the roughly 1M processes executing across
100k nodes expected for exascale operations remains challenging.  PMI Exascale
(PMIx) represents an attempt to resolve these questions by providing an
extended version of the PMI standard specifically designed to support clusters
up to and including exascale sizes. The overall objective of the project is not
to branch the existing pseudo-standard definitions - in fact, PMIx fully
supports both of the existing PMI-1 and PMI-2 APIs - but rather to (a) augment
and extend those APIs to eliminate some current restrictions that impact
scalability, and (b) provide a reference implementation of the PMI-server that
demonstrates the desired level of scalability.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
The Process Management Interface (PMI) has been used for quite some time as a
means of exchanging wireup information needed for interprocess communication.
Two versions (PMI-1 and PMI-2) have been released as part of the MPICH effort.
While PMI-2 demonstrates better scaling properties than its PMI-1 predecessor,
attaining rapid launch and wireup of the roughly 1M processes executing across
100k nodes expected for exascale operations remains challenging.  PMI Exascale
(PMIx) represents an attempt to resolve these questions by providing an
extended version of the PMI standard specifically designed to support clusters
up to and including exascale sizes. The overall objective of the project is not
to branch the existing pseudo-standard definitions - in fact, PMIx fully
supports both of the existing PMI-1 and PMI-2 APIs - but rather to (a) augment
and extend those APIs to eliminate some current restrictions that impact
scalability, and (b) provide a reference implementation of the PMI-server that
demonstrates the desired level of scalability.

%description
The Process Management Interface (PMI) has been used for quite some time as a
means of exchanging wireup information needed for interprocess communication.
Two versions (PMI-1 and PMI-2) have been released as part of the MPICH effort.
While PMI-2 demonstrates better scaling properties than its PMI-1 predecessor,
attaining rapid launch and wireup of the roughly 1M processes executing across
100k nodes expected for exascale operations remains challenging.  PMI Exascale
(PMIx) represents an attempt to resolve these questions by providing an
extended version of the PMI standard specifically designed to support clusters
up to and including exascale sizes. The overall objective of the project is not
to branch the existing pseudo-standard definitions - in fact, PMIx fully
supports both of the existing PMI-1 and PMI-2 APIs - but rather to (a) augment
and extend those APIs to eliminate some current restrictions that impact
scalability, and (b) provide a reference implementation of the PMI-server that
demonstrates the desired level of scalability.

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
# ml hwloc/1.11.13
ml

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
#export   CFLAGS="-march=native -mtune=native"
#export CXXFLAGS="-march=native -mtune=native"

export ncores=48

## --with-hwloc=${TACC_HWLOC_DIR} 
./configure                    \
--prefix=%{INSTALL_DIR}        \
--with-libevent=/usr           \
--enable-dstore                \
--with-hwloc                   \
--disable-debug                \
--enable-builtin-atomics       \
--disable-dlopen               \
--enable-static=yes            \
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
The Process Management Interface (PMI) has been used for quite some time as a
means of exchanging wireup information needed for interprocess communication.
Two versions (PMI-1 and PMI-2) have been released as part of the MPICH effort.
While PMI-2 demonstrates better scaling properties than its PMI-1 predecessor,
attaining rapid launch and wireup of the roughly 1M processes executing across
100k nodes expected for exascale operations remains challenging.  PMI Exascale
(PMIx) represents an attempt to resolve these questions by providing an
extended version of the PMI standard specifically designed to support clusters
up to and including exascale sizes. The overall objective of the project is not
to branch the existing pseudo-standard definitions - in fact, PMIx fully
supports both of the existing PMI-1 and PMI-2 APIs - but rather to (a) augment
and extend those APIs to eliminate some current restrictions that impact
scalability, and (b) provide a reference implementation of the PMI-server that
demonstrates the desired level of scalability.

This module defines the environmental variables TACC_%{MODULE_VAR}_DIR,
TACC_%{MODULE_VAR}_BIN, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_INC
for the location of the main pmix directory, binaries, libraries,
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
whatis("URL: https://github.com/pmix/pmix")

-- Export environmental variables
local pmix_dir="%{INSTALL_DIR}"
local pmix_bin=pathJoin(pmix_dir,"bin")
local pmix_lib=pathJoin(pmix_dir,"lib")
local pmix_inc=pathJoin(pmix_dir,"include")
setenv("TACC_%{MODULE_VAR}_DIR",pmix_dir)
setenv("TACC_%{MODULE_VAR}_BIN",pmix_bin)
setenv("TACC_%{MODULE_VAR}_LIB",pmix_lib)
setenv("TACC_%{MODULE_VAR}_INC",pmix_inc)

-- Prepend the pmix directories to the adequate PATH variables
prepend_path("PATH",pmix_bin)
prepend_path("LD_LIBRARY_PATH",pmix_lib)
prepend_path("MANPATH", pathJoin(pmix_dir, "share/man"))

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

