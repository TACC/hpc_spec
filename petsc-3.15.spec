Summary: PETSc install

# Give the package a base name
%define pkg_base_name petsc
%define MODULE_VAR    PETSC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 15
%define micro_version 0
%define versionpatch %{major_version}.%{minor_version}.%{micro_version}

%define pkg_version %{major_version}.%{minor_version}

####
#### configuration switches:
####
%define adios 0
%define p4p 1
# cuda only with intel
%define cuda 1
%define use_elemental 0
%define use_superlu 1

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
%package %{PACKAGE}-debug
Summary: Petsc local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Petsc local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description %{PACKAGE}-debug
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
module list

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
export BLAS_LAPACK_LOAD=--with-blas-lapack-dir=${MKLROOT}

##
## ML
##
export ML_OPTIONS="--with-ml=1 --download-ml"
export MLSTRING=ml
%if "%{is_impi}" == "1"
export ML_OPTIONS=
export MLSTRING=
%endif
# %if "%{is_mvapich2}" == "1"
# export ML_OPTIONS=
# export MLSTRING=
# %endif

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
export dynamiccc="i64 debug i64debug complex complexdebug complexi64 complexi64debug uni unidebug nohdf5 hyprefei"

%if "%{cuda}" == "1"
  export cudaext="rtx rtxdebug"
%else
  export cudaext=
%endif

for ext in \
  "" \
  single single-debug \
  ${dynamiccc} \
  ${cudaext} \
  ; do

export no_ext="\
  "

echo "configure install for ${ext}"
export versionextra=

if [ -z "${ext}" ] ; then
  export architecture=clx
else
  export architecture=clx-${ext}
fi

##
## Compiler flags
##
# we have our own avx flags, so --with-avx512-kernels not needed
export XOPTFLAGS="%{TACC_OPT} -O2 -g"
case "${ext}" in 
  ( *complex* )
  export XOPTFLAGS="%{TACC_OPT} -O1 -g"
  #-xCORE-AVX2 -axMIC-AVX512,COMMON-AVX512 -O1 -g"
  ;;
  ( *rtx* )
  export XOPTFLAGS="-O2 -g"
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

export HAS_HDF5=1

  module load phdf5
  export hdf5string="hdf5"
  export hdf5download="--with-hdf5=1 --with-hdf5-dir=${TACC_HDF5_DIR}"
  # --download-hdf5=1"
  export hdf5versionextra="; hdf5 support"


# sometimes actually we don't load hdf5 because the serial and parallel 
# are not compatible
case "${ext}" in
*nohdf5* ) export HAS_HDF5=0
        export hdf5string=
        export hdf5download=
        export hdf5versionextra=
	module unload phdf5
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
export versionextra="${versionextra}${clanguageversionextra}"

#
# Adios2
#
%if "%{adios}" == "1"
  export ADIOS_STRING=adios2
  export ADIOS_OPTIONS="--download-adios2=1"
%endif

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
%if "%{use_elemental}" == "1"
  export ELEMENTAL_OPTIONS="--with-elemental=1 --download-elemental --with-cxx-dialect=C++11 ${PARMETIS_OPTIONS}"
  export ELEMENTAL_STRING=elemental
%endif

#
# Fftw
#
module load fftw3
export FFTW_OPTIONS="--with-fftw=1 --with-fftw-dir=${TACC_FFTW3_DIR}"
export FFTW_STRING=fftw

#
# Hypre
#
export HYPRE_OPTIONS="--with-hypre=1 --download-hypre"
export HYPRESTRING=hypre
case "${ext}" in
hyprefei ) 
    export HYPRE_OPTIONS="${HYPRE_OPTIONS} --download-hypre-configure-arguments=--with-fei"
    ;;
esac

#
# Mumps & Superlu depend on parmetis which depends on metis
#
export MUMPS_OPTIONS="--with-mumps=1 --download-mumps ${PARMETIS_OPTIONS}"
export SCALAPACK_OPTIONS="--with-scalapack=1 --download-scalapack --with-blacs=1 --download-blacs"

#
# Spai
#
export SPAI_OPTIONS="--with-spai=1 --download-spai"
export SPAI_STRING=spai

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
# Slepc
#
export SLEPC_OPTIONS="--with-slepc=1 --download-slepc=1 --download-slepc-commit=bc612b8954dff673c924b3687ba87f3936ff792e"
export SLEPC_STRING="slepc"

#
# Sundials
#
export SUNDIALS_OPTIONS="--with-sundials=1 --download-sundials"
export SUNDIALSSTRING="sundials"

#
# SuperLU
#
%if "%{use_superlu}" == "1"
  export SUPERLU_OPTIONS="--with-superlu_dist=1 --download-superlu_dist \
   --with-superlu=1 --download-superlu ${PARMETIS_OPTIONS}"
  export superlustring="superlu (distributed/sequential)"
%endif

#
# Zoltan
# 
%if "%{comp_fam}" == "intel"
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
	ZOLTAN_OPTIONS= ;      ZOLTANSTRING= ;
                ;;
esac

##
## define packages; some are real & complex, others real only.
##
export complexpackages="${ADIOS_STRING} ${ELEMENTAL_STRING} ${FFTW_STRING} mumps scalapack ${SPOOLES_STRING} ${SLEPC_STRING} ${SUITESPARSE_STRING} ${superlustring} ${ZOLTANSTRING} ${hdf5string}"
export PETSC_COMPLEX_PACKAGES="\
  ${ADIOS_OPTIONS} \
  ${ELEMENTAL_OPTIONS} \
  ${FFTW_OPTIONS} \
  ${hdf5download} \
  ${MUMPS_OPTIONS}\
  ${SCALAPACK_OPTIONS} ${SPOOLES_OPTIONS} ${SLEPC_OPTIONS} \
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
esac

export packageslisting="${packageslisting} ${INDEX_STRING}"

#
# blas/lapack
#
export BLAS_LAPACK_OPTIONS="\
  ${BLAS_LAPACK_LOAD} \
  "
export noblas="\
  --with-blas-lib=[${THEBLAS}] \
  --with-lapack-lib=[${THEBLAS}] \
  "

#
# MPI settings
#
export MPICC=`which mpicc`
export MPICXX=`which mpicxx`
export MPIF90=`which mpif90`
echo "setting mpicc=${MPICC}"

# export MPI_OPTIONS="--with-mpi=1"
# # compilers are found by giving the "--with-mpi-dir"
# # --with-cc=${MPICC} --with-cxx=${MPICXX} --with-fc=${MPIF90}"
# %if "%{is_impi}" == "1"
#   export MPI_OPTIONS="${MPI_OPTIONS} \
#     --with-mpi-dir=${MPICH_HOME}/intel64 \
#     "
#   export full_MPI_OPTIONS="${MPI_OPTIONS} \
#     --with-cc=icc --with-fc=ifort --with-cxx=icpc \
#     --with-mpi-include=${TACC_IMPI_INC} \
#     --with-mpi-lib=[${TACC_IMPI_LIB}/libmpifort.so,${TACC_IMPI_LIB}/release_mt/libmpi.so] \
#      "
# %else
#   # why do we define this?
#   export MPI_OPTIONS="${MPI_OPTIONS} --with-mpi-dir=${MPICH_HOME}"
# %endif

export MPI_OPTIONS="--with-mpi=1"
# compilers are found by giving the "--with-mpi-dir"
# --with-cc=${MPICC} --with-cxx=${MPICXX} --with-fc=${MPIF90}"
%if "%{is_impi}" == "1"
  # why do we define this?
  export PETSC_MPICH_HOME="${MPICH_HOME}/intel64"
  export MPI_OPTIONS="${MPI_OPTIONS} --with-mpi-dir=${PETSC_MPICH_HOME}"
%else
  # why do we define this?
  export PETSC_MPICH_HOME="${MPICH_HOME}"
  export MPI_OPTIONS="${MPI_OPTIONS} --with-mpi-dir=${MPICH_HOME}"
%endif


%if "%{is_impi}" == "1"
  export I_MPI_LIBRARY_KIND=release_mt
  export I_MPI_LINK=opt_mt
%endif

#
# Petsc4py
#
##module use /opt/apps/intel19/impi19_0/modulefiles
module load python3
if [ %{p4p} -eq 1 ] ; then
  export petsc4py="--download-petsc4py=yes --with-python=1 --with-python-exec=python3"
fi
module list

#
# single precision
# (see also the rtx clause)
#
export precision=--with-precision=double
case "${ext}" in
( *single* ) 
    export precision=--with-precision=single ;
    export packageslisting= ;
    export packages= ;;
esac

#
# Cuda
# (see also the XOPTFLAGS)
#
export CUDA_OPTIONS=
case "${ext}" in
( *rtx* )
    module load cuda/10.2
#    export CUDA_OPTIONS="--with-cuda=yes --with-cudac=nvcc --with-cuda-include=${TACC_CUDA_DIR}/targets/x86_64-linux/include/ --with-cuda-lib=[${TACC_CUDA_DIR}/targets/x86_64-linux/lib/libcufft.so,libcusparse.so,libcusolver.so,libcublas.so,libcuda.so,libcudart.so] --download-cusp=yes CUDAFLAGS=-arch=sm_70 "
    export CUDA_OPTIONS="--with-cuda=1 --with-cuda-dir=${TACC_CUDA_DIR} --with-cudac=/opt/apps/cuda/10.2/bin/nvcc --with-cuda-gencodearch=70"
    export precision=--with-precision=single ;
    export packageslisting= ;
    export packages= ;;
esac

case "${ext}" in
*i64* ) 
    export packageslisting= ;
    export packages= ;;
esac 

#
# petsc can run single processor with a fake mpi
# in that case: no external packages, and explicit non-mp cc/fc compilers
#
case "${ext}" in
uni* ) export MPI_OPTIONS="--with-mpi=0 --with-cc=${CC} --with-fc=${FC} --with-cxx=0";
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
if [ "${ext}" = "tau" ] ; then
  module load papi/5.3.0 tau
  export TAU_MAKEFILE=$TACC_TAU_DIR/x86_64/lib/Makefile.tau-phase-icpc-papi-mpi-pdt
  export TAU_OPTIONS="${TAU_OPTIONS} -optRevert"
  ./configure \
    --with-fc=0 \
    CC="${TACC_TAU_DIR}/x86_64/bin/tau_cc.sh -I${MPICH_HOME}/include -mkl" \
    CXX="${TACC_TAU_DIR}/x86_64/bin/tau_cxx.sh -I${MPICH_HOME}/include -mkl" \
    --with-batch --known-mpi-shared-libraries=1
else

  module list
  # python config/configure.py
  export I_MPI_FABRICS=shm:tmi
  RPM_BUILD_ROOT=tmpfs PETSC_DIR=`pwd` ./configure \
    ${PETSC_CONFIGURE_OPTIONS} \
    --with-packages-search-path=[${EXTERNAL_PACKAGES_DIR}] \
    --with-packages-build-dir=${PACKAGES_BUILD_DIR} \
    ${MPI_OPTIONS} ${MPI_EXTRA_OPTIONS} \
    ${clanguage} ${scalar} ${dynamicshared} ${precision} ${packages} \
    ${petsc4py} ${slepc} \
    --with-debugging=${usedebug} \
    ${BLAS_LAPACK_OPTIONS} ${CUDA_OPTIONS} ${INDEX_OPTIONS} \
    CFLAGS="${CFLAGS}" FFLAGS="${FFLAGS}" CXXFLAGS="${CXXFLAGS}"
fi

export noops="\
    --with-packages-download-dir=${PACKAGE_DOWNLOAD_DIR} \
    "
####
#### post-processing fixes
#### <<<<<<<<<<<<<<<<
####
pushd ${architecture}
pwd
ls

# fix a weird bug that trips up John Peterson
if [ `ls ./lib/libsundials*.la | wc -l` -gt 0 ] ; then
  for f in ./lib/libsundials*.la ; do
    sed -i -e "/dependency_libs/s/lmpi./lmpi/" $f
  done
fi

popd
####
#### >>>>>>>>>>>>>>>>
####

##
## Make!

PETSC_DIR=`pwd` PETSC_ARCH=${architecture} make MAKE_NP=12 V=1
##
##

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
local             petsc_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(petsc_dir,petsc_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(petsc_dir,petsc_arch,"lib") )

setenv("PETSC_ARCH",            petsc_arch)
setenv("PETSC_DIR",             petsc_dir)
setenv("TACC_PETSC_DIR",        petsc_dir)
setenv("TACC_PETSC_BIN",        pathJoin(petsc_dir,petsc_arch,"bin") )
setenv("TACC_PETSC_INC",        pathJoin(petsc_dir,petsc_arch,"include") )
setenv("TACC_PETSC_LIB",        pathJoin(petsc_dir,petsc_arch,"lib") )
EOF

if [ %{p4p} -eq 1 ] ; then
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
prepend_path("PYTHONPATH", pathJoin(petsc_dir,petsc_arch,"lib") )
EOF
fi

case "${ext}" in
( *rtx* ) 
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF

depends_on("cuda")
EOF
;;
esac

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Petsc %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua 

rm -rf ${PACKAGES_BUILD_DIR}

##
## end of module file loop
##
done

cp -r config include lib makefile src \
    $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r clx* \
    $RPM_BUILD_ROOT/%{INSTALL_DIR}

popd
umount %{INSTALL_DIR}

echo "Directory to package up: $RPM_BUILD_ROOT/%{INSTALL_DIR}"
echo "listing:"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

%files %{PACKAGE}-debug
  %defattr(-,root,install,)
  %{INSTALL_DIR}/config
  %{INSTALL_DIR}/include
  %{INSTALL_DIR}/lib
  %{INSTALL_DIR}/makefile
  %{INSTALL_DIR}/src 
  %{INSTALL_DIR}/clx-debug
  %{INSTALL_DIR}/clx-unidebug
  %{INSTALL_DIR}/clx-complexi64debug
  %{INSTALL_DIR}/clx-complexdebug
  %{INSTALL_DIR}/clx-i64debug
  %{INSTALL_DIR}/clx-single-debug
%if "%{cuda}" == "1"
  %{INSTALL_DIR}/clx-rtxdebug
%endif

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}/clx
  %{INSTALL_DIR}/clx-uni
  %{INSTALL_DIR}/clx-complexi64
  %{INSTALL_DIR}/clx-complex
  %{INSTALL_DIR}/clx-i64
  %{INSTALL_DIR}/clx-single
%if "%{cuda}" == "1"
  %{INSTALL_DIR}/clx-rtx
%endif
  %{INSTALL_DIR}/clx-nohdf5
  %{INSTALL_DIR}/clx-hyprefei

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Tue May 04 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: temporarily remove elemental
* Wed Apr 14 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: better cuda specification, release_mt fix, rpm reorg
* Thu Apr 01 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
