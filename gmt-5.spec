#
# gmt.spec
# Victor Eijkhout
#
# based on Bar.spec
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

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name gmt
%define MODULE_VAR    GMT

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 2
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define gshhg_version 2.3.4

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
#%include name-defines-hidden.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   3
License:   GNU
Group:     Development/Tools
URL:       http://gmt.soest.hawaii.edu/
Packager:  TACC - eijkhout@tacc.utexas.edu
# VLE NOTE !!! the 5.2.1 source is manually edited
Source:    %{pkg_base_name}-%{pkg_version}-src.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: GMT is an open source collection of tools for manipulating geographic and Cartesian data sets
Group: Applications
%description package
This is the long description for the package RPM...

%package %{MODULEFILE} 
Summary: GMT is an open source collection of tools for manipulating geographic and Cartesian data sets
Group: Applications
%description modulefile
This is the long description for the package RPM...

%description 
GMT is an open source collection of
tools for manipulating geographic and Cartesian data sets Group:
Applications %description modulefile GMT is an open source collection
of about 80 command-line tools for manipulating geographic and
Cartesian data sets (including filtering, trend fitting, gridding,
projecting, etc.) and producing PostScript illustrations ranging from
simple x–y plots via contour maps to artificially illuminated surfaces
and 3D perspective views; the GMT supplements add another 40 more
specialized and discipline-specific tools. GMT supports over 30 map
projections and transformations and requires support data such as
GSHHG coastlines, rivers, and political boundaries and optionally DCW
country polygons. GMT is developed and maintained by Paul Wessel,
Walter H. F. Smith, Remko Scharroo, Joaquim Luis and Florian Wobbe,
with help from a global set of volunteers, and is supported by the
National Science Foundation. It is released under the GNU Lesser
General Public License version 3 or any later version.


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

# Insert further module commands

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
  
#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
#tacctmpfs -m %{INSTALL_DIR}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# need netcdf libs also
 module load cmake netcdf
 export NETCDF_INC=${TACC_NETCDF_INC}
 export NETCDF_LIB=${TACC_NETCDF_LIB}

#
# config/make
#

mkdir -p %{INSTALL_DIR}/share

# edit path for gshhg-gmt
#     target line: '# set (GSHHG_ROOT "gshhg_path")'
# we do this in the build directory; pushd after this
sed \
    -e '/GSHHG_ROOT/s/^#//' \
    -e '/COPY_GSHHG/s/^#//' \
    -e 's!gshhg_path!%{INSTALL_DIR}/share/gshhg-gmt-%{gshhg_version}!' \
    cmake/ConfigUserTemplate.cmake > cmake/ConfigUser.cmake
grep -i gshhg cmake/ConfigUser*.cmake

pushd %{INSTALL_DIR}

# unpack extra datasets
( cd share ; tar fxz %{_topdir}/SOURCES/gshhg-gmt-%{gshhg_version}.tar.gz )

# use icc not gcc
 export CC=`which icc`

cmake \
  -D CMAKE_INSTALL_PREFIX:PATH=%{INSTALL_DIR} \
  %{_topdir}/BUILD/gmt-%{version} \

make 

mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
make install

# Also need to unpack the supplemental tarballs containing maps and such
# I made a single tarball named GMT_suppl_share.tar.bz2 containing the following archives:
# These all go into %{INSTALL_DIR}/share
# GMT4.5.2_doc.tar.bz2    
# GMT4.5.2_share.tar.bz2  
# GSHHS2.0.2_coast.tar.bz2   
# GSHHS2.0.2_full.tar.bz2
# GMT4.5.2_suppl.tar.bz2  
# GSHHS2.0.2_high.tar.bz2

#create gmt.conf to make GMT use SI units instead of US
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/share
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/share/gmt.conf << 'EOF'
SI
EOF

popd


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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << EOF
local help_message = [[

This module provides the GMT environment variables:
TACC_GMT_DIR, TACC_GMT_LIB, TACC_GMT_INC

Version %{version}
]]

help(help_message,"\n")

whatis("Name: GMT")
whatis("Version: %{version}")
whatis("Category: ")
whatis("Keywords: System, Cartesian Grids")
whatis("URL: https://code.google.com/p/gmt/")
whatis("Description: Generic Mapping Tools: Tools for manipulating geographic and Cartesian data sets")

local gmt_dir="%{INSTALL_DIR}"

setenv("TACC_GMT_DIR",gmt_dir)
setenv("TACC_GMT_BIN",pathJoin(gmt_dir,"bin"))
setenv("TACC_GMT_LIB",pathJoin(gmt_dir,"lib64"))
setenv("TACC_GMT_SHARE",pathJoin(gmt_dir,"share"))
setenv("TACC_GMT_GSHHG_DIR",pathJoin(gmt_dir,"share","gshhg-gmt-%{gshhg_version}"))

prepend_path("PATH",pathJoin(gmt_dir,"bin"))
prepend_path("PATH",pathJoin(gmt_dir,"share"))
prepend_path("LD_LIBRARY_PATH",pathJoin(gmt_dir,"lib64"))

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

cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
umount tmpfs

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

#---------------------------------------
%changelog
#---------------------------------------
#
* Tue May 10 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: fixed the gshhg dataset
* Wed Mar 09 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: adding gshhg-gmt dataset
* Wed Feb 22 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
