# VASP Hang Liu
# 2017-05-03
# Modified for KNL deployment.
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
%define pkg_base_name vasp
%define MODULE_VAR    VASP

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 4
%define micro_version 4.pl2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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
License:   VASP
Group:     Applications/Chemistry
URL:       https://www.vasp.at/
Packager:  TACC - hliu@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}_all_TACC.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The Vienna Ab initio Simulation Package (VASP)
Group: Applications/Chemistry
%description package
The Vienna Ab initio Simulation Package (VASP)

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
The Vienna Ab initio Simulation Package (VASP)
%description
The Vienna Ab initio Simulation Package (VASP)
#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}_all_TACC
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

cd wannier90-1.2/
make lib

cd ../beef
./configure CC=icc --prefix=$PWD
make
make install

cd ../vasp.5.4.4.pl2
make all

cd ../vasp.5.4.4.pl2.vtst
make all

cd ./bin
mv vasp_std vasp_std_vtst
mv vasp_gam vasp_gam_vtst
mv vasp_ncl vasp_ncl_vtst

cd ../../

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/*
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

cd vasp.5.4.4.pl2/bin/
cp vasp_std $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_gam $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_ncl $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.

cd ../../vasp.5.4.4.pl2.vtst/bin
cp vasp_std_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_gam_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_ncl_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cd ../../beef/bin
cp bee $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cd ../../
#cp -r vtstscripts-947 $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.

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
The TACC VASP module appends the path to the vasp executables
to the PATH environment variable.  Also TACC_VASP_DIR, and
TACC_VASP_BIN are set to VASP home and bin directories.

Users have to show their licenses and be confirmed by
VASP team that they are registered users under that licenses
Scan a copy of the license with the license number and send to hliu@tacc.utexas.edu

The VASP executables are
vasp_std: compiled with pre processing flag: -DNGZhalf
vasp_gam: compiled with pre processing flag: -DNGZhalf -DwNGZhalf
vasp_ncl: compiled without above pre processing flags
vasp_std_vtst: vasp_std with VTST
vasp_gam_vtst: vasp_gam with VTST
vasp_ncl_vtst: vasp_ncl with VTST
vtstscripts-947/: utility scripts of VTST
bee: BEEF analysis code

This the VASP.5.4.4.pl2 release.

Version %{version}
]]


whatis("Version: %{pkg_version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Density Functional Theory, Molecular Dynamics")
whatis("URL:https://www.vasp.at/")
whatis("Description: Vienna Ab-Initio Simulation Package")
help(help_message,"\n")


local group = "G-802400"
found = userInGroup(group)


local err_message = [[
You do not have access to VASP.5.4.4.pl2!

Users have to show their licenses and be confirmed that they are registered users under that license.
Raise a ticket on user portal and send the email address that was used on the VASP portal to register
the user as a licensed user so the confirmation can be done online.

]]


if (found) then
local vasp_dir="%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(vasp_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_DIR",                vasp_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(vasp_dir, "bin"))

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

#  %defattr(-,root,install,)
%defattr(750,root,G-802400)
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

