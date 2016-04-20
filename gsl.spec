#
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
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
%define pkg_base_name gsl
%define MODULE_VAR    GSL

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 16
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

Release:   1
License:   GPL
Group:     Development/Tools
URL:       http://www.gnu.org/software/bar
Packager:  TACC - Kevin Chen chenk@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}

Summary: The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers.
Group: System Environment/Base

%description package

The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers. It is free software under the GNU General Public License.

The library provides a wide range of mathematical routines such as random number generators, special functions and least-squares fitting. There are over 1000 functions in total

The complete range of subject areas covered by the library includes,

Complex Numbers Roots of Polynomials
Special Functions Vectors and Matrices
Permutations  Sorting
BLAS Support  Linear Algebra
Eigensystems  Fast Fourier Transforms
Quadrature  Random Numbers
Quasi-Random Sequences  Random Distributions
Statistics  Histograms
N-Tuples  Monte Carlo Integration
Simulated Annealing Differential Equations
Interpolation Numerical Differentiation
Chebyshev Approximation Series Acceleration
Discrete Hankel Transforms  Root-Finding
Minimization  Least-Squares Fitting
Physical Constants  IEEE Floating-Point
Discrete Wavelet Transforms Basis splines

Unlike the licenses of proprietary numerical libraries the license of GSL does not restrict scientific cooperation. It allows you to share your programs freely with others.

The current version is GSL-1.16. It was released on 19 July 2013. Details of recent changes can be found in the NEWS file. This is a stable release.

GSL can be found in the gsl subdirectory on your nearest GNU mirror http://ftpmirror.gnu.org/gsl/.

Main GNU ftp site: ftp://ftp.gnu.org/gnu/gsl/
For other ways to obtain GSL, please read How to get GNU Software

Installation instructions can be found in the included README and INSTALL files.

Precompiled binary packages are included in most GNU/Linux distributions.

A compiled version of GSL is available as part of Cygwin on Windows (but we recommend using GSL on a free operating system, such as GNU/Linux).


%package %{MODULEFILE}
Summary: The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers.
Group: System Environment/Base
%description modulefile
%description

The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers. It is free software under the GNU General Public License.

The library provides a wide range of mathematical routines such as random number generators, special functions and least-squares fitting. There are ove



#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

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
#%include mpi-load.inc

# Insert further module commands

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
  WD=`pwd`

  # Create some dummy directories and files for fun
#  export CFLAGS="-O3 -xAVX -axCORE-AVX2 -fp-model precise"
#  export CPPFLAGS="-O3 -xAVX -axCORE-AVX2 -fp-model precise"
 %if "%is_intel" == "1" 
  export CC=`which icc`
  export CXX=`which icpc`
  export CFLAGS="-O3 -xAVX -axCORE-AVX2"
  export CPPFLAGS="-O3 -xAVX -axCORE-AVX2" 
  export LDFLAGS="-xAVX -axCORE-AVX2"
%endif

%if "%is_gcc" == "1" 
  export CC=`which gcc`
  export CXX=`which g++`
  export CFLAGS="-O3 -march=sandybridge -mtune=haswell"
  export CPPFLAGS="-O3 -march=sandybridge -mtune=haswell"
  export LDFLAGS="-march=sandybridge -mtune=haswell"
%endif
 

  export CONFIG_FLAGS=""
  ./configure $CONFIG_FLAGS --prefix=%{INSTALL_DIR}
  make -j 12
  make install
#  sed -i -- 's/tmprpm/opt\/apps/g' %{INSTALL_DIR}/bin/gsl-config 
# Copy everything from tarball over to the installation directory
  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}

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
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.
]]

--help(help_msg)
help(help_msg)

whatis("Name: bar")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local bar_dir           = "%{INSTALL_DIR}"

family("bar")
prepend_path(    "PATH",                pathJoin(bar_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "lib"))
prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/bar1_1/modulefiles")
setenv( "TACC_%{MODULE_VAR}_DIR",                bar_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(bar_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(bar_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(bar_dir, "bin"))
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

