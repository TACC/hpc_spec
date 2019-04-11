#
# W. Cyrus Proctor
# 2015-11-07
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
%define pkg_base_name mkl-dnn
%define MODULE_VAR    MKLDNN

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 18
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   Apache-2.0
Group:     System/libraries
URL:       https://github.com/intel/mkl-dnn
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
Intel(R) Math Kernel Library for Deep Neural Networks (Intel(R) MKL-DNN) is an
open-source performance library for deep-learning applications. The library
accelerates deep-learning applications and frameworks on Intel architecture.
Intel MKL-DNN contains vectorized and threaded building blocks that you can use
to implement deep neural networks (DNN) with C and C++ interfaces.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Intel(R) Math Kernel Library for Deep Neural Networks (Intel(R) MKL-DNN) is an
open-source performance library for deep-learning applications. The library
accelerates deep-learning applications and frameworks on Intel architecture.
Intel MKL-DNN contains vectorized and threaded building blocks that you can use
to implement deep neural networks (DNN) with C and C++ interfaces.

%description
Intel(R) Math Kernel Library for Deep Neural Networks (Intel(R) MKL-DNN) is an
open-source performance library for deep-learning applications. The library
accelerates deep-learning applications and frameworks on Intel architecture.
Intel MKL-DNN contains vectorized and threaded building blocks that you can use
to implement deep neural networks (DNN) with C and C++ interfaces.

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

%setup -n %{pkg_base_name}-%{pkg_version}


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
ml cmake
ml

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
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
 
  export ncores=24
  mkdir -p build
  cd build
  
cmake                                       \
-DCMAKE_INSTALL_PREFIX="%{INSTALL_DIR}"     \
-DCMAKE_C_COMPILER="${CC}"                  \
-DCMAKE_CXX_COMPILER="${CXX}"               \
-DMKLINC="${TACC_MKL_INC}"                  \
-DMKLIOMP5LIB="${TACC_MKL_LIB}/libiomp5.so" \
-DMKLLIB="${TACC_MKL_LIB}/libmkl_rt.so"     \
-DARCH_OPT_FLAGS="${TACC_VEC_FLAGS}"        \
../
  
  make -j ${ncores} VERBOSE=1
  make DESTDIR=$RPM_BUILD_ROOT install
  
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
Intel(R) Math Kernel Library for Deep Neural Networks (Intel(R) MKL-DNN) is an
open-source performance library for deep-learning applications. The library
accelerates deep-learning applications and frameworks on Intel architecture.
Intel MKL-DNN contains vectorized and threaded building blocks that you can use
to implement deep neural networks (DNN) with C and C++ interfaces.

This module defines the environmental variables TACC_%{MODULE_VAR}_DIR,
TACC_%{MODULE_VAR}_INC, and TACC_%{MODULE_VAR}_LIB for the location of the main directory,
the include files, and the shared libraries.

The value of MKLDNNROOT is also set to TACC_%{MODULE_VAR}_DIR.

A simple compile and link step might look like:

icpc -std=c++11 -I${MKLDNNROOT}/include -L${MKLDNNROOT}/lib simple_net.cpp -lmkldnn

More information can be found here:

https://github.com/intel/mkl-dnn#linking-your-application

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: system, libraries")
whatis("Keywords: System, Library")
whatis("Description: Intel Math Kernel Library for Deep Neural Networks ")
whatis("URL: https://github.com/intel/mkl-dnn")

-- Export environmental variables
local mkldnn_dir="%{INSTALL_DIR}"
local mkldnn_inc=pathJoin(mkldnn_dir,"include")
local mkldnn_lib=pathJoin(mkldnn_dir,"lib64")
setenv("TACC_%{MODULE_VAR}_DIR",mkldnn_dir)
setenv("TACC_%{MODULE_VAR}_INC",mkldnn_inc)
setenv("TACC_%{MODULE_VAR}_LIB",mkldnn_bin)

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{pkg_base_name}%{version}
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

