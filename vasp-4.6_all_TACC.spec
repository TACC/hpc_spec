#
# 
# VASP-4.6_all_TACC.spec
# 
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

Summary: Vienna Ab-Initio Simulation Package

# Give the package a base name
%define pkg_base_name vasp
%define MODULE_VAR    VASP

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 6
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

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
License:   VASP
Group:     Applications/Chemistry
URL:       https://www.vasp.at/
Packager:  TACC - hliu@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}_all_TACC.tar.gz
#Source0:   %{pkg_base_name}-%{pkg_version}.tar.bz2
#Source1:   libint-1.1.5.tar.gz
#Source2:   libxc-2.0.1.tar.gz

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

%setup -n %{pkg_base_name}-%{pkg_version}_all_TACC


#---------------------------------------
%build
#---------------------------------------
%include compiler-load.inc
%include mpi-load.inc

module load fftw3

cd vasp.4.lib
make

cd ../vasp.4.6

make -f Makefile.hliu.opt clean
make -f Makefile.hliu.opt
mv vasp vasp_std

make -f Makefile.hliu.opt.gamma clean
make -f Makefile.hliu.opt.gamma
mv vasp vasp_gamma


make -f Makefile.hliu.opt.ncl clean
make -f Makefile.hliu.opt.ncl
mv vasp vasp_ncl

cd ../vasp.4.6.vtst

cd ../vasp.4.6.vtst

make -f Makefile.hliu.opt.vtst clean
make -f Makefile.hliu.opt.vtst
mv vasp vasp_std_vtst

make -f Makefile.hliu.opt.gamma.vtst clean
make -f Makefile.hliu.opt.gamma.vtst
mv vasp vasp_gamma_vtst


make -f Makefile.hliu.opt.ncl.vtst clean
make -f Makefile.hliu.opt.ncl.vtst
mv vasp vasp_ncl_vtst



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
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/*
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

cd vasp.4.6
cp vasp_std $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_gamma $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_ncl $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cd ../vasp.4.6.vtst
cp vasp_std_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_gamma_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cp vasp_ncl_vtst $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.
cd ..
cp -r vtstscripts $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/.


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

The TACC VASP module appends the path to the vasp executables
to the PATH environment variable.  Also TACC_VASP_DIR, and
TACC_VASP_BIN are set to VASP home and bin directories.

Users have to show their licenses and be confirmed by
VASP team that they are registered users under that licenses
Scan a copy the license and send to hliu@tacc.utexas.edu

The VASP executables are
vasp_std: compiled with pre processing flag: -DNGZhalf
vasp_gamma: compiled with pre processing flag: -DNGZhalf -DwNGZhalf
vasp_ncl: compiled without above pre processing flags
vasp_std_vtst: vasp_std with TST
vasp_gamma_vtst: vasp_gamma with TST
vasp_ncl_vtst: vasp_ncl with TST
vtstscripts/: utility scripts of TST



Version %{version}
]]

local err_message = [[
You do not have access to VASP.4.6!


Users have to show their licenses and be confirmed by the 
VASP team that they are registered users under that license.
Scan a copy of the license and send it to hliu@tacc.utexas.edu
]]

local group  = "G-800548"
local grps   = capture("groups")
local found  = false
local isRoot = tonumber(capture("id -u")) == 0
for g in grps:split("[ \n]") do
   if (g == group or isRoot)  then
      found = true
      break
    end
end

whatis("Version: %{pkg_version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Density Functional Theory, Molecular Dynamics")
whatis("URL:https://www.vasp.at/")
whatis("Description: Vienna Ab-Initio Simulation Package")

--help(help_msg)
help(help_msg)

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
  
  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

# %defattr(-,root,install,)
%defattr(750,root,G-800548)
# RPM package contains files within these directories
%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

#  %defattr(-,root,install,)
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

