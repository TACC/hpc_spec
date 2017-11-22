#
# Spec file for NCO
#
Summary: NetCDF operators
Name: nco
Version: 4.6.9
Release: 1%{?dist}
License: GPL 3
Source: nco-4.6.9.tar.gz
Source1: antlr-2.7.7.tar.gz
# Udunits is installed as a module
#  Source2: udunits-2.1.20.tar.gz
Source3: antlr_patches_2.7.7.tar.gz
URL:  http://nco.sourceforge.net/
Packager: TACC - cazes@tacc.utexas.edu

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

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
programming environment. The NCO User's Guide illustrates their use
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

%prep
rm -rf  $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# The first call to setup untars the first source.  
%setup

# The second call untars the second source, in a subdirectory
# of the first. 
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory. 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!

#This untars antlr-2.7.7
%setup -T -D -a 1

# We should now have a ../BUILD/nco-4.6.9 and, within that, a
# ../BUILD/nco-4.6.9/antlr-2.7.7 directory.

#Use udunits module
# Third call to setup, untar the third source (udunits-2.1.20) in a subdirectory
# %setup -T -D -a 2

# Fourth call to setup, untar the fourth source (patches_antlr) in a subdirectory
%setup -T -D -a 3


%build

%include compiler-load.inc

#nco needs netcdf and gsl
#  but netcdf needs hdf5
# module load zlib
module load hdf5
module load gsl
module load netcdf
module load udunits
module list

#cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
#chmod -R a+rX $RPM_BUILD_ROOT/%INSTALL_DIR


# Create temporary directory for the install.  We need this to
# trick meep into thinking libctl is installed in its final location!
rm -rf %{INSTALL_DIR}
mkdir -p             %{INSTALL_DIR}
#clean up old
mount -t tmpfs tmpfs %{INSTALL_DIR}
#tacctmpfs -m %{INSTALL_DIR}


#Build antlr first
export ANTLR_PATH=%INSTALL_DIR

cd antlr-2.7.7

patch -p1 < ../antlr-charscanner.patch
patch -p1 < ../antlr-config.patch
patch -p1 < ../antlr-cs-signing.patch

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
# tacctmpfs -u  %{INSTALL_DIR}/


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

%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,root)
%{INSTALL_DIR}
%{MODULE_DIR}

%post


%clean
rm -rf $RPM_BUILD_ROOT
