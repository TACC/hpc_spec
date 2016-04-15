#
# W. Cyrus Proctor
# 2016-03-14
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

%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

# Give the package a base name
%define pkg_base_name rosetta
%define MODULE_VAR    ROSETTA

%define maintainer_email cproctor@tacc.utexas.edu, rtevans@tacc.utexas.edu
%define rpm_group G-814534

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
#%include name-defines.inc
#%include name-defines-noreloc-home1.inc
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

Release:   3
License:   http://depts.washington.edu/ventures/UW_Technology/Express_Licenses/rosetta.php
Group:     Development/Tools
URL:       https://www.rosettacommons.org
Packager:  TACC - %{maintainer_email}
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{PACKAGE}-database
Summary: The package database RPM
Group: Development/Tools
%description package-database
This is the long description for the package database RPM...

%package %{PACKAGE}-tools
Summary: The package tools RPM
Group: Development/Tools
%description package-tools
This is the long description for the package tools RPM...

%package %{PACKAGE}-protocols-a
Summary: The package protocols part a RPM
Group: Development/Tools
%description package-protocols-a
This is the long description for the package protocol part a RPM...

%package %{PACKAGE}-protocols-b
Summary: The package protocols part b RPM
Group: Development/Tools
%description package-protocols-b
This is the long description for the package protocol part b RPM...

%package %{PACKAGE}-apps-core
Summary: The package apps and core RPM
Group: Development/Tools
%description package-apps-core
This is the long description for the package apps and core RPM...

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

###%setup -n %{pkg_base_name}-%{pkg_version}

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

ml python

# Insert further module commands

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

cd %{INSTALL_DIR}
 
export rosetta=`pwd`
export rosetta_major=%{major_version}
export rosetta_minor=%{minor_version}
export rosetta_version=${rosetta_major}.${rosetta_minor}

# Add dummy wrappers (sigh scons)
# mpicc_wrapper and mpicxx_wrapper should pointt to local_bin
##tar xvfz %{_sourcedir}/rosetta_local_bin.tar.gz
export PATH=${rosetta}/rosetta_local_bin:${PATH}
mkdir -p ${rosetta}/rosetta_local_bin
export my_mpicc=`which mpicc`
cat > ${rosetta}/rosetta_local_bin/mpicc_wrapper << EOF
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
${my_mpicc} "\$@"
EOF
chmod +x ${rosetta}/rosetta_local_bin/mpicc_wrapper
export my_mpicxx=`which mpicxx`
cat > ${rosetta}/rosetta_local_bin/mpicxx_wrapper << EOF
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
${my_mpicxx} "\$@"
EOF
chmod +x ${rosetta}/rosetta_local_bin/mpicxx_wrapper
which mpicc_wrapper
which mpicxx_wrapper
more ${my_mpicc}
more ${my_mpicxx}

export INCLUDE=${TACC_CRAY_MPT_INC}:${TACC_ICC_INC}:${CPATH}:${TACC_CRAY_DMAPP_INC}:${TACC_CRAY_PMI_INC}:${TACC_MKL_INC}:${TACC_CRAY_UGNI_INC}:${TACC_CRAY_UDREG_INC}:${TACC_CRAY_XPMEM_INC}


cd ${rosetta}
# Untar
tar xvf %{_sourcedir}/rosetta-${rosetta_version}.tgz
cd ${rosetta}/rosetta-${rosetta_version}/rosetta_source

# Create site-specific settings (intel versions)
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
        "gcc"     : [ "3.3", "3.4", "4.0", "4.1", "4.2", "4.3","4.4","4.5", "4.6","4.7", "4.8", "4.9", "*" ],
        "icc"     : [ "8.0", "8.1", "9.0", "9.1", "10.0", "10.1", "11.1", "*", "13.1", "14.0", "15.0", "16.0" ], #PBHACK
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
rm options.settings
ln -s options.settings.stampede options.settings

# Add in MKL plus some mpi wrappers (sigh scons)
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
            "cxx" : "mpicxx_wrapper -g -xAVX -axCORE-AVX2",
            "cc"  : "mpicc_wrapper -g -xAVX -axCORE-AVX2",
        },
        "removes" : {
        },
    }
}
EOF
rm -f site.settings
ln -s site.settings.stampede site.settings
cd ../../



echo -e "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"
echo -e "PATH=${PATH}"

export COMPILER=icc
export     MODE=release
export   EXTRAS=mpi,omp

./scons.py -c
rm -f .sconsign.dblite
./scons.py -j16 mode=${MODE} extras=${EXTRAS} cxx=${COMPILER} bin 


  cd /
  cp -rp %{INSTALL_DIR}/rosetta-3.5/rosetta_source/doc   $RPM_BUILD_ROOT%{INSTALL_DIR}
  cp -rp %{INSTALL_DIR}/rosetta-3.5/rosetta_source/bin   $RPM_BUILD_ROOT%{INSTALL_DIR}
  cp -rp %{INSTALL_DIR}/rosetta-3.5/rosetta_source/build $RPM_BUILD_ROOT%{INSTALL_DIR}
  cp -rp %{INSTALL_DIR}/rosetta-3.5/rosetta_database     $RPM_BUILD_ROOT%{INSTALL_DIR}
  cp -rp %{INSTALL_DIR}/rosetta-3.5/rosetta_tools        $RPM_BUILD_ROOT%{INSTALL_DIR}
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

%if "%{is_intel14}" == "1"
  %define comp_ver 14.0
%endif
%if "%{is_intel15}" == "1"
  %define comp_ver 15.0
%endif
%if "%{is_intel16}" == "1"
  %define comp_ver 16.0
%endif

%define kern_ver() %(uname -r | cut -d . -f -2)
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN, TACC_%{MODULE_VAR}_DATABASE,
TACC_%{MODULE_VAR}_TOOLS for the location of the %{MODULE_VAR} distribution,
binaries, database, and tools respectively.

NOTE: %{MODULE_VAR} is hard-coded to attempt to write temporary files within
the designated database location. This action will fail if the user sets
-database=$TACC_%{MODULE_VAR}_DATABASE. Instead, copy the database from
TACC_%{MODULE_VAR}_DATABASE to a writable location via something like:

cp -r $TACC_%{MODULE_VAR}_DATABASE $WORK/rosetta_database

Then, to run for serial jobs:

ibrun -np 1 $TACC_%{MODULE_VAR}_BIN/<rosetta-executable>.linuxiccrelease [options] -database=$WORK/rosetta_database

and, to run for parallel jobs:

ibrun -np <n> $TACC_%{MODULE_VAR}_BIN/<rosetta-executable>.mpiomp.linuxiccrelease [options] -database=$WORK/rosetta_database

where <n> is the number of MPI processes.

Version %{pkg_version}
]]

local err_message = [[
You do not have access to %{pkg_base_name} %{pkg_version}.


Users have to show their licenses and be confirmed by the %{pkg_base_name} team
that they are registered users under that license.  Send a copy of the license
to https://portal.tacc.utexas.edu/tacc-consulting.
]]

local group  = "%{rpm_group}"
local grps   = capture("groups")
local found  = false
local isRoot = tonumber(capture("id -u")) == 0
for g in grps:split("[ \n]") do
   if (g == group or isRoot)  then
      found = true
      break
    end
end


--help(help_msg)
help(help_msg)

whatis("Name: %{pkg_base_name}")
whatis("Version: %{pkg_version}")
whatis("Category: Scientific Application")
whatis("Keywords: Molecular Dynamics, Folding, Biology")
whatis("URL: http://www.rosettacommons.org/")
whatis("Description: The premier software suite for macromolecular modeling")

if (found) then
  -- Create environment variables.
  local base_dir           = "%{INSTALL_DIR}"
  local rosetta_lib        = "build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp"
  local ext_lib            = "build/external/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp"

  prepend_path( "PATH",                   pathJoin(base_dir, "bin"))
  prepend_path( "LD_LIBRARY_PATH",        pathJoin(base_dir, ext_lib))
  prepend_path( "LD_LIBRARY_PATH",        pathJoin(base_dir, rosetta_lib))
  setenv( "TACC_%{MODULE_VAR}_DIR",                base_dir)
  setenv( "TACC_%{MODULE_VAR}_DATABASE",  pathJoin(base_dir, "rosetta_database"))
  setenv( "TACC_%{MODULE_VAR}_TOOLS",     pathJoin(base_dir, "rosetta_tools"))
  setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(base_dir, "bin"))
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
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
#------------------------

%defattr(750,root,%{rpm_group},)
# RPM package contains files within these directories
%{INSTALL_DIR}
%exclude %{INSTALL_DIR}/rosetta_database
%exclude %{INSTALL_DIR}/rosetta_tools
%exclude %{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/apps
%exclude %{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/core
%exclude %{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/protocols/[a-mA-M]*
%exclude %{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/protocols/[n-zN-Z]*


%files %{PACKAGE}-database
%defattr(750,root,%{rpm_group},)
%{INSTALL_DIR}/rosetta_database

%files %{PACKAGE}-tools
%defattr(750,root,%{rpm_group},)
%{INSTALL_DIR}/rosetta_tools

%files %{PACKAGE}-protocols-a
%defattr(750,root,%{rpm_group},)
%{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/protocols/[a-mA-M]*


%files %{PACKAGE}-protocols-b
%defattr(750,root,%{rpm_group},)
%{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/protocols/[n-zN-Z]*


%files %{PACKAGE}-apps-core
%defattr(750,root,%{rpm_group},)
%{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/apps
%{INSTALL_DIR}/build/src/release/linux/%{kern_ver}/64/x86/icc/%{comp_ver}/mpi-omp/core

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE} 
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
