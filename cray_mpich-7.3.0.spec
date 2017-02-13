#
# W. Cyrus Proctor
# Antonio Gomez
# 2015-01-12
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
%define pkg_base_name cray_mpich
%define MODULE_VAR    CMPICH

# Create some macros (spec file variables)
%define major_version 7
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include name-defines.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   15
License:   GPL
Group:     Development/Tools
Packager:  TACC - carlos@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This package provides Cray Message Passing Toolkit 7.3.0, a Cray 
optimized version of hte MPICH libraries and runtime.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This modulefile provides access to the Cray Message Passing Toolkit 7.3.0

%description
This module provides access to the Cray Message Passing Toolkit 7.3.0, a Cray 
optimized version of the MPICH libraries and runtime.  

#---------------------------------------
%prep -n %{pkg_base_name}-%{version}
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n %{pkg_base_name}-%{version}
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
%include compiler-defines.inc
%include compiler-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

%if "%{comp_fam}" == "intel"
cp ./intel/mpi* $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
chmod ugo+rx $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpi*
# Enable traditional TACC MPICH_HOME
ln -s /opt/cray/mpt/7.3.0/gni/mpich-intel/14.0/lib     $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
ln -s /opt/cray/mpt/7.3.0/gni/mpich-intel/14.0/include $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
%endif
%if "%{comp_fam}" == "gcc"
cp ./%{comp_fam_ver}/mpi* $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
chmod ugo+rx $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpi*
# Enable traditional TACC MPICH_HOME
%if "%{comp_fam_ver}" != "gcc4_9"
ln -s /opt/cray/mpt/7.3.0/gni/mpich-gnu/5.1/lib     $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
ln -s /opt/cray/mpt/7.3.0/gni/mpich-gnu/5.1/include $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
%endif
%if "%{comp_fam_ver}" == "gcc4_9"
ln -s /opt/cray/mpt/7.3.0/gni/mpich-gnu/4.9/lib     $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
ln -s /opt/cray/mpt/7.3.0/gni/mpich-gnu/4.9/include $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
%endif
%endif


%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  ##### Create TACC Canary Files ########
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
This module provides access to the Cray Message Passing Toolkit 7.3.0, a Cray
optimized version of the MPICH libraries and runtime. The following commands 
will be automatically available for compiling MPI applications:

 mpicc  (C   source)
 mpicxx (C++ source)
 mpif90 (F90 source)
 mpif77 (F77 source)

If you wish to take advantage of the DMAPP optimizations for small payloads
(<=16 bytes) in MPI_Allreduce you will need to add libdmapp to your link line.
This can be achieved by simply adding "-ldmapp" to the link flags.

By default Cray MPT does not enable MPI_THREAD_MULTIPLE. To achieve that level 
of support set the following environmental variable:

export MPICH_MAX_THREAD_SAFETY=multiple

Improved support for multi-threaded applications that perform MPI operations 
within threaded regions is available via a separate version of the Cray-MPICH 
library that is invoked by using the compiler option "-craympich-mt".

Version  7.3.0
]]

--help(help_msg)
help(help_msg)

whatis("Name: cray_mpich")
whatis("Version: %{pkg_version}%{dbg}")

-- Create environment variables.
local mpt_base    = "/opt/cray/mpt/"
local mpt_version = "7.3.0"
local mpt_path    = pathJoin( mpt_base, mpt_version, "gni" ) 
setenv( "MPICH_HOME", "%{INSTALL_DIR}" )
setenv( "TACC_MPI_GETMODE", "cray_slurm" )

-- Paths specific to GCC
-- These seem to be valid for both 5.1 and 5.2
%if "%{comp_fam}" == "gcc"
local comp_dir  = "/mpich-gnu/5.1"
local full_path = pathJoin( mpt_path, comp_dir )
setenv( "CRAY_MPICH2_DIR", full_path )
setenv( "MPICH_DIR", full_path )
setenv( "TACC_CRAY_MPT_INC", pathJoin( full_path, "include" ) )
setenv( "TACC_CRAY_MPT_LIB", pathJoin( full_path, "lib" ) )
prepend_path("LD_LIBRARY_PATH", pathJoin( full_path, "lib" ) )
%endif

%if "%{comp_fam_ver}" == "gcc4_9"
local comp_dir  = "/mpich-gnu/4.9"
local full_path = pathJoin( mpt_path, comp_dir )
setenv( "CRAY_MPICH2_DIR", full_path )
setenv( "MPICH_DIR", full_path )
setenv( "TACC_CRAY_MPT_INC", pathJoin( full_path, "include" ) )
setenv( "TACC_CRAY_MPT_LIB", pathJoin( full_path, "lib" ) )
prepend_path("LD_LIBRARY_PATH", pathJoin( full_path, "lib" ) )
%endif

-- Paths specific to Intel
%if "%{comp_fam}" == "intel"
local comp_dir  = "mpich-intel/14.0"
local full_path = pathJoin( mpt_path, comp_dir ) 
setenv( "PE_INTEL_FIXED_PKGCONFIG_PATH", pathJoin( full_path, "lib/pkgconfig" ) )
setenv( "CRAY_MPICH2_DIR", full_path )
setenv( "MPICH_DIR", full_path )
setenv( "TACC_CRAY_MPT_INC", pathJoin( full_path, "include" ) )
setenv( "TACC_CRAY_MPT_LIB", pathJoin( full_path, "lib" ) )
prepend_path( "LD_LIBRARY_PATH", pathJoin( full_path, "lib" ) )
%endif

-- Paths independent of the compiler
prepend_path( "MANPATH", pathJoin( mpt_path, "man/mpich" ) )
prepend_path( "PATH",    pathJoin( mpt_path, "bin" ) )

-- Variables and paths set by Cray 
setenv( "CRAY_MPICH2_BASEDIR", mpt_path )
setenv( "CRAY_MPICH2_ROOTDIR", pathJoin( mpt_base, mpt_version ) )
setenv( "CRAY_MPICH2_VER", mpt_version )
setenv( "PE_CXX_PKGCONFIG_LIBS",       "mpichcxx" )
setenv( "PE_FORTRAN_PKGCONFIG_LIBS",   "mpichf90" )
setenv( "PE_MPICH_CXX_PKGCONFIG_LIBS", "mpichcxx" )
setenv( "PE_MPICH_DIR_CRAY_DEFAULT64", "64" )
setenv( "PE_MPICH_DIR_PGI_DEFAULT64",  "64" )
setenv( "PE_MPICH_FIXED_PRGENV", "INTEL" )
setenv( "PE_MPICH_FORTRAN_PKGCONFIG_LIBS", "mpichf90" )
setenv( "PE_MPICH_GENCOMPILERS_CRAY", "8.3" )
setenv( "PE_MPICH_GENCOMPILERS_GNU", "51" )
setenv( "PE_MPICH_GENCOMPILERS_PGI", "15.3" )
setenv( "PE_MPICH_GENCOMPS_CRAY", "83" )
setenv( "PE_MPICH_GENCOMPS_GNU", "51" )
setenv( "PE_MPICH_GENCOMPS_PGI", "153" )
setenv( "PE_MPICH_MODULE_NAME", "cray-mpich" )
setenv( "PE_MPICH_MULTITHREADED_LIBS_multithreaded", "_mt" )
setenv( "PE_MPICH_NV_LIBS", "" )
setenv( "PE_MPICH_NV_LIBS_nvidia20", "-lcudart" )
setenv( "PE_MPICH_NV_LIBS_nvidia35", "-lcudart" )
setenv( "PE_MPICH_PKGCONFIG_LIBS", "mpich" )
setenv( "PE_MPICH_PKGCONFIG_VARIABLES", "PE_MPICH_NV_LIBS_@accelerator@:PE_MPICH_MULTITHREADED_LIBS_@multithreaded@" )
setenv( "PE_MPICH_TARGET_VAR_nvidia20", "-lcudart" )
setenv( "PE_MPICH_TARGET_VAR_nvidia35", "-lcudart" )
setenv( "PE_MPICH_VOLATILE_PKGCONFIG_PATH", pathJoin( mpt_path, "mpich-@PRGENV@@PE_MPICH_DIR_DEFAULT64@/@PE_MPICH_GENCOMPS@/lib/pkgconfig" ) )
setenv( "PE_MPICH_VOLATILE_PRGENV", "CRAY GNU PGI" )

--TACC env for Cray Lib/Include - CRF 2015.12.17
setenv( "TACC_CRAY_XPMEM_INC", "/opt/cray/xpmem/default/include" )
setenv( "TACC_CRAY_XPMEM_LIB", "/opt/cray/xpmem/default/lib64" )
setenv( "TACC_CRAY_UGNI_INC",  "/opt/cray/ugni/default/include" )
setenv( "TACC_CRAY_UGNI_LIB",  "/opt/cray/ugni/default/lib64" )
setenv( "TACC_CRAY_UDREG_INC", "/opt/cray/udreg/default/include" )
setenv( "TACC_CRAY_UDREG_LIB", "/opt/cray/udreg/default/lib64" )
setenv( "TACC_CRAY_PMI_INC",   "/opt/cray/pmi/default/include" )
setenv( "TACC_CRAY_PMI_LIB",   "/opt/cray/pmi/default/lib64" )
setenv( "TACC_CRAY_DMAPP_INC", "/opt/cray/dmapp/default/include" )
setenv( "TACC_CRAY_DMAPP_LIB", "/opt/cray/dmapp/default/lib64" )
prepend_path( "PE_PKGCONFIG_LIBS",     "mpich" )
prepend_path( "PE_PKGCONFIG_PRODUCTS", "PE_MPICH" )

family( "MPI" )

-- Update LD_LIBRARY_PATH with Cray Libs - CRF 2015.12.17
prepend_path( 'LD_LIBRARY_PATH', "/opt/cray/xpmem/default/lib64" )
prepend_path( 'LD_LIBRARY_PATH', "/opt/cray/dmapp/default/lib64" )
prepend_path( 'LD_LIBRARY_PATH', "/opt/cray/pmi/default/lib64" )
prepend_path( 'LD_LIBRARY_PATH', "/opt/cray/ugni/default/lib64" )
prepend_path( 'LD_LIBRARY_PATH', "/opt/cray/udreg/default/lib64" )

local base_dir = "%{INSTALL_DIR}"
prepend_path( "PATH", pathJoin( base_dir, "bin" ) )
prepend_path( "MODULEPATH"    , "%{MODULE_PREFIX}/%{comp_fam_ver}/cray_mpich_7_2/modulefiles")
prepend_path( "MODULEPATH"    , "%{MODULE_PREFIX}/%{comp_fam_ver}/cray_mpich_7_3/modulefiles")
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

%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
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

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

