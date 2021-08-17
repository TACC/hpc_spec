Summary: Aspect install

# https://www.aspect.org/9.1.1/readme.html

# Give the package a base name
%define pkg_base_name aspect
%define MODULE_VAR    ASPECT

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define aspectdealversion/9.2.0-real

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
URL: http://www.aspect.org/
Vendor: TAMU
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Aspect is an open source finite element package
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Aspect is an open source finite element package
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}

%description %{MODULEFILE}

%prep

%setup -n aspect-%{version}

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

# module load python%{python_version}/%{python_module}

module list
for m in \
    dealii/%{aspectdealversion} \
    ; do
  module --ignore_cache load $m ; 
done
module list

export BASIC_FLAGS="-g %{TACC_OPT}"

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

####
#### PETSc
####

  export CMAKE_USE_PETSC="ON"

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
  module load trilinos/%{aspecttrilinosversion}
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
# ls -l %{_topdir}/BUILD/aspect-9.1.1/cmake/configure/configure_1_threads.cmake
# patch -p1 < %{_topdir}/SPECS/victor_scripts/remove_pthread_workarounds.patch
# popd 

export LOGDIR=`pwd`
export DEALDIR=`pwd`
export DEALVERSION=%{pkg_version}

rm -rf /tmp/aspect-build
mkdir -p /tmp/aspect-build
pushd /tmp/aspect-build

rm -f CMakeCache.txt

%if "%{is_impi}" == "1"
  export I_MPI_LIBRARY_KIND=release_mt
  export I_MPI_LINK=opt_mt
%endif

cmake -VV \
    -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} \
    -D DEAL_II_DIR=${TACC_DEALII_DIR} \
    \
    %{_topdir}/BUILD/aspect-%{version}

##
## abort if cmake fails
if [ $? -ne 0 ] ; then exit 1 ; fi
##
##

##
## Make!
##

make -j 12 2>&1 | tee ${LOGDIR}/aspect_compile.log
make install
## ( make test || true )

popd # back out of INSTALL_DIR

cp -r contrib   data    unit_tests \
    benchmarks  doc  source    VERSION \
    CITATION     CODE_OF_CONDUCT.md  cookbooks  LICENSE          tests \
    %{INSTALL_DIR}

##
## start of module file section
##

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The aspect module defines the following environment variables:
TACC_ASPECT_DIR, TACC_ASPECT_BIN, and
TACC_ASPECT_LIB for the location
of the Aspect distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Aspect" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/aspect/aspect-as/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             aspect_dir =     "%{INSTALL_DIR}"

prepend_path("PATH",            pathJoin(aspect_dir,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(aspect_dir,"lib") )

setenv("ASPECT_DIR",             aspect_dir)
setenv("TACC_ASPECT_DIR",        aspect_dir)
setenv("TACC_ASPECT_BIN",        pathJoin(aspect_dir,"bin") )
setenv("TACC_ASPECT_INC",        pathJoin(aspect_dir,"include") )
setenv("TACC_ASPECT_LIB",        pathJoin(aspect_dir,"lib") )

EOF
# depends_on( "boost" )

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module1.0#################################################
##
## version file for Aspect %version
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
# release 4: adding boost-mpi dependency
* Fri Jul 30 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release of 2.2.0
