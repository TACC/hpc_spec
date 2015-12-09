#
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
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
%define pkg_base_name cp2k
%define MODULE_VAR    CP2K

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 6
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  

%include compiler-defines.inc
%include mpi-defines.inc

#%include name-defines-noreloc.inc

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
License:   GPL
Group:     Theoretical and Computational Biophysics Group, UIUC
URL:       https://www.cp2k.org/
Packager:  TACC - huang@tacc.utexas.edu
Source0:   %{pkg_base_name}-%{pkg_version}.tar.bz2
Source1:   libint-1.1.5.tar.gz
Source2:   libxc-2.0.1.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The cp2k distribution for login and compute nodes.
Group: Applications/Chemistry
%description package
CP2K, program to perform atomistic and molecular simulations of solid state, 
liquid, molecular, and biological systems. It provides a general framework 
for different methods such as e.g., density functional theory (DFT) using 
a mixed Gaussian and plane waves approach (GPW) and classical pair and 
many-body potentials.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
CP2K, program to perform atomistic and molecular simulations of solid state, 
liquid, molecular, and biological systems. It provides a general framework 
for different methods such as e.g., density functional theory (DFT) using 
a mixed Gaussian and plane waves approach (GPW) and classical pair and 
many-body potentials.

%description
CP2K, program to perform atomistic and molecular simulations of solid state, 
liquid, molecular, and biological systems. It provides a general framework 
for different methods such as e.g., density functional theory (DFT) using 
a mixed Gaussian and plane waves approach (GPW) and classical pair and 
many-body potentials.

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

%setup -n %{pkg_base_name}-%{pkg_version}


#---------------------------------------
%build
#---------------------------------------
%include compiler-load.inc
%include mpi-load.inc

tar -xvf $RPM_SOURCE_DIR/libxc-2.0.1.tar.gz 
tar -xvf $RPM_SOURCE_DIR/libint-1.1.5.tar.gz 

cd libint-1.1.5 
CC=icc CXX=icpc F77=ifort ./configure ; make -j 12
cd ..

cd libxc-2.0.1
CC=icc CXX=icpc F77=ifort ./configure CFLAGS=" -O2 -fp-model strict "
make -j 12
cd ..

cp $RPM_SOURCE_DIR/cp2k-2.6.2_makefile_intel arch/Linux-x86-64-intel.popt
cd makefiles
make -j 12 ARCH=Linux-x86-64-intel VERSION=popt


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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

  cp -p exe/Linux-x86-64-intel/cp2k.popt $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
  cp -p lib/Linux-x86-64-intel/popt/*    $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/
  chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
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

The TACC CP2K module appends the path to the cp2k executable
to the PATH environment variable. Also TACC_CP2K_DIR, 
TACC_CP2K_BIN, and TACC_CP2K_LIB are set to CP2K home 
bin, and lib directories. 

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: CP2K")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Ab Initio Molecular Dynamics, Application")
whatis("URL: http://www.cp2k.org/")
whatis("Description: Open source Ab Initio Molecular Dynamics software")

-- Create environment variables.
local cp2k_dir           = "%{INSTALL_DIR}"

family("cp2k")
prepend_path(    "PATH",                pathJoin(cp2k_dir, "bin"))
prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/cp2k_2.6.2/modulefiles")
setenv( "TACC_%{MODULE_VAR}_DIR",                cp2k_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(cp2k_dir, "bin"))
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

