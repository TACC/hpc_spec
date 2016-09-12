Summary: PETSc install

# Give the package a base name
%define pkg_base_name petsc
%define MODULE_VAR    PETSC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 7
%define micro_version 3
%define versionpatch 3.7.3

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

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

Release: 1%{?dist}
License: BSD-like; see src/docs/website/documentation/copyright.html
Vendor: Argonne National Lab, MCS division
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{major_version}.%{minor_version}.%{micro_version}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
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
%description %{PACKAGE}-sources
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description %{MODULEFILE}
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.

%prep

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

##
## Hypre
##
export HYPRE_OPTIONS="--with-hypre=1 --download-hypre"
export HYPRESTRING=hypre

%if "%{is_intel}" == "1"
export LOCALCC=icc
export LOCALFC=ifort
export XOPTFLAGS="-xAVX -axCORE-AVX2,CORE-AVX-I -g"
#### "-xCORE-AVX2 -xMIC-AVX512 -g"
export COPTFLAGS=${XOPTFLAGS}
#"-xhost -O2"
export CXXOPTFLAGS=${XOPTFLAGS}
export FOPTFLAGS=${XOPTFLAGS}

export CNOOPTFLAGS="-O0 -g" ; export CXXNOOPTFLAGS="-O0 -g" ; export FNOOPTFLAGS="-O0 -g"
%endif

%if "%{is_mvapich2}" == "1"
export MPI_EXTRA_OPTIONS="--with-mpiexec=mpirun_rsh"
%endif

# matlab will only be invoked for real packages
#module load matlab
#export MATLABOPTIONS="--with-matlab --with-matlab-dir=${TACC_MATLAB_DIR}"

export PETSC_CONFIGURE_OPTIONS="\
  --with-x=0 -with-pic \
  --with-external-packages-dir=%{INSTALL_DIR}/externalpackages \
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
export dynamiccc="i64 debug i64debug uni unidebug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"
#export static="cxxstatic cxxstaticdebug static staticdebug complexstatic complexstaticdebug cxxcomplexstatic cxxcomplexstaticdebug"
#module load python

for ext in \
  single "" \
  ${dynamiccc} ${dynamiccxx} \
  ; do

export noext="\
  reinstate: \
  \
  ${dynamiccxx} \
  tau \
  ${static} we don't do static anymore \
  nono"

echo "configure install for ${ext}"
export versionextra=

if [ -z "${ext}" ] ; then
  export architecture=sandybridge
else
  export architecture=sandybridge-${ext}
fi

##
## C compiler flags
export usedebug=no
export CFLAGS="${COPTFLAGS}"
export CXXFLAGS="${CXXOPTFLAGS}"
export FFLAGS="${FOPTFLAGS}"
case "${ext}" in 
*debug ) export usedebug=yes 
	export CFLAGS="${CNOOPTFLAGS}"
	export CXXFLAGS="${CXXNOOPTFLAGS}"
	export FFLAGS="${FNOOPTFLAGS}"
         ;;
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
# not available with gcc right now
export hdf5string=
export hdf5download=
export hdf5versionextra=

%if "%{comp_fam}" == "intel" && "%{comp_fam_ver}" != "intel15"
    export hdf5string="hdf5"
    export hdf5download="--with-hdf5=1 --with-hdf5-dir=${TACC_HDF5_DIR}"
    export hdf5versionextra="; hdf5 support"
%endif

# waiting for McLay
export hdf5string=
export hdf5download=
export hdf5versionextra=

if [ ! -z "${hdf5string}" ] ; then
    module load phdf5
fi

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
# Mumps & Superlu depend on parmetis which depends on metis
export PARMETIS_OPTIONS="--with-parmetis=1 --download-parmetis --with-metis=1 --download-metis"
export MUMPS_OPTIONS="--with-mumps=1 --download-mumps ${PARMETIS_OPTIONS}"
export SUPERLU_OPTIONS="--with-superlu_dist=1 --download-superlu_dist \
   --with-superlu=1 --download-superlu ${PARMETIS_OPTIONS}"
export superlustring="superlu (distributed/sequential)"
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

##
## 64-bit indices
##
INDEX_OPTIONS=
case "${ext}" in
*i64* ) INDEX_OPTIONS=--with-64-bit-indices ;
        CHACO_OPTIONS= ;   CHACOSTRING= ;
        MUMPS_OPTIONS= ;   MUMPSTRING= ;
	ML_OPTIONS= ;      ML_STRING= ;
	PLAPACK_OPTIONS= ; PLAPACK_STRING= ;
        SPAI_OPTIONS= ;    SPAITRING= ;
	SPOOLES_OPTIONS= ; SPOOLES_STRING= ;
	SUPERLU_OPTIONS= ; SUPERLU_STRING= ;
                ;;
esac

##
## define packages; some are real & complex, others real only.
##
export complexpackages="mumps scalapack spooles ${superlustring}"
export PETSC_COMPLEX_PACKAGES="\
  ${MUMPS_OPTIONS}\
  ${SCALAPACK_OPTIONS} ${SPOOLES_OPTIONS} \
  ${hdf5download} \
  "
export realonlypackages="${CHACOSTRING} ${hdf5string} ${HYPRESTRING} ${MLSTRING} parmetis spai ${PLAPACKSTRING}"

export PETSC_REALONLY_PACKAGES="\
  ${CHACO_OPTIONS} \
  ${HYPRE_OPTIONS} ${ML_OPTIONS} \
  ${MATLABOPTIONS} ${ML_OPTIONS} \
  ${PLAPACKOPTIONS} ${SPAI_OPTIONS} ${SUPERLU_OPTIONS} \
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
# cuda
#
export CUDA_OPTIONS=
%if "%{comp_fam}" == "gcc"
module load cuda/6.0 cusp/0.3
export CUDA_OPTIONS="--with-cuda=1 --with-cuda-dir=${TACC_CUDA_DIR} \
	--with-cudac=${TACC_CUDA_BIN}/nvcc \
	--with-cusp-dir=${TACC_CUSP_DIR} --with-thrust-dir=${TACC_CUDA_DIR}/include/ \
	"
%endif
case "${ext}" in
*complex* ) export CUDA_OPTIONS= 
            ;;
esac
export CUDA_OPTIONS=

export FPIC_OPTIONS=
#
# petsc can run single processor with a fake mpi
# in that case: no external packages, and explicit non-mp cc/fc compilers
#
%if "%{is_impi}" == "1"
  export PETSC_MPICH_HOME="${MPICH_HOME}/intel64"
#  export mpi="--with-cc=/opt/apps/intel15/impi/5.0.2.044/intel64/bin/mpicc
%else
  export PETSC_MPICH_HOME="${MPICH_HOME}"
%endif
  export mpi="--with-mpi-compilers=1 --with-mpi-dir=${PETSC_MPICH_HOME}"
echo "Finding mpi in ${PETSC_MPICH_HOME}"

case "${ext}" in
uni* ) export mpi="--with-mpi=0 --with-cc=${CC} --with-fc=${FC} --with-cxx=0";
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

##
## here we go
##
export PETSC_ARCH=${architecture}
noprefix=--prefix=%{INSTALL_DIR}/${architecture}
#export packages=
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
  RPM_BUILD_ROOT=tmpfs PETSC_DIR=`pwd` ./configure \
    ${PETSC_CONFIGURE_OPTIONS} \
    ${mpi} ${clanguage} ${scalar} ${dynamicshared} ${precision} ${packages} \
    --with-debugging=${usedebug} \
    ${BLAS_LAPACK_OPTIONS} ${MPI_EXTRA_OPTIONS} ${CUDA_OPTIONS} ${INDEX_OPTIONS} \
    --CFLAGS="${CFLAGS}" --FFLAGS="${FFLAGS}" --CXXFLAGS="${CXXFLAGS}"
fi

# # prevent compiler overflow on nasty routines
# case "${ext}" in
#   ( \
#   cxx* \
# %if "%{is_pgi}" == "1"
# %if "%{is_mvapich2}" == "1"
#   | "complex" \
# %endif
# %endif
#   )
#     for fmt in baij sbaij ; do
#       pushd src/mat/impls/${fmt}/seq
#       cp makefile makefile.bak
#       echo "PCC_FLAGS = -g -fPIC" >> makefile
#       popd
#     done
# esac

##
## Make!
PETSC_DIR=`pwd` PETSC_ARCH=${architecture} make MAKE_NP=4
##
##

# as of 3.7 the object files are kept. I don't think we need them
/bin/rm -rf $PETSC_ARCH/obj/src

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
The petsc module defines the following environment variables:
TACC_PETSC_DIR, TACC_PETSC_BIN, and
TACC_PETSC_LIB for the location
of the Petsc distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: PETSc" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/petsc/petsc-as/" )
whatis( "Description: Numerical library for sparse linear algebra" )

local             petsc_arch =    "${architecture}"
local             petsc_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(petsc_dir,petsc_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(petsc_dir,petsc_arch,"lib") )

setenv("PETSC_ARCH",            petsc_arch)
setenv("PETSC_DIR",             petsc_dir)
setenv("TACC_PETSC_DIR",        petsc_dir)
setenv("TACC_PETSC_BIN",        pathJoin(petsc_dir,petsc_arch,"bin") )
setenv("TACC_PETSC_LIB",        pathJoin(petsc_dir,petsc_arch,"lib") )
EOF

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

rm -rf ${architecture}/obj
cp -r bin config externalpackages include lib makefile src    \
                                     $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r sandybridge*                   $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r %{MODULE_DIR}/                $RPM_BUILD_ROOT/%{MODULE_DIR}

#find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name CMakeFiles -exec rm -rf {} \;

popd
umount tmpfs # $INSTALL_DIR

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}/sandybridge*

%files %{PACKAGE}-sources
  %defattr(-,root,install,)
%{INSTALL_DIR}/bin 
%{INSTALL_DIR}/config
%{INSTALL_DIR}/externalpackages
%{INSTALL_DIR}/include
%{INSTALL_DIR}/lib
%{INSTALL_DIR}/makefile
%{INSTALL_DIR}/src 

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Sun Aug 14 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
