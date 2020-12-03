#
# Joe Allen
# 2020-12-03
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

%define shortsummary The Amber suite of biomolecular simulation programs
Summary: %{shortsummary}

# Give the package a base name
%define pkg_base_name amber
%define MODULE_VAR    AMBER

# Create some macros (spec file variables)
%define major_version 20
%define minor_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include system-defines.inc
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
########################################

Release:   2
License:   UCSF
Group:     Applications/Life Sciences
URL:       http://ambermd.org
Packager:  TACC - wallen@tacc.utexas.edu
Source0:   Amber20.tar.bz2 
Source1:   AmberTools20.tar.bz2
Source2:   AmberPatch20.tar.bz2

%package %{PACKAGE}
Summary: %{shortsummary}
Group:   Applications/Life Sciences
%description package
%{pkg_base_name}: %{shortsummary}

%package %{MODULEFILE}
Summary: The modulefile RPM
Group:   Lmod/Modulefiles
%description modulefile
Module file for %{pkg_base_name}

%description
%{pkg_base_name}: %{shortsummary}

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# For setup macros:
# -n specify non-standard name for build directory
# -b <n> means unpack the nth source *before* changing directories.
# -a <n> means unpack the nth source *after* changing to the
#        top-level build directory (i.e. as a subdirectory of the main source).
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!

%setup  -n %{pkg_base_name}%{major_version}_src
%setup -T -D -b 1 -n %{pkg_base_name}%{major_version}_src
%setup -T -D -b 2 -n %{pkg_base_name}%{major_version}_src


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
##################################
# If using build_rpm
##################################
%include compiler-load.inc
%include mpi-load.inc
%include mpi-env-vars.inc
##################################
# Manually load modules
##################################
module load cmake

%if "%{PLATFORM}" == "longhorn"
  module load python3/3.8.1
  module load cuda/10.2
%endif

##################################

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


# this was last built on Dec 3 and includes 11 AmberTools patches and 7 Amber patches
# https://ambermd.org/AmberPatches.php
# https://ambermd.org/ATPatches.php

# Apply all amber patches
./update_amber --update

# Patch to force boost toolset = gcc
patch -p1 < patch1

# Patch to increase max number of titratable residues
patch -p1 < patch2

mkdir install/
cd build/

#env CC=`which gcc` CXX=`which g++` F90=`which gfortran` \
cmake -DCMAKE_INSTALL_PREFIX=../install \
      -DCOMPILER=GNU \
      -DMPI=TRUE \
      -DOPENMP=TRUE \
      -DCUDA=TRUE \
      -DBUILD_GUI=FALSE \
      -DBUILD_PYTHON=TRUE \
      -DPYTHON_EXECUTABLE=/opt/apps/gcc7_3/python3/3.8.1/bin/python3 \
      -DDOWNLOAD_MINICONDA=FALSE \
      -DPRINT_PACKAGING_REPORT=TRUE \
      ../

make -j8 install

mv ../install/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
help(
[[
This version of Amber was built on %(date +'%B %d, %Y') and contains all
available Amber and AmberTools patches up to that date. The TACC Amber
installation includes the parallel binaries with the '.MPI' suffix and
GPU-enabled binaries with 'cuda' in the name. For example, see:

cpptraj.cuda      mdgx.cuda  pmemd.cuda       pmemd.cuda_DPFP.MPI  pmemd.cuda_SPFP
cpptraj.MPI.cuda  pbsa.cuda  pmemd.cuda_DPFP  pmemd.cuda.MPI       pmemd.cuda_SPFP.MPI

Visit https://ambermd.org/GPUHowTo.php for more information on running with GPUs
as  well as the TACC userguide at https://portal.tacc.utexas.edu/user-guides

Amber tools examples and benchmarks are included in the AmberTools directory.
Examples, data, docs, includes, info, libs are included in directories with
corresponding names.

The Amber modulefile defines the following environment variables:
TACC_AMBER_DIR   TACC_AMBER_TOOLS   TACC_AMBER_BIN   TACC_AMBER_DAT
TACC_AMBER_DOC   TACC_AMBER_INC     TACC_AMBER_LIB
for the corresponding Amber directories.

Also, AMBERHOME is set to the Amber Home Directory (TACC_AMBER_DIR),
and $AMBERHOME/bin is included in the PATH variable.

Version %{version}
]]
)

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Version-notes: Compiler:%{comp_fam_ver}, MPI:%{mpi_fam_ver}")
whatis("Category: computational biology, chemistry")
whatis("Keywords:  Chemistry, Biology, Molecular Dynamics, Cuda, Application")
whatis("URL: %{url}")
whatis("Description: %{shortsummary}")

local amber_dir   = "%{INSTALL_DIR}"
local amber_tools = "%{INSTALL_DIR}/AmberTools"
local amber_bin   = "%{INSTALL_DIR}/bin"
local amber_dat   = "%{INSTALL_DIR}/dat"
local amber_doc   = "%{INSTALL_DIR}/doc"
local amber_inc   = "%{INSTALL_DIR}/include"
local amber_lib   = "%{INSTALL_DIR}/lib"
local amber_python= "%{INSTALL_DIR}/lib/python3.8/site-packages"
local amber_perl  = "%{INSTALL_DIR}/lib/perl"
local amber_man   = "%{INSTALL_DIR}/share/man"

setenv("TACC_AMBER_DIR"   , amber_dir  )
setenv("TACC_AMBER_TOOLS" , amber_tools)
setenv("TACC_AMBER_BIN"   , amber_bin  )
setenv("TACC_AMBER_DAT"   , amber_dat  )
setenv("TACC_AMBER_DOC"   , amber_doc  )
setenv("TACC_AMBER_INC"   , amber_inc  )
setenv("TACC_AMBER_LIB"   , amber_lib  )
setenv("TACC_AMBER_MAN"   , amber_man  )
setenv("AMBERHOME"        , amber_dir  )

setenv("CUDA_HOME", "/usr/local/cuda-10.2")

prepend_path("PATH"           , amber_bin   )
prepend_path("LD_LIBRARY_PATH", amber_lib   )
prepend_path("PYTHONPATH"     , amber_python)
prepend_path("PERL5LIB"       , amber_perl  )
prepend_path("MANPATH"        , amber_man   )

family("amber")

always_load("gcc/7.3.0")
always_load("mvapich2-gdr/2.3.4")
always_load("cuda/10.2")
always_load("python3/3.8.1")
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
