Summary:    RstatsPackages provides pre-installed versions of CRAN packages compatible with the Rstats module.
Name:       RstatsPackages
Version:    3.2.1
Release:    3%{?dist} 
License:    GPLv2
Vendor:     R Foundation for Statistical Computing
Group:      Applications/Statistics
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - walling@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define PNAME RstatsPackages
%define MODULE_VAR TACC_R
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}

%package -n %{PACKAGE_NAME}
Summary: CRAN packages for Rstats
Group:  Applications/Statistics

%description
%description -n %{PACKAGE_NAME} 
RstatsPackages provides pre-installed versions of CRAN packages compatible with the Rstats module.

%prep
echo 'PREP'
echo $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


# %setup 

%build

%install

%include system-load.inc
%include compiler-load.inc
%include mpi-load.inc


# Create temporary directory for the install.  We need this to ???
echo 'mkdir INSTALL_DIR'
echo %{INSTALL_DIR}
#mkdir -p             %{INSTALL_DIR}
#mount -t tmpfs tmpfs %{INSTALL_DIR}
tacctmpfs -m %{INSTALL_DIR}


module purge
module load TACC
module load Rstats

# Load other dependent libraries
module load hdf5
module load netcdf
module load boost

echo COMPILER LOAD: %{comp_fam_ver_load}
echo MPI      LOAD: %{mpi_fam_ver_load}

 
WD=`pwd`
MKL_HOME=$TACC_MKL_DIR
export WD MKL_HOME

# Set up src directory
echo 'Setup SRC_DIR'
export SRC_DIR=${WD}/src
echo $SRC_DIR
mkdir -p ${SRC_DIR}
echo ${SRC_DIR}
cd ${SRC_DIR}

#############################################################
# Hand-install a set of modules that require specific compiler
# behavior and flags
#############################################################

# Use this CRAN folder 
CRAN=http://cloud.r-project.org

# Create and Specificy the packages install location
PACKAGE_DIR=%{INSTALL_DIR}/packages
mkdir ${PACKAGE_DIR} 
export R_LIBS=${PACKAGE_DIR}

# SPeed up all builds
export MAKEFLAGS="-j100"

########
# Devtools
########
Rscript -e "install.packages('devtools', repos='${CRAN}');"

########
# nloptr and friends
######
cd ${SRC_DIR}
wget -q -N http://ab-initio.mit.edu/nlopt/nlopt-2.4.2.tar.gz
sleep 5
tar xvfz nlopt-2.4.2.tar.gz
NLOPT_HOME=%{INSTALL_DIR}/nlopt-2.4.2
echo $NLOPT_HOME
export NLOPT_HOME
mkdir ${NLOPT_HOME}
cd ${SRC_DIR}/nlopt-2.4.2
./configure --prefix=${NLOPT_HOME} --enable-shared CC='icc' CXX='icpc' F77='ifort' FC='ifort'
make -j20
make install
cd ${SRC_DIR}
rm -r nlopt-2.4.2.tar.gz

# Now the R package
wget -q -N https://cran.r-project.org/src/contrib/nloptr_1.0.4.tar.gz
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/${NLOPT_HOME}/lib
PKG_LIBS="-lnlopt" R CMD INSTALL --configure-args='--with-nlopt-cflags="-I${NLOPT_HOME}/include" --with-nlopt-libs=-L${NLOPT_HOME}/lib' nloptr_1.0.4.tar.gz
rm nloptr_1.0.4.tar.gz

# lme4
Rscript -e "library(devtools); install_version('nlme', repos='${CRAN}'); install_version('lme4', repos='${CRAN}');"

# pbkrtest
cd ${SRC_DIR}
wget -q -N https://cran.r-project.org/src/contrib/Archive/pbkrtest/pbkrtest_0.4-5.tar.gz
R CMD INSTALL pbkrtest_0.4-5.tar.gz

#############################################################
# RMPI
#############################################################
# Note the include and libpath are for mvapich2/2.0a on stampede
# the same package will be installed on ls4
cd ${SRC_DIR}
wget -q -N 'https://cran.r-project.org/src/contrib/Archive/Rmpi/Rmpi_0.6-5.tar.gz'
#R CMD INSTALL Rmpi_0.6-5.tar.gz --configure-args="--with-Rmpi-include=${MPICH_HOME}/include64 --with-Rmpi-libpath=${MPICH_HOME}/lib64 --with-Rmpi-type=MPICH2"
R CMD INSTALL Rmpi_0.6-5.tar.gz --lib=/admin/build/R/x86_64-unknown-linux-gnu-library/3.2 --configure-args="--with-Rmpi-include=${MPICH_HOME}/include64 --with-Rmpi-libpath=${MPICH_HOME}/intel64/lib --with-Rmpi-type=OPENMPI"

#############################################################
# pdbMPI pbdSLAP pbdBASE pbdDMAT pbdDEMO pbdNCDF4 pmclust
#############################################################
cd ${SRC_DIR}
wget -q -N 'http://cran.r-project.org/src/contrib/Archive/rlecuyer/rlecuyer_0.3-3.tar.gz'
sleep 5
wget -q -N 'http://cran.r-project.org/src/contrib/Archive/pbdMPI/pbdMPI_0.3-1.tar.gz'
sleep 5
R CMD INSTALL rlecuyer_0.3-3.tar.gz
R CMD INSTALL pbdMPI_0.3-1.tar.gz --configure-args=" --with-mpi-include=${MPICH_HOME}/include64 --with-mpi-libpath=${MPICH_HOME}/lib64 --with-mpi-type=OPENMPI"

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

wget -q -N https://cran.r-project.org/src/contrib/Archive/sp/sp_1.2-1.tar.gz
R CMD INSTALL sp_1.2-1.tar.gz
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
wget -q -N http://ufpr.dl.sourceforge.net/project/mcmc-jags/JAGS/3.x/Source/JAGS-3.4.0.tar.gz 
sleep 10 
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

export PATH=${JAGS_HOME}/bin:$PATH
export LD_LIBRARY_PATH=${JAGS_HOME}/lib:${JAGS_HOME}/lib64:$LD_LIBRARY_PATH

wget -q -N https://cran.r-project.org/src/contrib/Archive/coda/coda_0.17-1.tar.gz
sleep 10
R CMD INSTALL coda_0.17-1.tar.gz

wget -q -N http://cran.r-project.org/src/contrib/Archive/rjags/rjags_3-15.tar.gz
sleep 10
R CMD INSTALL rjags_3-15.tar.gz
rm rjags_3-15.tar.gz

##########################################
# Install other 'easy' packages - Use devtools to avoid cran craziness of constanstly updated packages being incompatiable with this versino of R
##########################################

# DevTools
echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
library(devtools)
install_version("snow");
install_version("pbdSLAP");
install_version("pbdBASE");
install_version("pbdDMAT");
install_version("pbdDEMO");
install_version("pbdNCDF4");
install_version("pmclust");
install_version("snowfall");
install_version("doSNOW");
install_version("doMPI");' > optional-mpvapich2-specific.R
Rscript optional-mpvapich2-specific.R


echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
library(devtools)
install_version("ggplot2");
install_version("iterators");
install_version("foreach");
install_version("multicore");
install_version("doMC");
install_version("doParallel");
install_version("BH");
install_version("bigmemory.sri");
install_version("bigmemory");
install_version("biganalytics");
install_version("bigtabulate");
install_version("synchronicity");
install_version("Rdsm");
install_version("SparseM");
install_version("slam");
install_version("cluster");
install_version("randomForest");
install_version("bit");
install_version("ff");
install_version("mchof");
install_version("lattice");
install_version("zoo");
install_version("sqldf");
install_version("forecast");
install_version("stringr");
install_version("qcc");
install_version("reshape2");
install_version("caret");
install_version("RColorBrewer");
install_version("labeling");
install_version("scales");
install_version("car");
install_version("Hmisc");
install_version("mvtnorm");
install_version("foreign");
install_version("rgl");
install_version("gtools");
install_version("sp");
install_version("gdata");
install_version("Rcpp");
install_version("igraph");
install_version("nlme");
install_version("apsrtable");
install_version("plm");
install_version("lubridate");
install_version("proto");
install_version("munsell");
install_version("lmtest");
install_version("coda");
install_version("data.table");
install_version("inline");
install_version("R2jags"); ' > optional.R

Rscript optional.R

#################
# RStan - depends on some of the above
#################
#echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
#source("http://mc-stan.org/rstan/install.R", echo = TRUE, max.deparse.length = 2000)
#install_rstan()' > rstan_install.R
#Rscript rstan_install.R

echo '  Sys.setenv(MAKEFLAGS = "-j100") 
        devtools::install_url("http://cran.r-project.org/src/contrib/Archive/BH/BH_1.55.0-3.tar.gz")
        devtools::install_url("https://github.com/stan-dev/rstan/releases/download/v2.6.0/rstan_2.6.0.tar.gz",dependencies = TRUE)
' > rstan_install.R

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
# REDUNDANT mkdir???
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


# check with ls
echo "testing with an ls"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..


#----------------------------------------------------------
# UNMOUNT THE TEMP FILESYSTEM
#----------------------------------------------------------
#umount  %{INSTALL_DIR}
tacctmpfs -u %{INSTALL_DIR}

#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
This is the R statistics (RstatsPackages) package built on %(date +'%B %d, %Y').

It includes the following accessory packages including but not limited to:
Rmpi, snow, snowfall
pdbMPI, pbdSLAP, pbdBASE, pbdDMAT, pbdDEMO, pbdNCDF4, pmclust
multicore
doMC, doSNOW, doMPI, doParallel
BH, bigmemory, biganalytics, bigtabulate, synchronicity
Rdsm, SparseM, slam, cluster, randomForest, bit, ff, mchof
BioConductor (base installation plus some common packages)
ggplot2, rjags/r2jags, rgdal, rstan

The RstatsPackages modulefile extends the PATH and LD_LIBRARY_PATH paths as appropriate and creates the R_LIBS env variable.

Version %{version}
]]
)

--
-- Create environment variables.
--
local r_libs   = "%{INSTALL_DIR}/packages" 
setenv("R_LIBS", r_libs)

local nlopt_lib = "%{INSTALL_DIR}/nlopt-2.4.2/lib"
prepend_path("LD_LIBRARY_PATH", nlopt_lib)

local snow_bin = "%{INSTALL_DIR}/packages/snow/"
local gdal_bin = "%{INSTALL_DIR}/gdal-1.9.2/bin"
local gdal_lib = "%{INSTALL_DIR}/gdal-1.9.2/lib"
local protobuf_bin = "%{INSTALL_DIR}/protobuf-4.7.1/bin"
local protobuf_lib = "%{INSTALL_DIR}/protobuf-4.7.1/lib"
local proj_lib = "%{INSTALL_DIR}/proj-4.7.0/lib"
local jags_bin = "%{INSTALL_DIR}/jags-3.4.0/bin"
local jags_lib = "%{INSTALL_DIR}/jags-3.4.0/lib64"
local jags_modules = "%{INSTALL_DIR}/jags-3.4.0/lib64/JAGS/modules-3"


prepend_path("PATH", snow_bin)
prepend_path("PATH", gdal_bin)
prepend_path("PATH", protobuf_bin)
prepend_path("PATH", jags_bin)


prepend_path("LD_LIBRARY_PATH", gdal_lib)
prepend_path("LD_LIBRARY_PATH", protobuf_lib)
prepend_path("LD_LIBRARY_PATH", proj_lib)
prepend_path("LD_LIBRARY_PATH", jags_lib)
prepend_path("LD_LIBRARY_PATH", jags_modules)


local rstats_loaded = isloaded("Rstats/3.2.1")
if (not rstats_loaded) then
	load("Rstats/3.2.1")
end

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

