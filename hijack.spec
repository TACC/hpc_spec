#
# W. Cyrus Proctor
# 2015-11-20
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
%define pkg_base_name hijack
%define MODULE_VAR    HIJACK

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-hidden.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   2
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
Hijack Cray-MPICH shared-object libraries

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
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichcxx_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpichcxx.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichf90_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpichf90.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpich_intel.so    $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpich.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpich_intel.so    $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpich.so.12
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpich_intel.so    $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpi_dbg.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichf90_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpifort.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichf90_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpifort.so.12
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichcxx_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpigc4.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpichf90_intel.so $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpigf.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpich_intel.so    $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpi.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpich_intel.so    $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpi.so.12
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpl.so            $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpl.so
ln -s /opt/cray/mpt/7.2.4/gni/mpich2-INTEL/140/lib/libmpl.so            $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libopa.so

ln -s /opt/apps/intel16/impi/5.1.1/impi/5.1.1.109/lib64/libmpigi.a      $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/libmpigi.a

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
Hijack Cray-MPICH Shared-Object Libraries.
]]

--help(help_msg)
help(help_msg)

whatis("Name:Hijack")
whatis("Version: %{pkg_version}%{dbg}")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  #### DO not check hidden modulefiles
  ####%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

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

