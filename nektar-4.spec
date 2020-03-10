#
# Spec file for NEKTAR:
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
%define pkg_base_name nektar
%define MODULE_VAR    NEKTAR

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 4
%define micro_version 1
%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define modmetisversion 5.1.0_2

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc
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

Release:   4%{?dist}
License:   GNU
Group:     Development/Tools
Vendor:     Nektar
Group:      Libraries/maps
# The nektar tarball unpacks to nektar++-4.4.1. That's silly.
Source:	    nektar-%{version}.tar.gz
URL:	    https://www.nektar.info/
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: NEKTAR install
Group: System Environment/Base
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: NEKTAR install
Group: System Environment/Base
%description modulefile
This is the long description for the modulefile RPM...

%description
Nektar


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
# Load Compiler
%include compiler-load.inc
# Load MPI Library
%include mpi-load.inc

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
  
%if "%{comp_fam}" == "intel"
  %{error: Nektar is for now only with gcc}
  exit
%endif

#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

module load boost mkl

export NEKTARDIR=`pwd`

# source directories
export WORK=%{SPEC_DIR}/../BUILD/
export NEKTARSRC=${WORK}/nektar-%{pkg_version}
export BOOST_HOME=${TACC_BOOST_DIR}
export GSMPI_LIBRARY=${NEKTARSRC}/ThirdParty/gsmpi-1.2
( cd ${NEKTARSRC} \
  && if [ -d modmetis* ] ; then rm -rf modmetis* ; fi \
  && tar fx %{SPEC_DIR}/../SOURCES/modmetis-%{modmetisversion}.tar \
)
export MODMETIS_LIBRARY=${NEKTARSRC}/modmetis-%{modmetisversion}

# build location, we do cmake there
export BUILDDIR=/tmp/nektar-build
rm -rf ${BUILDDIR}
mkdir -p ${BUILDDIR}
pushd ${BUILDDIR}

# how does it find MKL with gcc?
# http://doc.nektar.info/userguide/latest/user-guidese3.html#x7-180001.3.5

cmake \
          -D CMAKE_CXX_COMPILER=mpicxx \
          -D CMAKE_C_COMPILER=mpicc \
          -D THIRDPARTY_BUILD_BOOST:BOOL=OFF \
          -D THIRDPARTY_BUILD_GSMPI:BOOL=ON \
          -D NEKTAR_USE_MKL:BOOL=ON \
          -D NEKTAR_USE_MPI:BOOL=ON \
          \
          -D CMAKE_INSTALL_PREFIX:PATH=%{INSTALL_DIR} \
        ${NEKTARSRC}
make install
popd

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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
Simplified Wrapper and Interface Generator
This module loads nektar.
The command directory is added to PATH.
The include directory is added to INCLUDE.
The lib     directory is added to LD_LIBRARY_PATH.

Version %{version}
]] )

whatis( "Simplified Wrapper and Interface Generator" )
whatis( "Version: %{version}" )
whatis( "Category: Development/Tools" )
whatis( "Description: NEKTAR is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages." )
whatis( "https://www.nektar.info/" )

local nektar_dir = "%{INSTALL_DIR}"

prepend_path( "PATH", pathJoin( nektar_dir,"bin" ) )
setenv("TACC_NEKTAR_DIR", nektar_dir )
setenv("TACC_NEKTAR_BIN", pathJoin(nektar_dir,"bin" ) )
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
* Tue Aug 28 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: just to disambiguate for intel18
* Thu Jun 15 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: proper path in modulefiles
* Thu Jun 01 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: lua modulefiles
* Fri Feb 24 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
