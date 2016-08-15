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
%define bazel_base_name     bazel
%define pkg_base_name       tensorflow
%define BAZEL_MODULE_VAR    BAZEL
%define MODULE_VAR          TENSORFLOW

# Create some macros (spec file variables)
%define bazel_major_version 0
%define bazel_minor_version 3
%define bazel_micro_version 1
%define major_version 0
%define minor_version 9
%define micro_version 0

%define bazel_pkg_version %{bazel_major_version}.%{bazel_minor_version}.%{bazel_micro_version}
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
License:   BSD
Group:     System/Utils
URL:       https://github.com/bazelbuild/bazel
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long descrTensorFlow™ is an open source software library for numerical computation using data flow graphs. Nodes in the graph represent mathematical operations, while the graph edges represent the multidimensional data arrays (tensors) communicated between them. The flexible architecture allows you to deploy computation to one or more CPUs or GPUs in a desktop, server, or mobile device with a single API. TensorFlow was originally developed by researchers and engineers working on the Google Brain Team within Google's Machine Intelligence research organization for the purposes of conducting machine learning and deep neural networks research, but the system is general enough to be applicable in a wide variety of other domains as well.iption for the package RPM...
%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
TensorFlow™ is an open source software library for numerical computation using data flow graphs. Nodes in the graph represent mathematical operations, while the graph edges represent the multidimensional data arrays (tensors) communicated between them. The flexible architecture allows you to deploy computation to one or more CPUs or GPUs in a desktop, server, or mobile device with a single API. TensorFlow was originally developed by researchers and engineers working on the Google Brain Team within Google's Machine Intelligence research organization for the purposes of conducting machine learning and deep neural networks research, but the system is general enough to be applicable in a wide variety of other domains as well.
%description
TensorFlow™ is an open source software library for numerical computation using data flow graphs. Nodes in the graph represent mathematical operations, while the graph edges represent the multidimensional data arrays (tensors) communicated between them. The flexible architecture allows you to deploy computation to one or more CPUs or GPUs in a desktop, server, or mobile device with a single API. TensorFlow was originally developed by researchers and engineers working on the Google Brain Team within Google's Machine Intelligence research organization for the purposes of conducting machine learning and deep neural networks research, but the system is general enough to be applicable in a wide variety of other domains as well.

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

# Insert necessary module commands
ml purge
ml TACC
#ml gcc/4.9.1 git mkl/11.3 cuda/7.5 cudnn/4.0 binutils/2.25 swig/3.0.10 python/2.7.12
ml gcc/4.9.1 git mkl/11.3 cuda/7.5 cudnn/4.0 binutils/2.25 python/2.7.12
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
export JAVA_HOME=/usr/java/jdk1.8.0_77

echo $PATH
echo $LD_LIBRARY_PATH


export tensorflow=`pwd`
git clone https://github.com/bazelbuild/bazel.git
cd %{bazel_base_name}
git checkout tags/%{bazel_pkg_version}
patch -p0 < %{_sourcedir}/CROSSTOOL-%{bazel_pkg_version}.patch
./compile.sh
./output/bazel # Start bazel java daemon
cd ${tensorflow}
git clone --recurse-submodules https://github.com/tensorflow/tensorflow
cd %{pkg_base_name}
git checkout tags/v%{pkg_version}
#patch -p0 < %{_sourcedir}/swig-v%{pkg_version}.patch
patch -p0 < %{_sourcedir}/CROSSTOOL-v%{pkg_version}.patch
patch -p0 < %{_sourcedir}/crosstool_wrapper_driver_is_not_gcc-v%{pkg_version}.patch
./configure < %{_sourcedir}/%{pkg_base_name}.input
${tensorflow}/%{bazel_base_name}/output/bazel build -c opt --copt=-mavx --linkopt '-lrt' --copt="-DGPR_BACKWARDS_COMPATIBILITY_MODE" --conlyopt="-std=c99" --genrule_strategy=standalone --spawn_strategy=standalone --config=cuda -s --verbose_failures //tensorflow/tools/pip_package:build_pip_package
cd ${tensorflow}/%{pkg_base_name}
bazel-bin/tensorflow/tools/pip_package/build_pip_package ${tensorflow}/%{pkg_base_name}/tensorflow_pkg 
pip install --prefix=%{INSTALL_DIR} --no-binary :all: --install-option="--prefix=%{INSTALL_DIR}" ${tensorflow}/%{pkg_base_name}/tensorflow_pkg/tensorflow-0.9.0-py2-none-any.whl 
cp -rp %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

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
TensorFlow is an open source software library for numerical computation using
data flow graphs. Nodes in the graph represent mathematical operations, while
the graph edges represent the multidimensional data arrays (tensors)
communicated between them. The flexible architecture allows you to deploy
computation to one or more CPUs or GPUs in a desktop, server, or mobile device
with a single API. TensorFlow was originally developed by researchers and
engineers working on the Google Brain Team within Googles Machine Intelligence
research organization for the purposes of conducting machine learning and deep
neural networks research, but the system is general enough to be applicable in
a wide variety of other domains as well.

This module defines the environmental variables TACC_%{MODULE_VAR}_DIR,
TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_BIN for the location of 
the main TensorFlow directory, libraries, and the binaries.

The location of the libraries are added to your LD_LIBRARY_PATH and to your
PYTHONPATH. The location of the binary files is also added to your PATH.

To load this module:
module reset
module load gcc/4.9.1 cuda/7.5 cudnn/4.0 python/2.7.12 mkl/11.3 tensorflow/0.9.0

Tutorial information can be found here:
https://github.com/aymericdamien/TensorFlow-Examples

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: Library")
whatis("Keywords: Machine Learning")
whatis("URL: https://www.tensorflow.org")

-- Export environmental variables
local tensorflow_dir="%{INSTALL_DIR}"

prepend_path("PATH",               pathJoin(tensorflow_dir,"bin"))
prepend_path("LD_LIBRARY_PATH",    pathJoin(tensorflow_dir,"lib"))
prepend_path("PYTHONPATH",         pathJoin(tensorflow_dir,"lib/python2.7/site-packages"))

setenv("TACC_%{MODULE_VAR}_DIR",   tensorflow_dir)
setenv("TACC_%{MODULE_VAR}_BIN",   pathJoin(tensorflow_dir,"bin"))
setenv("TACC_%{MODULE_VAR}_LIB",   pathJoin(tensorflow_dir,"lib"))

prereq("cuda/7.5", "cudnn/4.0", "python/2.7.12", "mkl/11.3")

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

