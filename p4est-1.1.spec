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

Summary: P4est rpm build script

# Give the package a base name
%define pkg_base_name p4est
%define MODULE_VAR    P4EST

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 1

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
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

Release:   2
License:   GPL
Vendor: https://github.com/cburstedde/p4est
Group: Carsten Burstedde
Source: p4est-%{pkg_version}.tar.gz
Packager:  TACC - eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: P4est local binary install
Group: Numerical library

%package %{MODULEFILE}
Summary: P4est local binary install
Group: Numerical library

%description
%description package
P4EST has octree forest support for dealii
%description modulefile
P4EST has octree forest support for dealii


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
%include compiler-load.inc
%include mpi-load.inc

export modulefilename=%{pkg_version}

# Insert necessary module commands
module load boost cmake phdf5 parallel-netcdf python2 swig
# python

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

export P4EST_DIR=`pwd`
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

cd /admin/rpms/SOURCES
CC=mpicc CXX=mpicxx sh ./p4est-setup.sh p4est-%{pkg_version}.tar.gz %{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
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
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{pkg_version}.lua << EOF
help( [[
The P4EST modulefile defines the following environment variables:
TACC_P4EST_DIR, TACC_P4EST_LIB, and TACC_P4EST_INC 
for the location of the P4EST %{version} distribution, 
libraries, and include files, respectively.\n

Version %{pkg_version}
]] )

whatis( "Name: P4est 'p4-est of octrees'" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${pkg_version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://github.com/cburstedde/p4est" )
whatis( "Description: octree support for dealii" )

local             p4est_dir =     "%{INSTALL_DIR}/FAST"

prepend_path("LD_LIBRARY_PATH", pathJoin(p4est_dir,petsc_arch,"lib") )

setenv(          "P4EST_DIR",             p4est_dir)
setenv(          "TACC_P4EST_DIR",        p4est_dir)
setenv(          "TACC_P4EST_BIN",        pathJoin(p4est_dir,"bin"))
setenv(          "TACC_P4EST_LIB",        pathJoin(p4est_dir,petsc_arch,"lib"))
setenv(          "TACC_P4EST_INC",        pathJoin(p4est_dir,petsc_arch,"include"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{pkg_version} << EOF
#%Module1.0##################################################
##
## version file for p4est
##
 
set     ModulesVersion      "%{pkg_version}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua

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

%changelog
#
* Sat Aug 19 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: adding bin to modulefile
* Wed Jun 21 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
