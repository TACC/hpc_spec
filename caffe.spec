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
%define pkg_base_name caffe 
%define MODULE_VAR    CAFFE 

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0
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

Release:   1%{?dist}
License:   BSD-2
Group:     Data/Deep Learning
URL:       https://github.com/intel/caffe
Packager:  TACC - zzhang@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Caffe is a deep learning framework. This is the Intel distribution with MPI support. 
Group: Data/Deep Learning
%description package
Caffe is a deep learning framework made with expression, speed, and modularity in mind. It is developed by the Berkeley Vision and Learning Center (BVLC) and community contributors.

%package %{MODULEFILE}
Summary: Caffe is a deep learning framework. This is the Intel distribution with MPI support.
Group: Data/Deep Learning
%description modulefile

%description
Caffe is a deep learning framework made with expression, speed, and modularity in mind. It is developed by the Berkeley Vision and Learning Center (BVLC) and community contributors.


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#The following line extract the tar ball from previously specified path
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

module load TACC

module load boost/1.64
module load hdf5/1.8.16

# Load Compiler
#%include compiler-load.inc
# Load MPI Library
%include mpi-load.inc

# Insert further module commands

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
  
  # Create some dummy directories and files for fun
  #mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  #mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  #mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
  # download libraries
  git clone https://github.com/zhaozhang/caffe-stampede2.git

  # Install MLSL
  mkdir -p ../mlsl
  pushd ../mlsl
  wget https://github.com/01org/MLSL/releases/download/v2017-Preview/l_mlsl_p_2017.0.014.tgz
  tar zxf l_mlsl_p_2017.0.014.tgz
  ./install.sh -s -d /admin/build/rpms/BUILD/caffe-1.0.0/caffe-stampede2/libraries/mlsl
  popd

  # Install protocol-buffer
  pushd caffe-stampede2/libraries
  mkdir protocol-buffer-build
  pushd protocol-buffer-build
  wget https://github.com/google/protobuf/releases/download/v3.0.0/protobuf-cpp-3.0.0.tar.gz
  tar zxf protobuf-cpp-3.0.0.tar.gz
  pushd protobuf-3.0.0
  CC=icc CXX=icpc ./configure --prefix=/admin/build/rpms/BUILD/caffe-1.0.0/caffe-stampede2/libraries/protocol-buffer-build
  make
  make install
  export PATH=/admin/build/rpms/BUILD/caffe-1.0.0/caffe-stampede2/libraries/protocol-buffer-build/bin:$PATH
  popd
  popd
  popd

  # Build Caffe
  cp caffe-stampede2/Makefile.config .
  cp caffe-stampede2/Makefile .
  #cd caffe-1.0.0
  unset MKLROOT
  #make clean
  CXX=icpc CXXFLAGS="-xCORE-AVX2 -axMIC-AVX512" make all -j 8
  #make pycaffe
  make distribute

  # Zhao: After make distribute, simply copy distribute/ to $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r external/mkl/mklml_lnx_2017.0.2.20170110 caffe-stampede2/libraries/mklml
  cp -r caffe-stampede2/libraries distribute/
  rm -rf distribute/libraries/protocol-buffer-build

  # echo "TACC_OPT %{TACC_OPT}"
  # move . to %{INSTALL_DIR} 

  # Copy everything from tarball over to the installation directory
  cp -r distribute/* $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

whatis("Name: caffe")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local bar_dir           = "%{INSTALL_DIR}"

family("caffe")
prepend_path(    "PATH",                pathJoin(bar_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/boost/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/gflags/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/glog/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/leveldb/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/lmdb/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/mlsl/intel64/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/opencv/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/protocol-buffer/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/snappy/lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(bar_dir, "libraries/mklml/lib"))
prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/bar1_1/modulefiles")
setenv( "TACC_%{MODULE_VAR}_DIR",                bar_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(bar_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(bar_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(bar_dir, "bin"))
load("hdf5")
load("boost")
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

