#
# W. Cyrus Proctor
# 2015-11-12
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
%define pkg_base_name intel
%define MODULE_VAR    INTEL

# Create some macros (spec file variables)
%define major_version 19
%define minor_version 0
%define micro_version 4

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define lib_dir 2019.4.243
%define year 2019

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
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

Release:   2%{?dist}
License:   proprietary
Group:     Compiler
URL:       https://software.intel.com/en-us/intel-compilers
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
This is specifically an rpm for the Intel Compiler modulefile
used on Frontera.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
This is specifically an rpm for the Intel Compiler modulefile
used on Frontera.

%description
This is specifically an rpm for the Intel Compiler modulefile
used on Frontera.

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
 
  # Nothing to do!
  
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
Intel compilers %{version} produce optimized code that can run significantly
faster by taking advantage of the ever increasing core count and vector
register width in Intel Xeon processors, Intel Xeon Phi coprocessors and
compatible processors. The Intel compilers plug right into popular development
environments and are compatible with compilers including GCC (Linux).

The Intel module enables the Intel family of compilers (C/C++ and Fortran) and
updates the $PATH, $LD_LIBRARY_PATH, $INCLUDE, and $MANPATH environment
variables to access the compiler binaries, libraries, include files, and
available man pages, respectively.

The following additional environment variables are also defined:

$ICC_BIN                (path to icc/icpc compilers          )
$ICC_LIB                (path to C/C++  libraries            )
$IFC_BIN                (path to ifort compiler              )
$IFC_LIB                (path to Fortran libraries           )
$TACC_MKL_DIR           (path to Math Kernel Library root    )
$TACC_MKL_LIB           (path to Math Kernel Library libs    )
$TACC_MKL_INC           (path to Math Kernel Library includes)

In general, users need only to add the "-mkl" flag during compile and link time
to utlize thei Math Kernel Library provided by Intel.  This includes any calls
to BLAS and LAPACK functions.
 
See the man pages for icc, icpc, and ifort for detailed information on
available compiler options and command-line syntax.

Note: To provide C++11/14/17 support for the Intel compiler, this module adds the
paths for the gcc/8.3.0 bin, lib, and lib64 directories to your environment.

Note: The $TACC_VEC_FLAGS environment variable is provided as a convenience
during your compliation step. This variable specifies instruction sets
appropriate to build and run on any Frontera node (login node, KNL compute
node, SKX compute node), and use CPU dispatch to produce a multi-architecture
binary.

The %{MODULE_VAR} module also defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution,
libraries, include files, and tools respectively.

Version %{version}
]]

help(help_msg)

whatis("Name: Intel Compiler"                                               )
whatis("Version: %{version}"                                                )
whatis("Category: compiler, Runtime Support"                                )
whatis("Description: Intel Compiler Family (C/C++/Fortran for x86_64)"      )
whatis("URL: http://software.intel.com/en-us/articles/intel-compilers"      )

-- Create environment variables.
local base         = "/home1/apps/intel/19.0.4"
local gcc_base     = "/opt/apps/gcc/8.3.0"
local full_xe      = "compilers_and_libraries_%{lib_dir}/linux"
local arch         = "intel64"
local installDir   = pathJoin(base,full_xe)
local tbbRoot      = pathJoin(installDir,"tbb")
local mklRoot      = pathJoin(installDir,"mkl")
local ippRoot      = pathJoin(installDir,"ipp")
local daalRoot     = pathJoin(installDir,"daal")
local pstlRoot     = pathJoin(installDir,"pstl")


setenv( "MKLROOT"      ,                  mklRoot )
setenv( "TACC_MKL_DIR" ,                  mklRoot )
setenv( "TACC_MKL_LIB" ,              pathJoin( mklRoot , "lib/intel64" ) )
setenv( "TACC_MKL_INC" ,              pathJoin( mklRoot , "include"     ) )

--MKLROOT=
--/opt/intel/compilers_and_libraries_2019.4.243/linux/mkl

prepend_path( "MANPATH" ,             pathJoin( base ,       "documentation_%{year}/en/debugger/gdb-ia/man"   ) )
prepend_path( "MANPATH" ,             pathJoin( base ,       "documentation_%{year}/en/man/common"            ) )

--MANPATH=
-- /opt/intel/documentation_2018/en/debugger//gdb-ia/man
-- /opt/intel/documentation_2018/en/man/common

local home = os.getenv("HOME")

prepend_path( "INTEL_LICENSE_FILE" ,  pathJoin( installDir , "licenses"       ) )
prepend_path( "INTEL_LICENSE_FILE" ,  pathJoin( base       , "licenses"       ) )
prepend_path( "INTEL_LICENSE_FILE" ,  pathJoin( home       , "intel/licenses" ) )

--INTEL_LICENSE_FILE=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/licenses
-- /opt/intel/licenses
-- ${HOME}/intel/licenses

setenv( "IPPROOT" ,                   ippRoot )
--IPPROOT=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/ipp

prepend_path( "LIBRARY_PATH" ,        pathJoin( installDir , "compiler/lib/intel64_lin"            ) )
prepend_path( "LIBRARY_PATH" ,        pathJoin( installDir , "ipp/lib/intel64"                     ) )
prepend_path( "LIBRARY_PATH" ,        pathJoin( installDir , "mkl/lib/intel64_lin"                 ) )
prepend_path( "LIBRARY_PATH" ,        pathJoin( installDir , "tbb/lib/intel64/gcc4.7"              ) )
prepend_path( "LIBRARY_PATH" ,        pathJoin( installDir , "daal/lib/intel64_lin"                ) )
prepend_path( "LIBRARY_PATH" ,        pathJoin( base       , "debugger_%{year}/libipt/intel64/lib" ) )

--LIBRARY_PATH=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/ipp/lib/intel64
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64_lin
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/tbb/lib/intel64/gcc4.7
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/daal/lib/intel64_lin
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/daal/../tbb/lib/intel64_lin/gcc4.4

prepend_path( "LD_LIBRARY_PATH" ,     pathJoin( gcc_base , "lib" ) )
prepend_path( "LD_LIBRARY_PATH" ,     pathJoin( gcc_base , "lib64" ) )

prepend_path( "LD_LIBRARY_PATH" ,        pathJoin( installDir , "compiler/lib/intel64_lin"            ) )
prepend_path( "LD_LIBRARY_PATH" ,        pathJoin( installDir , "ipp/lib/intel64"                     ) )
prepend_path( "LD_LIBRARY_PATH" ,        pathJoin( installDir , "mkl/lib/intel64_lin"                 ) )
prepend_path( "LD_LIBRARY_PATH" ,        pathJoin( installDir , "tbb/lib/intel64_lin/gcc4.7"          ) )
prepend_path( "LD_LIBRARY_PATH" ,        pathJoin( installDir , "daal/lib/intel64_lin"                ) )
prepend_path( "LD_LIBRARY_PATH" ,        pathJoin( base       , "debugger_%{year}/libipt/intel64/lib" ) )

--LD_LIBRARY_PATH=
-- /opt/apps/gcc/8.3.0/lib64
-- /opt/apps/gcc/8.3.0/lib
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64_lin
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/ipp/lib/intel64
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/tbb/lib/intel64/gcc4.7
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/daal/lib/intel64_lin
-- /opt/intel/debugger_2018/libipt/intel64/lib

prepend_path( "CPATH" ,     pathJoin( installDir , "ipp/include"  ) )
prepend_path( "CPATH" ,     pathJoin( installDir , "mkl/include"  ) )
prepend_path( "CPATH" ,     pathJoin( installDir , "tbb/include"  ) )
prepend_path( "CPATH" ,     pathJoin( installDir , "daal/include" ) )
prepend_path( "CPATH" ,     pathJoin( installDir , "pstl/include" ) )

--CPATH=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/ipp/include
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/mkl/include
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/tbb/include
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/daal/include
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/pstl/include

prepend_path( "NLSPATH" ,     pathJoin( installDir , "compiler/lib/intel64/locale/%l_%t/%N"               ) )
prepend_path( "NLSPATH" ,     pathJoin( installDir , "mkl/lib/intel64_lin/locale/%l_%t/%N"                ) )
prepend_path( "NLSPATH" ,     pathJoin( base       , "debugger_%{year}/gdb/intel64/share/locale/%l_%t/%N" ) )

--NLSPATH=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64/locale/%l_%t/%N
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/mkl/lib/intel64_lin/locale/%l_%t/%N
-- /opt/intel/debugger_2018/gdb/intel64/share/locale/%l_%t/%N

prepend_path( "PATH" ,        pathJoin( gcc_base   , "bin"         ) )
prepend_path( "PATH" ,        pathJoin( installDir , "bin/intel64" ) )

--PATH=
-- /opt/apps/gcc/8.3.0/bin
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/bin/intel64

setenv( "TBBROOT" ,           tbbRoot )

--TBBROOT=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/tbb

setenv( "DAALROOT" ,          daalRoot )

--DAALROOT=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/daal

setenv( "PSTLROOT" ,          pstlRoot )

--PSTLROOT=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/pstl

setenv("PKG_CONFIG_PATH",     pathJoin(mklRoot, "bin/pkgconfig") )

--PKG_CONFIG_PATH=
-- /opt/intel/compilers_and_libraries_2019.4.243/linux/mkl/bin/pkgconfig

setenv( "PSXE_2019",            "1"                                              )
setenv( "ICC_BIN" ,             pathJoin(installDir , "bin" , arch               ) )
setenv( "IFC_BIN" ,             pathJoin(installDir , "bin" , arch               ) )
setenv( "ICC_LIB" ,             pathJoin(installDir , "compiler/lib" , arch      ) )
setenv( "IFC_LIB" ,             pathJoin(installDir , "compiler/lib" , arch      ) )
setenv( "TACC_INTEL_DIR" ,      installDir                                       )
setenv( "TACC_INTEL_BIN" ,      pathJoin(installDir , "bin/intel64"              ) )
setenv( "TACC_INTEL_LIB" ,      pathJoin(installDir , "compiler/lib/intel64"     ) )
setenv( "TACC_INTEL_INC" ,      pathJoin(installDir , "compiler/include/intel64" ) )

if (os.getenv("TACC_SYSTEM") == "frontera") then
  setenv( "TACC_VEC_FLAGS" ,      "-xCORE-AVX2 -axCORE-AVX512,MIC-AVX512" )
elseif (os.getenv("TACC_SYSTEM") == "stampede2") then
  setenv( "TACC_VEC_FLAGS" ,      "-xCORE-AVX2 -axCORE-AVX512,MIC-AVX512" )
elseif (os.getenv("TACC_SYSTEM") == "ls5") then
  setenv( "TACC_VEC_FLAGS" ,      "-xCORE-AVX-I -axCORE-AVX2" )
else
  setenv( "TACC_VEC_FLAGS" ,      "-xCORE-AVX2" )
end

prepend_path( "MODULEPATH" , "/opt/apps/intel19/modulefiles" )

family("compiler")
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

