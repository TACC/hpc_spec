Summary:    Big data R packages (RHadoop, SparkR, RHIPE) with Rstat/3.2.1
Name:       big-data-r
Version:    3.2.1
Release:    1 
License:    GPLv2
Vendor:     RHadoop by revolutionanalytics, SparkR by AMP lab at UC-Berkeley, RHIPE by Purdue Statistics Department 
Group:      Applications/Statistics
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - rhuang@tacc.utexas.edu, walling@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc


%define PNAME big-data-r
%define MODULE_VAR TACC_big-data-r
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}   
%define MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}

%package -n %{PACKAGE_NAME}
Summary: Big data R packages (RHadoop, SparkR, RHIPE) with Rstat/3.2.1
Group:  Applications/Statistics

%description
%description -n %{PACKAGE_NAME} 
RHadoop is a collection of five R packages that allow users to manage and analyze data with Hadoop.
SparkR is an R package that provides a light-weight frontend to use Apache Spark from R. SparkR exposes 
the Spark API through the RDD class and allows users to interactively run jobs from the R shell on a cluster.


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
tacctmpfs -m %{INSTALL_DIR}


echo "Once more into the breach...."

module purge
module load TACC
#module swap intel intel/15.0.1 # This is the default on Wrangler, no need to import

#Use default mvapich

# Load other dependent libraries
#module load hdf5
#module load netcdf
module load boost
module load Rstats
#module load java-paths

echo COMPILER LOAD: %{comp_fam_ver_load}
echo MPI      LOAD: %{mpi_fam_ver_load}

which R

WD=`pwd`
MKL_HOME=$TACC_MKL_DIR
export WD MKL_HOME

# Set up src directory
export SRC_DIR=`cd "$WD";pwd`/../SOURCES    #${WD}/src
#mkdir -p ${SRC_DIR}
echo ${SRC_DIR}
cd ${SRC_DIR}

## set r-library to store R packages
rm -rf %{INSTALL_DIR}/r-library
mkdir %{INSTALL_DIR}/r-library
## add a library path for R to install, R CMD INSTALL to
export R_LIBS=%{INSTALL_DIR}/r-library
###########################################################
# RHadoop: rmr2, plyrmr, rhdfs
###########################################################
cd ${SRC_DIR}
echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
install.packages(c("Rcpp", "RJSONIO", "digest", "functional", "reshape2",
"stringr", "plyr", "caTools"))' > pre-rmr2.R
Rscript pre-rmr2.R

export HADOOP_CMD=/usr/bin/hadoop
export HADOOP_STREAMING=/usr/lib/hadoop-mapreduce/hadoop-streaming-2.5.0-cdh5.3.0.jar
R CMD INSTALL  rmr2_3.3.1.tar.gz


## install plyrmr
echo 'options("repos" = c(CRAN="http://cran.fhcrc.org"))
install.packages(c("dplyr", "R.methodsS3", "Hmisc", "memoise", "lazyeval","rjson"))' > pre-plyrmr.R
Rscript pre-plyrmr.R

R CMD INSTALL  plyrmr_0.6.0.tar.gz

## install rhdfs
export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.75.x86_64/jre
export PATH=/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.75.x86_64/bin:$PATH

R CMD javareconf
unset JAVA_HOME
R CMD INSTALL rJava_0.9-6.tar.gz

R CMD INSTALL rhdfs_1.0.8.tar.gz

###########################################################
# SparkR
###########################################################
cd ${SRC_DIR}
tar xvzf scala-2.10.4.tgz

SCALA_HOME=%{INSTALL_DIR}/scala-2.10.4
export SCALA_HOME
rm -rf %{INSTALL_DIR}/scala-2.10.4
cp -r ${SRC_DIR}/scala-2.10.4  %{INSTALL_DIR}

cd ${SRC_DIR}
rm -r scala-2.10.4

export PATH=%{INSTALL_DIR}/scala-2.10.4/bin:$PATH

unzip SparkR-pkg-master.zip
cd SparkR-pkg-master
SPARK_VERSION=1.2.0-cdh5.3.3 USE_YARN=1 SPARK_YARN_VERSION=2.5.0-cdh5.3.0 SPARK_HADOOP_VERSION=2.5.0-cdh5.3.0 ./install-dev.sh
rm -rf ${R_LIBS}/SparkR
cp -r  lib/SparkR ${R_LIBS}
cd ..

rm -r SparkR-pkg-master


#echo 'library(devtools)
#install_github("amplab-extras/SparkR-pkg", subdir="pkg")' > install-sparkR.R
#Rscript install-sparkR.R


################
# Rhipe
################
# Instructions: http://www.datadr.org/install.html
cd ${SRC_DIR}
tar jxvf protobuf-2.5.0.tar.bz2

PROTOBUF_HOME=%{INSTALL_DIR}/protobuf-2.5.0
export PROTOBUF_HOME
rm -rf ${PROTOBUF_HOME}
mkdir ${PROTOBUF_HOME}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${PROTOBUF_HOME}/lib
cd protobuf-2.5.0
./configure --prefix=${PROTOBUF_HOME} CC='icc' CXX='icpc' CFLAGS='-fPIC -mkl' CXXFLAGS='-fPIC -mkl' 
make -j4
make install


export PKG_CONFIG_PATH=${PROTOBUF_HOME}/lib/pkgconfig
# LD_LIBRARY_PATH set above
export HADOOP=/usr/lib/hadoop

cd ${SRC_DIR}
R CMD INSTALL Rhipe_0.75.0_cdh5mr2.tar.gz
#echo "LD_LIBRARY_PATH=${PROTOBUF_HOME}/lib:${LD_LIBRARY_PATH}" >> ${TACC_R_DIR}/lib64/R/etc/Renviron


cd ${SRC_DIR}
rm -r protobuf-2.5.0



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

cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..


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
This is the big data R packages built on July 5th, 2015 wth Rstat/3.2.1.

It includes the following accessory packages:
RHadoop(rmr2_3.3.1, plyrmr_0.6.0, rhdfs_1.0.8),
SparkR and RHIPE

The R modulefile defines the environment variables R_LIBS,
JAVA_HOME,HADOOP_HOME and extends the PATH and LD_LIBRARY_PATH paths as appropriate.

Version 3.2.1
]]
)

whatis("Name: big-data-r")
whatis("Version: 3.2.1")
whatis("Version-notes: Compiler:intel15, MPI:mvapich2_2_1")
whatis("Category: RHadoop, SparkR, RHIPE")
whatis("Keywords: Applications, Big data, Mapreduce")
whatis("Description: big data R packages")


always_load("Rstats/3.2.1")

--
-- Create environment variables.
--
-- set variable
local big_data_r_dir   = "/opt/apps/intel15/mvapich2_2_1/big-data-r/3.2.1"
local r_libs = "%{INSTALL_DIR}/r-library"
local hadoop_cmd = "/usr/bin/hadoop"
local hadoop_home = "/usr/lib/hadoop"
local hadoop_streaming = "/usr/lib/hadoop-mapreduce/hadoop-streaming-2.5.0-cdh5.3.0.jar"
local java_home = "/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.75.x86_64/jre"
local spark_home = "/usr/lib/spark"
local yarn_conf_dir = "/etc/hadoop/conf"
local hadoop_conf_dir = "/etc/hadoop/conf"
local hadoop_bin = "/usr/lib/hadoop/bin"
local hadoop_libs = "/usr/lib/hadoop:/usr/lib/hadoop/lib:/usr/lib/hadoop-hdfs:/usr/lib/hadoop-mapreduce:/usr/lib/hadoop-yarn:/usr/lib/hadoop/client"
local pkg_config_path = "/opt/apps/intel15/mvapich2_2_1/big-data-r/3.2.1/protobuf-2.5.0/lib/pkgconfig"
local rhipe_hadoop_tmp_folder = "/tmp"

-- bin or executable
local java_bin="/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.75.x86_64/bin"
local scala_bin="/opt/apps/intel15/mvapich2_2_1/big-data-r/3.2.1/scala-2.10.4/bin"
local spark_submit_dir = "/opt/apps/intel15/mvapich2_2_1/big-data-r/3.2.1/r-library/SparkR"
local protobuf_bin = "/opt/apps/intel15/mvapich2_2_1/big-data-r/3.2.1/protobuf-2.5.0/bin"

--  LD_LIBRARY_PATH
local protobuf_lib = "/opt/apps/intel15/mvapich2_2_1/big-data-r/3.2.1/protobuf-2.5.0/lib"

setenv("TACC_BIG_DATA_R_DIR", big_data_r_dir)
setenv("R_LIBS",r_libs)
setenv("HADOOP_CMD", hadoop_cmd)
setenv("HADOOP_STREAMING", hadoop_streaming)
setenv("JAVA_HOME", java_home)
setenv("SPARK_HOME",spark_home)
setenv("YARN_CONF_DIR",yarn_conf_dir)
setenv("HADOOP_CONF_DIR",hadoop_conf_dir)
setenv("HADOOP_HOME", hadoop_home)
setenv("HADOOP_BIN", hadoop_bin)
setenv("HADOOP_LIBS", hadoop_libs)
setenv("PKG_CONFIG_PATH", pkg_config_path)
setenv("RHIPE_HADOOP_TMP_FOLDER", rhipe_hadoop_tmp_folder)

prepend_path("PATH", java_bin)
prepend_path("PATH", scala_bin)
prepend_path("PATH", spark_submit_dir)
prepend_path("PATH", protobuf_bin)

prepend_path("LD_LIBRARY_PATH", protobuf_lib)

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


