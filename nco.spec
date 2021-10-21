#
# Spec file for NCO
# NetCdf Operator
# See http://nco.sourceforge.net/
# ANTLR https://www.antlr.org/download.html
#
# Victor Eijkhout, 2021

# Give the package a base name
%define pkg_base_name nco
%define MODULE_VAR    NCO

%define major_version 5
%define minor_version 0
%define micro_version 3

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define antlr_version 5.0

%include rpm-dir.inc                  
%include compiler-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Summary: NetCDF operators
Release: 1%{?dist}
License: GPL 3
Source: nco-%{version}.tar.gz
URL:  http://nco.sourceforge.net/
Packager: TACC - cazes@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: NetCDF operators
Group: applications/io

%package %{MODULEFILE}
Summary: NetCDF operators
Group: applications/io

%description
%description %{PACKAGE}
The operators take netCDF files as input, then perform a set of
operations (e.g., deriving new data, averaging, hyperslabbing, or
metadata manipulation) and produce a netCDF file as output. The
operators are primarily designed to aid manipulation and analysis of
gridded scientific data. The single command style of NCO allows users
to manipulate and analyze files interactively and with simple scripts,
avoiding the overhead (and some of the power) of a higher level
programming environment. The NCO User Guide illustrates their use
with examples from the field of climate modeling and analysis.
* ncap2 netCDF Arithmetic Processor
* ncatted netCDF Attribute Editor
* ncbo netCDF Binary Operator (includes ncadd, ncsubtract, ncmultiply, ncdivide)
* ncea netCDF Ensemble Averager
* ncecat netCDF Ensemble Concatenator
* ncflint netCDF File Interpolator
* ncks netCDF Kitchen Sink
* ncpdq netCDF Permute Dimensions Quickly, Pack Data Quietly
* ncra netCDF Record Averager
* ncrcat netCDF Record Concatenator
* ncrename netCDF Renamer
* ncwa netCDF Weighted Averager

%description %{MODULEFILE}

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf ${RPM_BUILD_ROOT}/%{INSTALL_DIR}

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

module load cmake antlr netcdf udunits

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

# Create temporary directory for the install.  We need this to
# trick rpm into thinking stuff is installed in its final location!
mkdir -p %{INSTALL_DIR}
rm -rf   %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

#
# no copying or pushd because we build here, 
# but install in %{INSTALL_DIR}
#
ANTLR_ROOT=${TACC_ANTLR_DIR} \
NETCDF_ROOT=${TACC_NETCDF_DIR} \
UDUNITS2_PATH=${TACC_UDUNITS_DIR} \
./configure \
    -v \
    --prefix=%{INSTALL_DIR} \
    --enable-shared --with-pic \
    --enable-netcdf4 \
    --enable-udunits2

make && make install

mkdir -p ${RPM_BUILD_ROOT}/%{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

umount %{INSTALL_DIR}/

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

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
  

#Module for nco
rm -rf  $RPM_BUILD_ROOT/%MODULE_DIR
mkdir -p $RPM_BUILD_ROOT/%MODULE_DIR
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--  modulefile for NCO

local help_message = [[
The %{name} module file defines the following environment variables:
TACC_NCO_DIR, TACC_NCO_BIN, TACC_NCO_LIB, and 
TACC_NCO_INC for the location of the NCO distribution, binaries,
libraries, and include files, respectively.

To use the NCO library, compile the source code with the option:
	-I\${TACC_NCO_INC 

and add the following options to the link step: 
	-L\${TACC_NCO_LIB -lnco

Version %{version}

]]

help(help_message,"\n")

whatis("Version: 4.6.9")
whatis("Category: utility, runtime support")
whatis("Description: Programs for manipulating and analyzing NetCDF files")
whatis("URL: http://nco.sourceforge.net")

setenv("TACC_NCO_DIR","%{INSTALL_DIR}")
setenv("TACC_NCO_BIN","%{INSTALL_DIR}/bin")
setenv("TACC_NCO_INC","%{INSTALL_DIR}/include")
setenv("TACC_NCO_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_NCO_MAN","%{INSTALL_DIR}/share/man")
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("MANPATH","%{INSTALL_DIR}/share/man")
--prereq("gsl", "hdf5", "netcdf")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
##
## version file for nco
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

%defattr(-,root,root)
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

%post


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jan 04 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: first release

