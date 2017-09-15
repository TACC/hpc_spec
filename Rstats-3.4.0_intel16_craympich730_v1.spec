#
# David Walling
# 2016-01-12
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
%define pkg_base_name Rstats 
%define MODULE_VAR    RSTATS 

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 4 
%define micro_version 0 

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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

Release:   1 
License:   GPLv2
Group:     Applications/Statistics 
URL:       http://cran.r-project.org/ 
Packager:  TACC - walling@tacc.utexas.edu, rhuang@tacc.utexas.edu 
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
R provides a wide variety of statistical (linear and nonlinear 
modelling, classical statistical tests, time-series analysis, 
classification, clustering, ...) and graphical techniques, and 
is highly extensible. 

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}


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
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
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
  
  
echo "Once more into the breach...."

#module purge
module load TACC

# Load other dependent libraries
#module load hdf5
#module load netcdf
module load boost
#module load cxx11



# Move /usr area back in from of /root for the root user
export PATH=/usr/sbin:/usr/bin:${PATH}

########
# Dependencies for R.3+
########

# Set path for custom dependencies that are hand build for Cray


# Location of hand built stuf
export DEPS_DIR_BUILD=/root/rstats/build 
export DEPS_DIR_INSTALL=%{INSTALL_DIR}/dependencies
export DEPS_DIR=${DEPS_DIR_INSTALL} # Shorthand
# Copy to install dir 

mkdir ${DEPS_DIR_INSTALL} 

cp -ar ${DEPS_DIR_BUILD}/* ${DEPS_DIR_INSTALL}
 
# Set paths
export PATH=${DEPS_DIR}/bin:${PATH}
export LD_LIBRARY_PATH=${DEPS_DIR}/lib:${LD_LIBRARY_PATH}
export CPATH=${DEPS_DIR}/include:${CPATH}

#Debug Output
echo PATH=$PATH
echo LD_LIBRARY_PATH=$LD_LIBRARY_PATH
echo DEPS_DIR=$DEPS_DIR

echo COMPILER LOAD: %{comp_fam_ver_load}
echo MPI      LOAD: %{mpi_fam_ver_load}

 
WD=`pwd`
echo $TACC_MKL_DIR
MKL_HOME=$TACC_MKL_DIR
export WD MKL_HOME

# Set up src directory
export SRC_DIR=${WD}/src
mkdir -p ${SRC_DIR}
echo ${SRC_DIR}
cd ${SRC_DIR}

#wget -q -N 'http://cran.r-project.org/src/base/R-3/R-3.2.1.tar.gz'
#tar zxf R-3.2.1.tar.gz
#cd R-3.2.1

# Use custom edited build

cp /admin/rpms/SOURCES/R-3.4.0-custom.tar.gz .
tar zxf R-3.4.0-custom.tar.gz
cd R-3.4.0

./configure --prefix=%{INSTALL_DIR} \
  --enable-R-shlib --enable-shared \
  --with-blas --with-lapack --with-x=no \
  CC=mpicc CXX=mpicxx F77=ifort FC=ifort \
  LD=xild AR=xiar \
  SHLIB_CFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  "\
  MAIN_FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  "\
  SHLIB_FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  "\
  MAIN_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"\
  DYLIB_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_CXXLDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2   -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_FCLDFLAGS="-shared -fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2   -L${TACC_MKL_LIB} -lmkl_rt"\
  BLAS_LIBS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"\
  LAPACK_LIBS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"\
  CFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt -I${DEPS_DIR}/include"\
  LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt -L${DEPS_DIR}/lib"\
  CPPFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt -I${DEPS_DIR}/include"\
  FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"\
  CXXFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"\
  FCFLAGS="-fPIC -openmp -mkl=parallel -O3 -xAVX -axCORE-AVX2  -L${TACC_MKL_LIB} -lmkl_rt"

# read -p "Press [Enter] key to continue..."

make -j16
make install

cd ${SRC_DIR}
rm -r R-3.4.0

# Ensure the R just built is used in the rest of the commands below
export PATH=%{INSTALL_DIR}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR}/lib64:%{INSTALL_DIR}/lib:$LD_LIBRARY_PATH


#----------------------------------------------------------
# Copy into rpm directory
#----------------------------------------------------------
# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.

# test
mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
# check with ls
echo "testing with an ls"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..


#----------------------------------------------------------
# UNMOUNT THE TEMP FILESYSTEM
#----------------------------------------------------------
umount  %{INSTALL_DIR}

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
help(
[[
This is the R statistics (Rstats) package built on %(date +'%B %d, %Y').

It includes the following accessory packages:
Rmpi, snow, snowfall
pdbMPI, pbdSLAP, pbdBASE, pbdDMAT, pbdDEMO, pbdNCDF4, pmclust
multicore
doMC, doSNOW, doMPI, doParallel
BH, bigmemory, biganalytics, bigtabulate, synchronicity
Rdsm, SparseM, slam, cluster, randomForest, bit, ff, mchof
BioConductor (base installation plus some common packages)
ggplot2, rjags/r2jags, rgdal, rstan

The R modulefile defines the environment variables TACC_R_DIR, TACC_R_BIN,
TACC_R_LIB and extends the PATH and LD_LIBRARY_PATH paths as appropriate.

Version %{version}
]]
)

whatis("Name: Rstats")
whatis("Version: %{version}")
whatis("Version-notes: Compiler:%{comp_fam_ver}, MPI:%{mpi_fam_ver}")
whatis("Category: Applications, Statistics, Graphics")
whatis("Keywords: Applications, Statistics, Graphics, Scripting Language")
whatis("URL: http://www.r-project.org/")
whatis("Description: R statistics package")

--
-- Create environment variables.
--
local r_dir   = "%{INSTALL_DIR}"
local r_bin   = "%{INSTALL_DIR}/bin"
local r_inc   = "%{INSTALL_DIR}/include"
local r_lib   = "%{INSTALL_DIR}/lib64/R/lib"
local r_man   = "%{INSTALL_DIR}/share/man"
local deps_bin = "${DEPS_DIR}/bin"
local deps_lib = "${DEPS_DIR}/lib"

setenv("TACC_R_DIR", r_dir)
setenv("TACC_R_BIN", r_bin)
setenv("TACC_R_INC", r_inc)
setenv("TACC_R_LIB", r_lib)
setenv("TACC_R_MAN", r_man)
--setenv("MV2_SUPPORT_DPM", 1)

prepend_path("PATH", r_bin)
prepend_path("MANPATH", r_man)
prepend_path("LD_LIBRARY_PATH", r_lib)

prepend_path("PATH","/opt/apps/gcc/4.9.3/bin")
prepend_path("PATH", deps_bin)
prepend_path("LD_LIBRARY_PATH","/opt/apps/gcc/4.9.3/lib")
prepend_path("LD_LIBRARY_PATH","/opt/apps/gcc/4.9.3/lib64")
prepend_path("LD_LIBRARY_PATH", deps_lib)

try_load("RstatsPackages/3.4.0")

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

