# Amit Ruhela
# 2020-06-29
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
%define pkg_base_name itac
%define MODULE_VAR    ITAC

# Create some macros (spec file variables)
%define major_version 19
%define minor_version 1
%define micro_version 1

%define lib_version 2020

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define underscore_version %{major_version}_%{minor_version}

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

Release:   1%{?dist}
License:   proprietary
Group:     PROFILER
URL:       https://software.intel.com/en-us/intel-trace-analyzer
Packager:  TACC - jgarcia@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
This is specifically an rpm for the Intel itac modulefile
used on Stampede2

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
This is specifically an rpm for the Intel itac modulefile
used on Stampede2

%description
This is specifically an rpm for the Intel itac modulefile
used on Stampede2

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
local base        = "/opt"
local versionloc  = "2020.1.217"

whatis( "Name: itac" )
whatis( "Version: %{version}" )
whatis( "Category: System Software" )
whatis( "Keywords: System, Utility, Tools" )
whatis( "Description: Intel Trace Analyzer and Collector" )
whatis( "URL: https://software.intel.com/en-us/intel-trace-analyzer" )

local itac_full   = pathJoin( "intel", "itac_%{lib_version}" )
local relocatedir = pathJoin(  base,    itac_full      )
local arch64dir   = pathJoin( relocatedir, "intel64"   )

local addlibs     = "-ldwarf -lelf -lvtunwind -lm -lpthread"

setenv(       "VT_ROOT",                relocatedir                               )
setenv(       "VT_ARCH",               "intel64"                                  )

setenv(       "VT_MPI",                "impi4"                                    )
setenv(       "VT_LIB_DIR",             pathJoin( arch64dir, "lib"     )          )
setenv(       "VT_SLIB_DIR",            pathJoin( arch64dir, "slib"    )          )
setenv(       "VT_ADD_LIBS",            addlibs                                   )

prepend_path( "LD_LIBRARY_PATH",        pathJoin( arch64dir, "slib"    )          )
prepend_path( "PATH",                   pathJoin( arch64dir, "bin"     )          )
prepend_path( "INTEL_LICENSE_FILE",    "/opt/intel/licenses:/root/intel/licenses" )
prepend_path( "MANPATH",                pathJoin( relocatedir, "man"   )          )


setenv(       "MPS_INTEL_LIBITTNOTIFY64",
                                       "libmps.so"                                )
setenv(       "MPS_STAT_DIR_POSTFIX",  "_%D-%T"                                   )
setenv(       "MPS_LD_PRELOAD",        "libmps.so"                                )
setenv(       "MPS_STAT_ENABLE_IDLE_VAL",
                                       "1"                                        )
setenv(       "MPS_STAT_LEVEL",        "5"                                        )
setenv(       "MPS_KMP_FORKJOIN_FRAMES_MODE",
                                       "3"                                        )
setenv(       "MPS_STAT_ENABLE_IDLE",  "I_MPI_PVAR_IDLE"                          )
setenv(       "MPS_TOOL_ROOT",          relocatedir                               )
setenv(       "MPS_STAT_MESSAGES",     "1"                                        )

setenv(       "TACC_ITAC_DIR",          relocatedir                               )
setenv(       "TACC_ITAC_BIN",          pathJoin( arch64dir, "bin"     )          )
setenv(       "TACC_ITAC_INC",          pathJoin( arch64dir, "include" )          )
setenv(       "TACC_ITAC_LIB",          pathJoin( arch64dir, "lib"     )          )
setenv(       "TACC_ITAC_SLIB",         pathJoin( arch64dir, "slib"    )          )

help(
[[

Intel Analyzer and Collector (ITAC) is a graphical tool for understanding
MPI application behavior, quickly finding bottlenecks, improving
correctness, and achieving high performance.

For detailed info, consult the extensive documentation in
$TACC_ITAC_DIR/doc or online at
software.intel.com/en-us/intel-trace-analyzer/documentation.

ITAC is easiest to use with the Intel compiler and IMPI.
See Intel documentation for information regarding using ITAC with
other MPI stacks.

Using ITAC with the Intel Compiler and IMPI
*******************************************

To build your MPI application for ITAC and IMPI, load an intel
compiler module and impi module, then compile and link with
the trace switch; for example...

  $ module load intel/19.1.1
  $ module load impi/19.0.7
  $ module load itac/19.1.1
  $ mpicc -trace mycode.c -o mycode

To run an collection with ITAC, launch your MPI job with sbatch, srun,
or idev as desired.  Include the trace switch in your call to ibrun.
For example...

  $ ibrun -trace mycode

  ITAC will generate trace files in the current directory.   These will
  include multiple files for each MPI task, and a master file named
  mycode.stf (here "mycode" represents the name of your executable).

To analyze your collection, start a VNC or X11 session, then execute:

  $ traceanalyzer mycode.stf  # replace "mycode" with your executable

For instructions regarding MPI Performance Snapshot (MPS), see
$TACC_ITAC_DIR/doc/MPI_Perf_Snapshot_User_Guide.pdf.

NOTE: an easy way to start a VNC session is through the TACC vis portal
at https://vis.tacc.utexas.edu.

SPECIAL CIRCUMSTANCES
*********************

Here is a (partial) list of special circumstances; see the Intel docs for
more info:

  -- MPI stacks other than IMPI
  -- C++ programs that use the MPI C++ API instead of the C API
  -- Programs that make explicit calls to the ITAC API
  -- MPI programs with multi-threading (hybrid programs)

ENVIRONMENT VARIABLES
*********************

This module defines the following additional environment variables:

   VT_ARCH           host architecture (intel64)
   VT_ROOT           ITAC top-level directory
   VT_MPI            MPI type ("impi4" even with newer versions of IMPI)

   VT_ADD_LIBS       list of required libraries
   VT_LIB_DIR        directory containing static libs
   VT_SLIB_DIR       directory containing shared libs

   MPS_*             nine variables of this form needed by MPS

   TACC_ITAC_DIR     TACC equivalent of VT_ROOT
   TACC_ITAC_BIN     directory containing ITAC executables
   TACC_ITAC_INC     directory containing ITAC include files
   TACC_ITAC_LIB     TACC equivalent of VT_LIB_DIR
   TACC_ITAC_SLIB    TACC equivalent of VT_SLIB_DIR

The modulefile also prepends to PATH, CLASSPATH, LD_LIBRARY_PATH,
and a variety of other environment variables.

To see the exact effect of loading the module, execute "module show itac".

Version %{version} (file version %{version})
]]
)

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile
  ### don't check the hidden one!
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

