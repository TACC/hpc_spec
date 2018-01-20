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
%define pkg_base_name cuda
%define MODULE_VAR    CUDA

%define __jar_repack %{nil}

# Create some macros (spec file variables)
%define major_version 9
%define minor_version 0
%define patch_version 176
%define driver_version 384.81
%define local_release 1

%define pkg_version %{major_version}.%{minor_version}
%define cuda_fam_ver %{pkg_base_name}%{major_version}_%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   %{patch_version}_%{local_release}%{?dist}
License:   http://docs.nvidia.com/cuda/eula
Group:     Development/Languages
URL:       http://www.nvidia.com/cuda
Packager:  TACC - jbarbosa@tacc.utexas.edu, cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}_%{pkg_version}.%{patch_version}_%{driver_version}_linux.run
Provides:  %{pkg_base_name}
AutoReqProv: no

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
NVIDIA(R)CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the libraries and attendant files needed to run
programs that make use of CUDA.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
NVIDIA(R)CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the libraries and attendant files needed to run
programs that make use of CUDA.

%description
NVIDIA(R)CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the libraries and attendant files needed to run
programs that make use of CUDA.


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

%setup -q -T -c %{pkg_base_name}-%{pkg_version}.%{release}


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
  
#   -toolkit            : Install CUDA X.X Toolkit
#   -toolkitpath=<PATH> : Specify path for CUDA location (default: /usr/local/cuda-X.X)
#   -samples            : Install CUDA X.X Samples
#   -samplespath=<PATH> : Specify path for Samples location (default: /usr/local/cuda-X.X/samples)

%global install_options -silent -override -toolkit -toolkitpath=$RPM_BUILD_ROOT%{INSTALL_DIR} -samples -samplespath=$RPM_BUILD_ROOT%{INSTALL_DIR}/samples
bash %{SOURCE0} %{install_options}

#Remove the error about gcc 4.6, it's what we have and seems to work
sed -i -e '/error -- unsupported GNU version/d' $RPM_BUILD_ROOT%{INSTALL_DIR}/include/host_config.h

# Remove buildroot
sed -i -e s,$RPM_BUILD_ROOT,,g $RPM_BUILD_ROOT%{INSTALL_DIR}/bin/nsight
sed -i -e s,$RPM_BUILD_ROOT,,g $RPM_BUILD_ROOT%{INSTALL_DIR}/bin/.uninstall_manifest_do_not_delete.txt
find $RPM_BUILD_ROOT%{INSTALL_DIR}/samples -name Makefile | xargs sed -i -e s,$RPM_BUILD_ROOT,,g
find $RPM_BUILD_ROOT%{INSTALL_DIR}/pkgconfig -name "*.pc" | xargs sed -i -e s,$RPM_BUILD_ROOT,,g
  
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
The NVIDIA CUDA Toolkit provides a comprehensive development environment for C
and C++ developers building GPU-accelerated applications. The CUDA Toolkit
includes a compiler for NVIDIA GPUs, math libraries, and tools for debugging
and optimizing the performance of your applications. You will also find
programming guides, user manuals, API reference, and other documentation to
help you get started quickly accelerating your application with GPUs.

This module defines the environmental variables TACC_%{MODULE_VAR}_BIN,
TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC, TACC_%{MODULE_VAR}_DOC, and TACC_%{MODULE_VAR}_DIR 
for the location of the cuda binaries, libaries, includes, 
documentation, and main root directory respectively.

The location of the:
1.) binary files is added to PATH
2.) libraries is added to LD_LIBRARY_PATH
3.) header files is added to INCLUDE 
4.) man pages is added to MANPATH


Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{pkg_base_name}")
whatis("Version: %{pkg_version}")
whatis("Category: Compiler, Runtime Support")
whatis("Description: NVIDIA CUDA Toolkit for Linux")
whatis("URL: http://www.nvidia.com/cuda")

-- Export environmental variables
local cuda_dir="%{INSTALL_DIR}"
local cuda_bin=pathJoin(cuda_dir,"bin")
local cuda_lib=pathJoin(cuda_dir,"lib64")
local cuda_inc=pathJoin(cuda_dir,"include")
local cuda_doc=pathJoin(cuda_dir,"doc")
setenv("TACC_%{MODULE_VAR}_DIR",cuda_dir)
setenv("TACC_%{MODULE_VAR}_BIN",cuda_bin)
setenv("TACC_%{MODULE_VAR}_LIB",cuda_lib)
setenv("TACC_%{MODULE_VAR}_INC",cuda_inc)
setenv("TACC_%{MODULE_VAR}_DOC",cuda_doc)
prepend_path("PATH"           ,cuda_bin)
prepend_path("LD_LIBRARY_PATH",cuda_lib)
prepend_path("INCLUDE"        ,cuda_inc)
prepend_path("MANPATH"        ,pathJoin(cuda_doc,"man"))
-- Adding to MODULEPATH for CUDA-dependent packages
prepend_path("MODULEPATH"     ,pathJoin("%{MODULE_PREFIX}","%{cuda_fam_ver}","modulefiles"))
add_property("arch","gpu")

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
# Modify %{INSTALL_PREFIX} to ${POST_INSTALL_PREFIX} 
sed -i -e s,%{INSTALL_PREFIX},${POST_INSTALL_PREFIX},g ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}/bin/nsight
sed -i -e s,%{INSTALL_PREFIX},${POST_INSTALL_PREFIX},g ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}/bin/.uninstall_manifest_do_not_delete.txt
find ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}/samples -name Makefile | xargs sed -i -e s,%{INSTALL_PREFIX},${POST_INSTALL_PREFIX},g
find ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}/pkgconfig -name "*.pc" | xargs sed -i -e s,%{INSTALL_PREFIX},${POST_INSTALL_PREFIX},g
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

