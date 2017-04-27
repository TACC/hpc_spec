#
# W. Cyrus Proctor
# 2015-11-07
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
%define pkg_base_name cantera
%define MODULE_VAR    CANTERA

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
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

Release:   1
License:   BSD
Group:     System/Utils
URL:       http://www.cantera.org
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
Cantera is a suite of object-oriented software tools for problems involving
chemical kinetics, thermodynamics, and/or transport processes. Cantera provides
types (or classes) of objects representing phases of matter, interfaces between
these phases, reaction managers, time-dependent reactor networks, and steady
one-dimensional reacting flows. Cantera is currently used for applications
including combustion, detonations, electrochemical energy conversion and
storage, fuel cells, batteries, aqueous electrolyte solutions, plasmas, and
thin film deposition. Cantera can be used from Python and Matlab, or in
applications written in C++ and Fortran 90.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Cantera is a suite of object-oriented software tools for problems involving
chemical kinetics, thermodynamics, and/or transport processes. Cantera provides
types (or classes) of objects representing phases of matter, interfaces between
these phases, reaction managers, time-dependent reactor networks, and steady
one-dimensional reacting flows. Cantera is currently used for applications
including combustion, detonations, electrochemical energy conversion and
storage, fuel cells, batteries, aqueous electrolyte solutions, plasmas, and
thin film deposition. Cantera can be used from Python and Matlab, or in
applications written in C++ and Fortran 90.

%description
Cantera is a suite of object-oriented software tools for problems involving
chemical kinetics, thermodynamics, and/or transport processes. Cantera provides
types (or classes) of objects representing phases of matter, interfaces between
these phases, reaction managers, time-dependent reactor networks, and steady
one-dimensional reacting flows. Cantera is currently used for applications
including combustion, detonations, electrochemical energy conversion and
storage, fuel cells, batteries, aqueous electrolyte solutions, plasmas, and
thin film deposition. Cantera can be used from Python and Matlab, or in
applications written in C++ and Fortran 90.

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


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-load.inc

# Insert necessary module commands
module load python
module load scons

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
 
export ncores=16

CC=icc CXX=icc F90=ifort FC=ifort F77=ifort scons build -j${ncores} env_vars=all CC=icc CXX=icpc F77=ifort blas_lapack_libs=mkl_rt blas_lapack_dir=${MKLROOT}/lib/intel64 prefix=%{INSTALL_DIR}
scons test -j${ncores}
scons install


  # Copy everything over to the installation directory
  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}/

  
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
local help_message = [[
Cantera is a suite of object-oriented software tools for problems involving
chemical kinetics, thermodynamics, and/or transport processes. Cantera provides
types (or classes) of objects representing phases of matter, interfaces between
these phases, reaction managers, time-dependent reactor networks, and steady
one-dimensional reacting flows. Cantera is currently used for applications
including combustion, detonations, electrochemical energy conversion and
storage, fuel cells, batteries, aqueous electrolyte solutions, plasmas, and
thin film deposition. Cantera can be used from Python and Matlab, or in
applications written in C++ and Fortran 90.


This module defines the environmental variables TACC_%{MODULE_VAR}_DIR,
TACC_%{MODULE_VAR}_BIN and TACC_%{MODULE_VAR}_LIB for the location of 
the main Cantera directory, the binaries, and libraries respectively.

The location of the binary files is also added to your PATH while the 
location of the libaries are added to your LD_LIBRARY_PATH.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: system, utilities")
whatis("Keywords: System, Utility")
whatis("Description: tools for problems involving chemical kinetics, thermodynamics, and/or transport processes.")
whatis("URL: http://www.cantera.org")

-- Export environmental variables
local cantera_dir="%{INSTALL_DIR}"
local cantera_bin=pathJoin(cantera_dir,"bin")
local cantera_lib=pathJoin(cantera_dir,"lib")
setenv("TACC_CANTERA_DIR",cantera_dir)
setenv("TACC_CANTERA_BIN",cantera_bin)
setenv("TACC_CANTERA_LIB",cantera_lib)

-- Prepend the cantera directories to the adequate PATH variables
prepend_path("PATH",cantera_bin)
prepend_path("LD_LIBRARY_PATH",cantera_lib)

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

