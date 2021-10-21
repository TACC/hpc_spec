# Si Liu
# 2021-09-30

# rpmbuild -bb --clean --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_7' remora-1.8.4.spec 2>&1 | tee remora-1.8.4_i19_r2.log
# rpmbuild -bb --clean --define 'is_intel18 1' --define 'is_impi 1' --define 'mpiV 18_5' remora-1.8.4.spec 2>&1 | tee remora-1.8.4_i18_r1.log

# rpmbuild -bb --clean --define 'is_intel19 1' --define 'is_mvapich2 1' --define 'mpiV 2_3' remora-1.8.4.spec 2>&1 | tee remora-1.8.4_i19_mv2_r1.log
# rpmbuild -bb --clean --define 'is_intel18 1' --define 'is_mvapich2 1' --define 'mpiV 2_3' remora-1.8.4.spec 2>&1 | tee remora-1.8.4_i18_mv2_r1.log

#                    r=/admin/build/admin/rpms/frontera/RPMS/x86_64
# rpm -hiv --nodeps $r/tacc-remora-intel19-impi19_0-package-1.8.4-2.el7.x86_64.rpm
# rpm -hiv --nodeps $r/tacc-remora-intel19-impi19_0-modulefile-1.8.4-2.el7.x86_64.rpm

#
# Si Liu (siliu@tacc.utexas.edu)
# Kent Milfeld (milfeld@tacc.utexas.edu)
# Carlos Rosales-Fernandez (carlos@tacc.utexas.edu)
# Antonio Gomez (agomez@tacc.utexas.edu)

# Latest version 1.8.5

# 2020-10-19  version 1.8.4
#   Bug Fixes, Coeff of Variation reported for MPI.
#   Default reporting for gpu ndoes, REMORA_CUDA=0 turns off
#   Cleaned up some title in plots
# 2019-04-25
#   Bug Fixes, version 1.8.3
#   Remove gpu, temperature, power, and others that don't work at TACC 
#   Maybe fix temp and power for 1.8.5
# 2018-08-13
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
%define micro_version 5

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
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
Packager:  TACC - siliu@tacc.utexas.edu
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

  # %{pkg_base_name}-%{pkg_version}.tar.gz  is empty
  # get latest version from git

%setup -n %{pkg_base_name}-%{pkg_version}
  cd ..
  ls -la %{pkg_base_name}-%{pkg_version}
  rm -rf %{pkg_base_name}-%{pkg_version}
  git clone https://github.com/tacc/remora.git
  mv remora %{pkg_base_name}-%{pkg_version}

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

#module purge
module purge
ml intel/19.1.1 impi/19.0.9 
ml TACC

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
#sed -i 's/pip/#pip/g' ./install.sh

REMORA_INSTALL_PREFIX=%{INSTALL_DIR} ./install.sh

sed -i '/dvs,IO/d'                  %{INSTALL_DIR}/bin/config/modules
#sed -i '/gpu,MEMORY/d'              %{INSTALL_DIR}/bin/config/modules
sed -i '/power,POWER/d'             %{INSTALL_DIR}/bin/config/modules
sed -i '/temperature,TEMPERATURE/d' %{INSTALL_DIR}/bin/config/modules
sed -i '/network,NETWORK/d'         %{INSTALL_DIR}/bin/config/modules

#module load python
#pip install blockdiag --target=%{INSTALL_DIR}/python


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
#SBATCH -N 2
#SBATCH -n 16
#SBATCH -A my_project

remora ibrun my_parallel_program [arguments]

---------------------------------------
...
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -A my_project
remora ./my_program [arguments]

---------------------------------------

REMORA will create a set of folders with a number of files that contain
the values for the parameters previously introduced.

REMORA will also create a set of HTML files with the results plotted for
an easier analysis. There is an HTML index file (remora_summary.html) in 
the main results folder that contains links to the different results. 
Tar up the directory and transfer it to your own machine to visualize 
the google plots of the data. Just open the html index page in your 
browser by double clicking the index.

The following environment variables control the behaviour of the tool:

  - REMORA_PERIOD  - How often memory usage is checked. Default
                     is 10 seconds. (integer, 1=lowest value)
  - REMORA_VERBOSE - Verbose mode will save all information to
                     a file. Default is 0 (off).
  - REMORA_MODE    - FULL for all stats (default),
                     BASIC for memory and cpu only.
  - REMORA_CUDA    - Set to 0 to turn off gpu data collection on 
                     nodes that have GPUs.
  - REMORA_TMPDIR  - Directory for intermediate files. Default
                     is the remora output directory.
  - REMORA_PLOT_RESULTS - Set to 0 to turn of plot generation.

    remora --help  - to see these environmental control variables

The remora module also defines the REMORA_BIN environment variables,
and TACC_REMORA_DIR/LIB/INC/DOC the location of the REMORA distribution, 
libraries, include files, and documents respectively.

To generate a summary report after a crash use:

   remora_post_crash <JOBID>

Documentation:
https://github.com/TACC/remora/blob/master/docs/remora_user_guide.pdf
]]

help(help_message,"\n")

whatis("Name: Remora")
whatis("Version: 1.8.4")
whatis("Category: Profiling/Tools ")
whatis("Keywords: Tools, Profiling, Resources")
whatis("Description: REsource MOnitoring for Remote Applications")
whatis("URL: https://github.com/TACC/remora")

-- Create environment variables.
local remora_dir           = "%{INSTALL_DIR}"

family("remora")
prepend_path(    "PATH",                pathJoin(remora_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(remora_dir, "lib"))

setenv( "TACC_REMORA_DIR",       remora_dir)
setenv( "TACC_REMORA_INC",       pathJoin(remora_dir, "include"))
setenv( "TACC_REMORA_LIB",       pathJoin(remora_dir, "lib"))
setenv( "TACC_REMORA_DOC",       pathJoin(remora_dir, "docs"))
setenv( "REMORA_BIN",            pathJoin(remora_dir, "bin"))
setenv( "REMORA_PERIOD",    "10")
setenv( "REMORA_MODE",    "FULL")
setenv( "REMORA_VERBOSE",    "0")

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
