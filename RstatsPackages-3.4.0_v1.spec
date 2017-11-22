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
%define pkg_base_name RstatsPackages
%define MODULE_VAR    RSTATS_PACKAGES

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

Release:   2 
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

module load Rstats/3.4.0

# Move /usr area back in from of /root for the root user
export PATH=/usr/sbin:/usr/bin:${PATH}

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
export MAKEFLAGS="-j20"

########
# Devtools
########

# Need an LS5 compatible version of openssl
wget -q -N https://cran.r-project.org/src/contrib/Archive/openssl/openssl_0.4.tar.gz
sleep 5
R CMD INSTALL openssl_0.4.tar.gz

Rscript -e "install.packages(c('httr', 'devtools'), dependencies=F, repos='${CRAN}');"

########
# nloptr and friends
######

: <<'END'

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

END

#############################################################
# RMPI
#############################################################
# Note the include and libpath are for mvapich2/2.0a on stampede
# the same package will be installed on ls4
cd ${SRC_DIR}
wget -q -N 'http://cran.r-project.org/src/contrib/Archive/Rmpi/Rmpi_0.6-5.tar.gz'

# Adding a special config for TACCified version of Cray MPICH2
tar xvfz Rmpi_0.6-5.tar.gz
cd Rmpi
line=`grep -n CRAY\) configure | tr ":" "\n" | head -n 1`
line=$(($line+3))
sed -i "${line}i \ \ CRAY_TACC)\n    PKG_LIBS=\"-L\$\{MPI_LIBPATH\} -lmpich -lmpl \$\{MPI_LIBS\}\"\n    ;;" configure
cd ..
tar cvfz Rmpi_0.6-5-custom.tar.gz Rmpi

# Now install the tweaked version
export MPICH_HOME=${MPICH_DIR}
R CMD INSTALL Rmpi_0.6-5-custom.tar.gz --configure-args="--with-Rmpi-include=${MPICH_HOME}/include --with-Rmpi-libpath=${MPICH_HOME}/lib --with-Rmpi-type=CRAY_TACC" --no-test-load

#############################################################
# pdbMPI pbdSLAP pbdBASE pbdDMAT pbdDEMO pbdNCDF4 pmclust
#############################################################
cd ${SRC_DIR}
wget -q -N 'http://cran.r-project.org/src/contrib/rlecuyer_0.3-4.tar.gz'
sleep 5
wget -q -N 'https://cran.r-project.org/src/contrib/Archive/pbdMPI/pbdMPI_0.3-1.tar.gz'
sleep 5
R CMD INSTALL rlecuyer_0.3-4.tar.gz
R CMD INSTALL pbdMPI_0.3-1.tar.gz --configure-args=" --with-mpi-include=${MPICH_HOME}/include --with-mpi-libpath=${MPICH_HOME}/lib --with-mpi-type=MPICH2 --enable-opa=no" --no-test-load

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
wget -q -N http://downloads.sourceforge.net/project/mcmc-jags/JAGS/4.x/Source/JAGS-4.0.1.tar.gz
sleep 5
tar xvfz JAGS-4.0.1.tar.gz
JAGS_HOME=%{INSTALL_DIR}/jags-4.0.1
export JAGS_HOME
mkdir ${JAGS_HOME}
cd JAGS-4.0.1
./configure --prefix=${JAGS_HOME} CC='icc' CXX='icpc' CFLAGS='-fPIC -mkl' CXXFLAGS='-fPIC -mkl' --enable-shared
make -j20
make install
cp -r ${JAGS_HOME}/lib ${JAGS_HOME}/lib64
cd ${SRC_DIR}
rm -r JAGS-4.0.1

export PATH=${JAGS_HOME}/bin:$PATH
export LD_LIBRARY_PATH=${JAGS_HOME}/lib:${JAGS_HOME}/lib64:$LD_LIBRARY_PATH

echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
install.packages("coda");
' > coda_install.R
Rscript coda_install.R

wget -q -N 'https://cran.r-project.org/src/contrib/Archive/rjags/rjags_4-5.tar.gz' 
sleep 10
R CMD INSTALL rjags_4-5.tar.gz
rm rjags_4-5.tar.gz

##########################################
# Custom SNOW install
##########################################

cd ${SRC_DIR}
wget -q -N 'https://cran.r-project.org/src/contrib/Archive/snow/snow_0.4-1.tar.gz' 
sleep 5
tar xfz snow_0.4-1.tar.gz
# We need to replace RMPISNOW with our own version
wget -q -N --no-check-certificate https://gitlab.tacc.utexas.edu/data-group/R-patches/raw/master/snow/RMPISNOW
mv snow/inst/RMPISNOW snow/inst/RMPISNOW.orig
cp RMPISNOW snow/inst
chmod 755 snow/inst/RMPISNOW
# Remove the checksum info for RMPISNOW so it will install
sed -i '/14228e3f50d14bc0672d4badb6971975/d' snow/MD5
# Repackage and install
tar cfz snow-cust.tar.gz snow
R CMD INSTALL snow-cust.tar.gz
# cleanup
rm snow-cust.tar.gz snow_0.4-1.tar.gz RMPISNOW 


##########################################
# Install other 'easy' packages
##########################################

echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
Sys.setenv(MAKEFLAGS="-j16");
install.packages("pbdSLAP");
install.packages("pbdBASE");
install.packages("pbdDMAT");
install.packages("pbdDEMO");
install.packages("pbdNCDF4");
install.packages("pmclust");
install.packages("snowfall");
install.packages("doSNOW");
install.packages("doMPI");' > optional-craympich2-specific.R
Rscript optional-craympich2-specific.R

echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
Sys.setenv(MAKEFLAGS="-j16");
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
install.packages("data.table");
install.packages("R2jags"); ' > optional.R
Rscript optional.R

#################
# RStan - depends on some of the above
#################
#echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
#source("http://mc-stan.org/rstan/install.R", echo = TRUE, max.deparse.length = 2000)
#install_rstan()' > rstan_install.R
#Rscript rstan_install.R

#echo '  Sys.setenv(MAKEFLAGS = "-j10") 
#        devtools::install_url("http://cran.r-project.org/src/contrib/Archive/BH/BH_1.55.0-3.tar.gz")
#        devtools::install_url("https://github.com/stan-dev/rstan/releases/download/v2.6.0/rstan_2.6.0.tar.gz",dependencies = TRUE)
#' > rstan_install.R

echo '  options("repos" = c(CRAN="http://cran.fhcrc.org"))
	Sys.setenv(MAKEFLAGS = "-j10") 
        install.packages("BH", type="source") 
	install.packages("rstan", type="source")
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

whatis("Name: RstatsPackages")
whatis("Version: %{version}")
whatis("Version-notes: Compiler:%{comp_fam_ver}, MPI:%{mpi_fam_ver}")
whatis("Category: Applications, Statistics, Graphics")
whatis("Keywords: Applications, Statistics, Graphics, Scripting Language")
whatis("URL: http://www.r-project.org/")
whatis("Description: R statistics package")

--
-- Create environment variables.
--

--We want to ensure the users ~/R dir is always first, but also add these custom package locations
local r_libs   = "%{INSTALL_DIR}/packages" 
append_path("R_LIBS_SITE", r_libs)


local nlopt_lib = "%{INSTALL_DIR}/nlopt-2.4.2/lib"
prepend_path("LD_LIBRARY_PATH", nlopt_lib)


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
local jags_bin = "%{INSTALL_DIR}/jags-4.0.1/bin"
local jags_lib = "%{INSTALL_DIR}/jags-4.0.1/lib64"
local jags_modules = "%{INSTALL_DIR}/jags-4.0.1/lib64/JAGS/modules-3"


prepend_path("PATH", jags_bin)
prepend_path("PATH", snow_bin)
prepend_path("PATH", gdal_bin)
prepend_path("PATH", protobuf_bin)
prepend_path("LD_LIBRARY_PATH", gdal_lib)
prepend_path("LD_LIBRARY_PATH", protobuf_lib)
prepend_path("LD_LIBRARY_PATH", proj_lib)
prepend_path("LD_LIBRARY_PATH", jags_lib)
prepend_path("LD_LIBRARY_PATH", jags_modules)

prepend_path("PATH","/opt/apps/gcc/4.9.3/bin")
prepend_path("LD_LIBRARY_PATH","/opt/apps/gcc/4.9.3/lib")
prepend_path("LD_LIBRARY_PATH","/opt/apps/gcc/4.9.3/lib64")

local rstats_loaded = isloaded("Rstats/3.4.0")
if (not rstats_loaded) then
        load("Rstats/3.4.0")
end

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

