Summary:    R is a free software environment for statistical computing and graphics.
Name:       Rstats
Version:    3.2.1
Release:    1 
License:    GPLv2
Vendor:     R Foundation for Statistical Computing
Group:      Applications/Statistics
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - walling@tacc.utexas.edu, rhuang@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define PNAME Rstats
%define MODULE_VAR TACC_R
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}

%package -n %{PACKAGE_NAME}
Summary: The R statistical computing environment 
Group:  Applications/Statistics

%description
%description -n %{PACKAGE_NAME} 
R provides a wide variety of statistical (linear and nonlinear 
modelling, classical statistical tests, time-series analysis, 
classification, clustering, ...) and graphical techniques, and 
is highly extensible. 

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


# %setup 

%build



%install


%include system-load.inc
%include compiler-load.inc
%include mpi-load.inc


# Create temporary directory for the install.  We need this to ???
#mkdir -p             %{INSTALL_DIR}
#mount -t tmpfs tmpfs %{INSTALL_DIR}
#tacctmpfs -m %{INSTALL_DIR}


echo "Once more into the breach...."

module purge
module load TACC
#module swap intel intel/15.0.1 # This is the default on Wrangler, no need to import

#Use impi
module load impi

# Load other dependent libraries
#module load hdf5
#module load netcdf
module load boost
module load cxx11

echo COMPILER LOAD: %{comp_fam_ver_load}
echo MPI      LOAD: %{mpi_fam_ver_load}

 
WD=`pwd`
MKL_HOME=$TACC_MKL_DIR
export WD MKL_HOME

# Set up src directory
export SRC_DIR=${WD}/src
mkdir -p ${SRC_DIR}
echo ${SRC_DIR}
cd ${SRC_DIR}

wget -q -N 'http://cran.r-project.org/src/base/R-3/R-3.2.1.tar.gz'
tar zxf R-3.2.1.tar.gz
cd R-3.2.1

./configure --prefix=%{INSTALL_DIR} \
  --enable-R-shlib --enable-shared \
  --with-blas --with-lapack --with-x=no \
  CC=mpicc CXX=mpicxx F77=ifort FC=ifort \
  LD=xild AR=xiar \
  SHLIB_CFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  "\
  MAIN_FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  "\
  SHLIB_FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  "\
  MAIN_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  DYLIB_LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_CXXLDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost   -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_FCLDFLAGS="-shared -fPIC -openmp -mkl=parallel -O3 -xHost   -L${TACC_MKL_LIB} -lmkl_rt"\
  BLAS_LIBS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  LAPACK_LIBS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  CFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  LDFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  CPPFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  FFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  CXXFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"\
  FCFLAGS="-fPIC -openmp -mkl=parallel -O3 -xHost  -L${TACC_MKL_LIB} -lmkl_rt"

# read -p "Press [Enter] key to continue..."

make -j20
make install

cd ${SRC_DIR}
rm -r R-3.2.1

# Ensure the R just built is used in the rest of the commands below
export PATH=%{INSTALL_DIR}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR}/lib64:%{INSTALL_DIR}/lib:$LD_LIBRARY_PATH

#############################################################
# Hand-install a set of modules that require specific compiler
# behavior and flags
#############################################################


#############################################################
# RMPI
#############################################################
# Note the include and libpath are for mvapich2/2.0a on stampede
# the same package will be installed on ls4
cd ${SRC_DIR}
cp /admin/build/rpms/SOURCES/Rmpi_0.6-5.tar.gz .
#wget -q -N 'http://cran.r-project.org/src/contrib/Rmpi_0.6-5.tar.gz'
R CMD INSTALL Rmpi_0.6-5.tar.gz --configure-args="--with-mpi=${MPICH_HOME} --with-Rmpi-include=${MPICH_HOME}/include64 --with-Rmpi-libpath=${MPICH_HOME}/lib64 --with-Rmpi-type=INTELMPI"

#############################################################
# pdbMPI pbdSLAP pbdBASE pbdDMAT pbdDEMO pbdNCDF4 pmclust
#############################################################
cd ${SRC_DIR}
wget -q -N 'http://cran.r-project.org/src/contrib/rlecuyer_0.3-3.tar.gz'
sleep 5
wget -q -N 'http://cran.r-project.org/src/contrib/pbdMPI_0.2-5.tar.gz'
sleep 5
R CMD INSTALL rlecuyer_0.3-3.tar.gz
R CMD INSTALL pbdMPI_0.2-5.tar.gz --configure-args=" --with-mpi-include=${MPICH_HOME}/include --with-mpi-libpath=${MPICH_HOME}/lib --with-mpi-type=MPICH2"

############################################
# rgdal - Depends gdal & proj + R package 'sp'
############################################
cd ${SRC_DIR}
wget -q -N http://download.osgeo.org/gdal/gdal-1.9.2.tar.gz
sleep 5
tar xvfz gdal-1.9.2.tar.gz
GDAL_HOME=%{INSTALL_DIR}/gdal-1.9.2
export GDAL_HOME
mkdir ${GDAL_HOME}
cd gdal-1.9.2
./configure --prefix=${GDAL_HOME} CC='icc' CXX='icpc' F77='ifort' FC='ifort'
make -j20
make install
cd ${SRC_DIR}
rm -r gdal-1.9.2

cd ${SRC_DIR}
# project-4.8 has a bug, use 4.7
wget -q -N http://download.osgeo.org/proj/proj-4.7.0.tar.gz
sleep 5
tar xvfz proj-4.7.0.tar.gz
PROJ_HOME=%{INSTALL_DIR}/proj-4.7.0
export PROJ_HOME
mkdir ${PROJ_HOME}
cd proj-4.7.0
./configure --prefix=${PROJ_HOME} CC='icc' CXX='icpc' F77='ifort' FC='ifort'
make -j20
make install
cd ${SRC_DIR}
rm -r proj-4.7.0

R -e "options("repos" = c(CRAN='http://cran.fhcrc.org')); install.packages('sp')"

cd ${SRC_DIR}
wget -q -N http://cran.r-project.org/src/contrib/Archive/rgdal/rgdal_0.8-16.tar.gz 
export LD_LIBRARY_PATH=${GDAL_HOME}/lib:${PROJ_HOME}/lib:${LD_LIBRARY_PATH}
R CMD INSTALL --configure-args="--with-gdal-config=${GDAL_HOME}/bin/gdal-config --with-proj-include=${PROJ_HOME}/include --with-proj-lib=${PROJ_HOME}/lib" rgdal_0.8-16.tar.gz

##########################
# JAGS + rjags + R2jags
##########################
cd ${SRC_DIR}
#wget http://softlayer-dal.dl.sourceforge.net/project/mcmc-jags/JAGS/3.x/Source/JAGS-3.4.0.tar.gz
wget http://downloads.sourceforge.net/project/mcmc-jags/JAGS/3.x/Source/JAGS-3.4.0.tar.gz
sleep 5
tar xvfz JAGS-3.4.0.tar.gz
JAGS_HOME=%{INSTALL_DIR}/jags-3.4.0
export JAGS_HOME
mkdir ${JAGS_HOME}
cd JAGS-3.4.0 
./configure --prefix=${JAGS_HOME} CC='icc' CXX='icpc' CFLAGS='-fPIC -mkl' CXXFLAGS='-fPIC -mkl' --enable-shared
make -j20
make install
cp -r ${JAGS_HOME}/lib ${JAGS_HOME}/lib64
cd ${SRC_DIR}
rm -r JAGS-3.4.0

export JAGS_INCLUDE=${JAGS_HOME}/include/JAGS
export PATH=${JAGS_HOME}/bin:$PATH
export LD_LIBRARY_PATH=${JAGS_HOME}/include/JAGS:${JAGS_HOME}/lib:${JAGS_HOME}/lib64:$LD_LIBRARY_PATH

#wget http://cran.r-project.org/src/contrib/rjags_3-15.tar.gz
#sleep 10
#R CMD INSTALL rjags_3-15.tar.gz
#rm rjags_3-15.tar.gz

echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
install.packages("rjags");
install.packages("R2jags");' > jags.R
Rscript jags.R

##########################################
# Install other 'easy' packages
##########################################

echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
install.packages("snow");
install.packages("pbdSLAP");
install.packages("pbdBASE");
install.packages("pbdDMAT");
install.packages("pbdDEMO");
install.packages("pbdNCDF4");
install.packages("pmclust");
install.packages("snowfall");
install.packages("doSNOW");
install.packages("doMPI");' > optional-mpvapich2-specific.R
Rscript optional-mpvapich2-specific.R

echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
install.packages("ggplot2");
install.packages("iterators");
install.packages("foreach");
install.packages("multicore");
install.packages("doMC");
install.packages("doParallel");
install.packages("BH");
install.packages("bigmemory.sri");
install.packages("bigmemory");
install.packages("biganalytics");
install.packages("bigtabulate");
install.packages("synchronicity");
install.packages("Rdsm");
install.packages("SparseM");
install.packages("slam");
install.packages("cluster");
install.packages("randomForest");
install.packages("bit");
install.packages("ff");
install.packages("mchof");
install.packages("lattice");
install.packages("zoo");
install.packages("sqldf");
install.packages("forecast");
install.packages("stringr");
install.packages("qcc");
install.packages("reshape2");
#install.packages("xtable");
install.packages("caret");
install.packages("devtools");
install.packages("RColorBrewer");
install.packages("labeling");
install.packages("scales");
install.packages("car");
install.packages("Hmisc");
install.packages("mvtnorm");
install.packages("foreign");
install.packages("rgl");
install.packages("gtools");
install.packages("sp");
install.packages("gdata");
install.packages("Rcpp");
install.packages("Zelig");
install.packages("Statnet");
install.packages("igraph");
install.packages("nlme");
install.packages("apsrtable");
install.packages("plm");
install.packages("lubridate");
install.packages("proto");
install.packages("munsell");
install.packages("foreign");
install.packages("lmtest");
install.packages("coda");
install.packages("data.table");' > optional.R
Rscript optional.R

#################
# RStan - depends on some of the above
#################
echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
source("http://mc-stan.org/rstan/install.R", echo = TRUE, max.deparse.length = 2000)
install_rstan()' > rstan_install.R
Rscript rstan_install.R


###########################################################
# Bioconductor
###########################################################
# create the script for bioconductor
echo 'source("http://bioconductor.org/biocLite.R");
biocLite();
biocLite(c("ggplot2","ShortRead","RankProd","multtest","IRanges","edgeR","Biostrings","GenomicFeatures","bioDist","GenomicRanges"));' > bioConductor.R
Rscript bioConductor.R


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
#umount  %{INSTALL_DIR}
#tacctmpfs -u %{INSTALL_DIR}

#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
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
local snow_bin = "%{INSTALL_DIR}/lib64/R/library/snow/"
local gdal_bin = "%{INSTALL_DIR}/gdal-1.9.2/bin"
local gdal_lib = "%{INSTALL_DIR}/gdal-1.9.2/lib"
local protobuf_bin = "%{INSTALL_DIR}/protobuf-4.7.1/bin"
local protobuf_lib = "%{INSTALL_DIR}/protobuf-4.7.1/lib"
local proj_lib = "%{INSTALL_DIR}/proj-4.7.0/lib"
local jags_bin = "%{INSTALL_DIR}/jags-3.4.0/bin"
local jags_lib = "%{INSTALL_DIR}/jags-3.4.0/lib64"
local jags_modules = "%{INSTALL_DIR}/jags-3.4.0/lib64/JAGS/modules-3"

setenv("TACC_R_DIR", r_dir)
setenv("TACC_R_BIN", r_bin)
setenv("TACC_R_INC", r_inc)
setenv("TACC_R_LIB", r_lib)
setenv("TACC_R_MAN", r_man)
setenv("MV2_SUPPORT_DPM", 1)

prepend_path("PATH", jags_bin)
prepend_path("PATH", snow_bin)
prepend_path("PATH", gdal_bin)
prepend_path("PATH", protobuf_bin)
prepend_path("PATH", r_bin)
prepend_path("MANPATH", r_man)
prepend_path("LD_LIBRARY_PATH", r_lib)
prepend_path("LD_LIBRARY_PATH", gdal_lib)
prepend_path("LD_LIBRARY_PATH", protobuf_lib)
prepend_path("LD_LIBRARY_PATH", proj_lib)
prepend_path("LD_LIBRARY_PATH", jags_lib)
prepend_path("LD_LIBRARY_PATH", jags_modules)

prepend_path("PATH","/opt/apps/gcc/4.9.1/bin")
prepend_path("LD_LIBRARY_PATH","/opt/apps/gcc/4.9.1/lib")
prepend_path("LD_LIBRARY_PATH","/opt/apps/gcc/4.9.1/lib64")


EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for R version %{version}
##
set ModulesVersion "%version"
EOF

#----------------------------------------------------------
# Lua syntax check 
#----------------------------------------------------------
if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
    $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{PACKAGE_NAME} 
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post -n %{PACKAGE_NAME} 

%clean

