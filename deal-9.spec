Summary: Dealii install

# https://www.dealii.org/9.1.1/readme.html

# Give the package a base name
%define pkg_base_name dealii
%define MODULE_VAR    DEALII

# Create some macros (spec file variables)
%define major_version 9
%define minor_version 2
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define use_petsc 1
## petsc 3.11 has been compiled with impi: release instead of release_mt
%define dealiipetscversion 3.15
## as of petsc 3.15 slepc is rolled into petsc
%define explicit_slepc 0
%define python_version 3
# for gcc explicit python
%define python_module 3.8.2

%define use_trilinos 1
%define dealiitrilinosversion 12.18.1

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

Release: 5%{?dist}
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

%if "%{comp_fam}" == "gcc"
%error "too many problems with mt and petsc"
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

module load python%{python_version}/%{python_module}

module list
for m in boost cmake \
    gsl \
    p4est \
    ; do
  module --ignore_cache load $m ; 
done
module list

export BASIC_FLAGS="-g %{TACC_OPT}"
#export BASIC_FLAGS="-g -march=native"

####
#### MPI handling
####
%if "%{comp_fam}" == "intel"
export I_MPI_LIBRARY_KIND=release_mt
#     -DMPICH_IGNORE_CXX_SEEK=ON
%endif

#### problem:
#   PETSC has to be compiled against the same MPI library as deal.II but the
#   link line of PETSC contains:
#
#     /opt/intel/compilers_and_libraries_2019.5.281/linux/mpi/intel64/lib/release_mt/libmpi.so
#
#   which is not listed in MPI_LIBRARIES:
#
#     MPI_LIBRARIES = "/opt/intel/compilers_and_libraries_2019.5.281/linux/mpi/intel64/lib/libmpifort.so /opt/intel/compilers_and_libraries_2019.5.281/linux/mpi/intel64/lib/release/libmpi.so /lib64/librt.so /lib64/libpthread.so /lib64/libdl.so"
#

export no_mpi_spec="\
    -D MPI_LIBRARIES=${TACC_IMPI_DIR}/intel64/lib/libmpicxx.so;${TACC_IMPI_DIR}/intel64/lib/libmpifort.so;${TACC_IMPI_DIR}/intel64/lib/release_mt/libmpi.so;/lib64/librt.so;/lib64/libpthread.so;/lib64/libdl.so \
    -D MPI_LIBRARIES=${TACC_IMPI_DIR}/intel64/lib/release/libmpi.so \
    -DCMAKE_CXX_COMPILER=mpicxx -DCMAKE_C_COMPILER=mpicc \
    -DMPICH_IGNORE_CXX_SEEK=ON
    "
export MPI_SPECIFICATION="\
    "

####
#### Metis
####
CMAKE_USE_METIS="ON"
module load metis

####
#### MKL
####
%if "%{comp_fam}" == "gcc"
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif

export LAPACK_SPECIFICATION="-DDEAL_II_WITH_LAPACK=ON \
-D LAPACK_INCLUDE_DIRS=${MKLROOT}/include \
-D LAPACK_LIBRARIES=\
${MKLROOT}/lib/intel64_lin/libmkl_intel_lp64.so\
\;\
${MKLROOT}/lib/intel64_lin/libmkl_core.so\
\;\
${MKLROOT}/lib/intel64_lin/libmkl_intel_thread.so\
\;\
${MKLROOT}/../compiler/lib/intel64_lin/libiomp5.so\
\;\
libm.so\
"
## from the developers:
## LAPACK_LIBRARIES=
## /opt/intel/compilers_and_libraries_2020.1.217/linux/mkl/lib/intel64_lin/libmkl_intel_lp64.so;
## /opt/intel/compilers_and_libraries_2020.1.217/linux/mkl/lib/intel64_lin/libmkl_intel_thread.so;
## /opt/intel/compilers_and_libraries_2020.1.217/linux/mkl/lib/intel64_lin/libmkl_core.so;
## /opt/intel/compilers_and_libraries_2020.1.217/linux/compiler/lib/intel64_lin/libiomp5.so;
## -lm;-ldl'

rm -rf /tmp/deal-logs
mkdir /tmp/deal-logs

for scalar in real complex ; do

####
#### PETSc
####
%if "%{use_petsc}" == "1"

  export CMAKE_USE_PETSC="ON"
if [ "$scalar" = "complex" ] ; then

  module load petsc/%{dealiipetscversion}-complex
  %if "%{explicit_slepc}" == "1"
    module load slepc/%{dealiipetscversion}-complex
  %else
    export TACC_SLEPC_DIR=${TACC_PETSC_DIR}
  %endif
  petsc_select="-DDEAL_II_WITH_PETSC_COMPLEX=ON -DDEAL_II_WITH_SLEPC_COMPLEX=OFF"
  install_prefix=%{INSTALL_DIR}/complex

else # if scalar real

  module load petsc/%{dealiipetscversion}
  %if "%{explicit_slepc}" == "1"
    module load slepc/%{dealiipetscversion}
  %else
    export TACC_SLEPC_DIR=${TACC_PETSC_DIR}
  %endif
  petsc_select="-DDEAL_II_WITH_PETSC=ON -DDEAL_II_WITH_SLEPC=OFF"
  install_prefix=%{INSTALL_DIR}/real

fi

%else # if not use_petsc
  export CMAKE_USE_PETSC="OFF"
  export PETSC_DIR="/dev/null"
  export PETSC_ARCH="foobar"
%endif # end use_petsc

##
## TBBROOT
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

####
#### Trilinos
#### (p4est gets loaded higher up)
####
%if "%{use_trilinos}" == "1"
  export CMAKE_USE_TRILINOS="ON"
  module load trilinos/%{dealiitrilinosversion}
  find ${TACC_TRILINOS_DIR} -name \*.cmake -exec grep python {} \;
%else
  export CMAKE_USE_TRILINOS="OFF"
  export TACC_TRILINOS_DIR="/dev/null"
%endif

####
#### Netcdf, Hdf5
####
%if "%{comp_fam}" == "intel"
  module load mumps netcdf phdf5
%endif

##
## start of configure install
##

# pushd 
# ls -l %{_topdir}/SPECS/victor_scripts/remove_pthread_workarounds.patch 
# ls -l %{_topdir}/BUILD/dealii-9.1.1/cmake/configure/configure_1_threads.cmake
# patch -p1 < %{_topdir}/SPECS/victor_scripts/remove_pthread_workarounds.patch
# popd 

export LOGDIR=`pwd`
export DEALDIR=`pwd`
export DEALVERSION=%{pkg_version}

rm -rf /tmp/dealii-build
mkdir -p /tmp/dealii-build
pushd /tmp/dealii-build

rm -f CMakeCache.txt

##  CC=`which mpicc` CXX=`which mpicxx` F90=`which mpif90`

## https://www.dealii.org/developer/users/cmake_dealii.html

( set | grep pthreads ) || /bin/true

%if "%{is_impi}" == "1"
  export I_MPI_LIBRARY_KIND=release_mt
  export I_MPI_LINK=opt_mt
%endif

cmake -VV \
    -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR}/${scalar} \
    \
    -DDEAL_II_WITH_CXX11=ON \
    -DDEAL_II_WITH_CXX17=OFF \
    -DDEAL_II_CXX_FLAGS_DEBUG="${BASIC_FLAGS} -O0" \
    -DDEAL_II_CXX_FLAGS_RELEASE="${BASIC_FLAGS} -O2" \
    \
    -DDEAL_II_COMPONENT_MESH_CONVERTER=ON \
    \
    -DDEAL_II_WITH_MPI=ON \
    ${MPI_SPECIFICATION} \
    ${LAPACK_SPECIFICATION} \
    \
    -DBOOST_DIR=${TACC_BOOST_DIR} \
    -DDEAL_II_WITH_GSL=ON \
      -DGSL_INCLUDE_DIR=${TACC_GSL_INC:-NO_GSL_INC} \
      -DGSL_LIBRARY_DIR=${TACC_GSL_LIB:-NO_GSL_LIB} \
      -DGSL_LIBRARY=${TACC_GSL_LIB:-NO_GSL_LIB}/libgsl.so\;${TACC_GSL_LIB:-NO_GSL_LIB}/libgslcblas.so \
    -DHDF5_DIR=${TACC_HDF5_DIR} \
    -DDEAL_II_WITH_METIS=${CMAKE_USE_METIS} \
        -DMETIS_DIR=${TACC_METIS_DIR} \
    \
    ` if [ ${TACC_FAMILY_COMPILER} = "intel" ] ; then echo " \
        -DMUMPS_DIR=${TACC_MUMPS_DIR} \
    " ; fi ` \
    -DDEAL_II_WITH_PETSC=${CMAKE_USE_PETSC} \
        -DPETSC_DIR=${PETSC_DIR} -DPETSC_ARCH=${PETSC_ARCH} \
    -DDEAL_II_WITH_SLEPC=${CMAKE_USE_PETSC} \
        -DSLEPC_DIR=${TACC_SLEPC_DIR} \
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

make -j 12 2>&1 | tee ${LOGDIR}/dealii_compile.log
make install
## ( make test || true )

popd # back out of INSTALL_DIR

## this does not work for complex
# mkdir -p %{INSTALL_DIR}/examples
# cp -r examples/step* %{INSTALL_DIR}/examples
echo "examples:"
ls %{INSTALL_DIR}/${scalar}/examples


##
## start of module file section
##

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}-$scalar.lua << EOF
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

local             dealii_dir =     "%{INSTALL_DIR}/${scalar}"

prepend_path("PATH",            pathJoin(dealii_dir,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(dealii_dir,"lib") )

setenv("DEALII_DIR",             dealii_dir)
setenv("TACC_DEALII_DIR",        dealii_dir)
setenv("TACC_DEALII_BIN",        pathJoin(dealii_dir,"bin") )
setenv("TACC_DEALII_INC",        pathJoin(dealii_dir,"include") )
setenv("TACC_DEALII_LIB",        pathJoin(dealii_dir,"lib") )

depends_on( "python%{python_version}" )
EOF
# depends_on( "boost" )

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version}-$scalar << EOF
#%Module1.0#################################################
##
## version file for Dealii %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}-$scalar.lua 

##
## end of configure install section
##
done # end of real complex loop

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
# release 4: adding boost-mpi dependency
* Thu Apr 08 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: better lapack specification, real/complex versions
* Wed Aug 19 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: update to 9.2.0
* Fri May 01 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: trying trilinos again, using 12.18.1
* Sat Apr 18 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: using petsc 3.11 which has release-{non-mt} MPI
             adding GSL, Metis under gcc
             disabled: trilinos
* Mon Sep 02 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release of 9.1.1
