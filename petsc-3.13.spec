Summary: PETSc install

# Give the package a base name
%define pkg_base_name petsc
%define MODULE_VAR    PETSC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 13
%define micro_version 2
%define versionpatch %{major_version}.%{minor_version}.%{micro_version}

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define usecuda 1
%define usehdf 0
%define useelemental 0
%define usefft 0
%define usehypre 0
%define usesundials 0
%define usesuperlu 0
%define usezoltan 0

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 5%{?dist}
License: BSD-like; see src/docs/website/documentation/copyright.html
Vendor: Argonne National Lab, MCS division
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{versionpatch}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Petsc local binary install
Group: System Environment/Base
%package %{PACKAGE}-xx
Summary: Petsc local binary install
Group: System Environment/Base
%package %{PACKAGE}-sources
Summary: Petsc local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Petsc local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description %{PACKAGE}-xx
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description %{PACKAGE}-sources
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description %{MODULEFILE}
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.

%prep

#%setup -n petsc-%{major_version}.%{minor_version}.%{micro_version}
%setup -n petsc-%{versionpatch}

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
module purge
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
cp -r * %{INSTALL_DIR}
pushd %{INSTALL_DIR}

echo "contents of install-dir before installation"
ls
export PETSC_DIR=`pwd`

module load cmake
%if "%{comp_fam}" == "gcc"
  module load mkl
%endif
export BLAS_LAPACK_LOAD=--with-blas-lapack-lib=/opt/ibmmath/essl/6.2/lib64/libessl.so

##
## ML
##
## depends on more lapack than is present in ESSL
# export ML_OPTIONS="--with-ml=1 --download-ml"
# export MLSTRING=ml

%if "%{is_intel}" == "1"
export LOCALCC=icc
export LOCALFC=ifort
%endif

%if "%{is_mvapich2}" == "1"
export MPI_EXTRA_OPTIONS="--with-mpiexec=mpirun_rsh"
%endif

# matlab will only be invoked for real packages
#module load matlab
#export MATLABOPTIONS="--with-matlab --with-matlab-dir=${TACC_MATLAB_DIR}"

export PETSC_CONFIGURE_OPTIONS="\
  --with-x=0 -with-pic \
  --with-make-np=8 \
  "
mkdir -p %{INSTALL_DIR}/externalpackages
mkdir -p %{MODULE_DIR}

export PLAPACKSTRING=plapack
export PLAPACKOPTIONS="--with-plapack=1 --download-plapack"
%if "%{is_mvapich2}" == "1"
export PLAPACKSTRING=
export PLAPACKOPTIONS=
%endif

##
## configure install loop
##
export logdir=%{_topdir}/../apps/petsc/logs
mkdir -p ${logdir}; rm -rf ${logdir}/*
export dynamic="debug i64 i64debug complex complexdebug complexi64 complexi64debug uni unidebug nohdf5 hyprefei"
%if "%{usecuda}" == "1"
  export dynamic="cuda cudadebug ${dynamic}"
%endif

for ext in \
  "" \
  single singledebug \
  ${dynamic} \
  ; do

echo "configure install for ${ext}"
export versionextra=

if [ -z "${ext}" ] ; then
  export architecture=powernine
else
  export architecture=powernine-${ext}
fi

##
## Compiler flags
##
export XOPTFLAGS="%{TACC_OPT} -O2 -g"
case "${ext}" in
  ( *complex* )
  export XOPTFLAGS="%{TACC_OPT} -O1 -g"
  #-xCORE-AVX2 -axMIC-AVX512,COMMON-AVX512 -O1 -g"
  ;;
esac

export COPTFLAGS=${XOPTFLAGS}
export CXXOPTFLAGS=${XOPTFLAGS}
export FOPTFLAGS=${XOPTFLAGS}
export CNOOPTFLAGS="-O0 -g"
export CXXNOOPTFLAGS="-O0 -g"
export FNOOPTFLAGS="-O0 -g"

export CFLAGS=${COPTFLAGS}
export CXXFLAGS=${CXXOPTFLAGS}
export FFLAGS=${FOPTFLAGS}
case "${ext}" in
*debug ) export CFLAGS=${CNOOPTFLAGS}
         export CXXFLAGS=${CXXNOOPTFLAGS}
         export FFLAGS=${FNOOPTFLAGS}
         ;;
esac

export usedebug=no
case "${ext}" in
*debug ) export usedebug=yes
esac

## 
## dynamic and shared
export dynamicshared="--with-shared-libraries=1"
export versionextra="${versionextra}; shared library support"
case "${ext}" in
*static* ) export dynamicshared="--with-shared-libraries=0" ;
	   export versionextra="${versionextra}; no shared library support"
esac

##
## hdf5
##

%if "%{usehdf}" == "1"
  export HAS_HDF5=1
  export hdf5string="hdf5"
  #export hdf5download="--with-hdf5=1 --download-hdf5=1"
  #--with-hdf5-dir=${TACC_HDF5_DIR}"
  module load phdf5
  export hdf5download="--with-hdf5=1 --with-hdf5-dir=${TACC_HDF5_DIR}"
  export hdf5versionextra="; hdf5 support"
%else
  export HAS_HDF5=0
%endif

case "${ext}" in
*nohdf5* ) export HAS_HDF5=0
        export hdf5string=
        export hdf5download=
        export hdf5versionextra=
        module unload hdf5 phdf5
        ;;
esac

export versionextra="${versionextra}${hdf5versionextra}"

##
## C language
export clanguage=
export clanguageversionextra=
export USECXX=
case "${ext}" in
*cxx* ) export clanguage="--with-clanguage=C++"
       export clanguageversionextra="; C++ support"
       export USECXX=yes
       ;;
esac
%if "%{is_petsc_dev}" == "1"
case "${ext}" in
*cxx* ) export clanguage="--with-clanguage=C++ --with-sieve=1 --with-opt-sieve=1 --with-boost="
       export clanguageversionextra="; C++ support, sieve & boost included"
       ;;
esac
%endif
export versionextra="${versionextra}${clanguageversionextra}"

#
# Chaco
#
export CHACOSTRING=chaco
export CHACO_OPTIONS="--with-chaco=1 --download-chaco"

#
# Parmetis/metis
# needed for Elemental, Mumps, SuperLU
#
export PARMETIS_OPTIONS="--with-parmetis=1 --download-parmetis --with-metis=1 --download-metis"
export PARMETISSTRING="parmetis"

#
# Elemental
#
%if "%{useelemental}" == "1"
  export ELEMENTAL_OPTIONS="--with-elemental=1 --download-elemental --with-cxx-dialect=C++11 ${PARMETIS_OPTIONS}"
  export ELEMENTAL_STRING=elemental
%endif

#
# Fftw
#
%if "%{usefft}" == "1"
  module load fftw3
  export FFTW_OPTIONS="--with-fftw=1 --with-fftw-dir=${TACC_FFTW3_DIR}"
  export FFTW_STRING=fftw
%endif

#
# Hypre
#
%if "%{usehypre}" == "1"
  export HYPRE_OPTIONS="--with-hypre=1 --download-hypre"
  export HYPRESTRING=hypre
  case "${ext}" in
  hyprefei ) 
      export HYPRE_OPTIONS="${HYPRE_OPTIONS} --download-hypre-configure-arguments=--with-fei"
      ;;
  esac
%endif
# export HYPRE_OPTIONS=
# export HYPRESTRING=

#
# Mumps & Superlu depend on parmetis which depends on metis
#
%if "%{usesuperlu}" == "1"
  export MUMPS_OPTIONS="--with-mumps=1 --download-mumps ${PARMETIS_OPTIONS}"
  export SCALAPACK_OPTIONS="--with-scalapack=1 --download-scalapack --with-blacs=1 --download-blacs"
%endif

#
# Spai
#
## SPAI relies on Lapack functions that are not in ESSL
# export SPAI_OPTIONS="--with-spai=1 --download-spai"
# export SPAI_STRING=spai

#
# Spooles
#
export SPOOLES_OPTIONS="--with-spooles=1 --download-spooles"
export SPOOLES_STRING=spooles

#
# Suitesparse
#
export SUITESPARSE_OPTIONS="--with-suitesparse=1 --download-suitesparse"
export SUITESPARSE_STRING=suitesparse

#
# Sundials
#
%if "%{usesundials}" == "1"
  export SUNDIALS_OPTIONS="--with-sundials=1 --download-sundials"
  export SUNDIALSSTRING="sundials"
%endif

#
# SuperLU
#
%if "%{usesuperlu}" == "1"
  export SUPERLU_OPTIONS="--with-superlu_dist=1 --download-superlu_dist \
   --with-superlu=1 --download-superlu ${PARMETIS_OPTIONS}"
  export superlustring="superlu (distributed/sequential)"
%endif

#
# Zoltan
# 
%if "%{usezoltan}" == "1"
  export ZOLTAN_OPTIONS="--with-zoltan=1 --download-zoltan=1 --download-ptscotch=1"
  export ZOLTANSTRING="zoltan/ptscotch"
%endif

##
## 64-bit indices
##
INDEX_OPTIONS=
INDEX_STRING=
case "${ext}" in
*i64* ) INDEX_OPTIONS=--with-64-bit-indices ;
        INDEX_STRING="64-bit indexing" ;
        CHACO_OPTIONS= ;       CHACOSTRING= ;
        MUMPS_OPTIONS= ;       MUMPSTRING= ;
	ML_OPTIONS= ;          ML_STRING= ;
	PLAPACK_OPTIONS= ;     PLAPACK_STRING= ;
        SPAI_OPTIONS= ;        SPAITRING= ;
	SPOOLES_OPTIONS= ;     SPOOLES_STRING= ;
	SUNDIALS_OPTIONS= ;    SUNDIALSSTRING= ;
	SUPERLU_OPTIONS= ;     superlustring= ;
	SUITESPARSE_OPTIONS= ; SUITESPARSE_STRING= ;
                ;;
esac

##
## define packages; some are real & complex, others real only.
##
export complexpackages="${ELEMENTAL_STRING} ${FFTW_STRING} mumps scalapack ${SPOOLES_STRING} ${SUITESPARSE_STRING} ${superlustring} ${ZOLTANSTRING} ${hdf5string}"
export PETSC_COMPLEX_PACKAGES="\
  ${ELEMENTAL_OPTIONS} \
  ${FFTW_OPTIONS} \
  ${hdf5download} \
  ${MUMPS_OPTIONS}\
  ${SCALAPACK_OPTIONS} ${SPOOLES_OPTIONS} \
  ${SUITESPARSE_OPTIONS} ${SUPERLU_OPTIONS} \
  ${ZOLTAN_OPTIONS} \
  "

export realonlypackages="${CHACOSTRING} ${HYPRESTRING} ${MLSTRING} ${PARMETISSTRING} spai ${PLAPACKSTRING} ${SUNDIALSSTRING}"
export PETSC_REALONLY_PACKAGES="\
  ${CHACO_OPTIONS} \
  ${HYPRE_OPTIONS} ${ML_OPTIONS} \
  ${MATLABOPTIONS} ${ML_OPTIONS} \
  ${PARMETIS_OPTIONS} \
  ${PLAPACKOPTIONS} ${SPAI_OPTIONS} ${SUNDIALS_OPTIONS} \
  "

export packages="${PETSC_REALONLY_PACKAGES} ${PETSC_COMPLEX_PACKAGES}"
export packageslisting="${realonlypackages} ${complexpackages}"
export scalar="--with-scalar-type=real"

case "${ext}" in
*complex* ) export packages="${PETSC_COMPLEX_PACKAGES}"
	  export packageslisting="${complexpackages}"
          export scalar="--with-scalar-type=complex --with-fortran-kernels=1"
	  ;;
uni*     ) 
	  export packageslisting=
	  export packages=
	  ;;
*cuda*     ) # just like single, no packages
	  export packageslisting=
	  export packages=
	  ;;
esac

export packageslisting="${packageslisting} ${INDEX_STRING}"

#
# blas/lapack
#
export BLAS_LAPACK_OPTIONS="\
  ${BLAS_LAPACK_LOAD} \
  "

#
# CUDA
#
module unload cuda
export CUDA_OPTIONS=
case "$ext" in
( *cuda* )
  module load cuda
  export CUDA_OPTIONS="\
    --with-cuda=yes --download-cusp=yes --with-cudac=nvcc \
    --with-cuda-include=${TACC_CUDA_INC} \
    --with-cuda-lib=[${TACC_CUDA_LIB}/libcufft.so,libcusparse.so,libcusolver.so,libcublas.so,libcuda.so,libcudart.so] \
    CUDAFLAGS=-arch=sm_70 \
    "
  export BLAS_LAPACK_OPTIONS="${BLAS_LAPACK_OPTIONS} libesslsmpcuda.so"
esac

#
# petsc can run single processor with a fake mpi
# in that case: no external packages, and explicit non-mp cc/fc compilers
#
export MPICC=`which mpicc`
export MPICXX=`which mpicxx`
export MPIF90=`which mpif90`
echo "setting mpicc=${MPICC}"
ls -l ${MPICC}

export MPI_OPTIONS="\
    --with-mpi-compilers=1 \
    --with-cc=`which mpicc` --with-fc=`which mpif90` --with-cxx=`which mpicxx` \
    "
## compilers are found by giving the "--with-mpi-dir"
## export MPI_OPTIONS="${MPI_OPTIONS} --with-mpi-dir=${TACC_SPECTRUM_MPI_DIR}"

case "${ext}" in
uni* ) export MPI_OPTIONS="--with-mpi=0 --with-cc=${CC} --with-fc=${FC} --with-cxx=${CXX}";
       export packages= ;;
# cuda* ) export MPI_OPTIONS="--with-mpi=0 --with-cc=${CC} --with-fc=${FC} --with-cxx=0";
#        export packages= ;;
esac

#
# single precision
#
export precision=--with-precision=double
case "${ext}" in
single ) 
    export precision=--with-precision=single ;
    export packageslisting=
    export packages= ;;
esac

##
## here we go
##

export PETSC_ARCH=${architecture}
export EXTERNAL_PACKAGES_DIR=/admin/build/admin/rpms/stampede2/SOURCES/petsc-packages
export PACKAGES_BUILD_DIR=/tmp/petsc-%{version}/${architecture}
mkdir -p ${PACKAGES_BUILD_DIR}
noprefix=--prefix=%{INSTALL_DIR}/${architecture}
# export packages=

# python config/configure.py
export I_MPI_FABRICS=shm:tmi
RPM_BUILD_ROOT=tmpfs PETSC_DIR=`pwd` ./configure \
  --with_fortran=0 --with-fc=0 \
  ${PETSC_CONFIGURE_OPTIONS} \
  --with-packages-search-path=[${EXTERNAL_PACKAGES_DIR}] \
  --with-packages-build-dir=${PACKAGES_BUILD_DIR} \
  ${MPI_OPTIONS} ${clanguage} ${scalar} ${dynamicshared} ${precision} ${packages} \
  --with-debugging=${usedebug} \
  --LIBS="${EXTRALIBS}" \
  ${BLAS_LAPACK_OPTIONS} ${MPI_EXTRA_OPTIONS} ${CUDA_OPTIONS} ${INDEX_OPTIONS} \
  COPTFLAGS="${CFLAGS}" FOPTFLAGS="${FFLAGS}" CXXOPTFLAGS="${CXXFLAGS}"

####
#### post-processing fixes
####
%if "%{usecuda}" == "1"
  sed -i '/define PETSC_DEPRECATED_ENUM/s/__attribute..deprecated..//' \
    ${PETSC_ARCH}/include/petscconf.h 
%endif

####
#### >>>>>>>>>>>>>>>>
####

##
## Make!
##
PETSC_DIR=`pwd` PETSC_ARCH=${architecture} make MAKE_NP=12 V=2


#
# cleanup
#
# as of 3.7 the object files are kept. I don't think we need them
/bin/rm -rf $PETSC_ARCH/obj/src
find $PETSC_ARCH -name \*.o -exec rm -f {} \;
#/bin/rm -rf ${architecture}/obj

##
## modulefile part of the configure install loop
##
echo "module file for ${ext}"
#
# various settings
#
if [ -z "${ext}" ] ; then
  export modulefilename=%{version}
else
  export modulefilename=%{version}-${ext}
fi

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The petsc module defines the PETSc variables
PETSC_DIR and PETSC_ARCH
as well as the following environment variables:
TACC_PETSC_DIR, TACC_PETSC_BIN, and
TACC_PETSC_LIB for the location
of the Petsc distribution, documentation, binaries,
and libraries. It also updates PATH and LD_LIBRARY_PATH.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: PETSc" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/petsc/petsc-as/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             petsc_arch =    "${architecture}"
local             petsc_dir  =    "%{INSTALL_DIR}/"
local             optnogpu   =    "-use_gpu_aware_mpi 0"

prepend_path("PATH",            pathJoin(petsc_dir,petsc_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(petsc_dir,petsc_arch,"lib") )

setenv("PETSC_ARCH",            petsc_arch)
setenv("PETSC_DIR",             petsc_dir)
setenv("TACC_PETSC_DIR",        petsc_dir)
setenv("TACC_PETSC_BIN",        pathJoin(petsc_dir,petsc_arch,"bin") )
setenv("TACC_PETSC_INC",        pathJoin(petsc_dir,petsc_arch,"include") )
setenv("TACC_PETSC_LIB",        pathJoin(petsc_dir,petsc_arch,"lib") )
EOF

case "${ext}" in
  ( *cuda* )
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF

depends_on( "cuda" )
EOF
  ;;
  ( * )
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
setenv("PETSC_OPTIONS",        optnogpu)
EOF
esac

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Petsc %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua 

##
## end of module file loop
##
done

cp -r config include lib makefile src \
    $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r powernine* \
    $RPM_BUILD_ROOT/%{INSTALL_DIR}

popd
umount %{INSTALL_DIR}

echo "Directory to package up: $RPM_BUILD_ROOT/%{INSTALL_DIR}"
echo "listing:"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

%files %{PACKAGE}-sources
  %defattr(-,root,install,)
  %{INSTALL_DIR}/config
  %{INSTALL_DIR}/include
  %{INSTALL_DIR}/lib
  %{INSTALL_DIR}/makefile
  %{INSTALL_DIR}/src 

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}/powernine*

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Thu Jun 25 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 5 fix overenthousiastic cuda options
* Tue Jun 23 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 4 cuda
* Wed Jun 17 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: building to /opt/apps
* Tue Jun 16 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: use powernine as arch
* Wed Apr 01 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release