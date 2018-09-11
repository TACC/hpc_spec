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
%define pkg_base_name ospray
%define MODULE_VAR    OSPRAY
%define MODULE_VAR2    EMBREE

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 6
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc
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
License:   GPL
Group:     Software/Library
URL:       http://ospray.org
Packager:  TACC - jbarbosa@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%define ispc_version 1.9.2
%define embree_version 3.2.0
%define ospray_version %{version}
%define intel_tbb_path /opt/intel/tbb


%package %{PACKAGE}
Summary: The package RPM
Group: Software/Library
%description package
OSPRay is an open source, scalable, and portable ray tracing engine for high-performance, high-fidelity visualization on Intel® Architecture CPUs. OSPRay is released under the permissive Apache 2.0 license.

The purpose of OSPRay is to provide an open, powerful, and easy-to-use rendering library that allows one to easily build applications that use ray tracing based rendering for interactive applications (including both surface- and volume-based visualizations). OSPRay is completely CPU-based, and runs on anything from laptops, to workstations, to compute nodes in HPC systems.

OSPRay internally builds on top of Embree and ISPC (Intel® SPMD Program Compiler), and fully utilizes modern instruction sets like Intel® SSE4, AVX, AVX2, and AVX-512 to achieve high rendering performance, thus a CPU with support for at least SSE4.1 is required to run OSPRay.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
The longer-winded description of the package that will 
end in up inside the rpm and is queryable if installed via:
rpm -qi <rpm-name>


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#%setup -n %{pkg_base_name}-%{pkg_version}

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

rm -rf %{_sourcedir}/embree %{_sourcedir}/ispc %{_sourcedir}/ospray

cd %{_sourcedir}
wget -O ispc-linux.tar.gz http://sourceforge.net/projects/ispcmirror/files/v%{ispc_version}/ispc-v%{ispc_version}-linux.tar.gz


tar xzf ispc-linux.tar.gz
mv ispc-v%{ispc_version}-linux ispc
rm ispc-linux.tar.gz

cd %{_sourcedir}
git clone https://github.com/embree/embree.git embree
cd embree
git checkout v%{embree_version}

cd %{_sourcedir}
git clone https://github.com/ospray/ospray.git ospray
cd ospray
git checkout v%{ospray_version}

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
#%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  export QA_SKIP_BUILD_ROOT=1

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
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
  
  # Copy everything from tarball over to the installation directory
  # cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  export WORK_DIR=`pwd`
  export WORK_INSTALL_DIR=$RPM_BUILD_ROOT/%{INSTALL_DIR}
  export CFLAGS='%{TACC_OPT}'

  mkdir -p $WORK_INSTALL_DIR/bin
  cp %{_sourcedir}/ispc/ispc $WORK_INSTALL_DIR/bin

  module load intel/18.0.0 impi
  cd $WORK_DIR
  mkdir embree
  cd embree
  CC=icc CXX=icpc cmake %{_sourcedir}/embree -DCMAKE_INSTALL_PREFIX:PATH=$WORK_INSTALL_DIR -DEMBREE_ISPC_EXECUTABLE:FILE=$WORK_INSTALL_DIR/bin/ispc -DEMBREE_MAX_ISA=AVX512SKX -DEMBREE_TUTORIALS:BOOL=OFF -DEMBREE_TBB_ROOT:PATH=%{intel_tbb_path}
  make -j4
  make install

  export embree_DIR=$WORK_INSTALL_DIR

  cd $WORK_DIR
  mkdir ospray
  cd ospray
  #CC=icc CXX=icpc cmake %{_sourcedir}/ospray -DCMAKE_INSTALL_PREFIX:PATH=$WORK_INSTALL_DIR -DOSPRAY_APPS_BENCHMARK:BOOL=OFF -DOSPRAY_APPS_GLUTVIEWER:BOOL=OFF -DOSPRAY_APPS_PARAVIEW_TFN_CVT:BOOL=OFF -DOSPRAY_APPS_QTVIEWER:BOOL=OFF -DOSPRAY_APPS_VOLUMEVIEWER:BOOL=OFF -DOSPRAY_MODULE_MPI:BOOL=ON -DOSPRAY_APPS_UTILITIES:BOOL=OFF -DOSPRAY_SG_VTK:BOOL=ON
  CC=icc CXX=icpc cmake %{_sourcedir}/ospray -DCMAKE_INSTALL_PREFIX:PATH=$WORK_INSTALL_DIR
  make -j4
  make install


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

whatis("Name: OSPray")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local ospray_dir           = "%{INSTALL_DIR}"

family("ospray")
prepend_path(    "PATH",                pathJoin(ospray_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(ospray_dir, "lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(ospray_dir, "lib64"))
prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/ospray%{pkg_version}/modulefiles")

setenv( "TACC_%{MODULE_VAR}_DIR",                "%{INSTALL_DIR}")
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(ospray_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(ospray_dir, "lib64"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(ospray_dir, "bin"))

setenv( "embree_DIR",	"%{INSTALL_DIR}")
setenv( "ospray_DIR",	"%{INSTALL_DIR}")
setenv( "TACC_%{MODULE_VAR2}_DIR",                "%{INSTALL_DIR}")
setenv( "TACC_%{MODULE_VAR2}_INC",       pathJoin(ospray_dir, "include"))
setenv( "TACC_%{MODULE_VAR2}_LIB",       pathJoin(ospray_dir, "lib64"))
setenv( "TACC_%{MODULE_VAR2}_BIN",       pathJoin(ospray_dir, "bin"))
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

