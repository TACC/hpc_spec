Summary:    R is a free software environment for statistical computing and graphics.
Name:       Rstats
Version:    3.4.0
Release:    1%{?dist}
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

# Want default of intel17 and impi17

# Load other dependent libraries
module load boost

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

#wget -q -N 'http://cran.r-project.org/src/base/R-3/R-3.2.1.tar.gz'

# Ensure default new file permissions are what we want

#umask 022
#check_umask="$(umask)"
#echo $check_umask


# Using a custom modified version of R source that should live in SOURCES
cp /admin/build/admin/rpms/stampede2/SOURCES/R-3.4.0-custom.tar.gz R-3.4.0.tar.gz
tar zxfp R-3.4.0.tar.gz
cd R-3.4.0

./configure --prefix=%{INSTALL_DIR} \
  --enable-R-shlib --enable-shared \
  --with-blas --with-lapack --with-x=yes --with-cairo=yes \
  CC=mpicc CXX=mpicxx F77=ifort FC=ifort \
  LD=xild AR=xiar \
  SHLIB_CFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  "\
  MAIN_FFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  "\
  SHLIB_FFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  "\
  MAIN_LDFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_LDFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  DYLIB_LDFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_CXXLDFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  SHLIB_FCLDFLAGS="-shared -fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512   -L${TACC_MKL_LIB} -lmkl_rt"\
  BLAS_LIBS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  LAPACK_LIBS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  CFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  LDFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  CPPFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  FFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  CXXFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"\
  FCFLAGS="-fPIC -qopenmp -mkl=parallel -O3 -xCORE-AVX2 -axMIC-AVX512  -L${TACC_MKL_LIB} -lmkl_rt"

# read -p "Press [Enter] key to continue..."
#make clean
make -j20
make install

cd ${SRC_DIR}

rm -r R-3.4.0

# Ensure the R just built is used in the rest of the commands below
export PATH=%{INSTALL_DIR}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR}/lib64:%{INSTALL_DIR}/lib:$LD_LIBRARY_PATH

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

Please load RstatsPackages to all pre-installed packages for this Rstats module.

The R modulefile defines the environment variables TACC_R_DIR, TACC_R_BIN,
TACC_R_LIB and extends the PATH and LD_LIBRARY_PATH paths as appropriate.

Version %{version}
]]
)

--
-- Create environment variables.
--
local r_dir   = "%{INSTALL_DIR}"
local r_bin   = "%{INSTALL_DIR}/bin"
local r_inc   = "%{INSTALL_DIR}/include"
local r_lib   = "%{INSTALL_DIR}/lib64/R/lib"
local r_man   = "%{INSTALL_DIR}/share/man"


setenv("TACC_R_DIR", r_dir)
setenv("TACC_R_BIN", r_bin)
setenv("TACC_R_INC", r_inc)
setenv("TACC_R_LIB", r_lib)
setenv("TACC_R_MAN", r_man)
setenv("MV2_SUPPORT_DPM", 1)

prepend_path("PATH", r_bin)
prepend_path("MANPATH", r_man)

prepend_path("LD_LIBRARY_PATH", r_lib)

try_load("RstatsPackages/3.4.0")
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

