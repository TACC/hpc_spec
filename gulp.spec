#
# W. Cyrus Proctor
# 2015-09-01
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
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
%define pkg_base_name gulp
%define MODULE_VAR    GULP

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
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
License:   Free for academic use
Group:     Applications/Physics
URL:       http://nanochemistry.curtin.edu.au/gulp
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tgz
Patch0:    mkgulp.patch

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
GULP is a program for performing a variety of types of simulation on materials
using boundary conditions of 0-D (molecules and clusters), 1-D (polymers), 2-D
(surfaces, slabs and grain boundaries), or 3-D (periodic solids). The focus of
the code is on analytical solutions, through the use of lattice dynamics, where
possible, rather than on molecular dynamics. A variety of force fields can be
used within GULP spanning the shell model for ionic materials, molecular
mechanics for organic systems, the embedded atom model for metals and the
reactive REBO potential for hydrocarbons. Analytic derivatives are included up
to at least second order for most force fields, and to third order for many.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
GULP is a program for performing a variety of types of simulation on materials
using boundary conditions of 0-D (molecules and clusters), 1-D (polymers), 2-D
(surfaces, slabs and grain boundaries), or 3-D (periodic solids). The focus of
the code is on analytical solutions, through the use of lattice dynamics, where
possible, rather than on molecular dynamics. A variety of force fields can be
used within GULP spanning the shell model for ionic materials, molecular
mechanics for organic systems, the embedded atom model for metals and the
reactive REBO potential for hydrocarbons. Analytic derivatives are included up
to at least second order for most force fields, and to third order for many.

%description
GULP is a program for performing a variety of types of simulation on materials
using boundary conditions of 0-D (molecules and clusters), 1-D (polymers), 2-D
(surfaces, slabs and grain boundaries), or 3-D (periodic solids). The focus of
the code is on analytical solutions, through the use of lattice dynamics, where
possible, rather than on molecular dynamics. A variety of force fields can be
used within GULP spanning the shell model for ionic materials, molecular
mechanics for organic systems, the embedded atom model for metals and the
reactive REBO potential for hydrocarbons. Analytic derivatives are included up
to at least second order for most force fields, and to third order for many.

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
%patch0 -p0

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
module load TACC
module load %{comp_module}
module load %{mpi_module}
module load fftw3
module list

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


 
#################################################
export gulp=`pwd`
export gulp_install=%{INSTALL_DIR}
#################################################
 
# Serial Version
cd "${gulp}"/Src
rm -rf ${gulp}/Src/Linu*
"${gulp}"/Src/mkgulp -c intel -f
mkdir -p ${gulp_install}/bin
mv gulp ${gulp_install}/bin/gulp

# MPI Version
cd ${gulp}/Src
rm -rf ${gulp}/Src/Linu*
"${gulp}"/Src/mkgulp -c intel -m -f
mkdir -p ${gulp_install}/bin
mv gulp ${gulp_install}/bin/gulp.mpi

cd "${gulp}"
cp -ar Libraries ${gulp_install}/Libraries
cp -ar Docs      ${gulp_install}/Docs
cp -ar Utils     ${gulp_install}/Utils
cp -ar Examples  ${gulp_install}/Examples

# 
# export gulp_major=%{major_version}
# export gulp_minor=%{minor_version}
# export gulp_patch=%{micro_version}
# export gulp_version=${gulp_major}.${gulp_minor}
# 
# cd ${gulp}
# cp %{_sourcedir}/gulp-${gulp_version}.tgz ${gulp}
# tar xvfz gulp-${gulp_version}.tgz
# 
# # Serial Version
# cd ${gulp}/gulp-${gulp_version}/Src
# cat > getmachine << 'EOF'
# mkdir -p Linux
# cd Linux
# echo "RUNF90=ifort"       > makefile
# echo "RUNCC=icc"         >> makefile
# echo "FFLAGS=-I.."       >> makefile
# echo "CFLAGS=-I.."       >> makefile
# echo "LIBS=-mkl"         >> makefile
# echo "OPT=-O2"           >> makefile
# echo "OPT1=-O1"          >> makefile
# echo "OPT2='-O3 -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512'" >> makefile
# echo "DEFS="             >> makefile
# cat ../Makefile          >> makefile
# target=${1}_
# make ${target}
# mkdir -p ${gulp_install}/bin
# mv gulp ${gulp_install}/bin/gulp
# EOF
# make
# 
# # MPI Version
# make -i clean
# cd ${gulp}/gulp-${gulp_version}/Src
# cat > getmachine << 'EOF'
# mkdir -p Linux
# cd Linux
# echo "RUNF90=mpif90"      > makefile
# echo "RUNCC=mpicc"       >> makefile
# echo "FFLAGS=-I.."       >> makefile
# echo "CFLAGS=-I.."       >> makefile
# echo "LIBS=-mkl"         >> makefile
# echo "OPT=-O2"           >> makefile
# echo "OPT1=-O1"          >> makefile
# echo "OPT2='-O3 -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512'" >> makefile
# echo "DEFS=-DMPI"        >> makefile
# cat ../Makefile          >> makefile
# target=${1}_
# make ${target}
# mkdir -p ${gulp_install}/bin
# mv gulp ${gulp_install}/bin/gulp.mpi
# EOF
# make
# 
# cd ${gulp}/gulp-${gulp_version}
# cp -ar Libraries ${gulp_install}/Libraries
# cp -ar Docs  ${gulp_install}/Docs


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

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
local help_msg=[[
GULP is a program for performing a variety of types of simulation on materials
using boundary conditions of 0-D (molecules and clusters), 1-D (polymers), 2-D
(surfaces, slabs and grain boundaries), or 3-D (periodic solids). The focus of
the code is on analytical solutions, through the use of lattice dynamics, where
possible, rather than on molecular dynamics. A variety of force fields can be
used within GULP spanning the shell model for ionic materials, molecular
mechanics for organic systems, the embedded atom model for metals and the
reactive REBO potential for hydrocarbons. Analytic derivatives are included up
to at least second order for most force fields, and to third order for many.

The %{MODULE_VAR} module file defines the following environment variables:\n
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_DOC, and TACC_%{MODULE_VAR}_BIN.

The gulp executables are located in $TACC_%{MODULE_VAR}_BIN as gulp and gulp.mpi


Version %{version}
]]

--help(help_msg)
help(help_msg)


local err_message = [[
You do not have access to Gulp!

GULP is available for free for academic use by anyone with a valid University
email account. Users must provide license or demonstrate academic usership and
must request to be added to GULP user UNIX group through TACC User Portal
Attention: cproctor@tacc.utexas.edu

]]

local group  = "G-801978"
local grps   = capture("groups")
local found  = false
local isRoot = tonumber(capture("id -u")) == 0
local isBuild = tonumber(capture("id -u")) == 500
for g in grps:split("[ \n]") do
  if (g == group or isRoot or isBuild)  then
    found = true
    break
  end
end

whatis("Name: gulp")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: Applications/Physics")
whatis("Description: Gulp - A lattice dynamics program")
whatis("URL: http://nanochemistry.curtin.edu.au/gulp")

if (found) then
  setenv("TACC_%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
  setenv("TACC_%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/Libraries")
  setenv("TACC_%{MODULE_VAR}_DOC", "%{INSTALL_DIR}/Docs")
  setenv("TACC_%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

  prepend_path("PATH", "%{INSTALL_DIR}/bin")

  setenv("GULP_LIB", "%{INSTALL_DIR}/Libraries")
  setenv("GULP_DOC", "%{INSTALL_DIR}/Docs")
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
  
  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(750,root,G-801978)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(755,root,install)
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
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

