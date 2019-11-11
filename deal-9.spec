Summary: Dealii install

# https://www.dealii.org/9.1.1/readme.html

# Give the package a base name
%define pkg_base_name dealii
%define MODULE_VAR    DEALII

# Create some macros (spec file variables)
%define major_version 9
%define minor_version 1
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define dealiipetscversion 3.12
%define DEAL_USE_PETSC 1
%define dealiitrilinosversion 12.14.1
%define DEAL_USE_TRILINOS 1

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

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

%if "%{comp_fam}" == "intel"
  # ultimately we want python3 everywhere
  module load python2 ## only for boost! should not have to.
%else
  # all of a sudden we can load boost without python?
  # module load python3 ## only for boost! should not have to.
%endif

module list
for m in boost cmake \
    metis p4est \
    ; do
  module --ignore_cache load $m ; 
done

%if "${DEAL_USE_PETSC}" == "1"
  export CMAKE_USE_PETSC="ON"
  module load petsc/%{dealiipetscversion} slepc/%{dealiipetscversion}
  echo "Installing deal with Petsc: ${PETSC_DIR}/${PETSC_ARCH}"
%else
  export CMAKE_USE_PETSC="OFF"
  export PETSC_DIR="/dev/null"
  export PETSC_ARCH="foobar"
%endif

%if "${DEAL_USE_TRILINOS}" == "1"
  export CMAKE_USE_TRILINOS="ON"
  module load trilinos/%{dealiitrilinosversion}
  find ${TACC_TRILINOS_DIR} -name \*.cmake -exec grep python {} \;
%else
  export CMAKE_USE_TRILINOS="OFF"
  export TACC_TRILINOS_DIR="/dev/null"
%endif

%if "%{comp_fam}" == "intel"
  module load mumps netcdf phdf5
%endif

ls $TACC_P4EST_DIR
ls $TACC_TRILINOS_DIR

%if "%{comp_fam}" == "gcc"
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif

##
## start of configure install
##

export LOGDIR=`pwd`
export DEALDIR=`pwd`
export DEALVERSION=%{pkg_version}

rm -rf /tmp/dealii-build
mkdir -p /tmp/dealii-build
pushd /tmp/dealii-build

rm -f CMakeCache.txt

#export BASIC_FLAGS="-g %{TACC_OPT}"
export BASIC_FLAGS="-g -march=native"

##
## add TBBROOT
##
%if "%{comp_fam}" == "gcc"
  export TACC_INTEL_DIR=/opt/intel/compilers_and_libraries_2019.5.281/linux
  if [ ! -d ${TACC_INTEL_DIR} ] ; then 
      echo "Invalid TACC_INTEL_DIR: ${TACC_INTEL_DIR}" ; exit 1
  fi
  export TBBROOT=${TACC_INTEL_DIR}/tbb
%endif
if [ ! -d "${TBBROOT}" ] ; then
  echo "Trouble setting TBBROOT"
  exit 1
fi
export BASIC_FLAGS="${BASIC_FLAGS} -I${TBBROOT}/include"

##  CC=`which mpicc` CXX=`which mpicxx` F90=`which mpif90`

  cmake -VV \
    -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} \
    \
    -DDEAL_II_WITH_CXX11=ON \
    -DDEAL_II_WITH_CXX17=OFF \
    -DDEAL_II_CXX_FLAGS_DEBUG="${BASIC_FLAGS} -O0" \
    -DDEAL_II_CXX_FLAGS_RELEASE="${BASIC_FLAGS} -O2" \
    \
    -DDEAL_II_COMPONENT_MESH_CONVERTER=ON \
    \
    -DDEAL_II_WITH_MPI=ON \
    -DMPICH_IGNORE_CXX_SEEK=ON \
    -DBOOST_DIR=${TACC_BOOST_DIR} \
    -DHDF5_DIR=${TACC_HDF5_DIR} \
    ` if [ ${TACC_FAMILY_COMPILER} = "intel" ] ; then echo " \
        -DMUMPS_DIR=${TACC_MUMPS_DIR} \
        -DMETIS_DIR=${TACC_METIS_DIR} \
        -DSLEPC_DIR=${TACC_SLEPC_DIR} \
    " ; fi ` \
    -DDEAL_II_WITH_PETSC=${CMAKE_USE_PETSC} \
        -DPETSC_DIR=${PETSC_DIR} -DPETSC_ARCH=${PETSC_ARCH} \
    -DDEAL_II_WITH_SLEPC=${CMAKE_USE_PETSC} \
    -DDEAL_II_WITH_P4EST=ON \
        -DP4EST_DIR=${P4ESTDIR} \
    -DDEAL_II_WITH_TRILINOS=${CMAKE_USE_TRILINOS} \
        -DTRILINOS_DIR=${TACC_TRILINOS_DIR} \
    ${DEALDIR}/dealii-${DEALVERSION} \
    \
    %{_topdir}/BUILD/dealii-%{version} \
    2>&1 | tee ${LOGDIR}/dealii_cmake.log

export nocmake="\
    -DDEAL_II_HAVE_AVX=ON \
    -DDEAL_II_HAVE_AVX512=ON \
    -DDEAL_II_HAVE_FLAG_Wimplicit_fallthrough=0 \
    "

##
## abort if cmake fails
if [ $? -ne 0 ] ; then exit 1 ; fi
##
##

##
## options set aside
##
export disabled=" \
        -DPETSC_INCLUDE_DIR_COMMON=${PETSC_DIR} \
    -DNETCDF_DIR=${TACC_NETCDF_DIR} \
    "
##
## Make!
##

make 2>&1 | tee ${LOGDIR}/dealii_compile.log
make install
( make test || true )

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
setenv("TACC_DEALII_INC",        pathJoin(dealii_dir,dealii_arch,"include") )
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
* Mon Sep 02 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release of 9.1.1
