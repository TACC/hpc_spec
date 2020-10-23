Summary: PETSc install

# Give the package a base name
%define pkg_base_name petsc
%define MODULE_VAR    PETSC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 14
%define micro_version 0
%define versionpatch %{major_version}.%{minor_version}.%{micro_version}

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define p4p 1

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

# note the %{p4p} macro!
export USE_PETSC4PY=1
export USE_HDF5=1
export USE_FFTW3=1
export USE_HYPRE=1
export USE_ZOLTAN=1

%if "%{comp_fam}" == "gcc"
#export USE_PETSC4PY=0
export USE_HDF5=0
export USE_FFTW3=0
%endif

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

## gcc9 & zoltan go wrong without this
sed -i -e '/if not flag in/s/\[/["-fstack-protector",/' \
    config/BuildSystem/config/package.py

# echo "contents of install-dir before installation"
# ls
# export PETSC_DIR=`pwd`

module load cmake
%if "%{p4p}" == "1"
  module load python3
%endif
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
export dynamiccc="debug i64 i64debug complex complexdebug complexi64 complexi64debug uni unidebug nohdf5 hyprefei"

for ext in \
  "" \
  single \
  ${dynamiccc} \
  ; do

echo "configure install for ${ext}"
export versionextra=

if [ -z "${ext}" ] ; then
  export architecture=skylake
else
  export architecture=skylake-${ext}
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
export ELEMENTAL_OPTIONS="--with-elemental=1 --download-elemental --with-cxx-dialect=C++11 ${PARMETIS_OPTIONS}"
export ELEMENTAL_STRING=elemental

#
# Fftw
#
if [ "${USE_FFTW3}" = "1" ] ; then
  module load fftw3
  export FFTW_OPTIONS="--with-fftw=1 --with-fftw-dir=${TACC_FFTW3_DIR}"
  export FFTW_STRING=fftw
fi

if [ "%{comp_fam}" = "gcc" ] ; then
  export FFTW_OPTIONS="--download-fftw=1"
  export FFTW_STRING=fftw
fi

##
## hdf5
##

if [ "${USE_HDF5}" -eq 1 ] ; then
  export HAS_HDF5=1
  export hdf5string="hdf5"
  #export hdf5download="--with-hdf5=1 --download-hdf5=1"
  #--with-hdf5-dir=${TACC_HDF5_DIR}"
  module load phdf5
  export hdf5download="--with-hdf5=1 --with-hdf5-dir=${TACC_HDF5_DIR}"
  export hdf5versionextra="; hdf5 support"

  case "${ext}" in
  *nohdf5* ) export HAS_HDF5=0
	  export hdf5string=
	  export hdf5download=
	  export hdf5versionextra=
	  module unload hdf5 phdf5
	  ;;
  esac
  export versionextra="${versionextra}${hdf5versionextra}"
fi


#
# Hypre
#
if [ "${USE_HYPRE}"  = 1 ] ; then
  export HYPRE_OPTIONS="--with-hypre=1 --download-hypre"
  export HYPRESTRING=hypre
  case "${ext}" in
  hyprefei ) 
      export HYPRE_OPTIONS="${HYPRE_OPTIONS} --download-hypre-configure-arguments=--with-fei"
      ;;
  esac
fi

#
# Mumps & Superlu depend on parmetis which depends on metis
#
export MUMPS_OPTIONS="--with-mumps=1 --download-mumps ${PARMETIS_OPTIONS}"
export SCALAPACK_OPTIONS="--with-scalapack=1 --download-scalapack --with-blacs=1 --download-blacs"

#
# petsc4py
#
if [ "${USE_PETSC4PY}" = 1 ] ; then
  export PETSC4PY_OPTIONS="--download-petsc4py=1 --with-python-exec=`which python3`"
fi

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
# Sundials
#
export SUNDIALS_OPTIONS="--with-sundials=1 --download-sundials"
export SUNDIALSSTRING="sundials"

#
# SuperLU
#
export SUPERLU_OPTIONS="--with-superlu_dist=1 --download-superlu_dist \
   --with-superlu=1 --download-superlu ${PARMETIS_OPTIONS}"
export superlustring="superlu (distributed/sequential)"

#
# Zoltan
# 
if [ "${USE_ZOLTAN}" = "1" ] ; then
  export ZOLTAN_OPTIONS="--with-zoltan=1 --download-zoltan=1 --download-ptscotch=1"
  export ZOLTANSTRING="zoltan/ptscotch"
fi

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
# we have no cuda on stampede
#
export CUDA_OPTIONS=

#
# petsc can run single processor with a fake mpi
# in that case: no external packages, and explicit non-mp cc/fc compilers
#
export MPICC=`which mpicc`
export MPICXX=`which mpicxx`
export MPIF90=`which mpif90`
echo "setting mpicc=${MPICC}"
ls -l ${MPICC}

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
echo "Finding mpi in ${MPICH_HOME}"

case "${ext}" in
uni* ) export MPI_OPTIONS="--with-mpi=0 --with-cc=${CC} --with-fc=${FC} --with-cxx=0";
       export packages= ;;
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

if [ "%{comp_fam}" = "gcc" ] ; then
  # this is TACC_INTEL_LIB
  # -L/opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64/ -lirc
  # /opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64/libirc.so
  export EXTRALIBS="-L/opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64/ -Wl,-rpath,/opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64/ -lirc"
  #export EXTRALIBS=/opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64/libirc.so
fi

##
## here we go
##
ls /opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64/libirc.so

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

  # python config/configure.py
  export I_MPI_FABRICS=shm:tmi
  RPM_BUILD_ROOT=tmpfs PETSC_DIR=`pwd` ./configure \
    ${PETSC_CONFIGURE_OPTIONS} ${PETSC4PY_OPTIONS} \
    --with-packages-search-path=[${EXTERNAL_PACKAGES_DIR}] \
    --with-packages-build-dir=${PACKAGES_BUILD_DIR} \
    ${MPI_OPTIONS} ${clanguage} ${scalar} ${dynamicshared} ${precision} ${packages} \
    --with-debugging=${usedebug} \
    --LIBS="${EXTRALIBS}" \
    ${BLAS_LAPACK_OPTIONS} ${MPI_EXTRA_OPTIONS} ${CUDA_OPTIONS} ${INDEX_OPTIONS} \
    COPTFLAGS="${CFLAGS}" FOPTFLAGS="${FFLAGS}" CXXOPTFLAGS="${CXXFLAGS}"
fi

export noops="\
    ` if [ ! -z ${EXTRALIBS} ] ; then echo --LIBS="${EXTRALIBS}" ; fi ` \
    --with-packages-download-dir=${PACKAGE_DOWNLOAD_DIR} \
    "
####
#### post-processing fixes
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

# lower optimization for intel complex
# this is the petsc 3.8 location. no longer works in 3.9
%if "%{is_intel}" == "1"
case "${ext}" in 
  ( *pomplex* )
    for c in src/mat/impls/baij/seq/*.c ; do
      export CFLAGS=${LOPTFLAGS} ; \
      make -f gmakefile V=1 PCC_FLAGS="${LOPTFLAGS} -fPIC" \
          ${PETSC_ARCH}/obj/${c%%.c}.o
    done
    export CFLAGS=${XOPTFLAGS}
  ;;
esac
%endif

# and now the rest with full optimization
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

%if "%{p4p}" == "1"
cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF

prepend_path("PYTHONPATH",      pathJoin(petsc_dir,petsc_arch,"lib") )
EOF
%endif

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
cp -r skylake* \
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
  %{INSTALL_DIR}/skylake
  %{INSTALL_DIR}/skylake-single
  %{INSTALL_DIR}/skylake-i64
  %{INSTALL_DIR}/skylake-debug
  %{INSTALL_DIR}/skylake-i64debug
  %{INSTALL_DIR}/skylake-uni
  %{INSTALL_DIR}/skylake-unidebug
  %{INSTALL_DIR}/skylake-nohdf5
  %{INSTALL_DIR}/skylake-hyprefei
  %{INSTALL_DIR}/skylake-complex
  %{INSTALL_DIR}/skylake-complexi64
  %{INSTALL_DIR}/skylake-complexdebug
  %{INSTALL_DIR}/skylake-complexi64debug

# %files %{PACKAGE}-xx
#   %defattr(-,root,install,)
  # # and debug variants
  # %{INSTALL_DIR}/skylake-cxx
  # %{INSTALL_DIR}/skylake-cxxi64
  # %{INSTALL_DIR}/skylake-cxxdebug
  # %{INSTALL_DIR}/skylake-cxxi64debug
#  %{INSTALL_DIR}/skylake-cxxcomplex
#  %{INSTALL_DIR}/skylake-cxxcomplexdebug

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
# remember to notify OpenSees: Ian Wang
* Wed Sep 30 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
