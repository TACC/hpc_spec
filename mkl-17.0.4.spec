#
# W. Cyrus Proctor
# 2015-12-11
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
%define pkg_base_name mkl
%define MODULE_VAR    MKL

# Create some macros (spec file variables)
%define major_version 17
%define minor_version 0
%define patch_version 4

%define pkg_version %{major_version}.%{minor_version}.%{patch_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
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
This is specifically an rpm for the Intel MKL modulefile
used on Stampede 2 for GCC.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
This is specifically an rpm for the Intel MKL modulefile
used on Stampede 2 for GCC.

%description
This is specifically an rpm for the Intel MKL modulefile
used on Stampede 2 for GCC.

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
The Intel Math Kernel Library (Intel MKL) improves performance with math
routines for software applications that solve large computational problems.
Intel MKL provides BLAS and LAPACK linear algebra routines, fast Fourier
transforms, vectorized math functions, random number generation functions, and
other functionality.

The Intel MKL module enables the use of the MKL with the GNU GCC compilers by
updating the $LD_LIBRARY_PATH, $INCLUDE, and $MANPATH environment variables to
access the MKL libraries, include files, and available man pages, respectively.

The following additional environment variables are also defined:

$TACC_MKL_DIR           (path to Math Kernel Library root         )
$TACC_MKL_LIB           (path to Math Kernel Library libs         )
$TACC_MKL_INC           (path to Math Kernel Library includes     )
$TACC_MKL_DOC           (path to Math Kernel Library documentation)

To use the MKL with Intel compilers, please see the Intel module help
by issuing a "module help intel".

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: Intel MKL"                                                    )
whatis("Version: %{version}"                                                )
whatis("Category: Library, Runtime Support"                                 )
whatis("Description: Intel Math Kernel Library"                             )
whatis("URL: https://software.intel.com/en-us/intel-mkl"                    )

-- Create environment variables.
local base         = "/opt/intel"
local full_xe      = "compilers_and_libraries_2017.4.196/linux"
local installDir   = pathJoin(base,full_xe)
local mklRoot      = pathJoin(installDir,"mkl")

setenv( "MKLROOT"      ,              mklRoot )
setenv( "TACC_MKL_DIR" ,              mklRoot )
setenv( "TACC_MKL_LIB" ,              pathJoin( mklRoot    , "lib/intel64" ) )
setenv( "TACC_MKL_INC" ,              pathJoin( mklRoot    , "include" ) )
setenv( "TACC_MKL_DOC" ,              pathJoin( base       , "documentation_2017/en/mkl/ps2017" ) )

prepend_path( "LD_LIBRARY_PATH" ,     pathJoin( mklRoot    , "lib/intel64" ) )

prepend_path( "INCLUDE" ,             pathJoin( mklRoot    , "include" ) )

prepend_path( "MANPATH" ,             pathJoin( base ,       "documentation_2017/en/debugger/gdb-ia/man" ) )
prepend_path( "MANPATH" ,             pathJoin( base ,       "documentation_2017/en/debugger/gdb-igfx/man" ) )
prepend_path( "MANPATH" ,             pathJoin( base ,       "documentation_2017/en/man/common" ) )

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version << 'EOF'
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

