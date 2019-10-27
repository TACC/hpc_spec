#
# Spec file for reference blas/lapack
#
Summary:   Netlib blas and lapack

# Give the package a base name
%define pkg_base_name referencelapack
%define MODULE_VAR    REFERENCELAPACK

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 5
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

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

Release:   1
License:   GPL
Group:     Development/Tools
Source:    referencelapack-%{version}.tgz
URL:       http://netlib.org/lapack
Vendor:    University of Tennessee, Knoxville
Packager:  TACC - eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: Reference blas and lapack
Group: development/libraries
%description package
Netlib blas and lapack

%package %{MODULEFILE}
Summary: Reference blas and lapack
Group: development/libraries
%description modulefile
Netlib blas and lapack

%description
Lapack

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_full_version}

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
%include compiler-load.inc
%include mpi-load.inc

# Insert necessary module commands
#module purge

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
  
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

##
## here we go
##
#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

#
# config/make:
#

module load cmake

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 

cmake -DCMAKE_INSTALL_PREFIX:PATH=%{INSTALL_DIR} .
make all install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

umount %{INSTALL_DIR}

# make test

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The %{name} module file defines the following environment variables:
TACC_REFERENCELAPACK_DIR, TACC_REFERENCELAPACK_LIB, and 
for the location of sources and libraries respectively.

This Module Should NOT, I repeat !!!NOT!!!, Be Used In Production!

This module serves for debugging purposes or to compare against MKL.

Version %{version}

]]

help(help_message,"\n")


whatis("ReferenceLapack: Reference implementation of blas and lapack")
whatis("Version: %{version}")
whatis("Category: development, mathematics")
whatis("Keywords: Library, development, mathematics")
whatis("Description: Fortran reference implementation of Blas and Lapack.")
whatis("URL: http://netlib.org/lapack/")

-- Prerequisites

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

--Env variables 
setenv("TACC_REFERENCELAPACK_DIR", "%{INSTALL_DIR}")
setenv("TACC_REFERENCELAPACK_LIB", "%{INSTALL_DIR}/lib")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Referencelapack
##
 
set     ModulesVersion      "%{version}"
EOF

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

%defattr(-,root,install,-)
%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

%defattr(-,root,install,-)
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

%changelog
* Mon Aug 20 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial install
