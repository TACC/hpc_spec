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
%define pkg_base_name cmpich
%define MODULE_VAR    CMPICH

# Create some macros (spec file variables)
%define major_version 7
%define minor_version 2
%define micro_version 4

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
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

Release:   1
License:   GPL
Group:     Development/Tools
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

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
Cray-MPICH wrappers

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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
 
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc << 'EOF'
#!/usr/bin/env bash
icc -I/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/include -L/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/lib -lmpich_intel $@
EOF
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx << 'EOF'
#!/usr/bin/env bash
icpc -I/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/include -L/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/lib -lmpichcxx_intel $@
EOF
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90 << 'EOF'
#!/usr/bin/env bash
ifort -I/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/include -L/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0/lib -lmpichf90_intel $@
EOF

ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpich_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpi_dbg.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichcxx_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpigc4.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichf90_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpigf.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpich_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpi.so
  

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
Cray-MPICH Wrappers.
]]

--help(help_msg)
help(help_msg)

whatis("Name: cmpich")
whatis("Version: %{pkg_version}%{dbg}")

-- Create environment variables.
setenv("CRAY_MPICH2_BASEDIR","/opt/cray/mpt/7.2.4/gni")
setenv("CRAY_MPICH2_DIR","/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0")
setenv("CRAY_MPICH2_ROOTDIR","/opt/cray/mpt/7.2.4")
setenv("CRAY_MPICH2_VER","7.2.4")
prepend_path("MANPATH","/opt/cray/mpt/7.2.4/gni/man/mpich2")
setenv("MPICH_DIR","/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0")
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
prepend_path("PE_PKGCONFIG_LIBS","mpich")
prepend_path("PE_PKGCONFIG_PRODUCTS","PE_MPICH")

local base_dir           = "%{INSTALL_DIR}"
prepend_path("PATH", pathJoin(base_dir, "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin(base_dir, "lib"))
prepend_path( "MODULEPATH"            , "%{MODULE_PREFIX}/%{comp_fam_version}/cmpich_7_2/modulefiles")
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

