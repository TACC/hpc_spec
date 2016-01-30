#
# W. Cyrus Proctor
# 2015-12-01
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
%define pkg_base_name sge_wrapper
%define MODULE_VAR    SGE_WRAPPER

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
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   5
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
Wrap SGE commands to point users to user guide information.

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

# Insert necessary module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/opt/apps/tacc/bin
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

# Create generic wrapper script
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/sge_wrapper << "EOF"
#!/usr/bin/env bash

# Constants
export zero=0
export  one=1
export    R='\033[1;31m' # Red
export    G='\033[1;32m' # Green
export   NC='\033[0m'    # No Color
export  err="[ ${R}ERROR${NC} ]"

# Print functions
eprintf(){
printf "${err} $@"
}

printf "\n"
printf "=%.0s" {1..85}
printf "\n"
eprintf "You have invoked an SGE job scheduler-specific command:\n"
eprintf "  $0\n"
eprintf "Lonestar5 uses the SLURM job scheduler.\n"
eprintf "For more information on appropriate SLURM commands,\n"
eprintf "please visit our user guide here:\n"
eprintf "${G}https://portal.tacc.utexas.edu/user-guides/lonestar5${NC}\n"
printf "=%.0s" {1..85}
printf "\n"
printf "\n"
exit ${one}

EOF
chmod a+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/sge_wrapper


ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qselect  
#ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qmake    ### conflicts with Qt qmake
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qrsub    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qstat    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qrstat   
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qacct    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qquota   
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qsh      
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qping    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qtcsh    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qhost    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qconf    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qrdel    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qrsh     
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qmod     
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qhold    
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qalter   
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qresub   
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qsub     
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sgepasswd
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qdel     
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qlogin   
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qrls     
ln -s %{INSTALL_DIR}/bin/sge_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qmon     


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/




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

# Nothing to do!

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
/opt/apps/tacc/bin/qselect  
#/opt/apps/tacc/bin/qmake    ### conflicts with Qt qmake
/opt/apps/tacc/bin/qrsub    
/opt/apps/tacc/bin/qstat    
/opt/apps/tacc/bin/qrstat   
/opt/apps/tacc/bin/qacct    
/opt/apps/tacc/bin/qquota   
/opt/apps/tacc/bin/qsh      
/opt/apps/tacc/bin/qping    
/opt/apps/tacc/bin/qtcsh    
/opt/apps/tacc/bin/qhost    
/opt/apps/tacc/bin/qconf    
/opt/apps/tacc/bin/qrdel    
/opt/apps/tacc/bin/qrsh     
/opt/apps/tacc/bin/qmod     
/opt/apps/tacc/bin/qhold    
/opt/apps/tacc/bin/qalter   
/opt/apps/tacc/bin/qresub   
/opt/apps/tacc/bin/qsub     
/opt/apps/tacc/bin/sgepasswd
/opt/apps/tacc/bin/qdel     
/opt/apps/tacc/bin/qlogin   
/opt/apps/tacc/bin/qrls     
/opt/apps/tacc/bin/qmon     


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

