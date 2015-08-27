#
# W. Cyrus Proctor
# 2015-08-26
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
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
%define pkg_base_name rosetta
%define MODULE_VAR    ROSETTA

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 5
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
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
License:   http://depts.washington.edu/ventures/UW_Technology/Express_Licenses/rosetta.php
Group:     Molecular Dynamics
URL:       https://www.rosettacommons.org
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
Packager:  TACC - cproctor@tacc.utexas.edu, rtevans@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%define intel_major   %{nil}

%if "%{is_intel15}" == "1"
  %define intel_major 15.0
%endif
%if "%{is_intel14}" == "1"
  %define intel_major 14.0
%endif

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
The Rosetta software suite includes algorithms for
computational modeling and analysis of protein structures.


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
module load TACC
module load %{comp_module}
module load mvapich2
module load python
module load scons
module list

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

########################################  
export rosetta=`pwd`
export rosetta_install=%{INSTALL_DIR}
export ncores=8
########################################  

export rosetta_major=%{major_version}
export rosetta_minor=%{minor_version}
export rosetta_version=${rosetta_major}.${rosetta_minor}

cd ${rosetta}
cp %{_sourcedir}/rosetta-${rosetta_version}.tgz ${rosetta}
tar xvf rosetta-${rosetta_version}.tgz
cd rosetta-${rosetta_version}/rosetta_source

cd tools/build
cat > options.settings.stampede << EOF
# (c) Copyright Rosetta Commons Member Institutions.
# (c) This file is part of the Rosetta software suite and is made available under license.
# (c) The Rosetta software is developed by the contributing members of the Rosetta Commons.
# (c) For more information, see http://www.rosettacommons.org. Questions about this can be
# (c) addressed to University of Washington UW TechTransfer, email: license@u.washington.edu.

# Supported options
options = {

    "cxx" : {
        "gcc"     : [ "3.3", "3.4", "4.0", "4.1", "4.2", "4.3","4.4","4.5", "4.6","4.7", "*" ],
        "icc"     : [ "8.0", "8.1", "9.0", "9.1", "10.0", "10.1", "11.1", "*", "13.1", "14.0", "15.0" ], #PBHACK
        "msvc"    : [ "7.0", "7.1", "8.0", "8.1", "*" ],
        "xlc"     : [ "7.0", "8.0", "9.0", "XL", "*" ],
        "clang"   : [ "1.7", "2.1", "2.0", "2.8", "2.9", "3.0", "3.3", "4.0", "3.0-6ubuntu3", "4.1", "4.2", "*" ],
    },

    "os" : {
        "linux"   : [ "2.6", "*"],
        "windows" : [ "2000", "XP", "Vista", "*" ],
        "macos"   : [ "10.4", "*" ],
        "cygwin"  : [ "*" ],
        "*"       : [ "*" ],
    },

    "arch" : {
        # The following doesn't distinguish between x64 and Itanium.
        # "intel" : [ "32", "64", "*" ]
        "x86"     : [ "32", "64", "*" ],
        "ia64"    : [ "64", "*" ],
        # XXX: It's not clear if "amd" is a meaningful category
        "amd"     : [ "32", "64", "*" ],
        "ppc"     : [ "32", "64", "*" ],
        "ppc64"     : [ "64" ],
        "power4"  : [ "32", "64", "*" ],
        "*"       : [ "*" ],
    },

    "mode" : [
        "debug",
        "release",
        "release_debug",
        "profile",
        "coverage",
        "pyrosetta",
        "pyrosetta_debug",
        "warnings_as_errors",
    ],

    "cat" : [
        "src",
        "external",
        "test",
        "doc",
    ],

   # "binary" : [
   #     "program",              # Executable
   #     "static",               # Static library (archive)
   #     "shared"                # Dynamic library (dll)
   # ],

   "extras" : [
        # Enable BOINC.  Used by rosetta@home
        "boinc",
        
        # Build documentation quickly but without graphs (don't use dot)
        "fastdocs",
        
        # Build documentation with a full call graph (takes _forever_)
        "fulldocs",
        
        # Enable the (experimental?) graphical GUI
        "graphics",
        
        # Enable the use of the Message Passing Interface
        "mpi",
        
        # # Enable pre-compiled headers.  Experimental: speeds up build.
        # "precompile",
        
        # Enable runtime error checking
        "runtimecheck",
        
        # Build so that valgrind can follow the memory use.
        # Valgrind normally works fine with most executables but not
        # with static builds, which we are doing.
        "valgrind",
        
        # Build using static linking.
        "static",
        
        # Add -pg flag for use with gprof.
        "gprof",
        
        # Use the GCOV code coverage tool (only for GCC compiler).
        "gcov",
        
        # Build with floats rather than doubles.
        "rosetta_float",

        # Build with Boost libraries.
        "boost",

        # Enable OpenMP
        "omp",

        #enable mysql database support
        "mysql",

        #enable postgres database support
        "postgres",

        # Build with CUDA
        "cuda",

        # Build with OpenCL
        "opencl",

        # Build boost MPI and serialization dependent code (requires these libraries to be installed in /usr/local/lib)
        "boost_mpi",

        # Build using link-time optimization. Include whole program optimization as well
        "lto",

        # Build with Boost thread library
        "boost_thread",

        # Enable APBS integration
        "apbs",
    ],


    # Log debugging output

    "log" : [
        "environment",
        "options",
        "platform",
        "projects",
        "settings",
        "targets",
        "toplevel",
    ],

}
EOF
rm -f options.settings
ln -s options.settings.stampede options.settings

cat > site.settings.stampede <<EOF
# -*- mode:python;indent-tabs-mode:nil;show-trailing-whitespace:t; -*-
#
# Copy this file into site.settings:
#
#   cp site.settings.template site.settings
#
# and customize to fit your site's environment
# DO NOT make changes to this template
# DO NOT try and check in site.settings
# (c) Copyright Rosetta Commons Member Institutions.
# (c) This file is part of the Rosetta software suite and is made available under license.
# (c) The Rosetta software is developed by the contributing members of the Rosetta Commons.
# (c) For more information, see http://www.rosettacommons.org. Questions about this can be
# (c) addressed to University of Washington UW TechTransfer, email: license@u.washington.edu.


# Settings here are added to the combined build settings, after all basic
# settings, to allow you to override anything you need to.  They can in turn
# be overriden by user settings and project settings respectively.
#
# Typically you want to prepend to one of the settings listed to expand your
# paths, but you can also append, override, or remove settings.
#
# NOTE: At some point this file will allow you to have multiple site settings
# to select between.  For now there is only the "site" settings.
import os

settings = {
    "site" : {
        "prepends" : {
            # Location of standard and system binaries
            "program_path" : os.environ["PATH"].split(":"),
            "library_path" : os.environ["LD_LIBRARY_PATH"].split(":"),
            "include_path" : os.environ["INCLUDE"].split(":"),
        },
        "appends" : {
            "flags" : {
                "compile" : ["mkl"],
                "link" : ["mkl"],
                "warn" : [ "wd1684", "wd592" ]
            },
        },
        "overrides" : {
            "cxx" : "mpicxx",
            "cc"  : "mpicc",
        },
        "removes" : {
        },
    }
}
EOF
rm -f site.settings
ln -s site.settings.stampede site.settings
cd ../../


COMPILER=icc

echo -e "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"
echo -e "PATH=${PATH}"

MODE=release
EXTRAS=mpi,omp

./scons.py -c
rm -f .sconsign.dblite
./scons.py -j ${ncores} mode=${MODE} extras=${EXTRAS} cxx=${COMPILER} bin 

cd ${rosetta}
mkdir -p ${rosetta_install}
mv ${rosetta}/rosetta-${rosetta_version}/rosetta_source/bin   ${rosetta_install}
mv ${rosetta}/rosetta-${rosetta_version}/rosetta_source/build ${rosetta_install}
mv ${rosetta}/rosetta-${rosetta_version}/rosetta_database     ${rosetta_install}
rm -rf ${rosetta}/rosetta-${rosetta_version}
cd ${rosetta_install}/bin

# Get rid of all rpaths set on the binaries
# This is easier than modifying the nightmare
# that is SCons Rosetta.
for file in `ls -1`; do 
  echo $file 
  chrpath -d $file
done
  

  if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  fi
  
  cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  cd /
  umount %{INSTALL_DIR}

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
help(
[[
The %{MODULE_VAR} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_DATABASE, TACC_%{MODULE_VAR}_BIN, for the
location of the %{MODULE_VAR} distribution,  databases, binaries, respectively.

NOTE: %{MODULE_VAR} is hard-coded to attempt to write temporary files within
the designated database location. This action will fail if the user sets
-database=TACC_%{MODULE_VAR}_DATABASE. Instead, copy the database from
TACC_%{MODULE_VAR}_DATABASE to a writable location via something like:

cp -r $TACC_%{MODULE_VAR}_DATABASE $WORK/rosetta_database

Then, to run:

$TACC_%{MODULE_VAR}_BIN/<rosetta-executable>.mpiomp.linuxiccrelease [options] -database=$WORK/rosetta_database

Version %{version}
]]
)

local err_message = [[
You do not have access to Rosetta 3.5!

Users have to show their licenses and be confirmed by the
TACC team that they are registered users under that license.
Please provide a copy of the license to rtevans@tacc.utexas.edu
or to cproctor@tacc.utexas.edu
]]

local group  = "G-814534"
local grps   = capture("groups")
local found  = false
local isRoot = tonumber(capture("id -u")) == 0
local isBuild = tonumber(capture("id -u")) == 500
for g in grps:split("[ \n]") do
  if (g == group or isRoot or isBuild)  then
    found = true
    break
  end
end

whatis("Name: Rosetta")
whatis("Version: %{version}")
whatis("Category: Scientific Application")
whatis("Keywords: Molecular Dynamics, Folding, Biology")
whatis("URL: http://www.rosettacommons.org/")
whatis("Description: The premier software suite for macromolecular modeling")

if (found) then
  local base_dir                              ="%{INSTALL_DIR}"
  prepend_path("PATH",                        pathJoin(base_dir, "bin"))
  prepend_path("LD_LIBRARY_PATH",             pathJoin(base_dir, "build/src/release/linux/2.6/64/x86/icc/%{intel_major}/omp-mpi"))
  prepend_path("LD_LIBRARY_PATH",             pathJoin(base_dir, "build/external/release/linux/2.6/64/x86/icc/%{intel_major}/omp-mpi"))
  setenv (     "TACC_%{MODULE_VAR}_DIR",      base_dir)
  setenv (     "TACC_%{MODULE_VAR}_DATABASE", pathJoin(base_dir, "rosetta_database"))
  setenv (     "TACC_%{MODULE_VAR}_BIN",      pathJoin(base_dir, "bin"))
else
  LmodError(err_message,"\n")
end

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
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

