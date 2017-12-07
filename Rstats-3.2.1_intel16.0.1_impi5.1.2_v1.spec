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
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
#tacctmpfs -m %{INSTALL_DIR}


echo "Once more into the breach...."

module purge
module load TACC
#module swap intel intel/15.0.1 # This is the default on Wrangler, no need to import

#Use impi
#module load impi

# Load other dependent libraries
#module load hdf5
#module load netcdf
module load boost
#module load cxx11

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

make -j10
make install

cd ${SRC_DIR}
rm -r R-3.2.1

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

