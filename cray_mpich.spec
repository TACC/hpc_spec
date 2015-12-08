#
# W. Cyrus Proctor
# Antonio Gomez
# Jerome Vienne
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
%define minor_version 2
%define micro_version 4

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

Release:   5
License:   GPL
Group:     Development/Tools
Packager:  TACC - carlos@tacc.utexas.edu,cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This package provides Cray Message Passing Toolkit 7.2.4, a Cray 
optimized version of hte MPICH libraries and runtime.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This modulefile provides access to the Cray Message Passing Toolkit 7.2.4

%description
This module provides access to the Cray Message Passing Toolkit 7.2.4, a Cray 
optimized version of the MPICH libraries and runtime.  

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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

%if "%{comp_fam}" == "intel"
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc << 'EOF'
#!/usr/bin/env bash
icc -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_UDREG_INC -I$TACC_CRAY_DMAPP_INC -I$TACC_CRAY_PMI_INC -L$TACC_CRAY_XPMEM_LIB -L$TACC_CRAY_UGNI_LIB -L$TACC_CRAY_UDREG_LIB -L$TACC_CRAY_PMI_LIB -L$TACC_CRAY_DMAPP_LIB -L$TACC_CRAY_MPT_LIB -ldl -lmpich_intel -lrt -lugni -lpmi -ldl -lxpmem -lpthread -ludreg "$@"
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx << 'EOF'
#!/usr/bin/env bash
icpc -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_UDREG_INC -I$TACC_CRAY_DMAPP_INC -I$TACC_CRAY_PMI_INC -L$TACC_CRAY_XPMEM_LIB -L$TACC_CRAY_UGNI_LIB -L$TACC_CRAY_UDREG_LIB -L$TACC_CRAY_PMI_LIB -L$TACC_CRAY_DMAPP_LIB -L$TACC_CRAY_MPT_LIB -ldl -lmpichcxx_intel -lmpich_intel -lrt -lugni -lpmi -ldl -lxpmem -lpthread -ludreg "$@"
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90 << 'EOF'
#!/usr/bin/env bash
ifort -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_UDREG_INC -I$TACC_CRAY_DMAPP_INC -I$TACC_CRAY_PMI_INC -L$TACC_CRAY_XPMEM_LIB -L$TACC_CRAY_UGNI_LIB -L$TACC_CRAY_UDREG_LIB -L$TACC_CRAY_PMI_LIB -L$TACC_CRAY_DMAPP_LIB -L$TACC_CRAY_MPT_LIB -ldl -lmpichf90_intel -lmpich_intel -lrt -lugni -lpmi -ldl -lxpmem -lpthread -ludreg "$@"
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77 << 'EOF'
#!/usr/bin/env bash
ifort -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
%endif
%if "%{comp_fam}" == "gcc"
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc << 'EOF'
#!/usr/bin/env bash
gcc -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_UDREG_INC -I$TACC_CRAY_DMAPP_INC -I$TACC_CRAY_PMI_INC -L$TACC_CRAY_XPMEM_LIB -L$TACC_CRAY_UGNI_LIB -L$TACC_CRAY_UDREG_LIB -L$TACC_CRAY_PMI_LIB -L$TACC_CRAY_DMAPP_LIB -L$TACC_CRAY_MPT_LIB -ldl -lmpich_gnu_49 -lrt -lugni -lpmi -ldl -lxpmem -lpthread -ludreg "$@"
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx << 'EOF'
#!/usr/bin/env bash
g++ -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_UDREG_INC -I$TACC_CRAY_DMAPP_INC -I$TACC_CRAY_PMI_INC -L$TACC_CRAY_XPMEM_LIB -L$TACC_CRAY_UGNI_LIB -L$TACC_CRAY_UDREG_LIB -L$TACC_CRAY_PMI_LIB -L$TACC_CRAY_DMAPP_LIB -L$TACC_CRAY_MPT_LIB -ldl -lmpichcxx_gnu_49 -lmpich_gnu_49 -lrt -lugni -lpmi -ldl -lxpmem -lpthread -ludreg "$@"
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90 << 'EOF'
#!/usr/bin/env bash
gfortran -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_UDREG_INC -I$TACC_CRAY_DMAPP_INC -I$TACC_CRAY_PMI_INC -L$TACC_CRAY_XPMEM_LIB -L$TACC_CRAY_UGNI_LIB -L$TACC_CRAY_UDREG_LIB -L$TACC_CRAY_PMI_LIB -L$TACC_CRAY_DMAPP_LIB -L$TACC_CRAY_MPT_LIB -ldl -lmpichf90_gnu_49 -lmpich_gnu_49 -lrt -lugni -lpmi -ldl -lxpmem -lpthread -ludreg "$@"
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77 << 'EOF'
#!/usr/bin/env bash
gfortran -I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CR
EOF
chmod ugo+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
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
This module provides access to the Cray Message Passing Toolkit 7.2.4, a Cray
optimized version of the MPICH libraries and runtime. The following commands 
will be automatically available for compiling MPI applications:

 mpicc  (C   source)
 mpicxx (C++ source)
 mpif90 (F90 source)
 mpif77 (F77 source)

If you wish to take advantage of the DMAPP optimizations for small payloads
(<=16 bytes) in MPI_Allreduce you will need to add libdmapp to your link line.
This can be achieved by simply adding "-ldmapp" to the link flags.

Version  7.2.4
]]

--help(help_msg)
help(help_msg)

whatis("Name: cray_mpich")
whatis("Version: %{pkg_version}%{dbg}")

-- Create environment variables.
%if "%{comp_fam}" == "gcc"
local base_path="/opt/cray/mpt/7.2.4/gni/mpich2-gnu/4.9"
setenv("CRAY_MPICH2_DIR","/opt/cray/mpt/7.2.4/gni/mpich2-gnu/4.9")
setenv("MPICH_DIR","/opt/cray/mpt/7.2.4/gni/mpich2-gnu/4.9")
setenv("TACC_CRAY_MPT_INC","/opt/cray/mpt/7.2.4/gni/mpich2-gnu/4.9/include")
setenv("TACC_CRAY_MPT_LIB","/opt/cray/mpt/7.2.4/gni/mpich2-gnu/4.9/lib")
prepend_path("LD_LIBRARY_PATH", "/opt/cray/mpt/7.2.4/gni/mpich2-gnu/4.9/lib")
%endif
%if "%{comp_fam}" == "intel"
local base_path="/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0"
setenv("CRAY_MPICH2_DIR","/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0")
setenv("MPICH_DIR","/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0")
setenv("TACC_CRAY_MPT_INC","/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/include")
setenv("TACC_CRAY_MPT_LIB","/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/lib")
prepend_path("LD_LIBRARY_PATH", "/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/lib")
%endif
setenv("CRAY_MPICH2_BASEDIR","/opt/cray/mpt/7.2.4/gni")
setenv("CRAY_MPICH2_ROOTDIR","/opt/cray/mpt/7.2.4")
setenv("CRAY_MPICH2_VER","7.2.4")
prepend_path("MANPATH","/opt/cray/mpt/7.2.4/gni/man/mpich2")
prepend_path("PATH","/opt/cray/mpt/7.2.4/gni/bin")
setenv("PE_CXX_PKGCONFIG_LIBS","mpichcxx")
setenv("PE_FORTRAN_PKGCONFIG_LIBS","mpichf90")
setenv("PE_INTEL_FIXED_PKGCONFIG_PATH","/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/lib/pkgconfig")
setenv("PE_MPICH_CXX_PKGCONFIG_LIBS","mpichcxx")
setenv("PE_MPICH_DIR_CRAY_DEFAULT64","64")
setenv("PE_MPICH_DIR_PGI_DEFAULT64","64")
setenv("PE_MPICH_FIXED_PRGENV","INTEL")
setenv("PE_MPICH_FORTRAN_PKGCONFIG_LIBS","mpichf90")
setenv("PE_MPICH_GENCOMPILERS_CRAY","8.3")
setenv("PE_MPICH_GENCOMPILERS_GNU","4.9 4.8")
setenv("PE_MPICH_GENCOMPILERS_PGI","15.3")
setenv("PE_MPICH_GENCOMPS_CRAY","83")
setenv("PE_MPICH_GENCOMPS_GNU","49 48")
setenv("PE_MPICH_GENCOMPS_PGI","153")
setenv("PE_MPICH_MODULE_NAME","cray-mpich")
setenv("PE_MPICH_MULTITHREADED_LIBS_multithreaded","_mt")
setenv("PE_MPICH_NV_LIBS","")
setenv("PE_MPICH_NV_LIBS_nvidia20","-lcudart")
setenv("PE_MPICH_NV_LIBS_nvidia35","-lcudart")
setenv("PE_MPICH_PKGCONFIG_LIBS","mpich")
setenv("PE_MPICH_PKGCONFIG_VARIABLES","PE_MPICH_NV_LIBS_@accelerator@:PE_MPICH_MULTITHREADED_LIBS_@multithreaded@")
setenv("PE_MPICH_TARGET_VAR_nvidia20","-lcudart")
setenv("PE_MPICH_TARGET_VAR_nvidia35","-lcudart")
setenv("PE_MPICH_VOLATILE_PKGCONFIG_PATH","/opt/cray/mpt/7.2.4/gni/mpich2-@PRGENV@@PE_MPICH_DIR_DEFAULT64@/@PE_MPICH_GENCOMPS@/lib/pkgconfig")
setenv("PE_MPICH_VOLATILE_PRGENV","CRAY GNU PGI")

--TACC env for Cray Lib/Include (added by Jerome 12:1:2015)
setenv("TACC_CRAY_XPMEM_INC","/opt/cray/xpmem/default/include")
setenv("TACC_CRAY_XPMEM_LIB","/opt/cray/xpmem/default/lib64")
setenv("TACC_CRAY_UGNI_INC","/opt/cray/ugni/default/include")
setenv("TACC_CRAY_UGNI_LIB","/opt/cray/ugni/default/lib64")
setenv("TACC_CRAY_UDREG_INC","/opt/cray/udreg/default/include")
setenv("TACC_CRAY_UDREG_LIB","/opt/cray/udreg/default/lib64")
setenv("TACC_CRAY_PMI_INC","/opt/cray/pmi/default/include")
setenv("TACC_CRAY_PMI_LIB","/opt/cray/pmi/default/lib64")
setenv("TACC_CRAY_DMAPP_INC","/opt/cray/dmapp/default/include")
setenv("TACC_CRAY_DMAPP_LIB","/opt/cray/dmapp/default/lib64")

prepend_path("PE_PKGCONFIG_LIBS","mpich")
prepend_path("PE_PKGCONFIG_PRODUCTS","PE_MPICH")


-- Update LD_LIBRARY_PATH with Cray Libs (added by Jerome 12:1:2015)
prepend_path('LD_LIBRARY_PATH',"/opt/cray/xpmem/default/lib64")
prepend_path('LD_LIBRARY_PATH',"/opt/cray/dmapp/default/lib64")
prepend_path('LD_LIBRARY_PATH',"/opt/cray/pmi/default/lib64")
prepend_path('LD_LIBRARY_PATH',"/opt/cray/ugni/default/lib64")
prepend_path('LD_LIBRARY_PATH',"/opt/cray/udreg/default/lib64")

local base_dir           = "%{INSTALL_DIR}"
prepend_path("PATH", pathJoin(base_dir, "bin"))
prepend_path( "MODULEPATH"    , "%{MODULE_PREFIX}/%{comp_fam_ver}/cray_mpich_7_2/modulefiles")
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

