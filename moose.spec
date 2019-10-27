Summary: Moose install

# Give the package a base name
%define pkg_base_name moose
%define MODULE_VAR    MOOSE

# Create some macros (spec file variables)
%define major_version git20191007
%define minor_version 1

%define MOOSE_PETSC_VERSION 3.11

%define pkg_version %{major_version}

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

Release: 3%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tgz
URL: http://mooseframework.org/
Vendor: Idaho National Labs
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: The Multiphysics Object-Oriented Simulation Environment (MOOSE) is a finite-element, multiphysics framework primarily developed by Idaho National Laboratory. 
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: The Multiphysics Object-Oriented Simulation Environment (MOOSE) is a finite-element, multiphysics framework primarily developed by Idaho National Laboratory. 
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
The Multiphysics Object-Oriented Simulation Environment (MOOSE) is a finite-element, multiphysics framework primarily developed by Idaho National Laboratory. It provides a high-level interface to some of the most sophisticated nonlinear solver technology on the planet. MOOSE presents a straightforward API that aligns well with the real-world problems scientists and engineers need to tackle. Every detail about how an engineer interacts with MOOSE has been thought through, from the installation process through running your simulation on state of the art supercomputers, the MOOSE system will accelerate your research.
%description %{MODULEFILE}
The Multiphysics Object-Oriented Simulation Environment (MOOSE) is a finite-element, multiphysics framework primarily developed by Idaho National Laboratory. It provides a high-level interface to some of the most sophisticated nonlinear solver technology on the planet. MOOSE presents a straightforward API that aligns well with the real-world problems scientists and engineers need to tackle. Every detail about how an engineer interacts with MOOSE has been thought through, from the installation process through running your simulation on state of the art supercomputers, the MOOSE system will accelerate your research.

%prep

%setup -n moose-%{version}

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

%if "%{comp_fam}" == "intel"
  echo "Intel support officially terminated"
  exit 1
%endif

module list
module load boost petsc/%{MOOSE_PETSC_VERSION}

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

####
#### Make in tmpfs
####
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

( cd /tmp \
  && rm -rf moose-git \
  && git clone https://github.com/idaholab/moose.git moose-git \
  && ( cd moose-git && git checkout master ) \
  && cp -r moose-git/. %{INSTALL_DIR} \
  && rm -rf moose-git \
)

pushd %{INSTALL_DIR}
ls
ls examples

export CC=mpicc
export CXX=mpicxx
# this is TACC_INTEL_LIB
export ADDITIONAL_LIBS=export ADDITIONAL_LIBS=/opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64/libirc.so

./scripts/update_and_rebuild_libmesh.sh \
    2>&1 | tee /tmp/moose.log
cd modules/combined
make -j 8

ls examples
cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
popd
umount %{INSTALL_DIR}

rm -rf /tmp/moose-git

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The moose module defines the following environment variables:
TACC_MOOSE_DIR, TACC_MOOSE_BIN, and
TACC_MOOSE_LIB for the location
of the Moose distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Moose" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/moose/moose-as/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             moose_arch =    "${architecture}"
local             moose_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(moose_dir,moose_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(moose_dir,moose_arch,"lib") )

setenv("MOOSE_ARCH",            moose_arch)
setenv("MOOSE_DIR",             moose_dir)
setenv("TACC_MOOSE_DIR",        moose_dir)
setenv("TACC_MOOSE_BIN",        pathJoin(moose_dir,moose_arch,"bin") )
setenv("TACC_MOOSE_INC",        pathJoin(moose_dir,moose_arch,"include") )
setenv("TACC_MOOSE_LIB",        pathJoin(moose_dir,moose_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Moose %version
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
* Mon Oct 07 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: new git pull
* Mon Jul 29 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: completely redone
* Thu Jun 22 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
