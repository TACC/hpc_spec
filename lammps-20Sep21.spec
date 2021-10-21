################################################################
# 
#    LAMMPS SPEC FILE
#
#    MACHINE       :   TACC LONESTAR 6
#    VERSION       :   patch_20Sep2021
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   09-28-2021
#
################################################################

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
#
# rpmbuild -bb --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_0' lammps-20Sep21.spec | tee log_lammps_20Sep21
# rpm -ivh --nodeps --relocate /tmpmod=/opt/apps
# rpm -ivh --nodeps --relocate /tmprpm=/home1/apps
#
%define pkg_base_name lammps
%define MODULE_VAR    LAMMPS

%define major_version 20Sep21
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}

################################################################

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc
#%include name-defines-noreloc.inc

################################################################

Summary:   LAMMPS is a Classical Molecular Dynamics package.
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   1%{?dist}
License:   GPL
Vendor:    Sandia
Group:     applications/chemistry
URL:       http://lammps.sandia.gov
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Packager:  TACC Albert Lu- alu@tacc.utexas.edu

%define    buildroot   /var/tmp/%{name}-%{version}-buildroot

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

################################################################

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
LAMMPS Molecular Dynamics package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
LAMMPS Molecular Dynamics modulefile.

# Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
LAMMPS is a classical molecular dynamics code with the following functionality:
It can be run on a single processor or in parallel.
It is written in highly portable C++.
It is easy to extend with new features and functionality.
It has a syntax for defining and using variables and formulas,
as well as a syntax for looping over runs and breaking out of loops.

################################################################

%prep

%if %{?BUILD_PACKAGE}

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -q -n %{pkg_base_name}-%{pkg_version}

%endif # BUILD_PACKAGE 

%if %{?BUILD_MODULEFILE}

  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif # BUILD_MODULEFILE 

################################################################

%build

%if %{?BUILD_PACKAGE}

  set +x
  %include system-load.inc
  %include compiler-load.inc
  %include mpi-load.inc

  module load intel/19.1.1
  module load impi/19.0.9
  set -x

  mkdir -p bin

  cd src

  make yes-all
  make no-lib
  make no-ext
  make no-gpu
  make no-intel
  make no-kokkos
  make package-status

  # Build LAMMPS

  # Make lammmps (use src/MAKE/MACHINES/Makefile.lonestar)

  cat MAKE/OPTIONS/Makefile.icc_mpich | \
  sed 's/mpicxx -cxx=icc/mpicxx/g' | \
  sed 's/-g -O3 -restrict/-g -O3 -march=core-avx2 -qno-offload -restrict -qopenmp/g' >  \
  MAKE/MACHINES/Makefile.lonestar

  make -j4 lonestar \
  LINKFLAGS="-g -O3 -march=core-avx2 -qno-offload -restrict -qopenmp" \
  FFT_INC="-DFFT_MKL" \
  FFT_LIB="-lmkl_intel_lp64 -lmkl_sequential -lmkl_core"

  mv lmp_lonestar ../bin

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

# INSTALL LAMMPS

%if %{?BUILD_PACKAGE}

  # create bin
  mkdir -p           $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mv bin/lmp_*       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mv potentials      $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials

  chmod -Rf go+x     $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/*
  chmod -Rf go+r     $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials/*

%endif # BUILD_PACKAGE

################################################################

%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua <<EOF
local help_message = [[
LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator)
is a classical molecular dynamics code developed at Sandia
National Laboratories.

- TO RUN LAMMPS

Set the number of nodes (N) and MPI tasks (n) in the job script.

  E.g. One node with two MPI tasks

    #SBATCH -N 1
    #SBATCH -n 2

Load required modules and set library paths

  $ module load intel/intel/19.1.1
  $ module load impi/19.0.9
  $ module load lammps/%{major_version}

Run LAMMPS program

  * Basic

    ibrun lmp_lonestar -in lammps_input

  * Use USER-OMP package (e.g. with 2 omp threads)

    ibrun lmp_lonestar -sf omp -pk omp 2 -in lammps_input

- ENVIRONMENT VARIABLES

The LAMMPS modulefile defines the following environment
variables (with the prefix "TACC_LAMMPS_"):

TACC_LAMMPS_DIR/BIN/POT for the location of the LAMMPS home, binaries, and
potentials respectively. The modulefile also appends TACC_LAMMPS_BIN to PATH.

- REFERENCE

  LAMMPS website: http://lammps.sandia.gov
  LAMMPS at TACC: https://portal.tacc.utexas.edu/software/lammps

Version %{version}
]]

help(help_message,"\n")

whatis("Name: LAMMPS")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL:  http://lammps.sandia.gov/index.html")
whatis("Description: Molecular Dynamics Chemistry Package")

local lmp_dir="%{INSTALL_DIR}"
setenv("TACC_LAMMPS_DIR"       ,lmp_dir)
setenv("TACC_LAMMPS_BIN"       ,pathJoin(lmp_dir,"bin"))
setenv("TACC_LAMMPS_POT"       ,pathJoin(lmp_dir,"potentials"))

append_path("PATH",pathJoin(lmp_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} <<EOF
#%Module3.1.1#################################################
##
## version file for lammps
##

set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%endif # BUILD_MODULEFILE

################################################################

%if %{?BUILD_PACKAGE}
%files package
  %defattr(775,root,install,775)
  %{INSTALL_DIR}
%endif # BUILD_PACKAGE |

%if %{?BUILD_MODULEFILE}
%files modulefile
  %defattr(775,root,install,775)
  %{MODULE_DIR}
%endif # BUILD_MODULEFILE |

################################################################

# Fix Modulefile During Post Install

%post %{PACKAGE}

export PACKAGE_POST=1
%include post-defines.inc

%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc

%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc

################################################################

%clean
rm -rf $RPM_BUILD_ROOT

################################################################

