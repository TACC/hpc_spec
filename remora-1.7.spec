#
# remora-1.7.spec
# 2016-12-02
# Carlos Rosales (carlos@tacc.utexas.edu)
# Antonio Gomez  (agomez@tacc.utexas.edu)
# See http://github.com/TACC/remora

Summary:  REMORA. REsource MOnitoring of Remote Applications
Name:     remora
Version:  1.7
Release:  1
License:  MIT
Group:    Profiling/Tools
Source:   %{name}-%{version}.tar.gz
Packager: TACC - carlos@tacc.utexas.edu, agomez@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%package -n tacc-%{name}
Summary:  REMORA. REsource MOnitoring of Remote Applications
Group:    Profiling/Tools

%description
%description -n tacc-%{name}
REMORA provides an easy to use profiler that collects several different statistics for a running job:
        - Memory usage
        - CPU usage
        - I/O load
        - ...

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/scalasca-1.1
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
# Use mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}

# Start with a clean environment
%include system-load.inc
#if [ -f "$BASH_ENV" ]; then
#  . $BASH_ENV
##  . /etc/tacc/tacc_functions
#  module purge
#  clearMT
#  export MODULEPATH=/opt/apps/tools/modulefiles:/opt/apps/modulefiles
#fi

module purge
module load TACC

# Build remora
sed -i 's/pip/#pip/g' ./install.sh
REMORA_INSTALL_PREFIX=%{INSTALL_DIR} ./install.sh

module load python
pip install blockdiag --target=%{INSTALL_DIR}/python


%install
mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount                                   %{INSTALL_DIR}


# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
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

remora_post_crash JOBID

]]


whatis("Name: Remora")
whatis("Version: 1.5.0")
whatis("Category: Profiling/Tools ")
whatis("Keywords: Tools, Profiling, Resources")
whatis("Description: REsource MOnitoring for Remote Applications")
whatis("URL: https://github.com/TACC/remora")

help(help_message,"\n")

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


## %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n tacc-%{name}
# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the source files from /tmp/BUILD
rm -rf /tmp/BUILD/%{name}-%{version}

# Remove the installation files now that the RPM has been generated
rm -rf /var/tmp/%{name}-%{version}-buildroot

rm -rf $RPM_BUILD_ROOT
