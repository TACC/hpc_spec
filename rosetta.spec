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

# Give the package a base name
%define pkg_base_name rosetta
%define MODULE_VAR    ROSETTA

%define maintainer_email cproctor@tacc.utexas.edu, rtevans@tacc.utexas.edu
%define rpm_group G-814534

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 7
%define build_version 2016.32.58837

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc
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
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

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

#ml cxx11
ml python
#ml scons
ml boost
#ml boost-mpi
ml hdf5
ml

%if "%{is_intel14}" == "1"
  %define comp_ver 14.0
  %define comp icc
%endif
%if "%{is_intel15}" == "1"
  %define comp_ver 15.0
  %define comp icc
%endif
%if "%{is_intel16}" == "1"
  %define comp_ver 16.0
  %define comp icc
%endif
%if "%{is_intel17}" == "1"
  %define comp_ver 17.0
  %define comp icc
%endif
%if "%{is_gcc49}" == "1"
  %define comp_ver 4.9
  %define comp gcc
%endif
%if "%{is_gcc54}" == "1"
  %define comp_ver 5.4
  %define comp gcc
%endif
%if "%{is_gcc63}" == "1"
  %define comp_ver 6.3
  %define comp gcc
%endif

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
#!/bin/bash
export PATH=${PATH}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
export I_MPI_CC=icc
${my_mpicc} "\$@"
EOF
chmod +x ${rosetta}/rosetta_local_bin/mpicc_wrapper
export my_mpicxx=`which mpicxx`
cat > ${rosetta}/rosetta_local_bin/mpicxx_wrapper << EOF
#!/bin/bash
export PATH=${PATH}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
export I_MPI_CXX=icpc
${my_mpicxx} "\$@"
EOF
chmod +x ${rosetta}/rosetta_local_bin/mpicxx_wrapper
which mpicc_wrapper
which mpicxx_wrapper
more ${my_mpicc}
more ${my_mpicxx}
${my_mpicc} -show
${my_mpicxx} -show

cd ${rosetta}
# Untar
tar xvf %{_sourcedir}/rosetta_src_${rosetta_version}_bundle.tgz
cd ${rosetta}/rosetta_src_%{build_version}_bundle/main/source

# Create site-specific settings (intel versions)
cd tools/build
cat > basic.settings.stampede << 'EOF'
# -*- mode:python;indent-tabs-mode:nil;show-trailing-whitespace:t; -*-
# (c) Copyright Rosetta Commons Member Institutions.
# (c) This file is part of the Rosetta software suite and is made available
# (c) under license.
# (c) The Rosetta software is developed by the contributing members of the
# (c) Rosetta Commons.
# (c) For more information, see http://www.rosettacommons.org.
# (c) Questions about this can be addressed to University of Washington UW
# (c) TechTransfer, email: license@u.washington.edu.

"""The settings below are combined together to create the final set of settings
for the entire build.  They are combined in the order listed below, with each
new setting potentially changing the current combination.

This system does not claim to be perfect for all situations but trying to
determine a precise order for each possible combination is combinatorially
intractable.  Thus the order here may need to be customized and note that the
system does not currently warn you if any of the current combinations doesn't
occur, to prevent lots of mostly spurious messages.

   - os
   - os, os_version
   - compiler
   - compiler, compiler_version
   - compiler, kind
   - compiler, os
   - compiler, compiler_version, os
   - compiler, os, os_version
   - compiler, compiler_version, os, os_version
   - compiler, arch
   - compiler, compiler_version, arch
   - compiler, arch, arch_size
   - compiler, compiler_version, arch, arch_size
   - compiler, os, arch, arch_size
   - compiler, mode
   - compiler, compiler_version, mode
   - compiler, os, mode
   - compiler, compiler_version, os, mode
   - compiler, arch, mode
   - compiler, compiler_version, arch, mode
   - compiler, os, arch
   - compiler, os, arch, mode
   - compiler, extra
   - compiler, os, extra
   - compiler, os, os_version, extra

There are four ways to combine settings:
   - "prepends" add the contents of the settings in front of any existing
     settings.
   - "appends" add the contents of the settings at the end of any existing
     settings.
   - "overrides" replace the existing settings with the given settings.
   - "removes" remove a particular setting from the contents (but only that
     settings, so they are more precise than an override to an empty set.)

The settings use Python syntax, and all of them are currently either strings or
lists of strings.

"""

import os, commands

shell_gcc = commands.getoutput('which gcc').split()[0]

settings = {
    "base" : {
        "overrides" : {
            # SCons starts CXXFLAGS with a reference to CCFLAGS.
            # We want the two to be separate.
            "CCFLAGS" : "",
            "CXXFLAGS" : "",
            # SCons starts with a (short) default PATH.
            # We want only what is explicitly specified here.
            "program_path" : [
                "/bin",
                "/usr/bin",
                "/usr/local/bin",
            ],
            # Leading '#' means relative to the base directory, (i.e.,
            # main/external/boinc/api, etc.)
            "include_path" : [
                "#external/boost_1_55_0",
                "#external/libxml2/include",
                "#external/",
                "#external/dbio",
                "/usr/include",
                "/usr/local/include",
            ],
            "library_path" : [
                "/usr/lib",
                "/usr/local/lib",
            ],
            "defines" : [
                "BOOST_ERROR_CODE_HEADER_ONLY",
                "BOOST_SYSTEM_NO_DEPRECATED",
        "BOOST_MATH_NO_LONG_DOUBLE_MATH_FUNCTIONS",
                "PTR_BOOST"
            ],
        },
    },


    # Set a baseline environment for supported operating systems.

    "linux" : {},

    # Note: Setting the above paths for Windows is only useful in site.settings
    # as there is no standard location for installed libraries and headers.
    "windows" : {},

    "macos" : {
        "overrides" : {
            "library_path" : [ "/usr/lib", ],
        },
    },

    "cygwin" : {  # Is this correct for Cygwin?
        "prepends" : {
            "library_path" : [ "lib/cygwin/", ],
        },
        "overrides" : {
            #"libraries" : [ "z --enable-auto-import" ],
            "flags" : {
                "link" : [
                    "lz -Xlinker --enable-auto-import -Xlinker --export-all-symbols",
                ],
                #"ld" : [ "-enable-auto-import", ],
            }
        },
    },


    # Setup the environment for compilers and compilers run with other build
    # options.

    ###########################################################################
    # GCC #####################################################################
    ###########################################################################

    "gcc" : {
        "appends" : {
            "flags" : {
                # The "isystem" items here are to tell GCC not to print warn-
                # ings from these external headers.
                "cc" : [
                    "std=c99",
                    "isystem external/boost_1_55_0/",
                    "isystem external/",
                    "isystem external/include/",
                    "isystem external/dbio/",
                ],
                "cxx" : [
                    "std=c++98",
                    "ffor-scope",
                    "isystem external/boost_1_55_0/",
                    "isystem external/",
                    "isystem external/include/",
                    "isystem external/dbio/",
                ],
                "compile" : [
                    "pipe",
                ],
                # By default, warn about everything except the use of
                # long long, which we need for certain database functionality.
                "warn" : [
                    "Wall",
                    "Wextra",
                    "pedantic",
                    "Wno-long-long",
                    "Wno-strict-aliasing",
                ],
            },
        },
        "removes" : {
             "flags" : {
                 "warn" : [
                     # We turn off warnings as errors for Python build
                     # only because the automatic Python interface wrapping
                     # can introduce warnings.
                     "Werror",
                     "-Werror=maybe-uninitialized",
                 ],
             },
        },

    },

    "gcc, *" : {  # default version for installation
        "appends" : {
            "version" : [ ],
        },
    },

    "gcc, 3.3" : {
        "appends" : {
            "version" : [ "3", "3" ],
        },
    },

    "gcc, 3.4" : {
        "appends" : {
            "version" : [ "3", "4" ],
            "flags" : {
                # These flags likely cause memory exhaustion on whatever plat-
                # form they're active.
                #"compile" : [
                #    "-param inline-unit-growth=1000",
                #    "-param large-function-growth=50000"
                #],
            },
        },
    },

    "gcc, 4.0" : {
        "appends" : {
            "version" : [ "4", "0" ],
            "flags" : {
                # These flags causes memory exhaustion during compiling on
                # MacOS 10.5.
                #"compile" : [
                #    "-param inline-unit-growth=1000",
                #    "-param large-function-growth=50000"
                #],
            },
        },
    },

    "gcc, 4.1" : {
        "appends" : {
            "version" : [ "4", "1" ],
            "flags" : {
                # These flags causes memory exhaustion during compiling on the
                # test server.
                #"compile" : [
                #    "-param inline-unit-growth=1000",
                #    "-param large-function-growth=50000"
                #],
            },
        },
        "overrides" : {
            "flags" : {
                "cc" : [ "std=c99" ],
                "cxx" : [
                    "std=c++98",
                    "ffor-scope",
                ],
                "compile" : [
                    "pipe",
                ],
                "warn" : [],
            },
        },
    },

    "gcc, 4.4" : {
        "appends" : {
            "flags" : {
                "warn" : [ "Wno-uninitialized", ],
            },
        },
    },


    # OSs & architecures ######################################################

    "gcc, linux" : {
        "appends" : {
            "flags" : { },
        },
    },

    # These names are actually Fedora specific.
    # We need to determine names on SuSE, Debian, etc.
    "gcc, 3.3, linux" : {
        "overrides" : {
            "cc" : "gcc33",
            "cxx" : "g++33",
        },
    },

    "gcc, 3.4, linux" : {
        "overrides" : {
            "cc" : "gcc34",
            "cxx" : "g++34",
        },
    },

    "gcc, 4.0, linux" : {
        "overrides" : {
            "cc" : "gcc40",
            "cxx" : "g++40",
        },
    },

    "gcc, 4.1, linux" : {
        "overrides" : {
            "cc" : "gcc",
            "cxx" : "g++",
        },
    },

    "gcc, 4.3, linux" : {
        "overrides" : {
            "cc" : "gcc-4.3",
            "cxx" : "g++-4.3",
        },
    },

    "gcc, 4.5, linux" : {
        "overrides" : {
            "cc" : "gcc-4.5",
            "cxx" : "g++-4.5",
        },
    },
    "gcc, 4.6, linux" : {
        "overrides" : {
            "cc" : "gcc-4.6",
            "cxx": "g++-4.6",
        },
    },


    "gcc, macos" : {
        "appends" : {
            "flags" : {
                "warn"  : [ ],
                "link" : [ "Wl,-stack_size,4000000,-stack_addr,0xc0000000" ],
                # Change 'abspath' to 'file' to use DYLD_LIBRARY_PATH
                # environment variable
                "shlink" : [ "install_name ${TARGET.abspath}" ],
            },
        },
        "removes" : {
            "flags" : {
                "link" : [ "$__RPATH" ],
                "cxx" : [ "std=c++98" ],
                "shlink" : [ "$LINKFLAGS" ],
                "warn" : [
                    # For some reason, despite using isystem for boost,
                    # Mac.gcc.debug mode is throwing an error from an unused
                    # param in boost!
                    "Werror=unused-parameter",
                    # There is at least one variable only used on non-Macs.
                    "Werror=unused-variable",
                    # These don't exist in the Mac version of GCC used by the
                    # test server:
                    "Werror=enum-compare",
                    "Werror=type-limits",
                    "Werror=ignored-qualifiers",
                ],
            },
        },
    },

    "gcc, 3.3, macos" : {
        "overrides" : {
            "cc" : "gcc-3.3",
            "cxx" : "g++-3.3",
        },
    },

    "gcc, 3.4, macos" : {
        "overrides" : {
            "cc" : "gcc-3.4",
            "cxx" : "g++-3.4",
        },
    },

    "gcc, 4.0, macos" : {
        "overrides" : {
            "cc" : "gcc-4.0",
            "cxx" : "g++-4.0",
        },
        "removes" : {
            "flags" :  {
                "cxx" : [ "std=c++98" ],
            },
        },
    },

    "gcc, 4.1, macos" : {
        "overrides" : {
            "cc" : "gcc-4.1",
            "cxx" : "g++-4.1",
        },
    },

    "gcc, 4.2, macos" : {
        "overrides" : {
            "cc" : "gcc-4.2",
            "cxx" : "g++-4.2",
        },
    },

    "gcc, 4.2, macos, 10.7" : {
        "overrides" : {
            "cc" : "llvm-gcc-4.2",
            "cxx" : "llvm-g++-4.2",
        },
    },

    "gcc, 4.2, macos, 10.8" : {
        "overrides" : {
            "cc" : "llvm-gcc-4.2",
            "cxx" : "llvm-g++-4.2",
        },
    },


    "gcc, cygwin" : {
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98" ],
            },
        },
    },


    "gcc, x86, 32" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "malign-double",
                    "march=pentium4"
                ],
            },
        },
    },

    "gcc, x86, 64" : {
        "appends" : {
            "flags" : {
                # XXX: march=k8 is (?) the default.  There may be a speedup
                # XXX: with =nocona on Intel EM64T or =opteron on Opteron.
                "compile" : [
        "march=core2",
        "mtune=generic",
          ],
            },
        },
    },


    "gcc, macos, x86" : {
        "removes" : {
            "flags" : {
                "compile"   : [ "malign-double", "march=pentium4" ],
            },
        },
    },

    "gcc, macos, x86, 32" : {  # Mac Intel 32-bit
        "appends" : {
            "flags" : {
                "compile" : [
                    "m32",
                    "march=prescott",
                    "mtune=generic"
                ],
                "shlink" : [ "m32" ],
                "link" : [ "m32" ],
            },
        },
    },

    "gcc, macos, x86, 64" : {  # Mac Intel 64-bit
        "appends" : {
            "flags" : {
                "compile" : [
                    "m64",
                    "march=nocona",
                    "mtune=generic"
                ],
                "shlink" : [ "m64" ],
                "link" : [
                    "m64",
                    "Wl,-stack_size,4000000"
                ],
            },
        },
        "removes" : {
            "flags" : {
                "link"  : [ "Wl,-stack_size,4000000,-stack_addr,0xc0000000" ],
            },
        },
    },


    "gcc, ia64" : {
        "appends" : {
            "flags" : {
                "compile"  : [
                    "fprefetch-loop-arrays",
                    "mtune=itanium2"
                ],
            },
        },
    },


    "gcc, amd" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "malign-double",
                    "march=athlon"
                ],
            },
        },
    },


    # modes ###################################################################

    "gcc, debug" : {
        "appends" : {
            "flags" : {
                "compile" : [ "O0" ],
                "mode" : [
                    "g",
                    "ggdb",
                    "ffloat-store"
                    # "fstack-check"
                ],
            },
        },
    },

    "gcc, release" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "O3",
                    "ffast-math",
                    "funroll-loops",
                    "finline-functions",
                    "finline-limit=20000",
                    "s"
                ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
                ],
            },
            "defines" : [ "NDEBUG" ],
        },
    },

    "gcc, 4.4, release" : {
        "removes" : {
            "flags" : {
                "compile" : [ "finline-limit=20000" ],
            },
        },
        "appends" : {
            "flags" : {
                 # A bug in gcc4.4 that has not yet been fixed requires that
                 # this inline limit be removed.
                "compile" : [ "finline-limit=487" ],
            },
        },
    },

    "gcc, release_debug" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "O3",
                    "ffast-math",
                    "funroll-loops",
                    "finline-functions",
                    "finline-limit=20000",
                    "s",
                ],
                "mode" : [
                    "g",
                    "ggdb",
                    "ffloat-store",
                    "fno-omit-frame-pointer", # Keep frame pointer information, to help with stack traces
                    # "fstack-check",
                ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
                ],
            },
            #"defines" : [ "NDEBUG" ],
        },
    },

    "gcc, 4.9, release_debug" : {
        "appends" : {
            "flags" : {
                 # disable the strict-overflow warning produced by DynamicIndexRange.hh
                "warn" : [ "Wstrict-overflow=0" ],
            },
        },
    },

    "gcc, release_debug_no_symbols" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "O3",
                    "ffast-math",
                    "funroll-loops",
                    "finline-functions",
                    "finline-limit=20000",
                    "s",
        "ffloat-store", # "mfpmath=sse", "msse2",  WARNING WARNING WARNING this flags SIGNIFICANTLY degrade performance and only used to improved stability for integration tests, they should NEVER be enabled for production code
                ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
                ],
            },
            #"defines" : [ "NDEBUG" ],
        },
    },

    "gcc, profile" : {
        "appends" : {
            "flags" : {
                "compile"  : [
                    "O3",
                    "ffast-math",
                    "funroll-loops",
                    "finline-functions",
                    "finline-limit=20000"
                ],
                # These flags enable the actual profiling.
                # -g allows line by line profiling.
                "mode" : [
                    "g",
                    "ggdb",
                    "pg"
                ],
                "link" : [
                    "g",
                    "ggdb",
                    "pg"
                ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
                ],
            },
            "defines" : [ "NDEBUG" ],
        },
    },

    "gcc, pyrosetta" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "O3",
                    "ffast-math",
                    "funroll-loops",
                    "finline-functions",
                    "finline-limit=20000",
                    "s"
                ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter"
                ],
            },
            "defines" : [
                "NDEBUG",
                "PYROSETTA",
                "PYROSETTA3",
                'BOOST_THREAD_DONT_USE_CHRONO',
            ],
        },
    },

    "gcc, 4.4, pyrosetta" : {
        "removes" : {
            "flags" : {
                "compile" : [ "finline-limit=20000" ],
            },
        },
        "appends" : {
            "flags" : {
                # A bug in gcc4.4 that has not yet been fixed requires that
                # this inline limit be removed.
                "compile" : [ "finline-limit=487" ],
            },
        },
    },

    "gcc, pyrosetta_debug" : {
        "appends" : {
            "flags" : {
                #"compile" : [
                #    "O3",
                #    "ffast-math",
                #    "funroll-loops",
                #    "finline-functions",
                #    "finline-limit=20000",
                #    "s"
                #],
                "compile" : [ "O0" ],  # <-- real debug... do we need it?
                "mode" : [
                    "g",
                    "ggdb",
                    "ffloat-store"
                ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn"  : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter"
                ],
            },
            "defines" : [
                "PYROSETTA",
                "PYROSETTA3",
                'BOOST_THREAD_DONT_USE_CHRONO'
            ],
        },
    },

    "gcc, macos, pyrosetta" : {
        "appends" : {
           "libraries"  : [ "stdc++", ],
  },
        "removes" : {
            "flags" : {
                "warn" : [
                    # We turn off warnings as errors for Python build
                    # only because the automatic Python interface wrapping
                    # can introduce warnings.
                    "Werror",
                ],
            },
        },
        "overrides" : {  # for Mac PyRosetta builds we use GCC from user environment instead of system one
            "cc" :  shell_gcc,
            "cxx" : shell_gcc,
        },
    },
    "gcc, macos, pyrosetta_debug" : {
        "appends" : {
           "libraries"  : [ "stdc++", ],
  },
        "removes" : {
            "flags" : {
                "warn" : [
                    # We turn off warnings as errors for Python build
                    # only because the automatic Python interface wrapping
                    # can introduce warnings.
                    "Werror",
                ],
            },
        },
        "overrides" : { # for Mac PyRosetta builds we use GCC from user environment instead of system one
            "cc" :  shell_gcc,
            "cxx" : shell_gcc,
        },
    },

    # cats ####################################################################

    "gcc, src" : {
        "appends" : {
            "flags" : {
                # We can't have exceptions for efficiency reasons.
                #"compile" : [ "fno-exceptions" ],
            },
        },
    },

    "gcc, test" : {
        "appends" : {
            "flags" : {
                # The "isystem" items here are to tell gcc to not print warn-
                # ings from this external header.
                "cc" : [ "isystem external/cxxtest/"],
                "cxx" : [ "isystem external/cxxtest/"],
            },
        },
        "removes" : {
            "flags" : {
                #"compile" : [ "fno-exceptions" ],
            },
        },
    },

    "gcc, doc" : {
        # Default Doxygen settings go here, if they differ from the defaults
        # created by the Doxygen builder.
    },


    # extras ##################################################################

    "gcc, boinc" : {
        "appends" : {
            # Leading '#' means relative to the base directory, (i.e.,
            # main/external/boinc/api, etc.)
            "include_path"  : [
                "#external/boinc/api",
                "#external/boinc",
                "#external/boinc/lib",
                "#external/boinc/zip",
            ],
            # This file was only needed when building BOINC from source
            # (instead of using libs).
            #"includes" : [ "external/boinc/config.h" ],
            # The library_path must be defined depending on platform -- e.g.,
            # see gcc, macos, boinc (below).
            "libraries" : [
                "boinc_api",
                "boinc",
                "boinc_zip"
            ],
            "defines" : [ "BOINC" ],
            "flags" : {
                "compile" : [ "pthread" ],
                "warn" : [ "Wno-write-strings", "Wno-uninitialized", ],
            },
        },
        "removes" : {
            "flags" : {
                # BOINC headers won't work with -pedantic.
                "warn" : [ "pedantic" ],
                "compile" : [
                    "march=pentium4",
                    "march=athlon",
                    "mtune=itanium2"
                ],
            },
        },
    },

    "gcc, linux, boinc" : {
        "appends" : {
            "include_path"  : [
                "#external",
                "#external/dbio",
                "/usr/include/GL"
            ],
            "libraries" : [
                "boinc_graphics2",
            ],
            "library_path" : [
                "#external/boinc/api",
                "#external/boinc/lib",
                "#external/boinc/zip",
            ],
            "defines"  : [ "BOINC_GRAPHICS" ],
            "flags" : {
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
        #"Wno-unused-but-set-variable",
                ],
                "link" : [ "Wl,-Bdynamic -lglut -lGL -lGLU -Wl,--dynamic-linker=/lib64/ld-linux-x86-64.so.2"  ],
            },
        },
    },

    "gcc, macos, boinc" : {
        "appends" : {
            "libraries" : [ "boinc_graphics2" ],
            "library_path" : [
                "#external/boinc/mac_build/build/Deployment",
                "#external/boinc/zip",
                "/usr/X11R6/lib"
            ],
            "include_path" : [
                "#external",
                "#external/dbio"
            ],
            "defines" : [
                "MAC",
                "BOINC_GRAPHICS",
                "GL_GRAPHICS"
            ],
            "flags" : {
                "link" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "framework Cocoa"
                ],
                "shlink" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "framework Cocoa"
                ],
            },
        },
        "removes" : {
            "flags" : {
                "compile" : [ "pthread" ],
            },
        },
    },

    # This target is somewhat sketchy in its implementation.
    # It ought to be done as a separate executable.
    # Deprecated.  If it isn't used within a certain time frame it will go away.
    # Does this need to be linux only?
    "gcc, linux, graphics" : {
        "appends" : {
            "libraries" : [
                "pthread",
                "GL",
                "GLU",
                "glut"
            ],
            "defines" : [ "GL_GRAPHICS" ],
        },
    },

    "gcc, hdf5" : {
        "appends" : {
            "defines" : [ "USEHDF5" ],
            "libraries" : [ "libhdf5", "libhdf5_cpp", "libhdf5_hl", "libhdf5_hl_cpp"],
        },
    },

    "gcc, 4.3, mpi" : {
        "appends" : {
            "defines"       : [ "USEMPI" ],
        },
    },

    "gcc, macos, graphics" : {
        "appends" : {
            "include_path" : [ "/usr/X11R6/include" ],
            "library_path" : [ "/usr/X11R6/lib" ],
            "defines" : [
                "GL_GRAPHICS",
                "MAC"
            ],
            "flags" : {
                "link" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "dylib_file /System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib"
                ],
                "shlink" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "dylib_file /System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib"
                ],
            },
        },
    },

    # Below is a fix for compiling with extras=graphics on OSX 10.5.  For more
    # information, see Apple's page here:
    # http://developer.apple.com/qa/qa2007/qa1567.html
    # tex - 8/8/2008
    #"gcc, macos, 9.4, graphics" : {
    #    "appends" : {
    #        "flags" : {
    #            "compile" : [
    #                 "-dylib_file /system/library/frameworks/opengl.framework/versions/a/libraries/libgl.dylib:/system/library/frameworks/opengl.framework/versions/a/libraries/libgl.dylib"
    #            ],
    #        },
    #    },
    #},


    "gcc, mpi" : {
        "appends" : {
            "defines" : [ "USEMPI" ],
        },
        "overrides" : {
            "cc" : "mpicc",
            "cxx" : "mpiCC",
        },
    },

    "gcc, 4.3, mpi" : {
        "appends" : {
            "defines" : [ "USEMPI" ],
        },
        "appends" : {
            "cc" : " -V 4.3",
            "cxx" : " -V 4.3",
        },
    },

    "gcc, ia64, mpi" : {
        "appends" : {
            "flags" : {
                "compile" : [
                   "O3",
                   "ip",
                   "Qoption,c,-ip_ninl_max_stats=50000"
                ],
            },
        },
    },

    "gcc, macos, mpi" : {
        "appends" : {
            "defines" : [ "USEMPI" ],
        },
        "overrides" : {
            "cc" : "mpicc",
            "cxx" : "mpicxx",
        },
    },


    "gcc, linux, static" : {
        "appends" : {
            "flags" : {
                "link" : [ "static" ],
            },
        },
    },


    "gcc, gprof" : {
        "appends" : {
            "flags" : {
                "link" : [ "pg" ],
                "compile" : [ "pg" ],
            },
        },
    },


    "gcc, gcov" : {  # settings for gcov, code coverage tool for GCC
        "appends" : {
            "flags" : {
                "compile" : [
                    "fprofile-arcs",
                    "ftest-coverage"
                ],
                "link" : [ "-coverage" ],
            },
        },
    },


    "gcc, rosetta_float" : {
        "appends" : {
            "defines" : [ "ROSETTA_FLOAT" ],
        },
    },


    "gcc, omp" : {
        #"overrides" : {
        #    "cc" : "gcc4",
        #    "cxx" : "g++4",
        #},
        "appends" : {
            "defines" : [
                "USE_OPENMP",
                "MULTI_THREADED"
            ],
            "flags" : {
                "compile" : [ "fopenmp" ],
            },
            "libraries" : [ "gomp" ],
        },
    },


    "gcc, python" : {
        "appends" : {
            "include_path" : [ "#external/include/python2.7" ],
            "defines" : [ "WITH_PYTHON=1" ],
            "libraries" : [
                "python2.7",
                "dl",
                "pthread",
                "util"
            ],
        },
        "removes" : {
            "flags" : {
                "warn" : [
                    # We turn off warnings as errors for Python build
                    # only because the automatic Python interface wrapping
                    # can introduce warnings.
                    "Werror",
                ],
            },
        },
    },


    "gcc, mysql" : {
        "appends" : {
            "defines" : [ "USEMYSQL" ],
            "library_path" : [ "/usr/lib64/mysql" ],
        },
    },


    "gcc, postgres" : {
        "appends" : {
            "defines" : [ "USEPOSTGRES" ],
        },
    },


    "gcc, opencl" : {
        "appends" : {
            "include_path" : [
                "/opt/AMDAPP/include",
                "/opt/AMDAPP/include/CL",
                "/opt/AMDAPP/lib/x86",
                "/opt/AMDAPP/lib/x86_64",
            ],
            "libraries" : [ "OpenCL" ],
            "library_path" : [ "/opt/AMDAPP/lib/x86_64", ],
            "defines" : [ "USEOPENCL" ],
        },
    },

    "gcc, macos, opencl" : {
        "appends" : {
            "include_path" : [
                "/Developer/GPU\ Computing/OpenCL/common/inc",
                "/Developer/GPU\ Computing/OpenCL/common/inc/CL",
                "/Developer/GPU\ Computing/shared/inc",
                "/Developer-3.2.6/GPU\ Computing/OpenCL/common/inc",
                "/Developer-3.2.6/GPU\ Computing/OpenCL/common/inc/CL",
                "/Developer-3.2.6/GPU\ Computing/shared/inc"
            ],
            #"include_path" : [\
            #    "/Developer-3.2.6/GPU\ Computing/OpenCL/common/inc",
            #    "/Developer-3.2.6/GPU\ Computing/OpenCL/common/inc/CL",
            #    "/Developer-3.2.6/GPU\ Computing/shared/inc"
            #],
            #"include_path" : [
            #    "/Developer/GPU\ Computing/OpenCL/common/inc",
            #    "/Developer/GPU\ Computing/OpenCL/common/inc/CL",
            #    "/Developer/GPU\ Computing/shared/inc"
            #],
            #"libraries" : [ "OpenCL" ],
            #"library_path" : [ "/Developer/CUDA/lib" ],
            "defines"  : [
                "USEOPENCL",
                "MACOPENCL"
            ],
            "flags" : {
                "link" : [ "framework OpenCL" ],
                "shlink" : [ "framework OpenCL" ],
            }
        },
        "removes" : {
            "include_path" : [ "/usr/local/cuda/include", ],
            "libraries" : [ "OpenCL" ],
            "library_path" : [
                "/usr/local/cuda/lib64",
                "/usr/local/cuda/lib",
            ],
        }
    },


    "gcc, boost_mpi" : {
        "appends" : {
            "libraries"  : [
                "libboost_serialization",
                "libboost_mpi"
            ],
            "library_path" : [ "/usr/local/lib" ],
            "defines" : [ "USEBOOSTMPI" ],
        },
        "overrides" : {
            "cc" : "mpicc",
            "cxx" : "mpiCC",
        },
    },


    "gcc, lto" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "flto",
                    "fwhole-program"
                ],
                "link" : [
                    "flto",
                    "fwhole-program"
                ],
            },
        },
    },


    "gcc, boost_thread" : {
        "appends" : {
            "defines" : [
                "USE_BOOST_THREAD",
            ],
            "libraries" : [
                "pthread",
                "boost_thread"
            ],
            "library_path" : [
                "/usr/local/lib",
                "/opt/boost/lib"
            ],
            "flags"         : {
                "compile" : [ "pthread" ],
            },
        },
    },

    "gcc, cxx11" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
            ],
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ]
        },
    },

    "gcc, cxx11thread" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
                "MULTI_THREADED"
            ],
            "libraries" : [ "pthread" ]
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ]
        },
    },

    "gcc, cxx11serialization" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
    "SERIALIZATION",
            ],
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ]
        },
    },


    "gcc, apbs" : {
        "appends" : {
            "defines" : [ "LINK_APBS_LIB" ],
            "libraries" : [
                "iapbs",
                "apbs_routines",
                "apbs_generic",
                "apbs_mg",
                "apbs_pmgc",
                "maloc"
            ],
            "library_path" : [ "#external/apbs/apbs-1.4-rosetta/lib" ],
            "include_path" : [
                "#external/apbs/apbs-1.4-rosetta/include",
                "#external/apbs/apbs-1.4-rosetta/include/iapbs",
                "#external/apbs/apbs-1.4-rosetta/include/maloc",
                "#external/apbs/apbs-1.4-rosetta/src",
            ],
        },
    },

    "gcc, android_arm" : {
        "appends" : {
            "include_path" : [ "#external/androidarm-tc/arm-linux-androideabi/include", ],
            "library_path"    : [ "#external/androidarm-tc/arm-linux-androideabi/lib",
                                "#external/androidarm-tc/sysroot/usr/lib", ],
            "flags" : {
                "cc"        : [
                                "Wall", "O3",
                                "-sysroot=#external/androidarm-tc/sysroot",
                                "DANDROID",
                                 "mthumb", "frtti", "fno-strict-aliasing",
                              ],
                "cxx"        : [
                                  "Wall","O3",
                                  "-sysroot=#external/androidarm-tc/sysroot",
                                  "DANDROID",
                                  "mthumb", "frtti", "fno-strict-aliasing",
                               ],
                "link" : [
                    "Wl,-Bdynamic -lz -Wl,-Bstatic",
                ],

            },
            "libraries"  : [ "stdc++", "supc++" ],
        },
        "overrides" : {
            "cc"            : "#external/androidarm-tc/bin/arm-linux-androideabi-gcc",
            "cxx"           : "#external/androidarm-tc/bin/arm-linux-androideabi-g++",
            "link"            : "#external/androidarm-tc/bin/arm-linux-androideabi-ld",
        },
        "removes" : {
           "flags" : {
                "warn" : [ "pedantic" ],
                "compile" : [
                    "malign-double",
                    "march=pentium4",
                    "march=athlon",
                    "mtune=itanium2"
                ],
           },
           "defines"  : [ "BOINC_GRAPHICS", ],
           "include_path" : [ "/usr/local/include", "/usr/include", "/usr/include/GL", "#external/include", "#external" ],
           "library_path"  : [ "/lib", "/usr/lib", "/usr/local/lib","#external/lib", "#external", ],
        },
    },

    ###########################################################################
    # ICC #####################################################################
    ###########################################################################

    # OSs & architecures ######################################################
    "icc, linux" : {
        "appends" : {
            "flags" : {
                "cc" : [ "std=c99" ],
                "warn" : [
                    "Wall",
                    # When we ICC on the test server, we should probably turn on warnings-as-errors
        "w2", # More verbose warnings
                    "Wp64",
        # Disable Specific warinings
        # 279: controlling expression is constant
        # 1682: implicit conversion of a 64-bit integral type to a smaller integral type
        # 1684: conversion from pointer to same-sized integral type -- Boost has issues with this
        # 1170: invalid redeclaration of nested class -- Boost has issues with this
        # 2196: routine is both "inline" and "noinline" -- Boost has issues with this
        # 2259: non-pointer conversion from "type" to "type" may lose significant bits
                    "wd279,1682,1684,1170,2196,2259",
                ],
                "link" : [ "lsvml", "shared-intel", ],
            },
        },
        "overrides" : {
            "cc" : "icc",
            "cxx" : "icpc",
        },
    },

    "icc, *, linux" : {
        "overrides" : {
            "version" : [ ],
        },
    },

    "icc, 8.0, linux" : {
        "overrides" : {
            "cc" : "icc",
            "cxx" : "icc",
            "version" : [ "8", "0" ],
        },
    },

    "icc, 8.1, linux" : {
        "overrides" : {
            "version" : [ "8", "1" ],
        },
    },

    "icc, 9.0, linux" : {
        "overrides" : {
            "version" : [ "9", "0" ],
        },
    },

    "icc, 9.1, linux" : {
        "overrides" : {
            "version" : [ "9", "1" ],
        },
    },

    "icc, 10.1, linux" : {
        "overrides" : {
            "version" : [ "10", "1" ],
        },
    },

    "icc, 11.1, linux" : {
        "overrides" : {
            "version" : [ "11", "1" ],
        },
    },

    "icc, 12.0, linux" : {
        "overrides" : {
           "version" : [ "12", "0" ],
        },
    },


    #"icc, windows" : {
    #    "overrides" : {
    #        "cc" : "icl",
    #        "cxx" : "icl",
    #    },
    #},

    #"icc, *, windows" : {
    #    "appends" : {
    #        "defines" : [
    #            "VC_EXTRALEAN",
    #            "WIN32_LEAN_AND_MEAN",
    #            "NOMINMAX",
    #            "ZLIB_WINAPI"
    #        ],
    #        "flags" : {
    #            "compile" : [
    #                "nologo",
    #                "Zc:forScope",
    #                "GR",
    #                "Wp64",
    #                "Qwd279",
    #                "Qwd1478",
    #                "Qwd1572",
    #            ],
    #            "link" : [  # LINKFLAGS
    #                 "nologo",
    #                 "Zc:forScope",
    #                 "GR",
    #                 "Wp64",
    #                 "Qwd279",
    #                 "Qwd1478",
    #                 "Qwd1572",
    #                 "F2097162",
    #                  # LINKOPTS
    #                  "link",
    #                  "NODEFAULTLIB:libcd",
    #            ],
    #            "warn" : [ "Wp64" ],
    #            #"warn" : [ "wd279,383,869,981,1505,1572" ]
    #        },
    #    },
    #},


    # modes ###################################################################

    "icc, linux, debug" : {
        "appends" : {
            "flags" : {
                "mode" : [ "O0", "g" ],
            },
        },
    },

    "icc, linux, release" : {
        "appends" : {
            "flags" : {
                "compile" : [ "ip" ],
                "mode" : [ "O3" ],
            },
            "defines" : [ "NDEBUG" ],
        },
    },

    "icc, linux, release_debug" : {
        "appends" : {
            "flags" : {
                "compile" : [ "ip" ],
                "mode" : [ "O3", "g" ],
            },
            #"defines" : [ "NDEBUG" ],
        },
    },


    #"icc, windows, debug" : {
    #    "appends" : {
    #        "flags" : {
    #            "mode" : [
    #                "Zi",
    #                "Od",
    #                "traceback",
    #                "Qtrapuv",
    #            ],
    #        },
    #    },
    #},

    #"icc, windows, release" : {
    #    "appends" : {
    #        "defines" : [ "NDEBUG" ],
    #        "flags" : {
    #            "mode" : [
    #                "O3",
    #                "fp:fast",
    #                "Qprec-div-",
    #                "Qip",
    #            ],
    #        },
    #    },
    #},

    #"icc, windows, profile" : {
    #    "appends" : {
    #        "defines" : [ "NDEBUG" ],
    #        "flags" : {
    #            "mode" : [
    #                "Zi",
    #                "Oy",
    #                "O3",
    #                "fp:fast",
    #                "Qprec-div-",
    #                "Qip",
    #            ],
    #        },
    #    },
    #},


    "icc, x86, release" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "Qoption,c,-ip_ninl_max_stats=500",
                    "Qoption,c,-ip_ninl_max_total_stats=5000",
                ],
            },
        },
    },


    "icc, ia64, release" : {
        "appends" : {
            "flags" : {
                "compile" : [ "Qoption,c,-ip_ninl_max_stats=50000" ],
            },
        },
    },


    # extras ##################################################################

    "icc, mpi" : {
        "appends" : {
            "defines" : [ "USEMPI" ],
        },
        "overrides" : {
            "cc" : "mpicc",
            "cxx" : "mpiCC",
        },
    },


    #"icc, windows, runtimecheck" : {
    #    "appends" : {
    #        "flags" : {
    #            "mode" : [
    #                "Gs0",
    #                "Qfpstkchk",
    #                "RTCsu"
    #            ],
    #        },
    #    },
    #},


    "icc, linux, valgrind" : {
        # Deliberately empty
        # So far no ICC flags need to change for use with valgrind.
    },


    "icc, static" : {
        "appends" : {
            "flags" : {
                "link" : [ "static" ],
            },
        },
    },


    "icc, omp" : {
        "appends" : {
            "defines" : [
                "USE_OPENMP",
                "MULTI_THREADED"
            ],
            "flags" : {
                "compile" : [ "openmp" ],
                "link" : ["openmp"],
            },
        },
    },


    "icc, mysql" : {
        "appends" : {
            "defines" : [ "USEMYSQL" ],
        },
    },


    "icc, postgres" : {
        "appends" : {
            "defines" : [ "USEPOSTGRES" ],
        },
    },
    

    "icc, cxx11" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
            ],
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ]
        },
    },

    "icc, cxx11thread" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
                "MULTI_THREADED"
            ],
            "libraries" : [ "pthread" ]
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ]
        },
    },

    "icc, cxx11serialization" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
    "SERIALIZATION",
            ],
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ]
        },
    },

     "icc, hdf5" : {
         "appends" : {
             "defines" : [ "USEHDF5" ],
             "libraries" : [ "libhdf5", "libhdf5_cpp", "libhdf5_hl", "libhdf5_hl_cpp"],
         },
     },


     "icc, python" : {
         "appends" : {
             "include_path" : [ "#external/include/python2.7" ],
             "defines" : [ "WITH_PYTHON=1" ],
             "libraries" : [
                 "python2.7",
                 "dl",
                 "pthread",
                 "util"
             ],
         },
         "removes" : {
             "flags" : {
                 "warn" : [
                     # We turn off warnings as errors for Python build
                     # only because the automatic Python interface wrapping
                     # can introduce warnings.
                     "Werror",
                 ],
             },
         },
     },


     "icc, boost_mpi" : {
         "appends" : {
             "libraries"  : [
                 "libboost_serialization",
                 "libboost_mpi"
             ],
             "library_path" : [ "/opt/apps/intel15/mvapich2_2_1/boost-mpi/1.55.0/lib" ],
             "defines" : [ "USEBOOSTMPI" ],
         },
         "overrides" : {
             "cc" : "mpicc",
             "cxx" : "mpiCC",
         },
     },
 
 
     "icc, lto" : {
         "appends" : {
             "flags" : {
                 "compile" : [
                     "flto",
                     "fwhole-program"
                 ],
                 "link" : [
                     "flto",
                     "fwhole-program"
                 ],
             },
         },
     },
 
 
     "icc, boost_thread" : {
         "appends" : {
             "defines" : [
                 "USE_BOOST_THREAD",
             ],
             "libraries" : [
                 "pthread",
                 "boost_thread"
             ],
             "library_path" : [
                 "/opt/apps/intel15/boost/1.55.0/x86_64/lib"
             ],
             "flags"         : {
                 "compile" : [ "pthread" ],
             },
         },
     },


     "icc, apbs" : {
         "appends" : {
             "defines" : [ "LINK_APBS_LIB" ],
             "libraries" : [
                 "iapbs",
                 "apbs_routines",
                 "apbs_generic",
                 "apbs_mg",
                 "apbs_pmgc",
                 "maloc"
             ],
             "library_path" : [ "#external/apbs/apbs-1.4-rosetta/lib" ],
             "include_path" : [
                 "#external/apbs/apbs-1.4-rosetta/include",
                 "#external/apbs/apbs-1.4-rosetta/include/iapbs",
                 "#external/apbs/apbs-1.4-rosetta/include/maloc",
                 "#external/apbs/apbs-1.4-rosetta/src",
             ],
         },
     },



    ###########################################################################
    # MS Visual C #############################################################
    ###########################################################################

    "msvc, windows" : {
        "overrides" : {
            "cxx" : "cl",
        },
    },

    "msvc, *, windows" : {
        "appends" : {
            "defines" : [
                "VC_EXTRALEAN",
                "WIN32_LEAN_AND_MEAN",
                "NOMINMAX",
                "_CRT_SECURE_NO_DEPRECATE",
                "_CRT_SECURE_CPP_OVERLOAD_STANDARD_NAMES",
                "ZLIB_WINAPI",
                "_WIN32",
                "WIN32",
            ],
            "flags" : {
                "compile" : [
                    "nologo",
                    "Zc:forScope",
                    "EHsc",
                    "GR",
                    "wd4258",
                    "wd4355",
                    "wd4996",
                    "TP",
                    "GX",
                ],
                "link" : [
                    # LINKFLAGS
                    #"nologo",
                    #"Zc:forScope",
                    #"EHsc",
                    #"GR",
                    #"wd4258",
                    #"wd4355",
                    #"wd4996",
                    #"F2097152",
                    # LINKOPTS
                    #"link",
                    #"NODEFAULTLIB:libcmt",
                    #'EXPORT',
                    #'NODEFAULTLIB:libcd',
                    "INCREMENTAL:NO",
                    #"MAP",
                    #"MAPINFO:EXPORTS"
                ],
            },
        },
    },


    # modes ###################################################################

    "msvc, windows, debug" : {
        "appends" : {
            "flags" : {
                "compile" : [
                    "Zi",
                    "Od",
                    "Ob0",
                    "RTCcsu",
                    "W1",
                    "MDd",
                    "LD",
                    #"MTd"
                ],
                "link" : [
                    "DEBUG",
                    #"DLL",
                    #"Zi",
                    #"Od",
                    #"Ob0",
                    #"RTCcsu",
                    #'NODEFAULTLIB:msvcrtd',
                ],
            },
        },
    },

    "msvc, windows, release" : {
        "appends" : {
            "defines" : [ "NDEBUG"],
            "flags" : {
                "compile" : [
                    "fp:fast",
                    "O2",
                    "Ob2",
                    "MT",
                ],
                "link"      : [
                    #"fp:fast",
                    #"O2",
                    #"LTCG",
                    #'NODEFAULTLIB:msvcrt',
                ],
            },
        },
    },


    "msvc, windows, profile" : {
        "appends" : {
            "defines" : [ "NDEBUG"],
            "flags" : {
                "compile" : [
                    "Zi",
                    "fp:fast",
                    "O2",
                ],
                "link"      : [
                    "Zi",
                    "fp:fast",
                    "O2",
                    "fixed:no",
                ],
            },
        },
    },


    # extras ##################################################################

    "msvc, windows, static" : {
        "removes" : {
            "flags" : {
                "compile" : [
                    "MDd",
                    "LD",
                ],
                "link" : [
                    "DLL",
                    "MAP",
                ],
            },
        },
        "appends" : {
            "flags" : {
                "compile" : [
                    "MTd",
                ],
                "link" : [
                    'NODEFAULTLIB:libcd',
                ],
            },
        },
    },


    ###########################################################################
    # XLC #####################################################################
    ###########################################################################

    "xlc, 7.0, power4" : {  # Datastar (XLC++ 7.0 Power4)
        "appends" : {
            "defines" : [
                "NDEBUG",
                "USEMPI",
                "MPICH_IGNORE_CXX_SEEK"
            ],
            "flags" : {
                "cxx" : [ "qlanglvl=cpp__func__" ],
                "compile" : [
                    "O3",
                    "qarch=pwr4",
                    "qtune=pwr4",
                    "qmaxmem=64000",
                ],
            },
        },
        "overrides" : {
            "cc" : "mpcc",
            "cxx" : "mpCC",
            "version" : [ ],
            "include_path" : [
                "#external/boost_1_55_0",
                "#external/dbio",
            ],
        },
    },


    # Does this need some other extra (e.g. "bluegene")?
    "xlc, 8.0, ppc" : {  # Blue Gene (XLC++ 8.0 PowerPC)
        "appends" : {
            "defines" : [
                "NDEBUG",
                "USEMPI",
                "MPICH_IGNORE_CXX_SEEK"
            ],
            "flags" : {
                "cxx" : [ "qlanglvl=cpp__func__" ],
                "compile" : [
                    "O3",
                    "qhot=nosimd",
                    "qarch=440",
                    "qtune=440",
                    "qmaxmem=-1",
                ],
            },
            "library_path" : [ "/bgl/BlueLight/V1R2M1_020_2006-060110/ppc/bglsys/lib" ],
            "libraries" : [
                "cxxmpich.rts",
                "mpich.rts",
                "msglayer.rts",
                "rts.rts",
                "devices.rts"
            ],
        },
        "overrides" : {
            "cc" : "mpcc",
            "cxx" : "mpCC",
            "version" : [ ],
            "include_path" : [
                "#external/boost_1_55_0",
                "#external/dbio",
            ],
        },
    },


    # Does this need some other extra (e.g. "bluegene")?
    "xlc, *, ppc64" : {  # Blue Gene (XLC++ PowerPC)
        "appends" : {
            "defines" : [
                "NDEBUG",
                "USEMPI",
                "MPICH_IGNORE_CXX_SEEK"
            ],
            "library_path" : [ "/bgsys/drivers/ppcfloor/arch/include" ],
            "flags" : {
                "compile" : [ "O3" ],
                "link" : [ "static" ],
                # jk note: Dynamic linking via XLC requires .a files (though
                # dynamic linking shouldn't need them).  The solution is to use
                # static linking.  (This is expected to have static linking,
                # and will.)
            },
        },
        "overrides" : {
            "cc" : "/bgsys/drivers/ppcfloor/comm/bin/mpicc",
            "cxx" : "/bgsys/drivers/ppcfloor/comm/bin/mpicxx",
            "version" : [ ],
            "include_path" : [
                "#external/boost_1_55_0",
                "#external/dbio",
            ],
        },
        "removes" : {
            "include_path" : [
                "/usr/local/include",
                "/usr/include",
            ],
            "library_path" : [
                "/usr/local/lib",
                "/usr/lib",
            ],
        }
    },


    ###########################################################################
    # Clang ###################################################################
    ###########################################################################

    "clang" : {
        "overrides" : {
            "cc" : "clang",
            "cxx" : "clang++",
        },
        "appends" : {
            "flags" : {
                # We don't use any C -- but if we did would it really be C99?
                # Are there portability issues?
                # (The "isystem" directives here are to tell clang not to print
                # warnings found in these external headers.)
                "cc" : [
                    "std=c99",
                    "isystem external/boost_1_55_0/",
                    "isystem external/",
                    "isystem external/include/",
                    "isystem external/dbio/"
                ],
                "cxx" : [
                    "std=c++98",
                    "isystem external/boost_1_55_0/",
                    "isystem external/",
                    "isystem external/include/",
                    "isystem external/dbio/"
                ],
                "compile" : [
        "march=core2",
        "mtune=generic",
                    "pipe",
                    "Qunused-arguments",
                    'DUNUSUAL_ALLOCATOR_DECLARATION',
                    'ftemplate-depth-256',
                    "stdlib=libstdc++",
                ],
                'shlink' : [ "stdlib=libstdc++"],
                'link' : [ "stdlib=libstdc++"],
                "warn" : [
                    "W",
                    "Wall",
                    "Wextra",
                    "pedantic",
                    #"Weverything",
                    "Werror",
                    "Wno-long-long",
                    "Wno-strict-aliasing",
                    #"Wno-documentation",
                    #"Wno-padded",
                    #"Wno-weak-vtables"
                ],
            },
        },
    },


    # OSs #####################################################################

    "clang, linux" : {
        "appends" : {
            "flags" : {
                "warn" : [
                    # This will become necessary at some point! and for some compilers
                    # But if you include it now it won't build with clang 3.4 (testing server)
                    #"Wno-undefined-var-template",
                ],
            },
        },
  "prepends" : {
            # This makes clang use libstdc++ 4.4.0 on CentOS.
            # (requires gcc44-c++ and libstdc++44-devel)
            #"library_path" : [ "/usr/lib/gcc/x86_64-redhat-linux6E/4.4.0" ],
        },
    },

    "clang, macos" : {
        "appends" : {
            "flags" : {
                # Change 'abspath' to 'file' to use DYLD_LIBRARY_PATH environ-
                # ment variable.
                "compile" : [ "march=native", "mtune=native", "stdlib=libc++", ],
                "shlink" : [ "install_name ${TARGET.abspath}", "stdlib=libc++", ],
                "link"   : [ "stdlib=libc++"],
                "cxx" : [ "std=c++11" ],
                # There is at least one variable only used on non-Macs.
                "warn" : ["Wno-unused-variable"],
            },
            "defines" : [ "CXX11", "PTR_STD" ],
        },
        "removes" : {
            "flags" : {
                "link" : [ "$__RPATH", "stdlib=libstdc++", ],
                "cxx" : [ "std=c++98", "std=c++0x", ],
                "shlink" : [ "$LINKFLAGS", "stdlib=libstdc++", ],
                "link"   : [ "stdlib=libstdc++", ],
            },
            "defines" : [ "PTR_BOOST", ],
        },
    },

    "clang, macos, 15.0" : {
        "removes" : {
            "include_path" : [ "/usr/local/include" ],
        },
    },

    # modes ###################################################################

    "clang, debug" : {
        "appends" : {
            "flags" : {
                "compile" : [ "O0" ],
                "mode" : [ "g" ],
            },
        },
    },

    "clang, release" : {
        "appends" : {
            "flags" : {
                "compile" : [ "O3" ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
                ],
            },
            "defines" : [ "NDEBUG" ],
        },
    },

    "clang, release_debug" : {
        "appends" : {
            "flags" : {
                "compile" : [ "O3" ],
                "mode" : [
                    "g",
                    "fno-omit-frame-pointer", # Keep frame pointer information, to help with stack traces
    ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
                ],
            },
            #"defines" : [ "NDEBUG" ],
        },
    },

    "clang, release_debug_no_symbols" : {
        "appends" : {
            "flags" : {
                "compile" : [
        "O3",
        "ffloat-store", # "mfpmath=sse", "msse2",  WARNING WARNING WARNING this flags SIGNIFICANTLY degrade performance and only used to improved stability for integration tests, they should NEVER be enabled for production code
    ],
                # Asserts can leave variables unused, making warnings spurious.
                # We count on debug builds to catch actual unused variables.
                "warn" : [
                    "Wno-unused-variable",
                    "Wno-unused-parameter",
                ],
            },
            #"defines" : [ "NDEBUG" ],
        },
    },

    # cats ####################################################################

    "clang, test" : {
        "appends" : {
            "flags" : {
                # The "isystem" items here are to tell Clang to not print warn-
                # ings from these external headers
                "cc" : [ "isystem external/cxxtest/"],
                "cxx" : [ "isystem external/cxxtest/"],
            },
        },
    },


    # extras ##################################################################

    "clang, cxx11" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
            ],
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ],
        },
    },

    "clang, cxx11serialization" : {
        "appends" : {
            "flags" : {
                "cxx" : [ "std=c++11" ],
                "warn" : [ "Wno-unused-function", ],
            },
            "defines" : [
                "CXX11",
                "PTR_STD",
    "SERIALIZATION",
            ],
        },
        "removes" : {
            "flags" : {
                "cxx" : [ "std=c++98", "std=c++0x" ],
            },
            "defines" : [
                "PTR_BOOST"
            ]
        },
    },


    "clang, graphics" : {
        "appends" : {
            "include_path" : [ "/usr/X11R6/include" ],
            "library_path" : [ "/usr/X11R6/lib" ],
            "defines" : [
                "GL_GRAPHICS",
                "MAC"
            ],
            "flags" : {
                "link" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "dylib_file /System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib"
                ],
                "shlink" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "dylib_file /System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib:/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/libGL.dylib"
                ],
            },
        },
    },

    "clang, mpi" : {
        "appends" : {
            "defines" : [ "USEMPI" ],
        },
        "overrides" : {
            "cc" : "mpicc",
            "cxx" : "mpicxx",
        },
    },

    "clang, python" : {  # Include python interpreter.
        "appends" : {
            "include_path" : [ "#external/include/python2.7" ],
            "defines" : [ "WITH_PYTHON=1" ],
            "libraries" : [
                "python2.7",
                "dl",
                "pthread",
                "util"
            ],
        },
    },

    "clang, mysql" : {
        "appends" : {
            "defines" : [ "USEMYSQL" ],
            "library_path" : [ "/usr/lib64/mysql" ],
        },
    },

    "clang, postgres" : {
        "appends" : {
            "defines" : [ "USEPOSTGRES" ],
        },
    },

    "clang, opencl" : {
        "appends" : {
            "include_path"  : [ "/usr/local/cuda/include", ],
            "libraries" : [ "OpenCL" ],
            "library_path" : [
                "/usr/local/cuda/lib64",
                "/usr/local/cuda/lib",
            ],
            "defines" : [ "USEOPENCL" ],
        },
    },

    "clang, macos, opencl" : {
        "appends" : {
            "defines"  : [
                "USEOPENCL",
                "MACOPENCL"
            ],
            "flags" : {
                "link" : [ "framework OpenCL" ],
                "shlink" : [ "framework OpenCL" ],
                # GPU code needs to cast into to void pointer
                "warn" : [ "Wno-int-to-void-pointer-cast" ],
            },
        },
        "removes" : {
          "libraries" : [ "OpenCL" ]
        },
    },

    "clang, macos, boinc" : {
        "appends" : {
            "libraries" : [
    "boinc_graphics2",
                "boinc_api",
                "boinc",
                "boinc_zip"
      ],
            "library_path" : [
                "#external/boinc/mac_build/build/Deployment",
                "#external/boinc/zip",
                "/usr/X11R6/lib",
                "#external/boinc/api",
                "#external/boinc/lib",
            ],
            "include_path" : [
                "#external",
                "#external/dbio",
                "#external/boinc/api",
                "#external/boinc",
                "#external/boinc/lib",
                "#external/boinc/zip",
            ],
            "defines" : [
                "MAC",
    "BOINC",
                "BOINC_GRAPHICS",
                "GL_GRAPHICS"
            ],
            "flags" : {
    "warn" : [
        "Wno-deprecated-declarations",
    ],
                "link" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "framework Cocoa"
                ],
                "shlink" : [
                    "framework GLUT",
                    "framework OpenGL",
                    "framework Cocoa"
                ],
            },
        },
        "removes" : {
            "flags" : {
                "compile" : [ "pthread" ],
            },
        },
    },


    "clang, boost_mpi" : {
        "overrides" : {
            "cc" : "mpicc",
            "cxx" : "mpiCC",
        },
        "appends" : {
            "libraries" : [ "libboost_mpi" ],
            "libraries" : [ "libboost_serialization" ],
            "library_path" : [ "/usr/local/lib" ],
            "defines" : [ "USEBOOSTMPI" ],
        },
    },

    "gcc, cuda" : {
        "appends" : {
            "include_path"  : [ "/usr/local/cuda/include", "#external/include/cuda"],
            "libraries"     : [ "cudart"],
            "library_path"  : [ "/usr/local/cuda/lib64", "/usr/local/cuda/lib"],
            "defines"       : [ "USECUDA" ],
        },
    },


}  # end settings
EOF
rm basic.settings
ln -s basic.settings.stampede basic.settings

cat > options.settings.stampede << EOF
# (c) Copyright Rosetta Commons Member Institutions.
# (c) This file is part of the Rosetta software suite and is made available under license.
# (c) The Rosetta software is developed by the contributing members of the Rosetta Commons.
# (c) For more information, see http://www.rosettacommons.org. Questions about this can be
# (c) addressed to University of Washington UW TechTransfer, email: license@u.washington.edu.

# Supported options
options = {

    "cxx" : {
        "gcc"     : [ "3.3", "3.4", "4.0", "4.1", "4.2", "4.3","4.4","4.5", "4.6","4.7", "4.9", "*" ],
        "icc"     : [ "8.0", "8.1", "9.0", "9.1", "10.0", "10.1", "11.1", "*", "13.1", "14.0", "15.0", "16.0", "17.0" ], #PBHACK
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
        
        # Link to python interpreter
        "python",

        #enable mysql database support
        "mysql",

        #enable postgres database support
        "postgres",

        # Build with CUDA
        "cuda",

        # Build with OpenCL
        "opencl",
        
        # Build with Math Kernel Library (Intel, Stampede)
        "mkl",

        # Build boost MPI and serialization dependent code (requires these libraries to be installed in /usr/local/lib)
        "boost_mpi",

        # Build using link-time optimization. Include whole program optimization as well
        "lto",
        
        # Build with Boost thread library
        "boost_thread",
        
        # Enable HDF5 file stores
        "hdf5",
        
        # Build with C++11 std:: pointers
        "cxx11",
        
        # Build with the C++11 thread utilities enabled
        "cxx11thread",
        
        # Build with C++11 serialization
        "cxx11serialization",
        
        # Build with boost non-intrusive pointers
        "ptr_boost",
        
        # Enable APBS integration
        "apbs",
        
        # Build for Android ARM
        "android_arm",

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
###            "include_path" : os.environ["INCLUDE"].split(":"),
        },
        "appends" : {
            "flags" : {
                "compile" : ["mkl"],
                "link" : ["mkl"],
                "warn" : [ "wd1684", "wd592" ]
            },
        },
        "overrides" : {
            "cxx" : "mpicxx_wrapper -g -xHOST",
            "cc"  : "mpicc_wrapper -g -xHOST",
        },
        "removes" : {
        },
    }
}
EOF
rm -f site.settings
ln -s site.settings.stampede site.settings
cd ../../

#sed -i '33i#include<iostream>' src/utility/string_util.hh

echo -e "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"
echo -e "PATH=${PATH}"

export COMPILER=%{comp}
export     MODE=release
#export   EXTRAS=mpi,omp,mkl,cxx11,cxx11thread,cxx11serialization,hdf5,python,boost_mpi,lto,boost_thread,apbs
export   EXTRAS=mpi

./scons.py -c
rm -f .sconsign.dblite
./scons.py -j48 mode=${MODE} extras=${EXTRAS} cxx=${COMPILER} bin 


  cd $RPM_BUILD_ROOT 
  cp -rp %{INSTALL_DIR}/rosetta_src_%{build_version}_bundle/main/source/doc   $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -rp %{INSTALL_DIR}/rosetta_src_%{build_version}_bundle/main/source/bin   $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -rp %{INSTALL_DIR}/rosetta_src_%{build_version}_bundle/main/source/build $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -rp %{INSTALL_DIR}/rosetta_src_%{build_version}_bundle/main/database     $RPM_BUILD_ROOT/%{INSTALL_DIR}
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
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN, and TACC_%{MODULE_VAR}_DATABASE
for the location of the %{MODULE_VAR} distribution, binaries, and database
respectively.

NOTE: %{MODULE_VAR} is hard-coded to attempt to write temporary files within
the designated database location. This action will fail if the user sets
-database=$TACC_%{MODULE_VAR}_DATABASE. Instead, copy the database from
TACC_%{MODULE_VAR}_DATABASE to a writable location via something like:

cp -r $TACC_%{MODULE_VAR}_DATABASE $WORK/rosetta_database

Then, to run:

$TACC_%{MODULE_VAR}_BIN/<rosetta-executable>.mpi.linuxiccrelease [options] -database=$WORK/rosetta_database

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
  local rosetta_lib        = "build/src/release/linux/%{kern_ver}/64/x86/%{comp}/%{comp_ver}/mpi"
  local ext_lib            = "build/external/release/linux/%{kern_ver}/64/x86/%{comp}/%{comp_ver}/mpi"


  prepend_path( "PATH",                   pathJoin(base_dir, "bin"))
  prepend_path( "LD_LIBRARY_PATH",        pathJoin(base_dir, ext_lib))
  prepend_path( "LD_LIBRARY_PATH",        pathJoin(base_dir, rosetta_lib))
  setenv( "TACC_%{MODULE_VAR}_DIR",                base_dir)
  setenv( "TACC_%{MODULE_VAR}_DATABASE",  pathJoin(base_dir, "database"))
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
%files package
#------------------------

  %defattr(750,root,%{rpm_group},)
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

