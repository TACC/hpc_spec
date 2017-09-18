#
# W. Cyrus Proctor
# 2015-08-25
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
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
%define pkg_base_name dakota
%define MODULE_VAR    DAKOTA

# Create some macros (spec file variables)
%define major_version 6
%define minor_version 6
%define patch_version 0

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc-home1.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1
License:   BSD
Group:     System/Utils
URL:       https://dakota.sandia.gov
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
The Dakota toolkit provides a flexible, extensible interface between analysis
codes and iterative systems analysis methods. Dakota contains algorithms for:
optimization with gradient and nongradient-based methods; uncertainty
quantification with sampling, reliability, stochastic expansion, and epistemic
methods; parameter estimation with nonlinear least squares methods; and
sensitivity/variance analysis with design of experiments and parameter study
methods.  These capabilities may be used on their own or as components within
advanced strategies such as hybrid optimization, surrogate-based optimization,
mixed integer nonlinear programming, or optimization under uncertainty.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
The Dakota toolkit provides a flexible, extensible interface between analysis
codes and iterative systems analysis methods. Dakota contains algorithms for:
optimization with gradient and nongradient-based methods; uncertainty
quantification with sampling, reliability, stochastic expansion, and epistemic
methods; parameter estimation with nonlinear least squares methods; and
sensitivity/variance analysis with design of experiments and parameter study
methods.  These capabilities may be used on their own or as components within
advanced strategies such as hybrid optimization, surrogate-based optimization,
mixed integer nonlinear programming, or optimization under uncertainty.

%description
The Dakota toolkit provides a flexible, extensible interface between analysis
codes and iterative systems analysis methods. Dakota contains algorithms for:
optimization with gradient and nongradient-based methods; uncertainty
quantification with sampling, reliability, stochastic expansion, and epistemic
methods; parameter estimation with nonlinear least squares methods; and
sensitivity/variance analysis with design of experiments and parameter study
methods.  These capabilities may be used on their own or as components within
advanced strategies such as hybrid optimization, surrogate-based optimization,
mixed integer nonlinear programming, or optimization under uncertainty.


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

#%setup -n %{pkg_base_name}-%{pkg_version}


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge
%include compiler-load.inc
%include mpi-load.inc
#ml cxx11
ml cmake
ml python
ml boost
ml gsl
ml trilinos
ml


echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
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

##################################################
export dakota=`pwd`
export dakota_install=%{INSTALL_DIR}
##################################################

export dakota_major=6
export dakota_minor=6
export dakota_patch=0
export dakota_dlversion=${dakota_major}.${dakota_minor}
export dakota_version=${dakota_major}.${dakota_minor}.${dakota_patch}

export dak_src=${dakota}/dakota-${dakota_version}.src
export dak_build=${dakota}/build

export ncores=64

export CC=mpicc
export CXX=mpicxx
export FC=mpif90

export BLASLIB="-Wl,-rpath,/opt/intel/compilers_and_libraries/linux/lib/intel64 -L/opt/intel/compilers_and_libraries/linux/lib/intel64 -Wl,-rpath,${MKLROOT}/lib/intel64 -L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_core -lmkl_intel_thread -liomp5 -lpthread -lm -ldl"

cd ${dakota}
wget https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-${dakota_dlversion}-public.src.tar.gz
tar xvfz dakota-${dakota_dlversion}-public.src.tar.gz
# Fix MPI variables to ints instead of size_t in text_book_par
sed -i "s:size_t i, j, k, num_vars, num_fns, num_deriv_vars;:size_t i, j, k;\n  int num_vars, num_fns, num_deriv_vars;:g" ${dak_src}/test/text_book_par.cpp
mkdir -p ${dak_build}/cmake
cp %{_sourcedir}/BuildDakotaCustom.cmake ${dak_src}/cmake
cd ${dak_build}
cmake -C ${dak_src}/cmake/BuildDakotaCustom.cmake \
-D CMAKE_INSTALL_PREFIX=%{INSTALL_DIR}            \
-D CMAKE_CXX_FLAGS="-std=c++11 -DUSE_MPI=1"       \
-D DAKOTA_PYTHON=ON                               \
-D DAKOTA_HAVE_GSL=ON                             \
-D TPL_ENABLE_MPI=ON                              \
-D DAKOTA_HAVE_MPI=ON                             \
-D MPIEXEC=`which ibrun`                          \
-D MPI_EXEC=`which ibrun`                         \
-D DAKOTA_ENABLE_TESTS=ON                         \
${dak_src}


make -j ${ncores} VERBOSE=1
make -j ${ncores} install

cd ${dakota}
cp %{_sourcedir}/TACC_parallelism.tar.gz .
tar xvfz TACC_parallelism.tar.gz
chmod -R go=u-w TACC_parallelism
sed -i 's:/path/to/dakota/install:%{INSTALL_DIR}:g' TACC_parallelism/Case1-MassivelySerial/text_book_driver
sed -i 's:/path/to/dakota/install:%{INSTALL_DIR}:g' TACC_parallelism/Case2-SequentialParallel/text_book_par_driver
sed -i 's:/path/to/dakota/install:%{INSTALL_DIR}:g' TACC_parallelism/Case3-EvaluationTiling/text_book_par_driver
sed -i 's:/path/to/dakota/install:%{INSTALL_DIR}:g' TACC_parallelism/Case4-EvaluationSubmission/text_book_par_driver
cp -r TACC_parallelism %{INSTALL_DIR}/examples
 
if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/
  
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
local help_message = [[
The Dakota toolkit provides a flexible, extensible interface between analysis
codes and iterative systems analysis methods. Dakota contains algorithms for:
optimization with gradient and nongradient-based methods; uncertainty
quantification with sampling, reliability, stochastic expansion, and epistemic
methods; parameter estimation with nonlinear least squares methods; and
sensitivity/variance analysis with design of experiments and parameter study
methods.  These capabilities may be used on their own or as components within
advanced strategies such as hybrid optimization, surrogate-based optimization,
mixed integer nonlinear programming, or optimization under uncertainty.

This module defines the environmental variables TACC_%{MODULE_VAR}_DIR,
TACC_%{MODULE_VAR}_BIN, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC,
and TACC_%{MODULE_VAR}_DOC for the location of the main Dakota directory,
the binaries, the libraries, the include files, and TACC-specific documentation
respectively.

The location of the binary files and tests are also added to your PATH.
The location of the libraries files are also added to your LD_LIBRARY_PATH.

To get started, copy the TACC examples:
mkdir -p ${WORK}/apps/dakota
cp -r ${TACC_DAKOTA_DOC} ${WORK}/apps/dakota
cat ${WORK}/apps/dakota/TACC_parallelism/README

Extended documentation on Dakota can be found under ${TACC_%{MODULE_VAR}_DIR}/examples.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: system, application")
whatis("Keywords: optimization, uncertainty quantification, parameter estimation, sensitivity analysis")
whatis("Description: Dakota toolkit provides a flexible, extensible interface between analysis codes and iterative systems analysis methods")
whatis("URL: https://dakota.sandia.gov")

-- Export environmental variables
local dakota_dir="%{INSTALL_DIR}"
local dakota_bin=pathJoin(dakota_dir,"bin")
local dakota_test=pathJoin(dakota_dir,"test")
local dakota_lib=pathJoin(dakota_dir,"lib")
local dakota_inc=pathJoin(dakota_dir,"include")
local dakota_doc=pathJoin(dakota_dir,"examples/TACC_parallelism")
setenv("TACC_DAKOTA_DIR",dakota_dir)
setenv("TACC_DAKOTA_BIN",dakota_bin)
setenv("TACC_DAKOTA_LIB",dakota_lib)
setenv("TACC_DAKOTA_INC",dakota_inc)
setenv("TACC_DAKOTA_DOC",dakota_doc)

-- Prepend the dakota directories to the adequate PATH variables
prepend_path("PATH",dakota_bin)
prepend_path("PATH",dakota_test)
prepend_path("LD_LIBRARY_PATH",dakota_bin)
prepend_path("LD_LIBRARY_PATH",dakota_lib)

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

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
# $RPM_INSTALL_PREFIX0 /tmpmod -> /opt/apps
# $RPM_INSTALL_PREFIX1 /tmprpm -> /opt/apps
#sed -i "s:%{INSTALL_DIR}:$RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}:g" $RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}/examples/TACC_parallelism/Case1-MassivelySerial/text_book_driver
#sed -i "s:%{INSTALL_DIR}:$RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}:g" $RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}/examples/TACC_parallelism/Case2-SequentialParallel/text_book_par_driver
#sed -i "s:%{INSTALL_DIR}:$RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}:g" $RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}/examples/TACC_parallelism/Case3-EvaluationTiling/text_book_par_driver
#sed -i "s:%{INSTALL_DIR}:$RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}:g" $RPM_INSTALL_PREFIX1/%{INSTALL_SUFFIX}/examples/TACC_parallelism/Case4-EvaluationSubmission/text_book_par_driver
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

