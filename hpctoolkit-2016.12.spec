#
# W. Cyrus Proctor
# Antonio Gomez
# Damon McDougall
# 2017-05-30
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

#
# Spec file for HPCToolkit
#
Summary: HPCToolkit

# Give the package a base name
%define pkg_base_name hpctoolkit
%define MODULE_VAR    HPCTOOLKIT

# Create some macros (spec file variables)
%define major_version 2016
%define minor_version 12

%define pkg_version %{major_version}.%{minor_version}

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

Release:   2%{?dist}
License:   BSD
Group:     Applications/HPC
URL:       www.hpctoolkit.org 
Packager:  TACC - agomez@tacc.utexas.edu, cproctor@tacc.utexas.edu, dmcdougall@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Source1:   %{pkg_base_name}-externals-%{pkg_version}.tar.gz
Source2:   hpcviewer-2017.01-linux.gtk.x86_64.tgz
Source3:   hpctraceviewer-2017.01-linux.gtk.x86_64.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: The package RPM
Group: Applications/HPC
%description package
HPCToolkit is an integrated suite of tools for measurement and analysis of program performance on computers ranging from multicore desktop systems to the nation's largest supercomputers. By using statistical sampling of timers and hardware performance counters, HPCToolkit collects accurate measurements of a program's work, resource consumption, and inefficiency and attributes them to the full calling context in which they occur.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
HPCToolkit is an integrated suite of tools for measurement and analysis of program performance on computers ranging from multicore desktop systems to the nation's largest supercomputers. By using statistical sampling of timers and hardware performance counters, HPCToolkit collects accurate measurements of a program's work, resource consumption, and inefficiency and attributes them to the full calling context in which they occur.

%description
HPCToolkit is an integrated suite of tools for measurement and analysis of program performance on computers ranging from multicore desktop systems to the nation's largest supercomputers. By using statistical sampling of timers and hardware performance counters, HPCToolkit collects accurate measurements of a program's work, resource consumption, and inefficiency and attributes them to the full calling context in which they occur.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-release-%{pkg_version}
%setup -D -T -n %{pkg_base_name}-release-%{pkg_version} -a 1
%setup -D -T -n %{pkg_base_name}-release-%{pkg_version} -a 2
%setup -D -T -n %{pkg_base_name}-release-%{pkg_version} -a 3

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
module load papi

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  
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

## Notes on hpctoolkit configure options
## --without-libunwind   Identify correct source lines in optimized code 
## --enable-demangling   I don't think this has any effect
## --with-papi           Top lelvel PAPI directory

cd %{pkg_base_name}-externals-release-%{pkg_version}
mkdir BUILD
mkdir INSTALL
cd BUILD
export current=`pwd`
../configure CC=gcc CXX=g++ \
             --without-libunwind \
             --enable-demangling \
             --prefix=%{INSTALL_DIR}
#             --prefix=$current/../INSTALL \

make -j56
make DESTDIR=$RPM_BUILD_ROOT install

cd ../../  # Now in the dir: hpctoolkit-release-%{pkg_version}
mkdir BUILD
cd BUILD
../configure CC=gcc CXX=g++ \
             --without-libunwind \
             --enable-demangling \
             --prefix=%{INSTALL_DIR} \
             --with-externals=%{INSTALL_DIR} \
             --with-papi=${TACC_PAPI_DIR}
#              --with-externals=../%{pkg_base_name}-externals-release-%{pkg_version}/INSTALL \

make -j56
make DESTDIR=$RPM_BUILD_ROOT install

cd ../hpcviewer
sed -i 's/grep -i java/grep openjdk/g' ./install
./install $RPM_BUILD_ROOT/%{INSTALL_DIR}
sed -i 's/grep -i java/grep openjdk/g' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/hpcviewer

cd ../hpctraceviewer
# sed -i 's/java -version/java -Xmx1G -version/g' ./install
sed -i 's/grep -i java/grep openjdk/g' ./install
./install $RPM_BUILD_ROOT/%{INSTALL_DIR}
sed -i 's/grep -i java/grep openjdk/g' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/hpctraceviewer
  
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
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

To use hpctoolkit compile your source with debugging flags:

icc   -g -debug inline-debug-info <source.c>
mpicc -g -debug inline-debug-info <mpi_source.c>

Then run your code in the batch system using hpcrun:

(serial/threaded): hpcrun <executable>
(mpi/hybrid):      ibrun hpcrun <executable>

This will create a directory with the collected measurements.
Once the run is complete obtain the static structure of the program :

hpcstruct <executable>

Then form the databasei form the measurements:

(serial/threaded): hpcprof     -S <executable.hpcstruct> <measurementDirName>
(mpi/hybrid):      hpcprof-mpi -S <executable.hpcstruct> <measurementDirName>

This will create a database directory that can then be examined:

hpcviewer <databaseDirName>

For more details go to http://www.hpctoolkit.org

Version %{pkg_version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: HPCToolkit")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: application,HPC ")
whatis("Keywords: HPC, profiling, parallel, performance")
whatis("URL: http://www.hpctoolkit.org")
whatis("Description: Profiler")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local hpct_dir          = "%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(hpct_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_DIR",       hpct_dir)
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(hpct_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(hpct_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(hpct_dir, "bin"))
EOF
  
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
