#
# Spec file for vtk
# Original spec by Greg Abram 
# Changed to a relocatable RPM by Dave Semeraro 8/2018
# Follows Bar.spec example by Cyrus Proctor and Antonio Gomez
#
# NOTE: this file depends on various include files that may or may not
#       exist on various platforms. So, while the rpm file is relocatable this
#       spec file may not be.
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
# ./build_rpm.sh -l --intel=18 --impi=18_0 vtk-8.1.1.spec
#
# After the build to deploy this package type the following :
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps tacc-vtk-intel18-impi18_0-package-8.1.1-0.el7.centos.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps tacc-vtk-intel18-impi18_0-modulefile-8.1.1-0.el7.centos.x86_64.rpm
# To remove the packages type the following:
# rpm -e tacc-vtk-intel18-impi18_0-package-8.1.1-0.el7.centos.x86_64 tacc-vtk-intel18-impi18_0-modulefile-8.1.1-0.el7.centos.x86_64

Summary:  vtk 9.0.1 local binary install

# Give the package a base name
%define pkg_base_name vtk
%define MODULE_VAR    VTK

# Create some macros (spec file variables). This is how we specify the version of
# VTK that we are packaging. For Example VTK-8.1.1 would have major_version
# set to 8, minor_version set to 1, and micro_version set to 1.

%define major_version 9
%define minor_version 0
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

# These bits control name compiler and mpi flovor deps. 
# VTK depends on the compiler not so sure about mpi. 
%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################
Release:  0%{?dist}
License:  BSD
URL:   https://www.vtk.org
Vendor:   vtk.org
Group:    Visualization
Packager:  TACC - semeraro@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%define VTK_SRC vtk.%{version}.%{comp_fam_ver}.%{mpi_fam_ver}.%{release}.tar.gz

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
The VTK package conains the VTK visualization software from Kitware. The package
contains the precompiled binary and any libraries and include files needed to 
support visualization application development.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
The module sets the required user environment needed to utilize VTK on TACC systems. It
sets paths to executables and modifies LD_LIBRARY_PATH

%description
The Visualization Toolkit (VTK) is a software library used for the construction of visualization applications. VTK forms the basis of the visualization bits of Paraview and VisIt. 
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
echo "prep MODULE_PREFIX:    %{MODULE_PREFIX}"
echo "prep MODULE_DIR:    %{MODULE_DIR}"
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

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

echo "Install before tar MODULE_PREFIX:    %{MODULE_PREFIX}"
echo "Install before tar MODULE_DIR:    %{MODULE_DIR}"
        mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

        #######################################
        ##### Create TACC Canary Files ########
        #######################################
        touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
        #######################################
        ########### Do Not Remove #############
        #######################################
        cd $RPM_BUILD_ROOT/%{INSTALL_DIR}
        tar xvzf %{_sourcedir}/%{VTK_SRC}
echo "Install after tar MODULE_PREFIX:    %{MODULE_PREFIX}"
echo "Install after tar MODULE_DIR:    %{MODULE_DIR}"

        #test -e current && /bin/rm -f current
        #ln -s %{pkg_version} current

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#-----------------------
%if %{?BUILD_MODULEFILE}
#-----------------------

echo "install module MODULE_PREFIX:    %{MODULE_PREFIX}"
echo "install module MODULE_DIR:    %{MODULE_DIR}"
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

whatis("Name: vtk")
whatis("Version: %{pkg_version}")
whatis("Category: application, visualization")
whatis("Description: a C++ visualization library")
whatis("URL: https/www.vtk.org")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

local vtk_dir ="%{INSTALL_DIR}"

family("vtk")

--conflict vtk
prereq("qt")

prepend_path("PATH",pathJoin(vtk_dir,"bin"))
prepend_path("LD_LIBRARY_PATH",pathJoin(vtk_dir,"lib64"))
prepend_path("INCLUDE",pathJoin(vtk_dir,"include"))
prepend_path("PYTHONPATH",pathJoin(vtk_dir,"lib64/python3.7/site-packages"))
prepend_path("PYTHONPATH",pathJoin(vtk_dir,"lib64/site-packages/mpi4py"))

setenv("TACC_%{MODULE_VAR}_DIR", vtk_dir)
setenv("TACC_%{MODULE_VAR}_INC", pathJoin(vtk_dir,"include"))
setenv("TACC_%{MODULE_VAR}_LIB", pathJoin(vtk_dir,"lib64"))
setenv("TACC_%{MODULE_VAR}_BIN", pathJoin(vtk_dir,"bin"))
setenv("VTK_LOCATION",vtk_dir)
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1#################################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion     "%{version}"
EOF

  # Check the syntax of the generated lua modulefile
  ### don't check the hidden one!
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#-------------------------
%endif # BUILD_MODULEFILE |
#-------------------------

#-----------------------
%if %{?BUILD_PACKAGE}
%files package
#-----------------------

%defattr(-,root,install,)
%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#-----------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#-----------------------

%defattr(-,root,install,)
# RPM package contains files withi these directories
%{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
%clean
rm -rf $RPM_BUILD_ROOT
