#
# Antonio Gomez/Carlos Rosales
# 2015-08-24
#

Summary: REMORA. REsource MOnitoring of Remote Applications

# Give the package a base name
%define pkg_base_name remora

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


#######################################
### TOGGLE ON/OFF WITH COMMENT ########
#######################################
# Include for basic macro definitions
%include rpm-dir.inc                  
# Include if compiler specific
#%include compiler-defines.inc
# Include if mpi wrapper specific
#%include mpi-defines.inc
#######################################
#######################################
#######################################


# Compiler Specific?
%if "%{?comp_fam_ver}"
  # Compiler *and* MPI Specific
  %if "%{?mpi_fam_ver}"
    %define pkg_name       %{pkg_base_name}-%{comp_fam_ver}-%{mpi_fam_ver}
    %define MODULE_SUFFIX  %{comp_fam_ver}/%{mpi_fam_ver}/modulefiles/%{pkg_base_name}
    %define INSTALL_SUFFIX %{comp_fam_ver}/%{mpi_fam_ver}/%{pkg_base_name}/%{pkg_version}
  # Compiler Specific Only
  %else
    %define pkg_name       %{pkg_base_name}-%{comp_fam_ver}
    %define MODULE_SUFFIX  %{comp_fam_ver}/modulefiles/%{pkg_base_name}
    %define INSTALL_SUFFIX %{comp_fam_ver}/%{pkg_base_name}/%{pkg_version}
  %endif
# Compiler Non-specific
%else
  %define pkg_name       %{pkg_base_name}
  %define MODULE_SUFFIX  modulefiles/%{pkg_base_name}
  %define INSTALL_SUFFIX %{pkg_base_name}/%{pkg_version}
%endif

# SPEC File Tags
Name:      %{pkg_name}
Version:   %{pkg_version}
Release:   1
License:   GPL
Group:     Profiling/Tools
URL:       https://github.com/TACC/remora
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
Packager:  TACC - agomez@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# NOTES:
# Leave MODULE_PREFIX and INSTALL_PREFIX as /tmpmod and /tmprpm!
# These are temporary placeholders that allow for install-time
# relocation via rpm. They must be unique and *not* nested. 
# /tmpmod and /tmprpm should *never* be the final install locations.


# Module macros
%define MODULE_PREFIX   /tmpmod 
%define MODULE_DIR      %{MODULE_PREFIX}/%{MODULE_SUFFIX}
%define MODULE_VAR      REMORA
%define MODULE_FILENAME %{version}.lua

# Install macros
%define INSTALL_PREFIX  /tmprpm
%define INSTALL_DIR     %{INSTALL_PREFIX}/%{INSTALL_SUFFIX}

# Subpackage macros
%define PACKAGE             package
%define MODULEFILE          modulefile
%define BUILD_PACKAGE       %( if [ ${NO_PACKAGE:=0}    = 0 ]; then echo "1"; else echo "0"; fi )
%define BUILD_MODULEFILE    %( if [ ${NO_MODULEFILE:=0} = 0 ]; then echo "1"; else echo "0"; fi )
%define RPM_PACKAGE_NAME    %{name}-%{PACKAGE}-%{version}-%{release}
%define RPM_MODULEFILE_NAME %{name}-%{MODULEFILE}-%{version}-%{release}

#---------------------------------------
#---------------------------------------
#---------------------------------------
# Default installation prefixes
# May be overridden at install
# with:
# rpm --relocate /foo=/bar <rpm-name>.rpm 
Prefix:    %{MODULE_PREFIX}
Prefix:    %{INSTALL_PREFIX}
#---------------------------------------
#---------------------------------------
#---------------------------------------

%package %{PACKAGE}
Summary: REMORA
Group: Profiling/Tools
%description package
REMORA provides an easy to use profiler that collects several different statistics for a running job:
	- Memory usage
	- CPU usage
	- I/O load
	- ...

%package %{MODULEFILE}
Summary: REMORA modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the RPM for REMORA modulefile

%description
REMORA provides an easy to use profiler that collects several different statistics for a running job:
        - Memory usage
        - CPU usage
        - I/O load
        - ...

# NOTE:
# If creating subpackages with the %package
# or %package -n directives, be sure to have
# appropriate %files, %pre, %post, %preun and
# %postun directvies as well.

#---------------------------------------
#---------------------------------------
#---------------------------------------
%prep
#---------------------------------------
#---------------------------------------
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

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

#--------
# untar |
#--------
# Source assumed to be located in ../SOURCES
# The first call to setup untars the first source.  
# The second call untars the second source, in a subdirectory of the first. 
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory.
# -T prevents the 'default' source file from re-unpacking.  
#    If you don't have this, the default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
#%setup -n %{pkg_base_name}-%{pkg_version}       # bar
#%setup -n %{some_macro}-%{version} -T -D -a 1  # foo


#---------------------------------------
#---------------------------------------
#---------------------------------------
%build
#---------------------------------------
#---------------------------------------
#---------------------------------------



#---------------------------------------
#---------------------------------------
#---------------------------------------
%install
#---------------------------------------
#---------------------------------------
#---------------------------------------

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"


# -----------------
# Package Section |
# -----------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  rm -rf $RPM_BUILD_ROOT
  rm -rf remora
  git clone https://github.com/TACC/remora/
  cd remora
  git checkout %{major_version}.%{minor_version}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  mkdir -p %{INSTALL_DIR}/bin
  cp remora* %{INSTALL_DIR}/bin

  mkdir -p %{INSTALL_DIR}/lib
  mkdir -p %{INSTALL_DIR}/include

  cd extra
  tar -xzf confuse-2.7.tar.gz
  cd confuse-2.7
  ./configure --prefix=%{INSTALL_DIR}/
  make
  make install

  cd ..
  tar -xzf libev-4.20.tar.gz
  cd libev-4.20
  ./configure --prefix=%{INSTALL_DIR}/
  make
  make install
 
  cd ..
  
  gcc mic_affinity.c -o %{INSTALL_DIR}/bin/ma

  cd xltop
  cd source
  export XLTOP_PORT=9901
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{INSTALL_DIR}/lib
  ./autogen.sh
  ./configure CFLAGS="-I%{INSTALL_DIR}/include" LDFLAGS="-L%{INSTALL_DIR}/lib -lev -lconfuse" --prefix=%{INSTALL_DIR}/
  make
  make install

  . /etc/tacc/tacc_functions
  module purge
  clearMT
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles

  module load intel
  module load python
  pip install blockdiag --target=%{INSTALL_DIR}/python


  mkdir -p              $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------



#------------------
# Modules Section |
#------------------

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
# Use the %{INSTALL_DIR} macro for package path locations inside the modulefile!
# Use the %{MODULE_DIR} macro for modulefile path locations inside the modulefile!
# The cat command and 'EOF' must be left justified to work correctly.
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
%{MODULE_VAR} is an easy to use profiler that allows user to get information regarding
their jobs. The information collected by the tool includes:
	- Memory usage
	- CPU usage
	- Lustre usage
	- I/O load
	- NUMA memory
	- Network topology

To use the tool, simply modify your batch script and include 'remora' before your
executable or ibrun.

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

remora will create a folder with a number of files that contain the values for the parameters previously introduced.

It is also possibly to get plots of those files for an easier analysis. Use the tool 'remora_post'. Within the 
batch script, 'remora_post' does not need any parameter. From the login node, you can cd to the location that contains
the jobstats_JOBID folder. Once there run 'jobstatsplot -j JOBID'.

The following environment variables control the behaviour of the tool:

  - TACC_%{MODULE_VAR}_PERIOD  - How often memory usage is checked. Default is 10 seconds.
  - TACC_%{MODULE_VAR}_VERBOSE - Verbose mode will save all information to a file. Default is 0 (off).
  - TACC_%{MODULE_VAR}_MODE    - FULL (default) for all stats, BASIC for memory and cpu only.


The %{MODULE_VAR} module also defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.
]]

--help(help_msg)
help(help_msg)

whatis("Name: remora")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local remora_dir           = "%{INSTALL_DIR}"

family("remora")
prepend_path(    "PATH",                pathJoin(remora_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(remora_dir, "lib"))
prepend_path(    "MODULEPATH",          "%{MODULE_PREFIX}/remora1_1/modulefiles")
prepend_path(    "PYTHONPATH",		pathJoin(remora_dir, "/python"))
setenv( "TACC_%{MODULE_VAR}_DIR",       remora_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(remora_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(remora_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(remora_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_PERIOD",    "10")
setenv( "TACC_%{MODULE_VAR}_MODE", 	"FULL")
setenv( "TACC_%{MODULE_VAR}_VERBOSE",   "0")

EOF
  
  
  #----------------
  #  version file |
  #----------------
  
# The cat command and 'EOF' must be left justified to work correctly.
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


#---------------------------------------
#---------------------------------------
#---------------------------------------
# files section
# NOTE:
# If creating subpackages with the %package
# or %package -n directives, be sure to have
# appropriate %files, %pre, %post, %preun and
# %postun directvies as well.
#---------------------------------------
#---------------------------------------
#---------------------------------------

#------------------------
#%if %{?BUILD_PACKAGE}
%files package
#------------------------

  # File attributes %defattr(<file mode>, <user>, <group>, <dir mode>)
  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
#%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  # File attributes %defattr(<file mode>, <user>, <group>, <dir mode>)
  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#---------------------------------------
#---------------------------------------
#---------------------------------------
# post section
# NOTE:
# If creating subpackages with the %package
# or %package -n directives, be sure to have
# appropriate %files, %pre, %post, %preun and
# %postun directvies as well.
#---------------------------------------
#---------------------------------------
#---------------------------------------



%post %{PACKAGE}
R='\033[1;31m'
G='\033[1;32m'
B='\033[1;34m'
W='\033[0m'
NC='\033[0m'
F='\033[0m'
printf "${F}===================================================${NC}\n"
printf "${F}||${B}MMP\"\"MM\"\"YMM   db ${W}      .g8\"\"\"bgd   .g8\"\"\"bgd  ${F}||${NC}\n"
printf "${F}||${B}P\'   MM   \`7  ;MM: ${W}   .dP\'     \`M .dP\'     \`M  ${F}||${NC}\n"
printf "${F}||${B}     MM      ,V^MM. ${W}  dM\'       \` dM\'       \`  ${F}||${NC}\n"
printf "${F}||${B}     MM     ,M  \`MM ${W}  MM          MM           ${F}||${NC}\n"
printf "${F}||${B}     MM     Ab${W}mmm${B}qMA ${R} MM.         MM.          ${F}||${NC}\n"
printf "${F}||${B}     MM    A\'     VML${R} \`Mb.     ,\' \`Mb.     ,\'  ${F}||${NC}\n"
printf "${F}||${B}   .JMML..AMA.   .AMMA.${R} \`\"bmmmd'    \`\"bmmmd\'   ${F}||${NC}\n"
printf "${F}===================================================${NC}\n"
echo "This is the %{RPM_PACKAGE_NAME} subpackage postinstall script"
# Query rpm after installation for location of canary files ---------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                       # |
  export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                    # |
  export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                     # |
  echo "Using default RPM database path:                             %{_dbpath}"                                              # |
else                                                                                                                          # |
  export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)             # |
  export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)              # |
  echo "Using user-specified RPM database path:                      ${RPM_DBPATH}"                                           # |
fi                                                                                                                            # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")              # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                # |
# -------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
echo "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       "                       > /dev/stderr # |
echo "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      "                       > /dev/stderr # |
echo "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          "                       > /dev/stderr # |
echo "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         "                       > /dev/stderr # |
if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                      # |
  echo -e "${R}ERROR: POST_INSTALL_PREFIX is currently set but null or unset"                                     > /dev/stderr # |
  echo -e "${R}ERROR: tacc_install_canary was not found"                                                          > /dev/stderr # |
  echo -e "${R}ERROR: Something is not right. Exiting!"                                                           > /dev/stderr # |
  exit -1                                                                                                                       # |
else                                                                                                                            # |
  echo "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} "                     > /dev/stderr # |
  echo "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"    > /dev/stderr # |
fi                                                                                                                              # |
if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                       # |
  echo -e "${G}POST_MODULE_PREFIX set but null or unset${NC}"                                                     > /dev/stderr # |
  echo -e "${G}Has %{RPM_MODULEFILE_NAME} been installed in this rpm database yet?${NC}"                          > /dev/stderr # |
  echo -e "${G}Install %{RPM_MODULEFILE_NAME} to automatically update %{MODULE_SUFFIX}/%{MODULE_FILENAME}${NC}"   > /dev/stderr # |
else                                                                                                                            # |
  echo "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  "                     > /dev/stderr # |
  echo "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  "    > /dev/stderr # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
  echo "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       "                     > /dev/stderr # |
  echo "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         "                     > /dev/stderr # |
  sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}               # |
  sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}                 # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
  cat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}            | \
      GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
      GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                         > /dev/stderr # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------

%post %{MODULEFILE}
R='\033[1;31m'
G='\033[1;32m'
B='\033[1;34m'
W='\033[0m'
NC='\033[0m'
F='\033[0m'
printf "${F}===================================================${NC}\n"
printf "${F}||${B}MMP\"\"MM\"\"YMM   db ${W}      .g8\"\"\"bgd   .g8\"\"\"bgd  ${F}||${NC}\n"
printf "${F}||${B}P\'   MM   \`7  ;MM: ${W}   .dP\'     \`M .dP\'     \`M  ${F}||${NC}\n"
printf "${F}||${B}     MM      ,V^MM. ${W}  dM\'       \` dM\'       \`  ${F}||${NC}\n"
printf "${F}||${B}     MM     ,M  \`MM ${W}  MM          MM           ${F}||${NC}\n"
printf "${F}||${B}     MM     Ab${W}mmm${B}qMA ${R} MM.         MM.          ${F}||${NC}\n"
printf "${F}||${B}     MM    A\'     VML${R} \`Mb.     ,\' \`Mb.     ,\'  ${F}||${NC}\n"
printf "${F}||${B}   .JMML..AMA.   .AMMA.${R} \`\"bmmmd'    \`\"bmmmd\'   ${F}||${NC}\n"
printf "${F}===================================================${NC}\n"
echo "This is the %{RPM_MODULEFILE_NAME} subpackage postinstall script"
# Query rpm after installation for location of canary files ---------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                       # |
  export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                    # |
  export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                     # |
  echo "Using default RPM database path:                             %{_dbpath}"                                              # |
else                                                                                                                          # |
  export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)             # |
  export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)              # |
  echo "Using user-specified RPM database path:                      ${RPM_DBPATH}"                                           # |
fi                                                                                                                            # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")              # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                # |
# -------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
echo "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       "                       > /dev/stderr # |
echo "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      "                       > /dev/stderr # |
echo "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          "                       > /dev/stderr # |
echo "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         "                       > /dev/stderr # |
if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                      # |
  echo -e "${G}POST_INSTALL_PREFIX is set but null or unset${NC}"                                                 > /dev/stderr # |
  echo -e "${G}Has %{RPM_PACKAGE_NAME} been installed in this rpm database yet?${NC}"                             > /dev/stderr # |
  echo -e "${G}Install %{RPM_PACKAGE_NAME} to automatically update %{MODULE_SUFFIX}/%{MODULE_FILENAME}${NC}"      > /dev/stderr # |
else                                                                                                                            # |
  echo "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} "                     > /dev/stderr # |
  echo "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"    > /dev/stderr # |
fi                                                                                                                              # |
if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                       # |
  echo -e "${R}ERROR: POST_MODULE_PREFIX is currently set but null or unset"                                      > /dev/stderr # |
  echo -e "${R}ERROR: tacc_module_canary was not found"                                                           > /dev/stderr # |
  echo -e "${R}ERROR: Something is not right. Exiting!"                                                           > /dev/stderr # |
  exit -1                                                                                                                       # |
else                                                                                                                            # |
  echo "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  "                     > /dev/stderr # |
  echo "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  "    > /dev/stderr # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
  echo "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       "                     > /dev/stderr # |
  echo "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         "                     > /dev/stderr # |
  sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}               # |
  sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}                 # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
  cat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}            | \
      GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
      GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                         > /dev/stderr # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------
#---------------------------------------
#---------------------------------------
%clean
#---------------------------------------
#---------------------------------------
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

