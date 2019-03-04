
Summary: HDF5 Library

# This spec file can be built in parallel with mpi or not.
#
#
%define hdf5_pkg_version   1.8.21
%define ncdf_c_version     4.6.2
%define ncdf_cxx_version   4.2
%define ncdf_cxx4_version  4.3.0
%define ncdf_ftn_version   4.4.4
%define szip_version 2.1

%define dbg %{nil}
%if "%{is_debug}" == "1"
   %define dbg -dbg
   %define hdf5_version %{hdf5_pkg_version}-dbg
   %define ncdf_version %{ncdf_c_version}-dbg
%else
   %define hdf5_version %{hdf5_pkg_version}
   %define ncdf_version %{ncdf_c_version}
%endif


Name: hdf5-netcdf
Version: %{hdf5_version}
Release: 3
License: see included Copyright
Vendor: NCSA
Group: Development/Libraries
Source:  hdf5-%{hdf5_pkg_version}.tar.bz2
Source1: szip-%{szip_version}.tar.gz
Patch2:  szip-config.patch
Source2: netcdf-c-%{ncdf_c_version}.tar.gz
Patch3:  netcdf_hdf5_1.8.13.patch
Source3: netcdf-fortran-%{ncdf_ftn_version}.tar.gz
Source4: netcdf-cxx4-%{ncdf_cxx4_version}.tar.gz
Source5: netcdf-cxx-%{ncdf_cxx_version}.tar.gz
Packager: TACC - mclay@tacc.utexas.edu
URL: http://hdf.ncsa.uiuc.edu/HDF5/

%define APPS     /opt/apps
%define MODULES modulefiles

%define debug_package %{nil}
%include rpm-dir.inc
%include compiler-defines.inc

# This is a hack to prevent mpi-defines.inc to complain if mpi is not set.
# CRF 2015.12.02 added mpi_label
%define  mpi_fam none
%define  mpi_label none
%include mpi-defines.inc



%if "%{mpi_fam}" == "none"
   # build non-parallel version of package
   %define HDF5_BASE_DIR         %{APPS}/%{comp_fam_ver}/hdf5/%{hdf5_version}

   %define HDF5_INSTALL_DIR      %{HDF5_BASE_DIR}/x86_64
   %define MIC_HDF5_INSTALL_DIR  %{HDF5_BASE_DIR}/k1om
   %define HDF5_MODULE_DIR       %{APPS}/%{comp_fam_ver}/%{MODULES}/hdf5

   %define NCDF_BASE_DIR         %{APPS}/%{comp_fam_ver}/netcdf/%{ncdf_version}

   %define NCDF_INSTALL_DIR      %{NCDF_BASE_DIR}/x86_64
   %define MIC_NCDF_INSTALL_DIR  %{NCDF_BASE_DIR}/k1om
   %define NCDF_MODULE_DIR       %{APPS}/%{comp_fam_ver}/%{MODULES}/netcdf

   %define RPM_NAME              tacc-%{name}-%{comp_fam_ver}%{dbg}
   %define MY_VERSION            (Serial Version)

   %{echo: NO MPI\n}
%else
   # build parallel version of package
   %define HDF5_BASE_DIR         %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/phdf5/%{hdf5_version}

   %define HDF5_INSTALL_DIR      %{HDF5_BASE_DIR}/x86_64
   %define MIC_HDF5_INSTALL_DIR  %{HDF5_BASE_DIR}/k1om
   %define HDF5_MODULE_DIR       %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/phdf5

   %define NCDF_BASE_DIR         %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/parallel-netcdf/%{ncdf_version}

   %define NCDF_INSTALL_DIR      %{NCDF_BASE_DIR}/x86_64
   %define MIC_NCDF_INSTALL_DIR  %{NCDF_BASE_DIR}/k1om
   %define NCDF_MODULE_DIR       %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/parallel-netcdf

   %define RPM_NAME              tacc-p%{name}-%{comp_fam_ver}-%{mpi_fam_ver}%{dbg}
   %define MY_VERSION            (Parallel Version)

   %{echo: WITH MPI p%{name}-%{comp_fam_ver}-%{mpi_fam_ver}\n}
   %{echo: WITH MPI %{RPM_NAME}\n}
%endif

%package -n %{RPM_NAME}
Summary: HDF5 library, Netcfd 4
Group: Development/Libraries

%description
%description -n %{RPM_NAME}
HDF5 is:
* A versatile data model that can represent very complex data objects and a wide variety of metadata.
* A completely portable file format with no limit on the number or size of data objects in the collection.
* A software library that runs on a range of computational platforms, from laptops to massively parallel systems, and implements a high-level API with C and Fortran 90 interfaces.
* A rich set of integrated performance features that allow for access time and storage space optimizations.
* Tools and applications for managing, manipulating, viewing, and analyzing the data in the collection.

NetCDF (network Common Data Form) is an interface for array-oriented data
access and a library that provides an implementation of the interface. The
netCDF library also defines a machine-independent format for representing
scientific data. Together, the interface, library, and format support the
creation, access, and sharing of scientific data. The netCDF software was
developed at the Unidata Program Center in Boulder, Colorado.

%prep

rm -rf hdf5-%{hdf5_pkg_version}
%setup -n hdf5-%{hdf5_pkg_version}
# The second call untars the second source, in a subdirectory
# of the first. 
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory. 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -n hdf5-%{hdf5_pkg_version} -T -D -a 1
cd szip-2.1
%patch2 -p0 

# netcdf-c
rm -rf ../netcdf-c-%{ncdf_c_version}
%setup -T -D -b 2 -n netcdf-c-%{ncdf_c_version}
#patch3 -p1

# netcdf-fortran
rm -rf ../netcdf-fortran-%{ncdf_ftn_version}
%setup -T -D -b 3 -n netcdf-fortran-%{ncdf_ftn_version}
cd ../
pwd
#patch4 -p1

# netcdf-cxx4
rm -rf ../netcdf-cxx4-%{ncdf_cxx4_version}
%setup -T -D -b 4 -n netcdf-cxx4-%{ncdf_cxx4_version}
cd ../
pwd
#patch5 -p1

# netcdf-cxx
# This is for legacy C++ support
rm -rf ../netcdf-cxx-%{ncdf_cxx_version}
%setup -T -D -b 5 -n netcdf-cxx-%{ncdf_cxx_version}
cd ../
pwd


%build

%install
%include system-load.inc
%include compiler-load.inc
%include mpi-load.inc

%if "%{is_debug}" == "1"
  DEBUG_FLAGS="--enable-using-memchecker=yes  --enable-clear-file-buffers=yes"
%endif

%if "%{comp_fam}" == "pgi"
  export LDFLAGS="-Mconcur=nonuma -nomp=nonuma"
%endif

%if "%{comp_fam}" == "intel"
  export CFLAGS="-diag-disable 10201,10120"
  export CXXFLAGS="-diag-disable 10201,10120"
  LDFLAGS="$LDFLAGS -limf -lm"

  path_icc=$(type -p icc)
  base=${path_icc%%/bin/intel64/icc}
  MIC_LIBS=${base}/compiler/lib/mic
# CRF 2015.12.02
#  module load zlib
%endif 

CC_serial=$CC

%if "%{mpi_fam}" == "none"
   CONF_OPTS="--enable-cxx"
%endif


%if "%{mpi_fam}" != "none"
   CC=mpicc
   CXX=mpicxx
   FC=mpif90
   F77=mpif77
   F90=$FC
   CONF_OPTS="--enable-parallel"
   PARALLEL="--enable-parallel"
%endif

module load autotools

FC_ORIG=$FC

TmpfsA=()

archA=()

have_k1om=""
if [ "%{comp_mic_support}" = 1 ]; then
  have_k1om="k1om"
fi

if [ "%{mpi_fam}" != none -a "%{mpi_mic_support}" != 1 ]; then
  have_k1om=""
fi

if [ -n "$have_k1om" ]; then
  archA+=($have_k1om)
fi

archA+=("x86_64")

cd ../hdf5-%{hdf5_pkg_version}
########################################################################
# Build HDF5
########################################################################

HDF5_DIR=`pwd`
WD=`pwd`


echo  "%@@%========================================="
echo  "Building HDF5 system"
echo  "%@@%========================================="


for ARCH in "${archA[@]}"; do

  INSTALL_DIR="%{HDF5_BASE_DIR}/$ARCH"

  FC=$FC_ORIG
  FFLAGS=""
  FCLAGS=""
  CFLAGS=""
  CXXFLAGS=""
  LDFLAGS=""
  HOST=""
  ZLIB_LIB=$TACC_ZLIB_LIB
  if [ "$ARCH" = "k1om" ]; then
     LDFLAGS="-mmic -Wl,-rpath,$MIC_LIBS -L$MIC_LIBS"
     FC="$FC ${LDFLAGS}"
     CFLAGS="-mmic"
     FFLAGS="-mmic"
     FCLAGS="-mmic"
     CXXFLAGS="-mmic"
     HOST="--host=x86_64-linux"
     ZLIB_LIB=$MIC_TACC_ZLIB_LIB
  fi
  echo $PATH | sed -e 's/:/\n/g'

# CRF 2015.12.01 - tacctmpfs not ready in ls5
#  tacctmpfs -m $INSTALL_DIR
  mkdir -p $INSTALL_DIR
  mount -t tmpfs tmpfs $INSTALL_DIR
  rm -rf $INSTALL_DIR/*
#  rm    -rf $RPM_BUILD_ROOT/$INSTALL_DIR/*


  # Remember all tmpfs dirs for later umount.
  TmpfsA+=($INSTALL_DIR)

  cd szip-%{szip_version}

  echo  "%@@%========================================="
  echo  "Building HDF5: szip $ARCH"
  echo  "%@@%========================================="

  CC=$CC_serial CFLAGS=$CFLAGS ./configure --prefix=$INSTALL_DIR $HOST
  make
  make install
  make distclean



  if [ "$ARCH" = "k1om" ]; then
    ssh mic0 tacctmpfs -m $INSTALL_DIR
    cd $INSTALL_DIR
    scp -r * mic0:`pwd`
  fi
  cd $WD
  

  echo  "%@@%========================================="
  echo  "Building HDF5: $ARCH"
  echo  "%@@%========================================="

  export FFLAGS="$FFLAGS -O3 -fPIC"
  export FCLAGS="$FCLAGS -O3 -fPIC"
  export CFLAGS="$CFLAGS -O3 -fPIC"
  export CXXFLAGS="$CXXFLAGS -O3 -fPIC"
  if [ -n "$ZLIB_LIB" ]; then
    export LDFLAGS="$LDFLAGS -Wl,-rpath,$ZLIB_LIB -L$ZLIB_LIB"
  fi
  export LDFLAGS="$LDFLAGS -Wl,-rpath,$INSTALL_DIR/lib -L$INSTALL_DIR/lib -lsz -lz"



  export LD_LIBRARY_PATH="$INSTALL_DIR:$LD_LIBRARY_PATH:$INSTALL_DIR"

  ./configure --prefix=$INSTALL_DIR --enable-production --with-szlib=$INSTALL_DIR --enable-fortran --enable-fortran2003 --enable-shared $CONF_OPTS $DEBUG_FLAGS

  make V=1 -j 4

  make install
  make distclean

  mkdir -p              $RPM_BUILD_ROOT/$INSTALL_DIR
  cp -r $INSTALL_DIR/ $RPM_BUILD_ROOT/$INSTALL_DIR/..

  if [ "$ARCH" = "k1om" ]; then
    cd $INSTALL_DIR
    scp -r * mic0:`pwd`
    cd $WD
  fi
done

## Module for hdf
mkdir -p $RPM_BUILD_ROOT/%{HDF5_MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{HDF5_MODULE_DIR}/%{hdf5_version}.lua << EOF
local help_msg=[[
The HDF5 module defines the following environment variables:
TACC_HDF5_DIR, TACC_HDF5_DOC, TACC_HDF5_LIB, and TACC_HDF5_INC for
the location of the HDF5 distribution, documentation,
libraries, and include files, respectively.

To use the HDF5 library, compile the source code with the option:

     -I\$TACC_HDF5_INC

and add the following options to the link step: 

     -Wl,-rpath,\$TACC_HDF5_LIB -L\$TACC_HDF5_LIB -lhdf5 -lz

The -Wl,-rpath,\$TACC_HDF5_LIB option is not required, however,
if it is used, then this module will not have to be loaded
to run the program during future login sessions.

]]

local help_msg_mic=[[
-----------------------------
To build a MIC native code:
-----------------------------

Compile the source code with the option:

     -I\$MIC_TACC_HDF5_INC

and add the following options to the link step: 

     -Wl,-rpath,\$MIC_TACC_HDF5_LIB -L\$MIC_TACC_HDF5_LIB -lhdf5 -lz
]]

local help_msg_version = [[

Version %{hdf5_version}
]]




whatis("Name: HDF5")
whatis("Version: %{hdf5_version}")
whatis("Category: library, runtime support")
whatis("Keywords: I/0, Library")
whatis("Description: General purpose library and file format for storing scientific data %{MY_VERSION}.")
whatis("URL: http://www.hdfgroup.org/HDF5/")

%if "%{is_debug}" == "1"
setenv("TACC_HDF5_DEBUG","1")
%endif


-- Create environment variables.


local hdf5_dir    = "%{HDF5_INSTALL_DIR}"
local hdf5_micdir = "%{MIC_HDF5_INSTALL_DIR}"

family("hdf5")
setenv(       "TACC_HDF5_DIR",    hdf5_dir)
setenv(       "TACC_HDF5_DOC",    pathJoin(hdf5_dir,"doc"))
setenv(       "TACC_HDF5_INC",    pathJoin(hdf5_dir,"include"))
setenv(       "TACC_HDF5_LIB",    pathJoin(hdf5_dir,"lib"))

setenv(       "TACC_HDF5_BIN",    pathJoin(hdf5_dir,"bin"))
prepend_path( "PATH"         ,    pathJoin(hdf5_dir,"bin"))
prepend_path( "LD_LIBRARY_PATH",  pathJoin(hdf5_dir,"lib"))

local have_mic = ("$have_k1om" == "k1om")

if (have_mic) then
   help(help_msg, help_msg_mic, help_msg_version)
   setenv(       "MIC_TACC_HDF5_DIR",    hdf5_micdir)
   setenv(       "MIC_TACC_HDF5_DOC",    pathJoin(hdf5_micdir,"doc"))
   setenv(       "MIC_TACC_HDF5_INC",    pathJoin(hdf5_micdir,"include"))
   setenv(       "MIC_TACC_HDF5_LIB",    pathJoin(hdf5_micdir,"lib"))
   setenv(       "MIC_TACC_HDF5_BIN",    pathJoin(hdf5_micdir,"bin"))
   prepend_path( "MIC_LD_LIBRARY_PATH",  pathJoin(hdf5_micdir,"lib"))
   add_property("arch","mic")
else
   help(help_msg, help_msg_version)
end

EOF

cat > $RPM_BUILD_ROOT/%{HDF5_MODULE_DIR}/.version.%{hdf5_version} << 'EOF'
#%Module1.0#################################################
##
## version file for HDF5
##

set     ModulesVersion      "%{hdf5_version}"
EOF


%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{HDF5_MODULE_DIR}/%{hdf5_version}.lua

########################################################################
# Build netcdf
########################################################################

cd $HDF5_DIR
cd ../netcdf-c-%{ncdf_c_version}

WD=`pwd`

echo  "%@@%========================================="
echo  "Building netcdf system"
echo  "%@@%========================================="


for ARCH in "${archA[@]}"; do

  INSTALL_DIR=%{NCDF_BASE_DIR}/$ARCH

  TACC_HDF5_INC=%{HDF5_BASE_DIR}/$ARCH/include
  TACC_HDF5_LIB=%{HDF5_BASE_DIR}/$ARCH/lib


  FC=$FC_ORIG
  FFLAGS=""
  FCLAGS=""
  CFLAGS=""
  CXXFLAGS=""
  LDFLAGS=""
  export FFLAGS="-O3 -fPIC"
  export FCFLAGS="-O3 -fPIC"
  export CFLAGS="-O3 -fPIC"
  export CXXFLAGS="-O3 -fPIC"

  HOST=""
  ZLIB_LIB=$TACC_ZLIB_LIB

  if [ "$ARCH" = k1om ]; then
     LDFLAGS="-mmic -Wl,-rpath,$MIC_LIBS -L$MIC_LIBS"
     FC="$FC ${LDFLAGS}"
     FFLAGS="-mmic  $FCFLAGS"
     FCFLAGS="-mmic  $FCFLAGS"
     CFLAGS="-mmic  $CCFLAGS"
     CXXFLAGS="-mmic $CXXFLAGS"
     ZLIB_LIB=$MIC_TACC_ZLIB_LIB
  fi
    


# CRF 2015.12.01 - tacctmpfs not ready in ls5
#  tacctmpfs -m $INSTALL_DIR
  mkdir -p $INSTALL_DIR
  mount -t tmpfs tmpfs $INSTALL_DIR
  rm -rf $INSTALL_DIR/*

  # Remember all tmpfs dirs for later umount.
  TmpfsA+=($INSTALL_DIR)


  echo  "%@@%========================================="
  echo  "Building netcdf $ARCH netcdf4"
  echo  "%@@%========================================="
  export CFLAGS="${CFLAGS} -I${TACC_HDF5_INC}" 
  export FCFLAGS="${FCFLAGS} -I${TACC_HDF5_INC}" 
  export FFLAGS="${FFLAGS} -I${TACC_HDF5_INC}" 
  export CXXFLAGS="${CXXFLAGS} -I${TACC_HDF5_INC}" 
  export CPPFLAGS="${CPPFLAGS} -I${TACC_HDF5_INC}" 
  if [ -n "$ZLIB_LIB" ]; then
    export LDFLAGS="$LDFLAGS -Wl,-rpath,$ZLIB_LIB -L$ZLIB_LIB"
  fi
  export LDFLAGS="${LDFLAGS} -Wl,-rpath,${TACC_HDF5_LIB} -L${TACC_HDF5_LIB}" 
  
  cd $HDF5_DIR
  cd ../netcdf-c-%{ncdf_c_version}

  rm -rf tacc_${ARCH}
  mkdir tacc_${ARCH}
  cd tacc_${ARCH}

  ../configure --prefix=$INSTALL_DIR --disable-dap --enable-shared --enable-netcdf-4 
  make -j 3
  make install
  make distclean
  cd ..
  
  if [ "$ARCH" = "k1om" ]; then
    ssh mic0 tacctmpfs -m $INSTALL_DIR
    cd $INSTALL_DIR
    scp -r * mic0:`pwd`
    cd $WD
  fi


  echo  "%@@%========================================="
  echo  "Building netcdf $ARCH netcdf-fortran"
  echo  "%@@%========================================="
  #Install fortran libraries
  cd ../netcdf-fortran-%{ncdf_ftn_version}
  export CFLAGS="-I$INSTALL_DIR/include ${CFLAGS}" 
  export FCFLAGS="-I$INSTALL_DIR/include ${FCFLAGS}"
  export FFLAGS="-I$INSTALL_DIR/include ${FFLAGS}"
  export LDFLAGS="-Wl,-rpath,$INSTALL_DIR/lib -L$INSTALL_DIR/lib ${LDFLAGS}" 

  rm -rf tacc_${ARCH}
  mkdir tacc_${ARCH}
  cd tacc_${ARCH}

  ../configure --prefix=$INSTALL_DIR --enable-shared $PARALLEL
  make -j 3
  make install
  make distclean
  cd ..
  
  
  echo  "%@@%========================================="
  echo  "Building netcdf $ARCH netcdf-cxx4"
  echo  "%@@%========================================="

  #Install for c++ libraries
  cd ../netcdf-cxx4-%{ncdf_cxx4_version}
  export CXXFLAGS="-I$INSTALL_DIR/include ${CXXFLAGS}" 
  export CPPFLAGS="-I$INSTALL_DIR/include ${CPPFLAGS}" 

  rm -rf tacc_${ARCH}
  mkdir tacc_${ARCH}
  cd tacc_${ARCH}
  ../configure --prefix=$INSTALL_DIR --enable-shared $PARALLEL
  make -j 3
  make install
  make distclean
  cd ..

  echo  "%@@%========================================="
  echo  "Building netcdf $ARCH netcdf-cxx legacy"
  echo  "%@@%========================================="
  cd ../netcdf-cxx-%{ncdf_cxx_version}
  rm -rf tacc_${ARCH}
  mkdir tacc_${ARCH}
  cd tacc_${ARCH}
  ../configure --prefix=$INSTALL_DIR --enable-shared 
  make -j 3
  make install
  make distclean
  cd ..

  mkdir -p            $RPM_BUILD_ROOT/$INSTALL_DIR
  cp -r $INSTALL_DIR/ $RPM_BUILD_ROOT/$INSTALL_DIR/..
done

# CRF 2015.12.02
for i in "${TmpfsA[@]}"; do
  case $i in
    *k1om*)
      ssh mic0 tacctmpfs -u $i
      tacctmpfs -u $i
      ;;
    *x86_64*)
      umount $i
      #tacctmpfs -u $i
      ;;
  esac
done


## Module for netcdf
mkdir -p $RPM_BUILD_ROOT/%{NCDF_MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{NCDF_MODULE_DIR}/%{ncdf_version}.lua << EOF
local help_msg=[[
The netcdf module file defines the following environment variables:
TACC_NETCDF_DIR, TACC_NETCDF_BIN, TACC_NETCDF_LIB, and 
TACC_NETCDF_INC forthe location of the NETCDF distribution, binaries,
libraries, and include files, respectively.

IMPORTANT NOTE: TACC has several different versions of netcdf installed.  Below is a list of each module type:

netcdf/3.6.3           -- Classic netcdf (serial)
netcdf/4.x.x           -- Serial version of Netcdf4 based upon hdf5 and is backwards compatiable with classic netcdf (serial)
parallel-netcdf/4.x.x  -- Parallel version of Netcdf4 based upon parallel hdf5 (parallel)
pnetcdf/1.x.x          -- Parallel netcdf(PnetCDF) that supports netcdf in the classic formats, CDF-1 and CDF-2 (parallel)


NETCDF %{ncdf_version} uses the hdf5 libraries to support the NETCDF 4 file format 
in addition to the classic NETCDF file format. 

To use the NETCDF library, compile the source code with the option:

	-I\${TACC_NETCDF_INC} 

Add the following options to the link step for C codes: 

	-L\${TACC_NETCDF_LIB} -lnetcdf 

Add the following options to the link step for Fortran codes: 

	-L\${TACC_NETCDF_LIB} -lnetcdf -lnetcdff 

Add the following options to the link step for C++ codes: 

	-L\${TACC_NETCDF_LIB} -lnetcdf -lnetcdf_c++4 

Version %{ncdf_version}


]]

local help_msg_mic=[[
-----------------------------
To build a MIC native code:
-----------------------------

Compile the source code with the option:

     -I\$MIC_TACC_NETCDF_INC

and add the following options to the link step: 
     -Wl,-rpath,\${MIC_TACC_NETCDF_LIB} -L\${MIC_TACC_NETCDF_LIB} -lnetcdf

]]

local help_msg_version = [[

Version %{ncdf_version}
]]

whatis("NetCDF: Network Common Data Form")
whatis("Version: %{ncdf_version}")
whatis("Category: library, runtime support")
whatis("Keywords: I/O, Library")
whatis("Description: I/O library which stores and retrieves data in self-describing, machine-independent datasets %{MY_VERSION}." )
whatis("URL: http://www.unidata.ucar.edu/software/netcdf/")

local ncdf_dir    = "%{NCDF_INSTALL_DIR}"
local ncdf_micdir = "%{MIC_NCDF_INSTALL_DIR}"

--Prepend paths

prepend_path("LD_LIBRARY_PATH",	pathJoin(ncdf_dir,"lib"))
prepend_path("PATH",           	pathJoin(ncdf_dir,"bin"))
prepend_path("MANPATH",        	pathJoin(ncdf_dir,"share/man"))
prepend_path("PKG_CONFIG_PATH",	pathJoin(ncdf_dir,"lib/pkgconfig"))

--Env variables 
setenv("TACC_NETCDF_DIR", ncdf_dir)
setenv("TACC_NETCDF_INC", pathJoin(ncdf_dir,"include"))
setenv("TACC_NETCDF_LIB", pathJoin(ncdf_dir,"lib"))
setenv("TACC_NETCDF_BIN", pathJoin(ncdf_dir,"bin"))

local have_mic = ("$have_k1om" == "k1om")

if (have_mic) then

   --MIC Env variables 
   help(help_msg,help_msg_mic,help_msg_version)
   prepend_path("MIC_LD_LIBRARY_PATH", pathJoin(ncdf_micdir,"lib"))
   prepend_path("MIC_PKG_CONFIG_PATH", pathJoin(ncdf_micdir,"lib/pkgconfig"))
   setenv("MIC_TACC_NETCDF_DIR", ncdf_micdir)
   setenv("MIC_TACC_NETCDF_INC", pathJoin(ncdf_micdir, "include"))
   setenv("MIC_TACC_NETCDF_LIB", pathJoin(ncdf_micdir, "lib"))
   setenv("MIC_TACC_NETCDF_BIN", pathJoin(ncdf_micdir, "bin"))
   add_property("arch","mic")
else
   help(help_msg, help_msg_version)
end


-- prepend path

EOF

cat > $RPM_BUILD_ROOT/%{NCDF_MODULE_DIR}/.version.%{ncdf_version} << 'EOF'
#%Module1.0#################################################
##
## version file for HDF5
##

set     ModulesVersion      "%{ncdf_version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{NCDF_MODULE_DIR}/%{ncdf_version}.lua

%files -n %{RPM_NAME}
%defattr(-,root,install)
%{HDF5_BASE_DIR}
%{HDF5_MODULE_DIR}
%{NCDF_BASE_DIR}
%{NCDF_MODULE_DIR}


%post

%clean
rm -rf $RPM_BUILD_ROOT

