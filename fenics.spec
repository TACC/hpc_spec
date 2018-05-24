Summary: Fenics install

# Give the package a base name
%define pkg_base_name fenics
%define MODULE_VAR    FENICS

# Create some macros (spec file variables)
%define major_version 2018may
#%define minor_version 10
#%define micro_version 1

%define pkg_version %{major_version}
#.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 6%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tgz
URL: https://fenicsproject.org/
Vendor: Fenics project
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: FEniCS is a popular open-source (LGPLv3) computing platform for solving partial differential equations (PDEs). 
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: FEniCS is a popular open-source (LGPLv3) computing platform for solving partial differential equations (PDEs). 
Group: Development/Numerical-Libraries

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

%prep

%setup -n fenics
#-%{version}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include compiler-load.inc
%include mpi-load.inc

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

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
# from the commandline:
# ./fenics.download /tmp/fenics-stuff/

# for some reason we can't do it here:
# ( cd ${FENICS_DIR} ; . %{_topdir}/SPECS/fenics.download )

rm -f ${LOG_DIR}/fenics_install.log
( cd ${FENICS_DIR} ; %{_topdir}/SPECS/fenics.install %{INSTALL_DIR} %{_topdir}/SPECS )

cp -r %{INSTALL_DIR}/{fiat,instant,dijitso,ufl,ffc,eigen,dolfin,mshr} \
      ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
#cp -r %{INSTALL_DIR}/python ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

##
## extra python paths have been written out:
##
export PYTHON_EXTRA_PATHS=`cat ${LOG_DIR}/fenics.pythonpath | sed 's/.//'`
echo "Deduced extra python paths: ${PYTHON_EXTRA_PATHS}"

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The fenics module defines the environment variables:
TACC_FENICS_DIR for the location of the Fenics distribution,
TACC_DOLFIN_DIR/INC/LIB for the dolfin library;
it also updates PYTHONPATH.
Fenics requires python3.

Version %{version}
]] )

whatis( "Name: Fenics" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://fenicsproject.org/" )
whatis( "Description: Fenics, finite element package" )

local             fenics_dir   = "%{INSTALL_DIR}/"

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"ufl","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"ufl","lib/python3.6/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"mshr","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"mshr","lib/python3.6/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"instant","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"instant","lib/python3.6/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"fiat","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"fiat","lib/python3.6/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"ffc","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"ffc","lib/python3.6/site-packages") )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"dolfin","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"dolfin","lib/python3.6/site-packages") )
prepend_path("CMAKE_PREFIX_PATH", pathJoin(fenics_dir,"dolfin","share","dolfin","cmake" ) )
prepend_path("CMAKE_MODULE_PATH", pathJoin(fenics_dir,"dolfin","share","dolfin","cmake" ) )

setenv("TACC_FENICS_DIR",        fenics_dir)
setenv("DOLFIN_DIR", pathJoin(fenics_dir,"dolfin" ) )
setenv("TACC_DOLFIN_DIR", pathJoin(fenics_dir,"dolfin" ) )
setenv("TACC_DOLFIN_BIN", pathJoin(fenics_dir,"dolfin","bin" ) )
setenv("TACC_DOLFIN_INC", pathJoin(fenics_dir,"dolfin","include" ) )
setenv("TACC_DOLFIN_LIB", pathJoin(fenics_dir,"dolfin","lib" ) )
setenv("DOLFIN", pathJoin(fenics_dir,"dolfin","share","dolfin","cmake","DOLFINConfig.cmake" ) )

prepend_path("LD_LIBRARY_PATH", pathJoin(fenics_dir,"dijitso","lib" ) )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"dijitso","lib/python3.6/site-packages") )

always_load("boost")
EOF

%if "%{comp_fam}" == "gcc"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF

setenv( "CC",    "/opt/apps/gcc/7.1.0/bin/gcc" )
setenv( "CXX",   "/opt/apps/gcc/7.1.0/bin/g++" )
setenv( "FC",    "/opt/apps/gcc/7.1.0/bin/gfortran" )
EOF
%endif

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Fenics %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Tue May 15 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 6 UNRELEASED : more dolfin fix, also re-clone everythin
* Wed May 02 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 5 : fixed the dolfin installation
* Sun Dec 03 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: load boost, redefine compiler macros damn-the-torpedoes
* Thu Sep 21 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: more variables thanks to David Kamensky (ticket 40339)
* Fri Aug 25 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: much LD_LIBRARY_PATH
* Fri Jul 28 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
