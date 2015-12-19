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
%define pkg_base_name TACC
%define MODULE_VAR    TACC

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
#### Note the cray_world addition to separate the cray_world from tacc_world in /opt/apps
%define MODULE_DIR      %{MODULE_PREFIX}/cray_world/%{MODULE_SUFFIX}
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
# hacked for reasonable name WCP 2015-12-03
Name:      tacc-cray_env_base_modules
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   4
License:   GPL
Group:     Module Magic
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
Welcome to the Cray Module way!

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
# Nothing to do!

# Insert necessary module commands
# None to have!

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

  # Nothing to see here!

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
#### Note modulefile name is only version number with no .lua for tmod
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
proc ModulesHelp { } {
puts stderr "The TACC modulefile defines the default paths and environment"
puts stderr "variables needed to use the local Cray software and utilities"
puts stderr "available, placing them after the vendor-supplied"
puts stderr "paths in PATH and MANPATH.:"
}

proc inMPath { path } {
    global env
    if { ! [file exists $path] } {
       return 0
    }
    if {[info exists env(MODULEPATH)]} {
       set separator ":"
       foreach dir [split $env(MODULEPATH) $separator] {
         if { $dir == $path } {
           return 1
         }
       }
    } 
    return 0
}

setenv ESWRAP_LOGIN login0

if [module-info mode load] {
     if { ! [inMPath /opt/modulefiles] } {
        module use   /opt/modulefiles
     }
     if { ! [inMPath /opt/cray/ari/modulefiles] } {
        module use   /opt/cray/ari/modulefiles
     }
     if { [file exists /opt/cray/ari/modulefiles/switch] } {
        module load switch
     }
     ### WCP 2015-12-01 Don't load Base-opts if you want typical compute module env
     #if { [file exists /opt/modulefiles/Base-opts] } {
     #   module load Base-opts
     #}

     if { ! [inMPath /opt/cray/craype/default/modulefiles] } {
        module use   /opt/cray/craype/default/modulefiles
     }
     module load craype-network-aries PrgEnv-intel cray-mpich craype-haswell

     ### WCP 2015-12-01 Don't load cray slurm -- see tacc slurm below
     #if { [file exists /opt/modulefiles/slurm] } {
     #   module load slurm
     #}
}

if [ module-info mode remove ] {
     #module del slurm craype-haswell cray-mpich PrgEnv-intel craype-network-aries 
     module del craype-haswell cray-mpich PrgEnv-intel craype-network-aries 
     #module del Base-opts switch
     module del switch
}

### WCP 2015-12-01 Add tacc slurm information instead.
set base_dir "/opt/slurm/default"
append-path PATH             "$base_dir/bin"
## append-path LD_LIBRARY_PATH  "$base_dir/lib"
prepend-path MANPATH         "$base_dir/share/man"
prepend-path MANPATH         "/usr/share/man"
prepend-path PERL5LIB        "$base_dir/lib/perl5/site_perl/5.10.0/x86_64-linux-thread-multi"
## setenv SINFO_FORMAT          {%20P %5a %.10l %16F}
## setenv SQUEUE_FORMAT         {%.18i %.9P %.9j %.8u %.2t %.10M %.6D %R}
## setenv SQUEUE_SORT           {-t,e,S}

setenv TACC_SLURM_DIR        "$base_dir"
setenv TACC_SLURM_INC        "$base_dir/include"
setenv TACC_SLURM_LIB        "$base_dir/lib"
setenv TACC_SLURM_BIN        "$base_dir/bin"

# "Wimmy Wham Wham Wozzle!" -- Slurms MacKenzie


prepend-path PATH /opt/apps/tacc/bin 10


EOF
  

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

