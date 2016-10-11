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

Summary: OpenSWR package

# Give the package a base name
%define pkg_base_name swr
%define MODULE_VAR    SWR

# Create some macros (spec file variables)
%define major_version 12
%define minor_version 1
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

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

Release:   1
License:   GPL
Group:     Development/Tools
URL:       http://openswr.org
Packager:  TACC - jbarbosa@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: OpenSWR RPM
Group: X11/Tools
%description package
Intel open source software rasterizer

%package %{MODULEFILE}
Summary: The OpenSWR modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This OpenSWR modulefile RPM...

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
  #cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}

export WORK_DIR=$RPM_BUILD_ROOT/tmp/
export WORK_INSTALL_DIR=$RPM_BUILD_ROOT/%{INSTALL_DIR}

# 2) Required modules
module load TACC intel python autotools cmake

# 3) Build LLVM
export LLVM_BUILD_DIR=${WORK_DIR}/llvm-3.8
export LLVM_WORK_INSTALL_DIR=${WORK_INSTALL_DIR}
mkdir -p $LLVM_BUILD_DIR && cd $LLVM_BUILD_DIR
wget -c -N http://www.llvm.org/releases/3.8.0/llvm-3.8.0.src.tar.xz
tar xf llvm-3.8.0.src.tar.xz && mv llvm-3.8.0.src src
mkdir -p build && cd build
cmake ../src \
 -DCMAKE_CXX_COMPILER=/opt/apps/gcc/4.9.3/bin/g++ \
 -DCMAKE_C_COMPILER=/opt/apps/gcc/4.9.3/bin/gcc \
 -DCMAKE_BUILD_TYPE=Release \
 -DLLVM_ENABLE_RTTI=ON \
 -DLLVM_ENABLE_TERMINFO=OFF \
 -DLLVM_TARGETS_TO_BUILD=X86 \
 -DLLVM_LINK_LLVM_DYLIB=ON \
 -DCMAKE_INSTALL_PREFIX=${LLVM_WORK_INSTALL_DIR}
make -j15 && make install
export PATH=${LLVM_WORK_INSTALL_DIR}/bin:$PATH

# 3) Setup python virtualenv and install tools
# (Prevents needing to alter base distribution)
# (Supposed to be a one-time setup, but doesn't seem to work that way)
# (Supposed to be able to reactivate the virtualenv by sourcing 'activate')
virtualenv ${WORK_INSTALL_DIR}/python_ve
source ${WORK_INSTALL_DIR}/python_ve/bin/activate
pip install --upgrade pip
pip install --upgrade mako
pip install --upgrade lxml

mkdir -p ${WORK_DIR}/openswr-mesa && cd ${WORK_DIR}/openswr-mesa

# (The older OpenSWR branch, development moved to mesa-master early March)
# git clone https://github.com/OpenSWR/openswr-mesa.git .
# -OR-
# (Realize this is mesa-master and not a stable release branch!)
git clone git://anongit.freedesktop.org/git/mesa/mesa .
mkdir -p build && cd build
../autogen.sh \
 --disable-dri \
 --disable-egl \
 --enable-xlib-glx \
 --enable-shared-glapi \
 --enable-gallium-osmesa \
 --with-gallium-drivers=swrast,swr \
 --prefix=${WORK_INSTALL_DIR}
 CPPFLAGS=-I/work/01206/jbarbosa/lonestar/swr/GL.stampede
make -j15
make install


cat > ${WORK_INSTALL_DIR}/bin/mesa << "EOF"
#!/bin/bash
if [ -z "$KNOB_MAX_WORKER_THREADS" ]; then
	NUMBER_CORES_IN_NODE=`cat /proc/cpuinfo | grep processor | wc -l`
	if [ -z "$SLURM_TASKS_PER_NODE" ]; then
            echo "Unable to determine processes per node"
	        KNOB_MAX_WORKER_THREADS=$NUMBER_CORES_IN_NODE
	else
            echo "Able to determine processes per node"
	        regex='([0-9]+).*'
	        [[ $SLURM_TASKS_PER_NODE =~ $regex ]]
	        NUMBER_PROCESSES_PER_NODE=${BASH_REMATCH[1]}
	        KNOB_MAX_WORKER_THREADS=$(($NUMBER_CORES_IN_NODE / $NUMBER_PROCESSES_PER_NODE))
	fi
fi
export LD_LIBRARY_PATH=${TACC_SWR_PATH}/lib:$LD_LIBRARY_PATH 
GALLIUM_DRIVER=swr $*
EOF


cat > ${WORK_INSTALL_DIR}/bin/swr << "EOF"
#!/bin/bash
if [ -z "$KNOB_MAX_WORKER_THREADS" ]; then
	NUMBER_CORES_IN_NODE=`cat /proc/cpuinfo | grep processor | wc -l`
	if [ -z "$SLURM_TASKS_PER_NODE" ]; then
            echo "Unable to determine processes per node"
	        KNOB_MAX_WORKER_THREADS=$NUMBER_CORES_IN_NODE
	else
            echo "Able to determine processes per node"
	        regex='([0-9]+).*'
	        [[ $SLURM_TASKS_PER_NODE =~ $regex ]]
	        NUMBER_PROCESSES_PER_NODE=${BASH_REMATCH[1]}
	        KNOB_MAX_WORKER_THREADS=$(($NUMBER_CORES_IN_NODE / $NUMBER_PROCESSES_PER_NODE))
	fi
fi
export LD_LIBRARY_PATH=${TACC_SWR_PATH}/lib:$LD_LIBRARY_PATH 
GALLIUM_DRIVER=swr $*
EOF


cat > ${WORK_INSTALL_DIR}/bin/swr_nk << "EOF"
#!/bin/bash
export LD_LIBRARY_PATH=${TACC_SWR_PATH}/lib:$LD_LIBRARY_PATH 
GALLIUM_DRIVER=swr $*
EOF



  
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

whatis("Name: OpenSWR")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local swr_dir           = "%{INSTALL_DIR}"
local python_swr_path   = pathJoin("%{INSTALL_DIR}","python_ve/lib/python2.7/site-packages")

family("SWR")
prepend_path(    "PATH",                pathJoin(swr_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(swr_dir, "lib"))
prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/bar1_1/modulefiles")
prepend_path(	 "PYTHONPATH", 		python_swr_path)
setenv( "TACC_%{MODULE_VAR}_DIR",       swr_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(swr_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(swr_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(swr_dir, "bin"))
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

