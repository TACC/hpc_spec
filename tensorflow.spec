#
# W. Cyrus Proctor
# 2016-12-13
# HERE BE DRAGONS -- Do not key off this file if you enjoy your sanity!
#
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
%define CUDA_MODULE_VAR     CUDA
%define CUDNN_MODULE_VAR    CUDNN
%define PYTHON_MODULE_VAR   PYTHON
%define MODULE_VAR          TENSORFLOW


# Create some macros (spec file variables)
%define gpu_build                 0
%define bazel_base_major_version  0
%define bazel_base_minor_version  3
%define bazel_base_micro_version  1
%define bazel_two_major_version   0
%define bazel_two_minor_version   4
%define bazel_two_micro_version   2
%define bazel_thr_major_version   0
%define bazel_thr_minor_version   4
%define bazel_thr_micro_version   4
%define bazel_fou_major_version   0
%define bazel_fou_minor_version   4
%define bazel_fou_micro_version   5
%define bazel_fiv_major_version   0
%define bazel_fiv_minor_version   5
%define bazel_fiv_micro_version   0
%define bazel_major_version       0
%define bazel_minor_version       5
%define bazel_micro_version       4
%define cuda_major_version        8
%define cuda_minor_version        0
%define cudnn_major_version       5
%define cudnn_minor_version       1
%define python_major_version      2
%define python_minor_version      7
%define python_patch_version      13
%define major_version             1
%define minor_version             4
%define micro_version             1
%define tensorboard_major_version 0
%define tensorboard_minor_version 4
%define tensorboard_micro_version 0rc3


%define bazel_base_version   %{bazel_base_major_version}.%{bazel_base_minor_version}.%{bazel_base_micro_version}
%define bazel_two_version   %{bazel_two_major_version}.%{bazel_two_minor_version}.%{bazel_two_micro_version}
%define bazel_thr_version   %{bazel_thr_major_version}.%{bazel_thr_minor_version}.%{bazel_thr_micro_version}
%define bazel_fou_version   %{bazel_fou_major_version}.%{bazel_fou_minor_version}.%{bazel_fou_micro_version}
%define bazel_fiv_version   %{bazel_fiv_major_version}.%{bazel_fiv_minor_version}.%{bazel_fiv_micro_version}
%define bazel_pkg_version    %{bazel_major_version}.%{bazel_minor_version}.%{bazel_micro_version}
%define cuda_pkg_version     %{cuda_major_version}.%{cuda_minor_version}
%define cuda_und_version     %{cuda_major_version}_%{cuda_minor_version}
%define cuda_fam_ver         cuda%{cuda_und_version}
%define cudnn_pkg_version    %{cudnn_major_version}.%{cudnn_minor_version}  
%define cudnn_und_version    %{cudnn_major_version}_%{cudnn_minor_version}
%define cudnn_fam_ver        cudnn%{cudnn_und_version}
%define python_pkg_version   %{python_major_version}.%{python_minor_version}.%{python_patch_version}
%define python_sht_version   %{python_major_version}.%{python_minor_version}
%define python_squ_version   %{python_major_version}%{python_minor_version}
%define python_und_version   %{python_major_version}_%{python_minor_version}
%define python_fam_ver       python%{python_und_version}

%if "%{python_major_version}" == "2"
  %define python_pkg_name   python
  %define pip_name          pip
  %define python_pkg_date   July 06, 2017
%else
  %define python_pkg_name   python3
  %define pip_name          pip3
  %define python_pkg_date   August 09, 2017 
%endif


%if "%{?gpu_build}" == "1"
  %define build_type gpu
  %define BUILD_TYPE GPU
%else
  %define build_type cpu
  %define BUILD_TYPE CPU
%endif

%define pkg_version         %{major_version}.%{minor_version}.%{micro_version}
%define tensorboard_version %{tensorboard_major_version}.%{tensorboard_minor_version}.%{tensorboard_micro_version}


### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
# Redefine name-defines macros for tensorflow dependencies
%if "%{build_type}" == "gpu"
  %define pkg_name        %{name_prefix}-%{pkg_base_name}-%{build_type}-%{comp_fam_ver}-%{cuda_fam_ver}-%{cudnn_fam_ver}-%{python_fam_ver}
  %define INSTALL_SUFFIX  %{comp_fam_ver}/%{cuda_fam_ver}/%{cudnn_fam_ver}/%{python_fam_ver}/%{pkg_base_name}-%{build_type}/%{pkg_version}
  %define MODULE_SUFFIX   %{comp_fam_ver}/%{cuda_fam_ver}/%{cudnn_fam_ver}/%{python_fam_ver}/modulefiles/%{pkg_base_name}-%{build_type}
%endif
%if "%{build_type}" == "cpu"
  %define pkg_name        %{name_prefix}-%{pkg_base_name}-%{build_type}-%{comp_fam_ver}-%{python_fam_ver}
  %define INSTALL_SUFFIX  %{comp_fam_ver}/%{python_fam_ver}/%{pkg_base_name}-%{build_type}/%{pkg_version}
  %define MODULE_SUFFIX   %{comp_fam_ver}/%{python_fam_ver}/modulefiles/%{pkg_base_name}-%{build_type}
%endif
%define MODULE_DIR      %{MODULE_PREFIX}/%{MODULE_SUFFIX}
%define INSTALL_DIR     %{INSTALL_PREFIX}/%{INSTALL_SUFFIX}
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   https://www.apache.org/licenses/LICENSE-2.0
Group:     System/Utils
URL:       https://www.tensorflow.org
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
TensorFlow™ is an open source software library for numerical computation using
data flow graphs. Nodes in the graph represent mathematical operations, while
the graph edges represent the multidimensional data arrays (tensors)
communicated between them. The flexible architecture allows you to deploy
computation to one or more CPUs or GPUs in a desktop, server, or mobile device
with a single API. TensorFlow was originally developed by researchers and
engineers working on the Google Brain Team within Google's Machine Intelligence
research organization for the purposes of conducting machine learning and deep
neural networks research, but the system is general enough to be applicable in
a wide variety of other domains as well.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
TensorFlow™ is an open source software library for numerical computation using
data flow graphs. Nodes in the graph represent mathematical operations, while
the graph edges represent the multidimensional data arrays (tensors)
communicated between them. The flexible architecture allows you to deploy
computation to one or more CPUs or GPUs in a desktop, server, or mobile device
with a single API. TensorFlow was originally developed by researchers and
engineers working on the Google Brain Team within Google's Machine Intelligence
research organization for the purposes of conducting machine learning and deep
neural networks research, but the system is general enough to be applicable in
a wide variety of other domains as well.

%description
TensorFlow™ is an open source software library for numerical computation using
data flow graphs. Nodes in the graph represent mathematical operations, while
the graph edges represent the multidimensional data arrays (tensors)
communicated between them. The flexible architecture allows you to deploy
computation to one or more CPUs or GPUs in a desktop, server, or mobile device
with a single API. TensorFlow was originally developed by researchers and
engineers working on the Google Brain Team within Google's Machine Intelligence
research organization for the purposes of conducting machine learning and deep
neural networks research, but the system is general enough to be applicable in
a wide variety of other domains as well.

#---------------------------------------
%prep
#---------------------------------------
echo "bazel_base_version   %{bazel_base_version}"
echo "bazel_two_version    %{bazel_two_version}"
echo "bazel_thr_version    %{bazel_thr_version}"
echo "bazel_fou_version    %{bazel_fou_version}"
echo "bazel_fiv_version    %{bazel_fiv_version}"
echo "bazel_pkg_version    %{bazel_pkg_version}"
echo "cuda_pkg_version     %{cuda_pkg_version}"
echo "cuda_und_version     %{cuda_und_version}"
echo "cuda_fam_ver         %{cuda_fam_ver}"
echo "cudnn_pkg_version    %{cudnn_pkg_version}"
echo "cudnn_und_version    %{cudnn_und_version}"
echo "cudnn_fam_ver        %{cudnn_fam_ver}"
echo "python_pkg_version   %{python_pkg_version}"
echo "python_und_version   %{python_und_version}"
echo "python_squ_version   %{python_squ_version}"
echo "python_fam_ver       %{python_fam_ver}"
echo "pkg_version          %{pkg_version}"
echo "tensorboard_version  %{tensorboard_version}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  rm -rf %{_builddir}/bazel
  rm -rf %{_builddir}/bazel-%{bazel_two_version}
  rm -rf %{_builddir}/bazel-%{bazel_thr_version}
  rm -rf %{_builddir}/bazel-%{bazel_fou_version}
  rm -rf %{_builddir}/bazel-%{bazel_fiv_version}
  rm -rf %{_builddir}/bazel-%{bazel_base_version}
  rm -rf %{_builddir}/tensorflow
  rm -rf %{_builddir}/tensorflow_pip
  rm -rf %{_builddir}/tensorboard
  rm -rf /root/.cache/bazel
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
# Load Compiler
%include compiler-load.inc

%if "%{build_type}" == "gpu"
ml git cuda/%{cuda_pkg_version} cudnn/%{cudnn_pkg_version} %{python_pkg_name}/%{python_pkg_version}
%endif

%if "%{build_type}" == "cpu"
ml git %{python_pkg_name}/%{python_pkg_version}
%endif

# System python is too old for subprocess module commands
# when doing #/usr/bin/env python shebangs.
%if "%{python_major_version}" == "3"
ml python
%endif

ml swig
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
# Installed on stampede c560-901
#export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.111-0.b15.el6_8.x86_64
# Installed on Stampede2 jail
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.151-1.b12.el7_4.x86_64
# Upgrade pip
export PATH=%{_builddir}/tensorflow_pip/bin:$PATH
export LD_LIBRARY_PATH=%{_builddir}/tensorflow_pip/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=%{_builddir}/tensorflow_pip/lib/python%{python_sht_version}/site-packages:${PYTHONPATH}
%{pip_name} install pip --upgrade --ignore-installed --install-option="--prefix=%{_builddir}/tensorflow_pip"
%{pip_name} install wheel --upgrade --ignore-installed --install-option="--prefix=%{_builddir}/tensorflow_pip"
%{pip_name} --version
%{pip_name} list

echo $PATH
echo $LD_LIBRARY_PATH


export tensorflow=`pwd`

# First, boostrap with earlier base version of bazel
cd ${tensorflow}
pgrep -f bazel | xargs --no-run-if-empty kill # Kill any bazel daemons
git clone https://github.com/bazelbuild/bazel.git
mv %{bazel_base_name} %{bazel_base_name}-%{bazel_base_version}
cd %{bazel_base_name}-%{bazel_base_version}
git checkout tags/%{bazel_base_version}
patch -p0 < %{_sourcedir}/CROSSTOOL-%{bazel_base_version}.patch
./compile.sh
./output/bazel # Start bazel java daemon
export PATH=%{_builddir}/%{bazel_base_name}-%{bazel_base_version}/output:${PATH} # Put base bazel on path for tensorflow configure script
which bazel
pgrep -f bazel | xargs --no-run-if-empty kill # Kill the bazel daemon


# Second, boostrap with earlier mid version of bazel
cd ${tensorflow}
pgrep -f bazel | xargs --no-run-if-empty kill # Kill any bazel daemons
git clone https://github.com/bazelbuild/bazel.git
mv %{bazel_base_name} %{bazel_base_name}-%{bazel_two_version}
cd %{bazel_base_name}-%{bazel_two_version}
git checkout tags/%{bazel_two_version}
patch -p0 < %{_sourcedir}/CROSSTOOL-%{bazel_two_version}.patch
bazel build //src:bazel --verbose_failures --sandbox_debug --genrule_strategy=standalone --spawn_strategy=standalone
./bazel-bin/src/bazel # Start bazel java daemon
export PATH=%{_builddir}/%{bazel_base_name}-%{bazel_two_version}/bazel-bin/src:${PATH} # Put mid bazel on path for tensorflow configure script
which bazel
pgrep -f bazel | xargs --no-run-if-empty kill # Kill the bazel daemon


# Third, boostrap with earlier mid version of bazel
cd ${tensorflow}
pgrep -f bazel | xargs --no-run-if-empty kill # Kill any bazel daemons
git clone https://github.com/bazelbuild/bazel.git
mv %{bazel_base_name} %{bazel_base_name}-%{bazel_thr_version}
cd %{bazel_base_name}-%{bazel_thr_version}
git checkout tags/%{bazel_thr_version}
patch -p0 < %{_sourcedir}/CROSSTOOL-%{bazel_thr_version}.patch
bazel build //src:bazel --verbose_failures --sandbox_debug --genrule_strategy=standalone --spawn_strategy=standalone
./bazel-bin/src/bazel # Start bazel java daemon
export PATH=%{_builddir}/%{bazel_base_name}-%{bazel_thr_version}/bazel-bin/src:${PATH} # Put mid bazel on path for tensorflow configure script
which bazel
pgrep -f bazel | xargs --no-run-if-empty kill # Kill the bazel daemon


# Fourth, boostrap with earlier mid version of bazel
cd ${tensorflow}
pgrep -f bazel | xargs --no-run-if-empty kill # Kill any bazel daemons
git clone https://github.com/bazelbuild/bazel.git
mv %{bazel_base_name} %{bazel_base_name}-%{bazel_fou_version}
cd %{bazel_base_name}-%{bazel_fou_version}
git checkout tags/%{bazel_fou_version}
patch -p0 < %{_sourcedir}/CROSSTOOL-%{bazel_fou_version}.patch
bazel build //src:bazel --verbose_failures --sandbox_debug --genrule_strategy=standalone --spawn_strategy=standalone
./bazel-bin/src/bazel # Start bazel java daemon
export PATH=%{_builddir}/%{bazel_base_name}-%{bazel_fou_version}/bazel-bin/src:${PATH} # Put mid bazel on path for tensorflow configure script
which bazel
pgrep -f bazel | xargs --no-run-if-empty kill # Kill the bazel daemon


# Fifth, boostrap with earlier mid version of bazel
cd ${tensorflow}
pgrep -f bazel | xargs --no-run-if-empty kill # Kill any bazel daemons
git clone https://github.com/bazelbuild/bazel.git
mv %{bazel_base_name} %{bazel_base_name}-%{bazel_fiv_version}
cd %{bazel_base_name}-%{bazel_fiv_version}
git checkout tags/%{bazel_fiv_version}
patch -p0 < %{_sourcedir}/CROSSTOOL-%{bazel_fiv_version}.patch
bazel build //src:bazel --verbose_failures --sandbox_debug --genrule_strategy=standalone --spawn_strategy=standalone
./bazel-bin/src/bazel # Start bazel java daemon
export PATH=%{_builddir}/%{bazel_base_name}-%{bazel_fiv_version}/bazel-bin/src:${PATH} # Put mid bazel on path for tensorflow configure script
which bazel
pgrep -f bazel | xargs --no-run-if-empty kill # Kill the bazel daemon


# Now, use earlier version of bazel to build mid version of bazel
cd ${tensorflow}
git clone https://github.com/bazelbuild/bazel.git
cd %{bazel_base_name}
git checkout tags/%{bazel_pkg_version}
patch -p0 < %{_sourcedir}/CROSSTOOL-%{bazel_pkg_version}.patch
bazel build //src:bazel --verbose_failures --sandbox_debug --genrule_strategy=standalone --spawn_strategy=standalone
pgrep -f bazel | xargs --no-run-if-empty kill # Kill the bazel daemon
./bazel-bin/src/bazel # Start bazel java daemon
export PATH=%{_builddir}/bazel/bazel-bin/src:${PATH} # Put bazel on path for tensorflow configure script
which bazel


# Tensorflow time!
cd ${tensorflow}
git clone --recurse-submodules https://github.com/tensorflow/tensorflow
cd %{pkg_base_name}
git checkout tags/v%{pkg_version}
patch -p0 < %{_sourcedir}/CROSSTOOL_nvcc.tpl-v%{pkg_version}.patch
patch -p0 < %{_sourcedir}/CROSSTOOL.toolchain.cpus-v%{pkg_version}.patch
patch -p0 < %{_sourcedir}/tensorflow.bzl-v%{pkg_version}.patch
#patch -p0 < %{_sourcedir}/BUILD.mpi-v%{pkg_version}.patch
#patch -p0 < %{_sourcedir}/BUILD.mkl-v%{pkg_version}.patch
#patch -p0 < %{_sourcedir}/mkl.BUILD-v%{pkg_version}.patch
##patch -p0 < %{_sourcedir}/CROSSTOOL-v%{pkg_version}.patch
##patch -p0 < %{_sourcedir}/crosstool_wrapper_driver_is_not_gcc-v%{pkg_version}.patch
./configure < %{_sourcedir}/%{pkg_base_name}-%{build_type}-py%{python_major_version}-%{pkg_version}.input
# # Fix protobuf env bug
# protobuf_bzl_filepath=`ls /root/.cache/bazel/_bazel_root/*/external/protobuf/protobuf.bzl`
# echo ${protobuf_bzl_filepath}
# sed -i 's:mnemonic="ProtoCompile",:mnemonic="ProtoCompile",\n        use_default_shell_env=True,:g' ${protobuf_bzl_filepath}
%if "%{build_type}" == "gpu"
${tensorflow}/%{bazel_base_name}/bazel-bin/src/bazel build -c opt --copt="-mavx2" --copt="-march=broadwell" --copt="-mtune=broadwell" --copt="-O3" --copt="-flto" --linkopt '-lrt' --genrule_strategy=standalone --spawn_strategy=standalone --config=cuda -s --verbose_failures //tensorflow/tools/pip_package:build_pip_package
%endif
%if "%{build_type}" == "cpu"
#export TF_MKL_ROOT=/opt/apps/intel/15/composer_xe_2015.3.187/mkl
#${tensorflow}/%{bazel_base_name}/bazel-bin/src/bazel build -c opt --copt=-mavx --linkopt '-lrt' --genrule_strategy=standalone --spawn_strategy=standalone --config=mkl --copt="-DEIGEN_USE_MKL_VML" -s --verbose_failures //tensorflow/tools/pip_package:build_pip_package
#export TF_MKL_ENABLED="true"
#export TF_NEED_MKL=1 
#export TF_DOWNLOAD_MKL=1
#export TF_MKL_ROOT=/opt/intel/compilers_and_libraries_2017.4.196/linux/mkl
${tensorflow}/%{bazel_base_name}/bazel-bin/src/bazel build -c opt --copt="-mavx2" --copt="-march=broadwell" --copt="-mtune=broadwell" --copt="-O3" --copt="-flto" --linkopt '-lrt' --genrule_strategy=standalone --spawn_strategy=standalone -s --verbose_failures //tensorflow/tools/pip_package:build_pip_package
%endif
cd ${tensorflow}/%{pkg_base_name}
bazel-bin/tensorflow/tools/pip_package/build_pip_package ${tensorflow}/%{pkg_base_name}/tensorflow_pkg 

# Cyclic dependency for tensorflow/tensorboard -- install with Pypi wheel to break the cycle
%{pip_name} install --prefix=%{INSTALL_DIR} tensorflow-tensorboard==%{tensorboard_version}

export PATH=%{INSTALL_DIR}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR}/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=%{INSTALL_DIR}/lib/python%{python_sht_version}/site-packages:${PYTHONPATH}

%{pip_name} install --prefix=%{INSTALL_DIR} --no-binary :all: --install-option="--prefix=%{INSTALL_DIR}" ${tensorflow}/%{pkg_base_name}/tensorflow_pkg/tensorflow-%{pkg_version}-cp%{python_squ_version}-cp%{python_squ_version}mu-linux_x86_64.whl
#touch %{INSTALL_DIR}/lib/python%{python_sht_version}/site-packages/google/__init__.py # Google schoogle *sigh*


# Tensorboard time!
#cd ${tensorflow}
#git clone https://github.com/tensorflow/tensorboard.git
#cd tensorboard
#git checkout tags/0.4.0-rc3
#${tensorflow}/%{bazel_base_name}/bazel-bin/src/bazel build -c opt --copt=-mavx --linkopt '-lrt' --genrule_strategy=standalone --spawn_strategy=standalone -s --verbose_failures //tensorboard/pip_package:build_pip_package


cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

umount %{INSTALL_DIR}/
  
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

%if "%{build_type}" == "gpu"

%define cuda_inherit   %{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/cuda
%define cudnn_inherit  %{MODULE_PREFIX}/%{comp_fam_ver}/%{cuda_fam_ver}/modulefiles/cudnn
%define python_inherit %{MODULE_PREFIX}/%{comp_fam_ver}/%{cuda_fam_ver}/%{cudnn_fam_ver}/modulefiles/%{python_pkg_name}

mkdir -p $RPM_BUILD_ROOT%{cuda_inherit}
cat > $RPM_BUILD_ROOT%{cuda_inherit}/%{cuda_pkg_version}.lua  << 'EOF'
local help_message = [[
The NVIDIA CUDA Toolkit provides a comprehensive development environment for C
and C++ developers building GPU-accelerated applications. The CUDA Toolkit
includes a compiler for NVIDIA GPUs, math libraries, and tools for debugging
and optimizing the performance of your applications. You will also find
programming guides, user manuals, API reference, and other documentation to
help you get started quickly accelerating your application with GPUs.

This module defines the environmental variables TACC_%{CUDA_MODULE_VAR}_BIN,
TACC_%{CUDA_MODULE_VAR}_LIB, TACC_%{CUDA_MODULE_VAR}_INC, TACC_%{CUDA_MODULE_VAR}_DOC, and TACC_%{CUDA_MODULE_VAR}_DIR 
for the location of the cuda binaries, libaries, includes, 
documentation, and main root directory respectively.

The location of the:
1.) binary files is added to PATH
2.) libraries is added to LD_LIBRARY_PATH
3.) header files is added to INCLUDE 
4.) man pages is added to MANPATH


Version %{cuda_pkg_version}
]]
help(help_message)
inherit()
prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{cuda_fam_ver}/modulefiles", priority=10}
EOF

mkdir -p $RPM_BUILD_ROOT%{cudnn_inherit}
cat > $RPM_BUILD_ROOT%{cudnn_inherit}/%{cudnn_pkg_version}.lua  << 'EOF'
local help_msg=[[
The NVIDIA CUDA Deep Neural Network library (cuDNN) is a GPU-accelerated
library of primitives for deep neural networks. cuDNN provides highly tuned
implementations for standard routines such as forward and backward convolution,
pooling, normalization, and activation layers. cuDNN is part of the NVIDIA Deep
Learning SDK.

The %{CUDNN_MODULE_VAR} module defines the following environment variables:
TACC_%{CUDNN_MODULE_VAR}_DIR, TACC_%{CUDNN_MODULE_VAR}_LIB, TACC_%{CUDNN_MODULE_VAR}_INC and 
for the location of the %{CUDNN_MODULE_VAR} distribution, libraries,
include files, and libraries respectively.

Version %{cudnn_pkg_version}
]]
help(help_msg)
inherit()
prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{cuda_fam_ver}/%{cudnn_fam_ver}/modulefiles", priority=10}
EOF

mkdir -p $RPM_BUILD_ROOT%{python_inherit}
cat > $RPM_BUILD_ROOT%{python_inherit}/%{python_pkg_version}.lua << 'EOF'
local help_msg=[[
This is the %{python_pkg_name} package built on %{python_pkg_date}.

You can install your own modules (choose one method):
        1. %{python_pkg_name} setup.py install --user
        2. %{python_pkg_name} setup.py install --home=<dir>
        3. %{pip_name} install --user module-name

Version %{python_pkg_version}
]]
help(help_msg)
inherit()
prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{cuda_fam_ver}/%{cudnn_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}
EOF
%endif 


%if "%{build_type}" == "cpu"


%define python_inherit       %( if [ ! -f "%{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua" ]; then echo "%{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua"; else echo ""; fi )
%define python_mv2_inherit   %( if [ ! -f "%{MODULE_PREFIX}/%{comp_fam_ver}/mvapich2_2_1/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua" ]; then echo "%{MODULE_PREFIX}/%{comp_fam_ver}/mvapich2_2_1/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua"; else echo ""; fi )

echo "%{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua"
echo "python_inherit     '%{python_inherit}'"
echo "python_mv2_inherit '%{python_mv2_inherit}'"

########## Python3 on Maverick does not have mv2 component
%define python_mv2_inherit %{nil}



# Need python and this file should already exist.
#if [ ! -f "%{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/python/%{python_pkg_version}.lua" ]; then
#echo "Adding python inherit file in build_modulefile"
#mkdir -p $RPM_BUILD_ROOT%{python_inherit}
#cat > $RPM_BUILD_ROOT%{python_inherit}/%{python_pkg_version}.lua << 'EOF'
#inherit()
#prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}
#EOF
#else
#  echo "Nope! %{python_inherit}"
#fi

%endif 

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

To load the GPU-enabled module:
module reset
module load %{comp_module} cuda/%{cuda_pkg_version} cudnn/%{cudnn_pkg_version} %{python_pkg_name}/%{python_pkg_version} %{pkg_base_name}-gpu/%{pkg_version}

To load the CPU-enabled module:
module reset
module load %{comp_module} %{python_pkg_name}/%{python_pkg_version} %{pkg_base_name}-cpu/%{pkg_version}

Tutorial information can be found here:
https://github.com/aymericdamien/TensorFlow-Examples

Version %{version} (%{BUILD_TYPE}-enabled)
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}-%{build_type}")
whatis("Version: %{version}")
whatis("Category: Library")
whatis("Keywords: Machine Learning")
whatis("URL: https://www.tensorflow.org")

-- Export environmental variables
local tensorflow_dir="%{INSTALL_DIR}"

prepend_path("PATH",               pathJoin(tensorflow_dir,"bin"))
prepend_path("LD_LIBRARY_PATH",    pathJoin(tensorflow_dir,"lib"))
prepend_path("PYTHONPATH",         pathJoin(tensorflow_dir,"lib/python%{python_sht_version}/site-packages"))

setenv("TACC_%{MODULE_VAR}_DIR",   tensorflow_dir)
setenv("TACC_%{MODULE_VAR}_BIN",   pathJoin(tensorflow_dir,"bin"))
setenv("TACC_%{MODULE_VAR}_LIB",   pathJoin(tensorflow_dir,"lib"))
family("tensorflow")

EOF

%if "%{build_type}" == "gpu"
  echo 'add_property("arch","gpu")' >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
%endif

  
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
%if "%{build_type}" == "gpu"
  %{cuda_inherit}
  %{cudnn_inherit}
  %{python_inherit}
%endif
%if "%{build_type}" == "cpu"
  %{python_inherit}
  %{python_mv2_inherit}
%endif

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
#set -x
if ! grep -qs 'prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}' %{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua; then
  #echo "Appending MP %{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua"
  echo 'prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}' >> %{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua
fi
### Must be on  for python2 on maverick
### Must be off for python3 on maverick
#if ! grep -qs 'prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}' %{MODULE_PREFIX}/%{comp_fam_ver}/mvapich2_2_1/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua; then
#  #echo "Appending mv2 MP %{MODULE_PREFIX}/%{comp_fam_ver}/mvapich2_2_1/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua"
#  echo 'prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}' >> %{MODULE_PREFIX}/%{comp_fam_ver}/mvapich2_2_1/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua
#fi
%preun %{MODULEFILE}
#set -x
if grep -qs 'prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}' %{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua; then
  #echo "Remove MP"
  sed -i '\:prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}:d' %{MODULE_PREFIX}/%{comp_fam_ver}/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua
fi
### Must be on  for python2 on maverick
### Must be off for python3 on maverick
#if grep -qs 'prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}' %{MODULE_PREFIX}/%{comp_fam_ver}/mvapich2_2_1/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua; then
#  #echo "Remove mv2 MP"
#  sed -i '\:prepend_path{"MODULEPATH", "%{MODULE_PREFIX}/%{comp_fam_ver}/%{python_fam_ver}/modulefiles", priority=10}:d' %{MODULE_PREFIX}/%{comp_fam_ver}/mvapich2_2_1/modulefiles/%{python_pkg_name}/%{python_pkg_version}.lua
#fi
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

