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

%define major_version 4
%define minor_version 9
%define micro_version 7

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define antlr_version 4.9
%define antlr_patch_version 2.7.7

%include rpm-dir.inc                  
%include compiler-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc-home1.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Summary: NetCDF operators
Release: 1%{?dist}
License: GPL 3
Source: nco-%{version}.tar.gz
Source1: antlr-%{antlr_version}.tar.gz
# Udunits is installed as a module
#  Source2: udunits-2.1.20.tar.gz
Source3: antlr_patches_%{antlr_patch_version}.tar.gz
URL:  http://nco.sourceforge.net/
Packager: TACC - eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package -n %{name}-%{comp_fam_ver}
Summary: NetCDF operators
Group: applications/io

%description
%description -n %{name}-%{comp_fam_ver}
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

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf ${RPM_BUILD_ROOT:?NO_RPM_BUILD_ROOT}/%{INSTALL_DIR}

# The first call to setup untars the first source.
%setup -n %{pkg_base_name}-%{pkg_version}

# The second call untars the second source, in a subdirectory
# of the first.
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory. 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!

#This untars antlr-2.7.7
#%setup -T -D -a 1

# We should now have a ../BUILD/nco-4.6.9 and, within that, a
# ../BUILD/nco-4.6.9/antlr-2.7.7 directory.

#Use udunits module
# Third call to setup, untar the third source (udunits-2.1.20) in a subdirectory
# %setup -T -D -a 2

# Fourth call to setup, untar the fourth source (patches_antlr) in a subdirectory
#%setup -T -D -a 3

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

#nco needs netcdf and gsl
#  but netcdf needs hdf5
# module load zlib
module load hdf5
module load gsl
module load netcdf
module load udunits
module list

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

# Create temporary directory for the install.  We need this to
# trick rpm into thinking stuff is installed in its final location!
mkdir -p %{INSTALL_DIR}
rm -rf   %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

#Build antlr first
tar fxz %{_topdir}/SOURCES/antlr-%{antlr_version}.tar.gz
tar fxz %{_topdir}/SOURCES/antlr_patches_%{antlr_patch_version}.tar.gz

pwd
ls

export ANTLR_PATH=%{INSTALL_DIR}
cd antlr4-%{antlr_version}

# patch -p1 < ../antlr-charscanner.patch
# patch -p1 < ../antlr-config.patch
# patch -p1 < ../antlr-cs-signing.patch

./configure \
--prefix=${ANTLR_PATH} \
--disable-csharp \
--disable-java \
--disable-python 
make 
make install 

# then build udunits
# export UDUNITS_PATH=%INSTALL_DIR
# cd ../udunits-2.1.20

# ./configure --prefix=$UDUNITS_PATH 
# make 
# make install 


# Finally, build NCO
export NCO_PATH=%INSTALL_DIR
cd ..


export LD_LIBRARY_PATH=${TACC_HDF5_LIB}:${LD_LIBRARY_PATH}
export PATH=${TACC_HDF5_BIN}:${PATH}
export LD_LIBRARY_PATH=${TACC_NETCDF_PATH}/lib:${LD_LIBRARY_PATH}
export PATH=${TACC_NETCDF_BIN}:${PATH}
export LD_LIBRARY_PATH=${ANTLR_PATH}/lib:${LD_LIBRARY_PATH}
export PATH=${ANTLR_PATH}/bin:${PATH}
export LD_LIBRARY_PATH=${TACC_UDUNITS_DIR}/lib:${LD_LIBRARY_PATH}
export PATH=${TACC_UDUNITS_DIR}/bin:${PATH}
# export LD_LIBRARY_PATH=/usr/lib64:${LD_LIBRARY_PATH}
# export PATH=/usr/bin:${PATH}

echo $LD_LIBRARY_PATH

NETCDF_INC=${TACC_NETCDF_INC} \
NETCDF_LIB=${TACC_NETCDF_LIB} \
NETCDF4_ROOT=${TACC_NETCDF_DIR} \
HDF5_LIB_DIR=${TACC_HDF5_LIB} \
UDUNITS2_PATH=${TACC_UDUNITS_DIR} \
LDFLAGS="-L${ANTLR_PATH}/lib -lantlr \
-lhdf5_hl -lhdf5 -L${TACC_NETCDF_LIB} -lnetcdf" \
CFLAGS="-I${TACC_HDF5_INC} \
-L${TACC_HDF5_LIB} \
-I${ANTLR_PATH}/include \
-L${ANTLR_PATH}/lib" \
CPPFLAGS="-I${TACC_HDF5_INC} \
-L${TACC_HDF5_LIB} \
-I${ANTLR_PATH}/include \
-L${ANTLR_PATH}/lib" \
./configure \
-v \
--prefix=${NCO_PATH} \
--enable-shared \
--with-pic \
--enable-netcdf-4 
make 
make install 


# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.
cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
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
#------------------------

%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,root)
%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
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

