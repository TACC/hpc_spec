Summary: PETSc install

Name: petsc
Version: 3.5
%define versionpatch 3.5.4
Release: 1
License: BSD-like; see src/docs/website/documentation/copyright.html
Vendor: Argonne National Lab, MCS division
Group: Development/Numerical-Libraries
Summary: Scientific computing toolkit
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{name}-%{versionpatch}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%package -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-static
Summary: Petsc local binary install
Group: System Environment/Base
%package -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-shared
Summary: Petsc local binary install
Group: System Environment/Base

%description
%description -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-static
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.
%description -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-shared
PETSC is the Portable Extendible Toolkit for Scientific Computing.
It contains solvers and tools mostly for PDE solving.

%prep

%setup -n petsc-%{versionpatch}

%build

%install

echo "Date: `date`"
echo "$BASH_ENV"

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

# is new enough on wrangler module load cmake
%if "%{comp_fam}" == "gcc"
  module load mkl
%endif
export BLAS_LAPACK_LOAD=--with-blas-lapack-dir=${MKLROOT}

##
## ML
##
export MLOPTIONS="--with-ml=1 --download-ml"
export MLSTRING=ml
%if "%{is_impi}" == "1"
export MLOPTIONS=
export MLSTRING=
%endif
# %if "%{is_mvapich2}" == "1"
# export MLOPTIONS=
# export MLSTRING=
# %endif

##
## Hypre
##
export HYPREOPTIONS="--with-hypre=1 --download-hypre"
export HYPRESTRING=hypre

%if "%{is_intel11}" == "1"
module load intel
export LOCALCC=icc
export LOCALFC=ifort
export COPTFLAGS=-xW ; export CXXOPTFLAGS=-xW ; export FOPTFLAGS=-xW
export CNOOPTFLAGS="-O0 -g" ; export CXXNOOPTFLAGS="-O0 -g" ; export FNOOPTFLAGS="-O0 -g"
export CHACOSTRING=chaco
export CHACOOPTIONS="--with-chaco=1 --download-chaco"
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
export dynamiccc="debug uni unidebug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug"
#export static="cxxstatic cxxstaticdebug static staticdebug complexstatic complexstaticdebug cxxcomplexstatic cxxcomplexstaticdebug"
#module load python

for ext in \
  single "" \
  ${dynamiccc} ${dynamiccxx} \
  ; do

export noext="\
  ${dynamiccxx} \
  tau \
  ${static} we don't do static anymore \
  nono"

echo "configure install for ${ext}"
export versionextra=

if [ -z "${ext}" ] ; then
  export architecture=haswell
else
  export architecture=haswell-${ext}
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
# Mumps & Superlu depend on parmetis which depends on metis
export PARMETIS_OPTIONS="--with-parmetis=1 --download-parmetis --with-metis=1 --download-metis"
export MUMPS_OPTIONS="--with-mumps=1 --download-mumps ${PARMETIS_OPTIONS}"
export SUPERLU_OPTIONS="--with-superlu_dist=1 --download-superlu_dist \
   --with-superlu=1 --download-superlu ${PARMETIS_OPTIONS}"
# %if "%{comp_fam_ver}" == "intel15"
#   export MUMPS_OPTIONS=
#   export SUPERLU_OPTIONS=
# %endif

export SCALAPACK_OPTIONS="--with-scalapack=1 --download-scalapack --with-blacs=1 --download-blacs"
# %if "%{comp_fam_ver}" == "intel15"
#   export SCALAPACK_OPTIONS=
# %endif

##
## define packages; some are real & complex, others real only.
##
%define complexpackages mumps scalapack spooles superlu (sequential/distributed)
export PETSC_COMPLEX_PACKAGES="\
  ${MUMPS_OPTIONS}\
  ${SCALAPACK_OPTIONS} \
  --with-spooles=1 --download-spooles \
  ${hdf5download} \
  "
%define realonlypackages ${CHACOSTRING} ${hdf5string} ${HYPRESTRING} ${MLSTRING} parmetis spai ${PLAPACKSTRING} 
# ml
export PETSC_REALONLY_PACKAGES="\
  ${CHACOOPTIONS} \
  ${HYPREOPTIONS} ${MLOPTIONS} \
  ${MATLABOPTIONS} ${MLOPTIONS} \
  ${PLAPACKOPTIONS} ${SUPERLU_OPTIONS} \
  --with-spai=1 --download-spai \
  "

export packages="${PETSC_REALONLY_PACKAGES} ${PETSC_COMPLEX_PACKAGES}"
export scalar="--with-scalar-type=real"
case "${ext}" in
*complex* ) export packages="${PETSC_COMPLEX_PACKAGES}"
           export scalar="--with-scalar-type=complex --with-fortran-kernels=1"
           ;;
esac
#export packages=

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
  export mpi="--with-mpi-compilers=1 --with-mpi-dir=${MPICH_HOME}/intel64/lib"
%else
  export mpi="--with-mpi-compilers=1 --with-mpi-dir=${MPICH_HOME}"
%endif
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
  PETSC_DIR=`pwd` python config/configure.py \
    ${PETSC_CONFIGURE_OPTIONS} \
    ${mpi} ${clanguage} ${scalar} ${dynamicshared} ${precision} ${packages} \
    --with-debugging=${usedebug} \
    ${BLAS_LAPACK_OPTIONS} ${MPI_EXTRA_OPTIONS} ${CUDA_OPTIONS} \
    --COPTFLAGS="$CFLAGS" --FOPTFLAGS="$FFLAGS" --CXXOPTFLAGS="${CXXFLAGS}"
fi

# VLE why? `if [ ! -z "${USECXX}" ] ; then echo '--CXXOPTFLAGS="${CXXFLAGS}"' ; else echo '-with-cxx=0' ; fi`

# prevent compiler overflow on nasty routines
case "${ext}" in
  ( \
  cxx* \
%if "%{is_pgi}" == "1"
%if "%{is_mvapich2}" == "1"
  | "complex" \
%endif
%endif
  )
    for fmt in baij sbaij ; do
      pushd src/mat/impls/${fmt}/seq
      cp makefile makefile.bak
      echo "PCC_FLAGS = -g -fPIC" >> makefile
      popd
    done
esac

##
## Make!
PETSC_DIR=`pwd` PETSC_ARCH=${architecture} make MAKE_NP=2
##
##

# roll back compiler overflow changes
case ${ext} in
  ( \
  cxx* \
%if "%{is_pgi}" == "1"
%if "%{is_mvapich2}" == "1"
  | "complex" \
%endif
%endif
  )
    for fmt in baij sbaij ; do
      pushd src/mat/impls/${fmt}/seq
      mv -f makefile.bak makefile
      popd
    done
esac

pushd conf
  mv rules rules.bak
  cat rules.bak \
  | sed '/^chkopts:/ { n ;  s/SHLIBS/SHLIBSdisable/ }' \
  > rules
  rm -f rules.bak
popd
pushd ${architecture}/conf
  mv configure.log tmp.log
  cat tmp.log | sed /rpmbuild/d > configure.log
  rm tmp.log
popd

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

export packageslisting="%{realonlypackages} %{complexpackages}"
case "${ext}" in
"*complex*" ) export packages="%{complexpackages}" ;;
"-uni*"     ) export packages="" ;;
esac

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

cp -r bin conf config externalpackages include makefile src    \
                                     $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r sandybridge*                   $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r %{MODULE_DIR}/                $RPM_BUILD_ROOT/%{MODULE_DIR}

#find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name CMakeFiles -exec rm -rf {} \;

popd
umount tmpfs # $INSTALL_DIR

%files -n %{name}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}-shared
%defattr(755,root,install)
%{MODULE_DIR}
%{INSTALL_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Tue Jun  02 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
