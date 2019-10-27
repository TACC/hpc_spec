#
# Kevin Schmidt was original author of this spec file
# 2019-06-12
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

Summary: PLATO Engine/Analyze design tools.

# Give the package a base name
%define pkg_base_name plato
%define MODULE_VAR    PLATO

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 6
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
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
License:   GUN
Group:     Sandia National Laboratories
URL:       https://sierradist.sandia.gov/licensing.html
Packager:  TACC - kschmidt@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
The PLATO Engine computer program serves as a collaborative testbed rich in
light-weight synthesis tools for optimization-based design. PLATO Engine is a
research code designed to facilitate collaboration with academia, labs and
industries by providing interfaces for plug-n-play insertion of synthesis
technologies in the areas of modeling, analysis and optimization. Currently,
PLATO Engine offers a set of light-weight tools for finite element analysis,
linear- and nonlinear-programming, and non-gradient based optimization. The
PLATO Engine program is designed to run on high-performance computers.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
The PLATO Engine computer program serves as a collaborative testbed rich in
light-weight synthesis tools for optimization-based design. PLATO Engine is a
research code designed to facilitate collaboration with academia, labs and
industries by providing interfaces for plug-n-play insertion of synthesis
technologies in the areas of modeling, analysis and optimization. Currently,
PLATO Engine offers a set of light-weight tools for finite element analysis,
linear- and nonlinear-programming, and non-gradient based optimization. The
PLATO Engine program is designed to run on high-performance computers.

%description
The PLATO Engine computer program serves as a collaborative testbed rich in
light-weight synthesis tools for optimization-based design. PLATO Engine is a
research code designed to facilitate collaboration with academia, labs and
industries by providing interfaces for plug-n-play insertion of synthesis
technologies in the areas of modeling, analysis and optimization. Currently,
PLATO Engine offers a set of light-weight tools for finite element analysis,
linear- and nonlinear-programming, and non-gradient based optimization. The
PLATO Engine program is designed to run on high-performance computers.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  rm -rf  %{_builddir}/PLATO

#%setup -n %{pkg_base_name}-%{pkg_version}

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
%include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
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
# Build script for PLATO Analyze
WD=`pwd`

###############################################################################
# USER INPUT
###############################################################################

PD=$WD/PLATO  # Root directory for PLATO
#if [ -e "$PD" ]; then
#  echo -e "\nPLATO_ROOT directory exists!\nEither remove "$PD" or rename.\n"
#  exit
#fi
mkdir -p $PD/{build,src}

###############################################################################
# REQUIRES:
# Modules|Software: gcc/5.2.0,cuda/9.0,mkl/18.0.2,netcdf/4.6.2,boost/1.68|zlib
###############################################################################

#ml gcc/5.2.0 #no CUDA9.0 support for gcc > 6
#6-12-19, current working build uses gcc/5.2.0
ml gcc/5.2.0
ml cmake/3.12.3
ml cuda/9.0 # 
ml mkl/18.0.2 #math libraries for Trilinos
ml netcdf/4.6.2
ml boost/1.68

PLATO_ROOT=$PD
CMAKE=`which cmake`
NPMAKE=10 # Number of Processors to Use During Make (e.g., make -j $NPMAKE)

###############################################################################
# DOWNLOADS:
#   AMGX (git clone https://github.com/NVIDIA/AMGX.git)
#   Trilinos (git clone https://github.com/trilinos/Trilinos.git)
#   nvcc_wrapper (git clone https://github.com/platoengine/nvcc_wrapper.git)
#   omega_h (v9.18)
#   All clones/wgets are placed in PLATO/src
###############################################################################

echo -e "Downloading into $PD/src..."
cd $PD/src
git clone https://github.com/NVIDIA/AMGX.git
git clone https://github.com/trilinos/Trilinos.git
git clone https://github.com/platoengine/nvcc_wrapper.git
git clone https://github.com/SNLComputation/omega_h.git
git clone https://github.com/platoengine/platoengine.git
git clone https://github.com/SNLComputation/lgrtk.git

# NVCC Changes
sed -i 's/@NVCC_WRAPPER_ARCH@/35/g;s/@NVCC_WRAPPER_COMPILER@/`which mpicxx`/g' $PD/src/nvcc_wrapper/nvcc_wrapper
###############################################################################
# AMGX
###############################################################################

# Checkout Specific AMGX Commit (this one works)
#6-12-19, current working build can use latest amgx
#cd $PD/src/AMGX && git checkout 3049527e0c396424df4582e837f9dd89a20f50df
mkdir $PD/build/AMGX && cd $PD/build/AMGX

AMGX_SRC=$PLATO_ROOT/src/AMGX
AMGX_INSTALL=%{INSTALL_DIR}/AMGX

$CMAKE $AMGX_SRC \
-DCMAKE_CXX_COMPILER=`which mpicxx` \
-DCMAKE_C_COMPILER=`which mpicc` \
-DCMAKE_INSTALL_PREFIX:PATH=$AMGX_INSTALL \
-DBUILD_SHARED_LIBS:BOOL=ON \
2>&1 | tee $PD/build/AMGX/.user.config.log

make -j $NPMAKE 2>&1 | tee $PD/build/AMGX/.user.make.log
make -j $NPMAKE DESTDIR=$RPM_BUILD_ROOT install 2>&1 | tee $PD/build/AMGX/.user.install.log

###############################################################################
# Trilinos
# For use with intel/mkl lapack/BLAS
# This configuration file is needed to enable optimization with Plato Analyze:
# this is the serial build
###############################################################################

# Checkout Specific Trilinos Commit (this one works)
#cd $PD/src/Trilinos && git checkout c56446dd2419e2059db8851c80cf52dbf0c9d4d6
#6-12-19, current working plato build uses trilinos-release-12-14-branch
cd $PD/src/Trilinos && git checkout trilinos-release-12-14-branch 
mkdir $PD/build/Trilinos && cd $PD/build/Trilinos

TRILINOS_SRC=$PLATO_ROOT/src/Trilinos
TRILINOS_INSTALL=%{INSTALL_DIR}/Trilinos
NVCC_WRAPPER=$PLATO_ROOT/src/nvcc_wrapper/nvcc_wrapper

$CMAKE $TRILINOS_SRC \
-DCMAKE_INSTALL_PREFIX:PATH=$TRILINOS_INSTALL \
-DCMAKE_BUILD_TYPE:STRING=NONE \
-DCMAKE_CXX_COMPILER:FILEPATH=$NVCC_WRAPPER \
-DCMAKE_C_COMPILER:FILEPATH=`which mpicc` \
-DCMAKE_Fortran_COMPILER:FILEPATH=`which mpif90` \
-DCMAKE_CXX_FLAGS:STRING="-O3 -g" \
-DCMAKE_C_FLAGS:STRING="-O3 -g" \
-DTrilinos_ENABLE_Fortran:BOOL=ON \
-DBUILD_SHARED_LIBS:BOOL=ON \
-DTPL_ENABLE_MPI:BOOL=ON \
-DKokkos_ENABLE_Serial:BOOL=ON \
-DKokkos_ENABLE_OpenMP:BOOL=OFF \
-DKokkos_ENABLE_Pthread:BOOL=OFF \
-DKokkos_ENABLE_Cuda:BOOL=ON \
-DKokkos_ENABLE_Cuda_UVM:BOOL=OFF \
-DKokkos_ENABLE_Cuda_Lambda:BOOL=ON \
-DTrilinos_ENABLE_ALL_PACKAGES:BOOL=OFF \
-DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF \
-DTrilinos_ENABLE_TeuchosParameterList:BOOL=ON \
-DTrilinos_ENABLE_TeuchosComm:BOOL=ON \
-DTrilinos_ENABLE_TeuchosParser:BOOL=ON \
-DTrilinos_ENABLE_KokkosCore:BOOL=ON \
-DTrilinos_ENABLE_KokkosContainers:BOOL=ON \
-DTrilinos_ENABLE_Sacado:BOOL=ON \
-DSacado_ENABLE_KokkosCore:BOOL=ON \
-DSacado_ENABLE_Teuchos:BOOL=ON \
-DTrilinos_ENABLE_SEACASExodus:BOOL=ON \
-DTrilinos_ENABLE_SEACASNemesis:BOOL=ON \
-DTrilinos_ENABLE_SEACASEpu:BOOL=ON \
-DTrilinos_ENABLE_SEACASExodiff:BOOL=ON \
-DTrilinos_ENABLE_SEACASNemslice:BOOL=ON \
-DTrilinos_ENABLE_SEACASNemspread:BOOL=ON \
-DTrilinos_ENABLE_STKMesh:BOOL=ON \
-DTrilinos_ENABLE_STKIO:BOOL=ON \
-DTrilinos_ENABLE_Intrepid:BOOL=ON \
-DTrilinos_ENABLE_Epetra:BOOL=ON \
-DTrilinos_ENABLE_EpetraExt:BOOL=ON \
-DTrilinos_ENABLE_AztecOO:BOOL=ON \
-DTrilinos_ENABLE_Anasazi:BOOL=ON \
-DTrilinos_ENABLE_ML:BOOL=ON \
-DBLAS_INCLUDE_DIRS:PATH="${TACC_MKL_INC}" \
-DBLAS_LIBRARY_DIRS:PATH="${TACC_MKL_LIB}" \
-DBLAS_LIBRARY_NAMES:STRING="mkl_intel_lp64;mkl_sequential;mkl_core;pthread" \
-DLAPACK_INCLUDE_DIRS:PATH="${TACC_MKL_INC}" \
-DLAPACK_LIBRARY_DIRS:PATH="${TACC_MKL_LIB}" \
-DLAPACK_LIBRARY_NAMES:STRING="mkl_intel_lp64;mkl_sequential;mkl_core;pthread" \
-DNetcdf_LIBRARY_DIRS:STRING="${TACC_NETCDF_LIB}" \
-DNetcdf_INCLUDE_DIRS:STRING="${TACC_NETCDF_INC}" \
-DTrilinos_CXX11_FLAGS:STRING="-std=c++11 -expt-extended-lambda -lineinfo" \
-DBoost_INCLUDE_DIRS:STRING="${TACC_BOOST_INC}" \
-DBoostLib_LIBRARY_DIRS:STRING="${TACC_BOOST_LIB}" \
-DBoostLib_INCLUDE_DIRS:STRING="${TACC_BOOST_INC}" \
2>&1 | tee $PD/build/Trilinos/.user.config.log

make -j $NPMAKE 2>&1 | tee $PD/build/Trilinos/.user.make.log
make -j $NPMAKE DESTDIR=$RPM_BUILD_ROOT install 2>&1 | tee $PD/build/Trilinos/.user.install.log

###############################################################################
# For omega_h
# May need to change bob.cmake file (comment out -Werror lines [2 in total])
###############################################################################

# Checkout Specific omega_h Commit (this one works)
#cd $PD/src/omega_h && git checkout 26ca8fd44afe6e9afdf2a6081bc5337f929b0096
#6-12-19, current working version of plato needs omega v9.26.5
cd $PD/src/omega_h && git checkout v9.26.5
#6-12-19, need to delete -Werror lines in bob.cmake file bc
#	  these are warnings that prevent a successful build
sed -i -e's/-Werror//g' cmake/bob.cmake
mkdir $PD/build/omega_h && cd $PD/build/omega_h
# Remove offending lines (could be a version mismatch) 
#sed -i '/-Werror/d' $PD/src/omega_h/cmake/bob.cmake
export PATH=$RPM_BUILD_ROOT/Trilinos/bin:$PATH
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/Trilinos/lib:$LD_LIBRARY_PATH
OMEGA_H_SRC=$PLATO_ROOT/src/omega_h
OMEGA_H_INSTALL=%{INSTALL_DIR}/omega_h
TRILINOS_INSTALL_TEMP=$RPM_BUILD_ROOT/$TRILINOS_INSTALL

$CMAKE $OMEGA_H_SRC \
-DCMAKE_INSTALL_PREFIX:PATH=$OMEGA_H_INSTALL \
-DBUILD_SHARED_LIBS:BOOL=ON \
-DCMAKE_CXX_COMPILER:FILEPATH=$NVCC_WRAPPER \
-DOmega_h_USE_Trilinos:BOOL=ON \
-DTrilinos_PREFIX:PATH=$TRILINOS_INSTALL_TEMP \
-DOmega_h_USE_ZLIB:BOOL=ON \
-DOmega_h_CHECK_BOUNDS=ON \
2>&1 | tee $PD/build/omega_h/.user.config.log

make -j $NPMAKE 2>&1 | tee $PD/build/omega_h/.user.make.log
make -j $NPMAKE DESTDIR=$RPM_BUILD_ROOT install 2>&1 | tee $PD/build/omega_h/.user.install.log

###############################################################################
# For platoengine
# This configuration file is needed to build plato engine 
#   and enable optimization with analyze
###############################################################################

# Checkout Specific platoengine Commit (this one works)
#cd $PD/src/platoengine && git checkout 765d272dda13f48038fd8ffcb139a98b045c2051
#6-12-19, current working build of plato can use latest platoengine

mkdir $PD/build/platoengine && cd $PD/build/platoengine

ANALYZE_PATH=$PLATO_ROOT/build/analyze
PLATO_ENGINE_SRC=$PLATO_ROOT/src/platoengine
PLATO_ENGINE_INSTALL=%{INSTALL_DIR}/platoengine
#Trilinos_DIR=%{INSTALL_DIR}/Trilinos/include
Trilinos_DIR=$TRILINOS_INSTALL_TEMP/include

$CMAKE $PLATO_ENGINE_SRC \
-DCMAKE_INSTALL_PREFIX:PATH=$PLATO_ENGINE_INSTALL \
-DCMAKE_CXX_COMPILER:FILEPATH=$NVCC_WRAPPER \
-DCMAKE_C_COMPILER=`which mpicc` \
-DBUILD_SHARED_LIBS:BOOL=ON \
-DPLATOMAIN:BOOL=ON \
-DPLATOSTATICS:BOOL=ON \
-DANALYZE:BOOL=OFF \
-DREGRESSION:BOOL=ON \
-DPLATOPROXY:BOOL=ON \
-DSTK_ENABLED:BOOL=ON \
-DSEACAS:BOOL=ON \
-DSEACAS_PATH:PATH=$TRILINOS_INSTALL_TEMP \
-DTRILINOS_INSTALL_DIR:PATH=$TRILINOS_INSTALL_TEMP \
-DCMAKE_CXX_FLAGS:STRING="-O3 -g --std=c++11 -arch=sm_35" \
-DCMAKE_C_FLAGS:STRING="-O3 -g --std=c++11" \
-DCMAKE_EXE_LINKER_FLAGS:STRING="-fopenmp" \
2>&1 | tee $PD/build/platoengine/.user.config.log

make -j $NPMAKE 2>&1 | tee $PD/build/platoengine/.user.make.log
make -j $NPMAKE DESTDIR=$RPM_BUILD_ROOT install 2>&1 | tee $PD/build/platoengine/.user.install.log

###############################################################################
# For platoAnalyze ($PLATO_ROOT/src/lgrtk)
# This configuration file is needed to build Plato Analyze 
#   and enable optimization through the Plato Engine
###############################################################################

# Checkout Specific analyze Commit (this one works)
#cd $PD/src/lgrtk && git checkout f2da8ab650ddc4dc519a33dcade7777b46c61ec1
#6-12-19, don't need above branch for current working build
mkdir $PD/build/analyze && cd $PD/build/analyze

ANALYZE_SRC=$PLATO_ROOT/src/lgrtk
OMEGA_H_INSTALL_TEMP=$RPM_BUILD_ROOT/$OMEGA_H_INSTALL
AMGX_INSTALL_TEMP=$RPM_BUILD_ROOT/$AMGX_INSTALL
PLATO_ENGINE_INSTALL_TEMP=$RPM_BUILD_ROOT/$PLATO_ENGINE_INSTALL

$CMAKE $ANALYZE_SRC \
-DBUILD_SHARED_LIBS:BOOL=ON \
-DTrilinos_PREFIX:PATH=$TRILINOS_INSTALL_TEMP \
-DOMEGA_H_PREFIX:PATH=$OMEGA_H_INSTALL_TEMP \
-DLGR_MPIEXEC:FILEPATH=`which mpiexec` \
-DAMGX_PREFIX:PATH=$AMGX_INSTALL_TEMP \
-DLGR_RANKS_PER_NODE:STRING="2" \
-DPLATO_PREFIX:PATH=$PLATO_ENGINE_INSTALL_TEMP \
-DLGR_ENABLE_PLATO=ON \
-DLGR_ENABLE_PLATO_MPMD=ON \
2>&1 | tee $PD/build/analyze/.user.config.log

make -j $NPMAKE 2>&1 | tee $PD/build/analyze/.user.make.log
#make -j $NPMAKE DESTDIR=$RPM_BUILD_ROOT install 2>&1 | tee $PD/build/analyze/.user.install.log
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/analyze/{bin,lib}
cp -a $PD/build/analyze/{lgr,ROCKET_MPMD,LGR_MPMD} $RPM_BUILD_ROOT/%{INSTALL_DIR}/analyze/bin
cp -a $PD/build/analyze/src/liblgrtk.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/analyze/lib

  # Create some dummy directories and files for fun
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
  
  # Copy everything from tarball over to the installation directory
#  cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
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
local help_msg=[[
The PLATO Engine computer program serves as a collaborative testbed rich in
light-weight synthesis tools for optimization-based design. PLATO Engine is a
research code designed to facilitate collaboration with academia, labs and
industries by providing interfaces for plug-n-play insertion of synthesis
technologies in the areas of modeling, analysis and optimization. Currently,
PLATO Engine offers a set of light-weight tools for finite element analysis,
linear- and nonlinear-programming, and non-gradient based optimization. The
PLATO Engine program is designed to run on high-performance computers.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

Basic usage of PLATO can be found at:

https://github.com/platoengine/platoengine/wiki/Basic-Usage

Version %{pkg_version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: PLATO")
whatis("Version: %{pkg_version}%{dbg}")

-- Create environment variables.
local base_dir                       = "%{INSTALL_DIR}"
local amgx_dir		             = pathJoin(base_dir, "AMGX")
local trilinos_dir		     = pathJoin(base_dir, "Trilinos")
local omegah_dir		     = pathJoin(base_dir, "omega_h")
local platoengine_dir		     = pathJoin(base_dir, "platoengine")
local analyze_dir		     = pathJoin(base_dir, "analyze")

prepend_path(    "PATH",                pathJoin(analyze_dir, "bin"))
prepend_path(    "PATH",                pathJoin(omegah_dir, "bin"))
prepend_path(    "PATH",                pathJoin(platoengine_dir, "bin"))
prepend_path(    "PATH",                pathJoin(trilinos_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(amgx_dir, "lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(analyze_dir, "lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(omegah_dir, "lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(platoengine_dir, "lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(trilinos_dir, "lib"))

setenv( "TACC_%{MODULE_VAR}_DIR",                base_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(base_dir, "platoengine/include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(base_dir, "platoengine/lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(base_dir, "platoengine/bin"))

depends_on( "boost" )
depends_on( "netcdf" )
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

#
# W. Cyrus Proctor
# Antonio Gomez
