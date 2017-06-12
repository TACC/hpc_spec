#
# Spec file for GMT:
# Generic Mapping Tools
# See http://gmt.soest.hawaii.edu/
#
# Victor Eijkhout, 2017
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
%define pkg_base_name gmt
%define MODULE_VAR    GMT

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 3
%define micro_version 3

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
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

Release:   2%{?dist}
License:   GNU
Group:     Development/Tools
Vendor:     SOEST - hawaii
Group:      Libraries/maps
Source:	    gmt-%{version}-src.tar.gz
URL:	    http://gmt.soest.hawaii.edu/ 
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

# coastlines database
%define gshhg_version 2.3.6

%package %{PACKAGE}
Summary: GMT is an open source collection of tools for manipulating geographic and Cartesian data sets
Group: Applications
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: GMT is an open source collection of tools for manipulating geographic and Cartesian data sets
Group: Applications
%description modulefile
This is the long description for the modulefile RPM...

%description
GMT is an open source collection of 60 
tools for manipulating geographic and Cartesian data sets


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
# need netcdf libs also
 module load netcdf
 export NETCDF_INC=${TACC_NETCDF_INC}
 export NETCDF_LIB=${TACC_NETCDF_LIB}


echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
  
#
# config/make
#

mkdir -p %{INSTALL_DIR}/share

sed \
    -e '/GSHHG_ROOT/s/^#//' \
    -e '/COPY_GSHHG/s/^#//' \
    -e 's!gshhg_path!%{INSTALL_DIR}/share/gshhg-gmt-%{gshhg_version}!' \
    cmake/ConfigUserTemplate.cmake > cmake/ConfigUser.cmake
grep -i gshhg cmake/ConfigUser*.cmake

pushd %{INSTALL_DIR}

# unpack extra datasets
( cd share ; tar fxz %{_topdir}/SOURCES/gshhg-gmt-%{gshhg_version}.tar.gz )

# recent versions use cmake instead of configure
module load cmake

# use icc not gcc
 export CC=`which icc`

# VLE i can't find this file.....
# tar jxvf /home1/0000/build/rpms/SOURCES/GMT4.5.5_triangle_repack_JL.tar.bz2

cmake \
  -D CMAKE_INSTALL_PREFIX:PATH=%{INSTALL_DIR} \
  %{_topdir}/BUILD/gmt-%{version} \

make 

mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
make install

#create gmt.conf to make GMT use SI units instead of US
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/share
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/share/gmt.conf << 'EOF'
SI
EOF

popd
  
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
the location of GMT directory, libraries, and binaries:
TACC_GMT_DIR TACC_GMT_LIB TACC_GMT_BIN

Version: %{version}
]] )

whatis( "GMT" )
whatis( "Version: %{version}" )
whatis( "Category: system, development" )
whatis( "Keywords: System, Cartesian Grids" )
whatis( "Description: Generic Mapping Tools: Tools for manipulating geographic and Cartesian data sets" )
whatis( "URL: http://gmt.soest.hawaii.edu/" )

local version =  "%{version}"
local gmt_dir =  "%{INSTALL_DIR}"

setenv("TACC_GMT_DIR",gmt_dir)
setenv("TACC_GMT_BIN",pathJoin( gmt_dir,"bin" ) )
setenv("TACC_GMT_LIB",pathJoin( gmt_dir,"lib" ) )
setenv("TACC_GMT_SHARE",pathJoin( gmt_dir,"share" ) )

prepend_path ("PATH",pathJoin( gmt_dir,"share" ) )
prepend_path ("PATH",pathJoin( gmt_dir,"bin" ) )
prepend_path ("LD_LIBRARY_PATH",pathJoin( gmt_dir, "lib" ) )
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
* Thu Jun 01 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: lua modulefiles
* Mon May 08 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
