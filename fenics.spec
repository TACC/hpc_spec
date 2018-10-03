#
# Fenics finite element package
# spec file by Victor Eijkhout
#
# Adapted from Bar.spec, Cyrus Proctor & Antonio Gomez
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

Summary: Fenics rpm build script

# Give the package a base name
%define pkg_base_name fenics
%define MODULE_VAR    FENICS

# Create some macros (spec file variables)
%define major_version 2018Jun

%define pkg_version %{major_version}

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

Release:   3
License:   GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tgz
URL: https://fenicsproject.org/
Vendor: Fenics project
Packager: TACC -- eijkhout@tacc.utexas.edu
## Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: FEniCS is a popular open-source (LGPLv3) computing platform for solving partial differential equations (PDEs). 
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile

%description
%description %{PACKAGE}
FEniCS is a popular open-source (LGPLv3) computing platform for
solving partial differential equations (PDEs). 
FEniCS enables users to
quickly translate scientific models into efficient finite element
code. With the high-level Python and C++ interfaces to FEniCS, it is
easy to get started, but FEniCS offers also powerful capabilities for
more experienced programmers. FEniCS runs on a multitude of platforms
ranging from laptops to high-performance clusters.

%description %{MODULEFILE}
FEniCS is a popular open-source (LGPLv3) computing platform for
solving partial differential equations (PDEs). FEniCS enables users to
quickly translate scientific models into efficient finite element
code. With the high-level Python and C++ interfaces to FEniCS, it is
easy to get started, but FEniCS offers also powerful capabilities for
more experienced programmers. FEniCS runs on a multitude of platforms
ranging from laptops to high-performance clusters.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n fenics-%{version}

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

# VLE here is where we start copying from the old spec file
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 

module load cmake boost python3 swig
module load gsl petsc phdf5
# trilinos : gives problems with the STKdoc_tests

%if "%{comp_fam}" == "gcc"
FENICS_C_COMPILER=gcc
FENICS_X_COMPILER=g++
%else
FENICS_C_COMPILER=icc
FENICS_X_COMPILER=icpc
%endif

export LOG_DIR=%{_topdir}/SPECS

##
## download sources in /tmp
##
export FENICS_DIR=/tmp/fenics-stuff
if [ ! -d ${FENICS_DIR} ] ; then 
  echo "%%%%%%%%%%%%%%%%"
  echo "There is no FENICS_STUFF dir"
  echo "%%%%%%%%%%%%%%%%"
  exit 1
fi

# from the commandline:
# ./fenics.download /tmp/fenics-stuff/

# for some reason we can't do it here:
# ( cd ${FENICS_DIR} ; . %{_topdir}/SPECS/fenics.download )

#export BUILD_DIR=%{_topdir}/BUILD/fenics
#export FENICS_DIR=%{INSTALL_DIR}
#export PYTHON_EXTRA_PATHS=

rm -f ${LOG_DIR}/fenics_install.log
( cd ${FENICS_DIR} ; %{_topdir}/SPECS/fenics.install %{INSTALL_DIR} %{_topdir}/SPECS )

cp -r %{INSTALL_DIR}/{fiat,instant,dijitso,ufl,ffc,eigen,dolfin,mshr} ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
#cp -r %{INSTALL_DIR}/python ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

##
## extra python paths have been written out:
##
export PYTHON_EXTRA_PATHS=`cat ${LOG_DIR}/fenics.pythonpath | sed 's/.//'`
echo "Deduced extra python paths: ${PYTHON_EXTRA_PATHS}"

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The fenics module defines the environment variables:
TACC_FENICS_DIR for the location of the Fenics distribution, 
and PYTHONPATH. Fenics requires python3.

Version %{version}
]] )

whatis( "Name: Fenics" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://fenicsproject.org/" )
whatis( "Description: Fenics, finite element package" )

local             fenics_dir   = "%{INSTALL_DIR}/"

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"ufl","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"ufl","lib/python3.5/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"mshr","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"mshr","lib/python3.5/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"instant","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"instant","lib/python3.5/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"fiat","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"fiat","lib/python3.5/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"ffc","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"ffc","lib/python3.5/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"dolfin","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"dolfin","lib/python3.5/site-packages") )
prepend_path("CMAKE_PREFIX_PATH", pathJoin(fenics_dir,"dolfin","share","dolfin","cmake" ) )
prepend_path("CMAKE_MODULE_PATH", pathJoin(fenics_dir,"dolfin","share","dolfin","cmake" ) )
setenv("DOLFIN_DIR", pathJoin(fenics_dir,"dolfin","share","dolfin","cmake" ) )
setenv("DOLFIN", pathJoin(fenics_dir,"dolfin","share","dolfin","cmake","DOLFINConfig.cmake" ) )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"dijitso","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"dijitso","lib/python3.5/site-packages") )

setenv("TACC_FENICS_DIR",        fenics_dir)

setenv( "CC",    "/opt/apps/gcc/5.2.0/bin/gcc" )
setenv( "CXX",   "/opt/apps/gcc/5.2.0/bin/g++" )
setenv( "FC",    "/opt/apps/gcc/5.2.0/bin/gfortran" )

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module1.0#################################################
##
## version file for Fenics %version
##

set     ModulesVersion      "${modulefilename}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

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
* Fri Jun 22 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: re-git, also fixing dolfin
* Wed Dec 06 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: adding CXX and such flags
* Mon Oct 16 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release