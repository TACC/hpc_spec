Summary: Dealii install

# Give the package a base name
%define pkg_base_name dealii
%define MODULE_VAR    DEALII

# Create some macros (spec file variables)
%define major_version 8
%define minor_version 5
%define micro_version 0

%define dealiipetscversion 3.7

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
%define INSTALL_PREFIX  /home1/apps/el7/

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 1%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tar.gz
URL: http://www.dealii.org/
Vendor: TAMU
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Dealii is an open source finite element package
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Dealii is an open source finite element package
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
The main aim of deal.II is to enable rapid development of modern
finite element codes, using among other aspects adaptive meshes and a
wide array of tools classes often used in finite element
program. Writing such programs is a non-trivial task, and successful
programs tend to become very large and complex. We believe that this
is best done using a program library that takes care of the details of
grid handling and refinement, handling of degrees of freedom, input of
meshes and output of results in graphics formats, and the
like. Likewise, support for several space dimensions at once is
included in a way such that programs can be written independent of the
space dimension without unreasonable penalties on run-time and memory
consumption.

%description %{MODULEFILE}
The main aim of deal.II is to enable rapid development of modern
finite element codes, using among other aspects adaptive meshes and a
wide array of tools classes often used in finite element
program. Writing such programs is a non-trivial task, and successful
programs tend to become very large and complex. We believe that this
is best done using a program library that takes care of the details of
grid handling and refinement, handling of degrees of freedom, input of
meshes and output of results in graphics formats, and the
like. Likewise, support for several space dimensions at once is
included in a way such that programs can be written independent of the
space dimension without unreasonable penalties on run-time and memory
consumption.

%prep

%setup -n dealii-%{version}

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

## courtesy of Carlos
%if "%{comp_fam}" == "intel"
  #source /scratch/projects/compilers/sourceme17.2.sh
# here's what's in that source:
  ver="2017.2.050"
  topdir="/scratch/projects/compilers/intel/17"
  source $topdir/parallel_studio_xe_$ver/bin/psxevars.sh
  export TACC_MPI_GETMODE=impi_hydra
  export MPICH_HOME=$I_MPI_ROOT
%endif

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
##cp -r * %{INSTALL_DIR}
##pushd %{INSTALL_DIR}

module list
for m in boost cmake netcdf p4est phdf5 \
        petsc/%{dealiipetscversion} slepc/%{dealiipetscversion} \
        trilinos/12.8.1 ; do
  module --ignore_cache load $m ; 
done

%if "%{comp_fam}" == "gcc"
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif

##
## start of configure install
##

export LOGDIR=`pwd`
mkdir -p %{INSTALL_DIR}/build
pushd %{INSTALL_DIR}/build

rm -f CMakeCache.txt

echo "Installing deal with Petsc: ${PETSC_DIR}/${PETSC_ARCH}"

  cmake -VV \
    -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} \
    -DCMAKE_C_COMPILER="mpicc" \
    -DCMAKE_CXX_COMPILER="mpicxx" \
    -DDEAL_II_WITH_CXX11=ON \
    -DCMAKE_Fortran_COMPILER=mpif90 \
    -DDEAL_II_CXX_FLAGS_DEBUG="-std=c++14" \
    -DDEAL_II_CXX_FLAGS_RELEASE="-std=c++14" \
    -DDEAL_II_WITH_MPI=ON \
    ` if [ ${TACC_FAMILY_COMPILER} = "gcc" ] ; then echo " \
        -DMPI_CXX_INCLUDE_PATH=${MPICH_HOME}/include \
        -DMPI_CXX_LIBRARIES=${MPICH_HOME}/lib \
    " ; fi ` \
    -DDEAL_II_COMPONENT_MESH_CONVERTER=ON \
    -DBOOST_DIR=${TACC_BOOST_DIR} \
    -DHDF5_DIR=${TACC_HDF5_DIR} \
    ` if [ ${TACC_FAMILY_COMPILER} = "intel" ] ; then echo " \
    -DMUMPS_DIR=${TACC_MUMPS_DIR} \
    -DMETIS_DIR=${TACC_METIS_DIR} \
    -DSLEPC_DIR=${TACC_SLEPC_DIR} \
    " ; fi ` \
    -DNETCDF_DIR=${TACC_NETCDF_DIR} \
    -DDEAL_II_WITH_PETSC=ON -DDEAL_II_WITH_SLEPC=ON \
        -DPETSC_DIR=${PETSC_DIR} -DPETSC_ARCH=${PETSC_ARCH} \
    -DDEAL_II_WITH_P4EST=ON \
        -DP4EST_DIR=${P4ESTDIR} \
    -DDEAL_II_WITH_TRILINOS=ON \
        -DTRILINOS_DIR=${TACC_TRILINOS_DIR} \
    ${DEALDIR}/dealii-${DEALVERSION} \
    \
    %{_topdir}/BUILD/dealii-%{version} \
    2>&1 | tee ${LOGDIR}/dealii_cmake.log

make 2>&1 | tee ${LOGDIR}/dealii_compile.log

make install
make test

popd # back out of INSTALL_DIR

mkdir -p %{INSTALL_DIR}/examples
cp -r examples/step* %{INSTALL_DIR}/examples

##
## start of module file section
##

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The dealii module defines the following environment variables:
TACC_DEALII_DIR, TACC_DEALII_BIN, and
TACC_DEALII_LIB for the location
of the Dealii distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Dealii" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/dealii/dealii-as/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             dealii_arch =    "${architecture}"
local             dealii_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(dealii_dir,dealii_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(dealii_dir,dealii_arch,"lib") )

setenv("DEALII_ARCH",            dealii_arch)
setenv("DEALII_DIR",             dealii_dir)
setenv("TACC_DEALII_DIR",        dealii_dir)
setenv("TACC_DEALII_BIN",        pathJoin(dealii_dir,dealii_arch,"bin") )
setenv("TACC_DEALII_LIB",        pathJoin(dealii_dir,dealii_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Dealii %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

module unload python
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Fri Apr 07 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
