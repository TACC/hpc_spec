# Carlos Rosales-Fernandez (carlos@tacc.utexas.edu)
# 2017-05-22
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
%define pkg_base_name siesta
%define MODULE_VAR    SIESTA

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
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
License:   GPL
Group:     Applications/Chemistry
URL:       http://www.icmab.es/siesta/
Packager:  TACC - carlos@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


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
Siesta (Spanish Initiative for Electronic Simulations with Thousands of Atoms)
is both a method and its computer program implementation, to perform electronic
structure calculations and ab initio molecular dynamics simulations of
molecules and solids.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

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

# Insert further module commands

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


# Mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}

# Prepare the build directory
cd ./Obj
sh ../Src/obj_setup.sh
cp ../Src/Sys/stampede_intel_mkl.make ./arch.make

# Build siesta
CC=icc CXX=icpc make
mkdir %{INSTALL_DIR}/bin
cp siesta %{INSTALL_DIR}/bin

# Build transiesta
make clean
CC=icc CXX=icpc make transiesta
cp transiesta %{INSTALL_DIR}/bin

mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r ../Examples %{INSTALL_DIR}
cp -r ../Tutorials %{INSTALL_DIR}
cp -r ../Docs %{INSTALL_DIR}

# Build Utilities
cd ../Util
sh ./build_all.sh
cp ./COOP/dm_creator %{INSTALL_DIR}/bin
cp ./COOP/mprop %{INSTALL_DIR}/bin
cp ./TBTrans/tbtrans %{INSTALL_DIR}/bin
cp ./Denchar/Src/denchar %{INSTALL_DIR}/bin
cp ./STM/ol-stm/Src/stm %{INSTALL_DIR}/bin
cp ./STM/simple-stm/plstm %{INSTALL_DIR}/bin
cp ./Gen-basis/gen-basis %{INSTALL_DIR}/bin
cp ./Gen-basis/ioncat %{INSTALL_DIR}/bin
cp ./Gen-basis/ionplot.sh %{INSTALL_DIR}/bin

mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount                                   %{INSTALL_DIR}

  
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
local help_message=[[
This module loads Siesta built with Intel 17 and Intel MPI 17.
This module makes available the following executables:

siesta
transiesta

as well as the following utilities:

tbtrans
denchar
dm_creator
mprop
stm
plstm
gen-basis
ioncat

In order to run siesta please create a link to the binary inside the execution
directory, and make sure your submission script contains the lines:

module load siesta
ibrun ./siesta < input.fdf

As of version 4.0 Siesta no longer provides the Atom program to generate 
pseudopotentials. Please go to this addresss in order to obtain one:

http://nninc.cnf.cornell.edu/

Version 4.0
]]

help(help_message,"\n")

whatis("Siesta")
whatis("Version: 4.0")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Molecular Dynamics, Application")
whatis("Description: Spanish Initiative for Electronic Simulations with Thousands of Atoms")
whatis("URL: http://www.icmab.es/siesta/")

help(help_message,"\n")

setenv("TACC_SIESTA_DIR","/opt/apps/intel17/impi/siesta/4.0")
setenv("TACC_SIESTA_BIN","/opt/apps/intel17/impi/siesta/4.0/bin")
prepend_path("PATH","/opt/apps/intel17/impi/siesta/4.0/bin")

EOF

# Version File
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

