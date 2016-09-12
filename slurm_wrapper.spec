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
%define pkg_base_name slurm_wrapper
%define MODULE_VAR    SLURM_WRAPPER

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
Wrap SLURM commands to point users to user guide information.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Wrap SLURM commands to point users to user guide information.

%description
Wrap SLURM commands to point users to user guide information.

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
cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/slurm_wrapper << "EOF"
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
eprintf "You have invoked an SLURM job scheduler-specific command:\n"
eprintf "  $0\n"
eprintf "To use this command, please issue either:\n"
eprintf "\n"
eprintf "                       ${G}module load TACC${NC}\n"
eprintf "\n"
eprintf "or:\n"
eprintf "\n"
eprintf "                   ${G}module load TACC-largemem${NC}\n"
eprintf "\n"
eprintf "and try again. For more information on appropriate module usage,\n"
eprintf "please visit our user guide here:\n"
eprintf "${G}https://portal.tacc.utexas.edu/user-guides/lonestar5${NC}\n"
printf "=%.0s" {1..85}
printf "\n"
printf "\n"
exit ${one}

EOF
chmod a+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/slurm_wrapper

# Executables taken from SLURM bin directory.
# Executables commented out are redundant with other wrappers.
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/generate_pbs_nodefile
#ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/mpiexec
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/pbsnodes
#ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qalter
#ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qdel
#ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qhold
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qrerun
#ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qrls
#ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qstat
#ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/qsub
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sacct
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sacctmgr
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/salloc
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sattach
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sbatch
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sbcast
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/scancel
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/scontrol
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sdiag
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sgather
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sinfo
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sjobexitmod
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sjstat
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/smap
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sprio
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/squeue
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sreport
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/srun
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sshare
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sstat
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/strigger
ln -s %{INSTALL_DIR}/bin/slurm_wrapper $RPM_BUILD_ROOT/opt/apps/tacc/bin/sview

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
# Executables taken from SLURM bin directory.
# Executables commented out are redundant with other wrappers.
/opt/apps/tacc/bin/generate_pbs_nodefile
#/opt/apps/tacc/bin/mpiexec
/opt/apps/tacc/bin/pbsnodes
#/opt/apps/tacc/bin/qalter
#/opt/apps/tacc/bin/qdel
#/opt/apps/tacc/bin/qhold
/opt/apps/tacc/bin/qrerun
#/opt/apps/tacc/bin/qrls
#/opt/apps/tacc/bin/qstat
#/opt/apps/tacc/bin/qsub
/opt/apps/tacc/bin/sacct
/opt/apps/tacc/bin/sacctmgr
/opt/apps/tacc/bin/salloc
/opt/apps/tacc/bin/sattach
/opt/apps/tacc/bin/sbatch
/opt/apps/tacc/bin/sbcast
/opt/apps/tacc/bin/scancel
/opt/apps/tacc/bin/scontrol
/opt/apps/tacc/bin/sdiag
/opt/apps/tacc/bin/sgather
/opt/apps/tacc/bin/sinfo
/opt/apps/tacc/bin/sjobexitmod
/opt/apps/tacc/bin/sjstat
/opt/apps/tacc/bin/smap
/opt/apps/tacc/bin/sprio
/opt/apps/tacc/bin/squeue
/opt/apps/tacc/bin/sreport
/opt/apps/tacc/bin/srun
/opt/apps/tacc/bin/sshare
/opt/apps/tacc/bin/sstat
/opt/apps/tacc/bin/strigger
/opt/apps/tacc/bin/sview


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

