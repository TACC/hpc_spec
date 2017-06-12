# Carlos Rosales-Fernandez (carlos@tacc.utexas.edu)
# 2017-05-22
# Modified for Stampede 2 deployment and avx512
# This version is patch 2 with the missing fortran hearders
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
%define pkg_base_name remora
%define MODULE_VAR    REMORA

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 8
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
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

Release:   1%{?dist}
License:   MIT
Group:     Profiling/Tools
URL:       https://github.com/TACC/remora
Packager:  TACC - carlos@tacc.utexas.edu
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
REMORA provides an easy to use profiler that collects several different statistics for a running job:
        - Memory usage
        - CPU usage
        - I/O load
        - ...

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

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
%include compiler-load.inc
# Load MPI Library
%include mpi-load.inc

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


# Mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}

export CFLAGS="%{TACC_OPT}"
export LDFLAGS="%{TACC_OPT}"

## sed -i 's/icc/#icc/g' ./install.sh
sed -i 's/pip/#pip/g' ./install.sh
REMORA_INSTALL_PREFIX=%{INSTALL_DIR} ./install.sh

module load python
pip install blockdiag --target=%{INSTALL_DIR}/python


mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount                                   %{INSTALL_DIR}

  
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
local help_message=[[
REMORA is an easy to use profiler that allows users to get information
regarding their jobs. The information collected by the tool includes:
    - Memory usage
    - CPU usage
    - I/O load (Lustre,DVS)
    - NUMA memory
    - Network topology

To use the tool, simply modify your batch script and include 'remora' before
your executable or ibrun.

Examples:
...
#SBATCH -n 16
#SBATCH -A my_project

remora ibrun my_parallel_program [arguments]

---------------------------------------
...
#SBATCH -n 1
#SBATCH -A my_project
remora ./my_program [arguments]

---------------------------------------

remora will create a folder with a number of files that contain the values
for the parameters previously introduced.

It is also possibly to get plots of those files for an easier analysis.
Load a python module ('module load python') and use the tool 'remora_post'.
Within the batch script, 'remora_post' does not need any parameter. From
the login node, you can cd to the location that contains the remora_JOBID
folder. Once there run 'remora_post -j JOBID'.

The following environment variables control the behaviour of the tool:

  - REMORA_PERIOD  - How often memory usage is checked. Default
                     is 10 seconds.
  - REMORA_VERBOSE - Verbose mode will save all information to
                     a file. Default is 0 (off).
  - REMORA_MODE    - FULL for all stats, BASIC for memory and cpu only.
                     Default if FULL.
  - REMORA_TMPDIR  - Directory for intermediate files. Default is the
                     remora output directory.

The remora module also defines the following environment variables:
REMORA_DIR, REMORA_LIB, REMORA_INC and REMORA_BIN for the location
of the REMORA distribution, libraries, include files, and tools respectively.

To generate a summary report after a crash use:

remora_post_crash <JOBID>
]]

help(help_message,"\n")

whatis("Name: Remora")
whatis("Version: 1.7.0")
whatis("Category: Profiling/Tools ")
whatis("Keywords: Tools, Profiling, Resources")
whatis("Description: REsource MOnitoring for Remote Applications")
whatis("URL: https://github.com/TACC/remora")

-- Create environment variables.
local remora_dir           = "%{INSTALL_DIR}"

family("remora")
prepend_path(    "PATH",                pathJoin(remora_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(remora_dir, "lib"))
prepend_path(    "PYTHONPATH",      pathJoin(remora_dir, "/python"))
setenv( "TACC_REMORA_DIR",       remora_dir)
setenv( "TACC_REMORA_INC",       pathJoin(remora_dir, "include"))
setenv( "TACC_REMORA_LIB",       pathJoin(remora_dir, "lib"))
setenv( "REMORA_BIN",       pathJoin(remora_dir, "bin"))
setenv( "REMORA_PERIOD",    "10")
setenv( "REMORA_MODE",  "FULL")
setenv( "REMORA_VERBOSE",   "0")

EOF

# Version File
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

