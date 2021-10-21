#
# Spec file for EIGEN:
# C++ linear algebra library
#
# Victor Eijkhout, 2019
# based on:
#
# Bar.spec, 
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

Summary:    Set of tools for manipulating geographic and Cartesian data sets

# Give the package a base name
%define pkg_base_name eigen
%define MODULE_VAR    EIGEN

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 4
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-scratch.inc
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
License:   GNU
Group:     Development/Tools
Vendor:     Tuxfamily
Group:      Libraries/maps
Source:	    eigen-%{version}.tar.gz
URL:	    http://eigen.tuxfamily.org/
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Eigen is a C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms.
Group: Applications
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Eigen is a C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms.
Group: Applications
%description modulefile
This is the long description for the modulefile RPM...

%description 
Eigen is a C++ template library for linear algebra:
matrices, vectors, numerical solvers, and related algorithms.


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

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
# cmake is a system package:
## module load cmake
module load python3
##module load boost
export TACC_BOOST_INC=/opt/apps/intel19/python3_9/boost/1.72/include
export TACC_BOOST_LIB=/opt/apps/intel19/python3_9/boost/1.72/lib

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
export EIGEN_SRC_DIR=`pwd`
export EIGEN_BUILD_DIR=/tmp/eigen-build
rm -rf ${EIGEN_BUILD_DIR}
mkdir ${EIGEN_BUILD_DIR}
export EIGEN_INSTALL_DIR=%{INSTALL_DIR}

#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
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
  
( \
  cd ${EIGEN_BUILD_DIR} \
  && echo "using CC=${CC}, CXX=${CXX}, FC=${FC}" \
  && cmake -D CMAKE_INSTALL_PREFIX:PATH=${EIGEN_INSTALL_DIR} \
        -D CMAKE_C_COMPILER:FILEPATH=${CC} \
        -D CMAKE_CXX_COMPILER:FILEPATH=${CXX} \
        -D CMAKE_Fortran_COMPILER:FILEPATH=${FC} \
        ${EIGEN_SRC_DIR} \
  && make && make install \
  && mkdir ${EIGEN_INSTALL_DIR}/cmake \
  && cp -r CMake* *cmake ${EIGEN_INSTALL_DIR}/cmake \
)

cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
umount tmpfs

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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
Module %{name} loads environmental variables defining
the location of EIGEN directory, libraries, and binaries:
TACC_EIGEN_DIR, TACC_EIGEN_INC, TACC_EIGEN_SHARE

Version: %{version}
]] )

whatis( "EIGEN" )
whatis( "Version: %{version}" )
whatis( "Category: system, development" )
whatis( "Keywords: Linear Algebra, C++" )
whatis( "Description: C++ template library for linear algebra" )
whatis( "URL: http://eigen.tuxfamily.org/" )

local version =  "%{version}"
local eigen_dir =  "%{INSTALL_DIR}"

setenv("TACC_EIGEN_DIR",eigen_dir)
setenv("TACC_EIGEN_INC",pathJoin( eigen_dir,"include","eigen3" ) )
setenv("TACC_EIGEN_SHARE",pathJoin( eigen_dir,"share" ) )

prepend_path ("PATH",pathJoin( eigen_dir,"share" ) )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for %{name} version %{version}
##
set ModulesVersion "%version"
EOF

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
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

%changelog
* Thu Sep 30 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
