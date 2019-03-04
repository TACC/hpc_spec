#
# Adapted from Bar.spec by Victor Eijkhout 2018/12/17
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

Summary: Slepc4py rpm build scxript

# Give the package a base name
%define pkg_base_name slepc4py
%define MODULE_VAR    SLEPC4PY

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 10
%define micro_version 0

%define slepcversion %{major_version}.%{minor_version}
%define slepc_full_version %{major_version}.%{minor_version}.%{micro_version}
%define pkg_version %{pythonV}.%{slepcversion}

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

Release:   1
License:   GPL
Group:     Development/Tools
URL:       https://bitbucket.org/slepc/slepc4py/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{slepc_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: SLEPC4PYc rpm building
Group: HPC/libraries
%description package
Python interface to Slepc

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Python interface to Slepc

%description
Python interface to Slepc


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{slepc_full_version}

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
module load python%{pythonV}

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

# same as in slepc
export dynamiccc="debug uni unidebug i64 i64debug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

echo "See what slepc versions there are"
module spider slepc
module spider slepc/%{slepcversion}

for ext in \
  "" debug complex complexdebug ; do

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

export architecture=haswell
if [ -z "${ext}" ] ; then
  module load petsc/%{slepcversion}
  module load slepc/%{slepcversion}
else
  module load petsc/%{slepcversion}-${ext}
  module load slepc/%{slepcversion}-${ext}
  export architecture=${architecture}-${ext}
fi

echo "What do we currently have loaded"
module list

pwd
mkdir -p %{INSTALL_DIR}/${architecture}
python%{pythonV} setup.py build
python%{pythonV} setup.py install --prefix=%{INSTALL_DIR}/${architecture}

module unload petsc slepc

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
  export moduleslepcversion=%{slepcversion}
else
  export moduleversion=%{version}-${ext}
  export moduleslepcversion=%{slepcversion}-${ext}
fi

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${moduleversion}.lua << EOF
help( [[
The SLEPC4PY modulefile defines the following environment variables:
TACC_SLEPC4PY_DIR for the package location
and it updates the PYTHONPATH

Version ${moduleversion} is for python%{pythonV} and Slepc %{slepcversion}
]] )

whatis( "Name: Slepc4py" )
whatis( "Version: %{moduleversion}" )
whatis( "Version-notes: ${moduleversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://bitbucket.org/slepc/slepc4py/" )
whatis( "Description: Python interface to Slepc" )

local             slepc_arch =    "${architecture}"
local             slepc4py_dir =     "%{INSTALL_DIR}"

prepend_path("PYTHONPATH",
    pathJoin(slepc4py_dir,slepc_arch,"lib","python${TACC_PYTHON_VER}","site-packages") )

setenv(          "TACC_SLEPC4PY_DIR",        slepc4py_dir)

prereq     ("python%{pythonV}")
always_load("petsc/${moduleslepcversion}")
always_load("slepc/${moduleslepcversion}")
always_load("petsc4py/${moduleversion}")
EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${moduleversion} << EOF
#%Module3.1.1#################################################
##
## version file for %{BASENAME}/%{version}
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
  # Copy the installation  over to the installation directory
  cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------

#------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

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

%changelog
* Mon Jan 14 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: first release
