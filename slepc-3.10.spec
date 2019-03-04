#
# Adapted from Bar.spec by Victor Eijkhout 2015/11/30
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

Summary: SLEPc rpm build scxript

# Give the package a base name
%define pkg_base_name slepc
%define MODULE_VAR    SLEPC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 10
%define micro_version 4

%define pkg_version %{major_version}.%{minor_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

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

Release:   2
License:   GPL
Group:     Development/Tools
URL:       http://www.gnu.org/software/bar
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: SLEPCc rpm building
Group: HPC/libraries
%description package
Simple Linear Eigenvalue Problem solvers

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
The longer-winded description of the package that will 
end in up inside the rpm and is queryable if installed via:
rpm -qi <rpm-name>


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_full_version}

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
%include compiler-load.inc
%include mpi-load.inc

# Insert further module commands
module load cmake

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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------

# same as in petsc
export dynamiccc="debug uni unidebug i64 i64debug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

echo "See what petsc versions there are"
module spider petsc
module spider petsc/%{version}

for ext in \
  "" \
  ${dynamiccc} ${dynamiccxx} ; do

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

export architecture=haswell
if [ -z "${ext}" ] ; then
  module load petsc/%{version}
else
  module load petsc/%{version}-${ext}
  export architecture=${architecture}-${ext}
fi

echo "What do we currently have loaded"
module list

pwd
# export SLEPC_DIR=`pwd`
./configure # ${arpackline}
make SLEPC_DIR=$PWD || /bin/true

module unload petsc

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
  
if [ -z "${ext}" ] ; then
  export moduleversion=%{version}
else
  export moduleversion=%{version}-${ext}
fi

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${moduleversion}.lua << EOF
help( [[
The SLEPC modulefile defines the following environment variables:
TACC_SLEPC_DIR, TACC_SLEPC_LIB, and TACC_SLEPC_INC 
for the location of the SLEPC %{version} distribution, 
libraries, and include files, respectively.

Usage:
    include \$(SLEPC_DIR)/conf/slepc_common
Alternatively:
    include \$(SLEPC_DIR)/conf/slepc_variables
    include \$(SLEPC_DIR)/conf/slepc_rules
in your makefile, then compile
    \$(CC) -c yourfile.c \$(PETSC_INCLUDE)
and link with
    \$(CLINKER) -o yourprog yourfile.o \$(SLEPC_LIB)

Version ${moduleversion}
]] )

whatis( "Name: SLEPc" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${moduleversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www.grycap.upv.es/slepc/" )
whatis( "Description: Scalable Library for Eigen Problem Computations: Library of eigensolvers" )

local             petsc_arch =    "${architecture}"
local             slepc_dir =     "%{INSTALL_DIR}"

prepend_path("LD_LIBRARY_PATH", pathJoin(slepc_dir,petsc_arch,"lib") )

setenv(          "SLEPC_DIR",             slepc_dir)
setenv(          "TACC_SLEPC_DIR",        slepc_dir)
setenv(          "TACC_SLEPC_LIB",        pathJoin(slepc_dir,petsc_arch,"lib"))
setenv(          "TACC_SLEPC_INC",        pathJoin(slepc_dir,petsc_arch,"include"))
setenv(          "SLEPC_VERSION",         "${moduleversion}")
setenv(          "TACC_SLEPC_VERSION",    "${moduleversion}")

always_load("petsc/${moduleversion}")
EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${moduleversion} << EOF
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "${moduleversion}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${moduleversion}.lua
  %endif
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


done # end of for ext loop

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Copy everything from tarball over to the installation directory
  cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------

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

%changelog
* Fri Mar 01 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: update to 3.10.4 because 3.10.3 has a SuperLU update
* Mon Jan 14 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: point update
* Wed Oct 10 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: first release
