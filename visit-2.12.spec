#
# Spec file for visit visualization tool installation.
# Changed to a relocatable RPM by Dave Semeraro 4/2017.
# Follows Bar.spec example by Cyrus Proctor and Antonio Gomez
#
# NOTE: this file depends on various include files that may or may not
# 	exist on various platforms. So, while the rpm file is relocatable this
# 	spec file may not be. 
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# To build this package type the following in the SPEC directory:
# ./build_rpm.sh -l --intel=17 --impi=17_0 visit-2.12.spec
#
# After the build to deploy this package type the following :
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps tacc-visit-intel17-impi17_0-package-2.12.0-1.el7.centos.x86_64.rpm 
# rpm -i --relocate /tmpmod=/opt/apps tacc-visit-intel17-impi17_0-modulefile-2.12.0-1.el7.centos.x86_64.rpm
# To remove the packages type the following:
# rpm -e tacc-visit-intel17-impi17_0-package-2.12.0-1.el7.centos.x86_64 tacc-visit-intel17-impi17_0-modulefile-2.12.0-1.el7.centos.x86_64

# I had to put this command in because rpmbuild tries to compile python files
# and some of the python files in this distro are not compiling and causing the
# build to fail. This command lets the build continue failures or not. 
%global _python_bytecompile_errors_terminate_build 0

Summary:  spec file to generate relocatable rpm for the visit visualization software

# Give the package a base name
%define pkg_base_name visit
%define MODULE_VAR    visit

# Create some macros (spec file variables). This is how we specify the version of
# VisIt that we are packaging. For Example VisIt-2.12.0 would have major_version
# set to 2, minor_version set to 12, and micro_version set to 0. 

%define major_version 2
%define minor_version 12
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

# These bits control name compiler and mpi flavor deps. 
# VisIt is both compiler and mpi dependent.
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
Release:  1%{?dist}
License:  GPL
URL:   https://wci.llnl.gov/simulation/computer-codes/visit
Group:    Visualization 
Packager:  TACC - semeraro@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%define VISIT_SRC visit.%{version}.%{comp_fam_ver}.%{mpi_fam_ver}.%{release}.tar.gz

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
The visit package conains the visit visualization software from LLNL. The package 
contains the precompiled binary and any libraries needed to support the various 
third party components  

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
The module sets the required user environment needed to run VisIt on TACC systems. It
sets paths to executables and modifies LD_LIBRARY_PATH  

%description 
The VisIt visualization software supports visualization of large scale scientific data 
in a variety of formats. The software runs in parallel or serial on a variety of compute
platforms. VisIt supports a large number of visualization methods. It also supports 
python scripting for batch use 

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# there is nothing to setup because the rpm does not compile anything. 
#%setup -n %{pkg_base_name}-%{pkg_version}

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
#%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

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
	cd $RPM_BUILD_ROOT/%{INSTALL_DIR}
	tar xvzf %{_sourcedir}/%{VISIT_SRC}

	test -e current && /bin/rm -f current
	ln -s %{pkg_version} current

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#-----------------------
%if %{?BUILD_MODULEFILE}
#-----------------------

 mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
help([[
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC, and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively. 
]])

--help(help_msg)
--help(help_msg)


whatis("Name: visit")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: application, visualization")
whatis("Description: a parallel visualization suite based in part on VTK")
whatis("URL: https://wci.llnl.gov/simulation/computer-codes/visit")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

local visit_dir = "%{INSTALL_DIR}"

family("visit")

--conflict visit
prereq("swr")

set_alias("visit", "visit -v %{version}")

prepend_path("PATH",pathJoin(visit_dir,"bin"))
prepend_path("PYTHONPATH",pathJoin(visit_dir,"current/linux-x86_64/lib/site-packages/visit"))
prepend_path("INCLUDE",pathJoin(visit_dir,"current/linux-x86_64/include"))
prepend_path("LD_LIBRARY_PATH",pathJoin(visit_dir,"current/linux-x86_64/lib"))

setenv("TACC_%{MODULE_VAR}_DIR", visit_dir)
setenv("TACC_%{MODULE_VAR}_INC", pathJoin(visit_dir,"%{version}/linux-x86_64/include"))
setenv("TACC_%{MODULE_VAR}_LIB", pathJoin(visit_dir,"%{version}/linux-x86_64/lib"))
setenv("TACC_%{MODULE_VAR}_BIN", pathJoin(visit_dir,"%{version}/linux-x86_64/bin"))
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1#################################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion     "%{version}"
EOF

# check the syntax of the generated lua modulefile only if a visible module
%if %{?VISIBLE}
 %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
%endif


#-------------------------
%endif # BUILD_MODULEFILE |
#-------------------------

#-----------------------
%if %{?BUILD_PACKAGE}
%files package
#-----------------------

%defattr(-,root,install)
# RPM package contains files withi these directories
%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#-----------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#-----------------------

%defattr(-,root,install)
# RPM package contains files withi these directories
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
# change the host file to point to the correct install directory
%define whereitallgoes ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}
#echo "package installed in ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"
#echo "where it all goes %{whereitallgoes}"
sed -e "s:VISITINSTALLDIR:%{whereitallgoes}:"  %{whereitallgoes}/current/.visit/hosts/dummy.xml > %{whereitallgoes}/current/.visit/hosts/host_tacc_stampede.xml 
chmod a+r %{whereitallgoes}/current/.visit/hosts/host_tacc_stampede.xml
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

%clean
rm -rf $RPM_BUILD_ROOT
