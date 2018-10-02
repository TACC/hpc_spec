#
# Portable Extendible Toolkit for Scientific Computing
# spec file by Victor Eijkhout
#
# Adapted from Bar.spec, Cyrus Proctor & Antonio Gomez
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

Summary: PETSc rpm build script

# Give the package a base name
%define pkg_base_name petsc
%define MODULE_VAR    PETSC

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 9
%define micro_version 3

%define pkg_version %{major_version}.%{minor_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   5
License:   GPL
Group:     Development/Tools
URL:       http://www.mcs.anl.gov/petsc/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: PETSc rpm building
Group: HPC/libraries
%description %{PACKAGE}
Portable Extendible Toolkit for Scientific Computations

%package %{PACKAGE}-xx
Summary: PETSc rpm building
Group: HPC/libraries
%description %{PACKAGE}-xx
Portable Extendible Toolkit for Scientific Computations

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
The longer-winded description of the package that will 
end in up inside the rpm and is queryable if installed via:
rpm -qi <rpm-name>


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_full_version}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-load.inc
%include mpi-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

# VLE here is where we start copying from the old spec file
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 
cp -r * %{INSTALL_DIR}
pushd %{INSTALL_DIR}
echo "contents of install-dir before installation"
ls
export PETSC_DIR=`pwd`
export SRC_DIR=%{_topdir}/SOURCES

module load cmake valgrind
%if "%{comp_fam}" == "gcc"
  module load mkl
%endif
export BLAS_LAPACK_LOAD=--with-blas-lapack-dir=${MKLROOT}

##
## ML
##
export ML_OPTIONS="--with-ml=1 --download-ml"
export ML_STRING=ml
%if "%{is_impi}" == "1"
export ML_OPTIONS=
export ML_STRING=
%endif
# %if "%{is_mvapich2}" == "1"
# %endif

### we have a hard time cloning this on s2
export ML_OPTIONS=
export ML_STRING=

##
## Hypre
##
export HYPRE_OPTIONS="--with-hypre=1 --download-hypre=1"
#export HYPRE_OPTIONS="--with-hypre=1 --download-hypre=${SRC_DIR}/git.hypre.tgz"
export HYPRE_STRING=hypre

%if "%{is_intel}" == "1"
export LOCALCC=icc
export LOCALFC=ifort
export COPTFLAGS="-xhost -O2 -g" ; export CXXOPTFLAGS="-xhost -O2 -g" ; export FOPTFLAGS="-xhost -O2 -g"
export CNOOPTFLAGS="-O0 -g" ; export CXXNOOPTFLAGS="-O0 -g" ; export FNOOPTFLAGS="-O0 -g"
%else
export COPTFLAGS=" -O2 -g" ; export CXXOPTFLAGS="-O2 -g" ; export FOPTFLAGS="-O2 -g"
export CNOOPTFLAGS="-O0 -g" ; export CXXNOOPTFLAGS="-O0 -g" ; export FNOOPTFLAGS="-O0 -g"
%endif

%if "%{is_mvapich2}" == "1"
export MPI_EXTRA_OPTIONS="--with-mpiexec=mpirun_rsh"
%endif

# matlab will only be invoked for real packages
#module load matlab
#export MATLABOPTIONS="--with-matlab --with-matlab-dir=${TACC_MATLAB_DIR}"


export EXTERNAL_PACKAGES_DIR=/tmp/petsc-stuff/externalpackages-%{pkg_version}
rm -rf ${EXTERNAL_PACKAGES_DIR}
mkdir -p ${EXTERNAL_PACKAGES_DIR}
export PETSC_CONFIGURE_OPTIONS="\
  --with-x=0 -with-pic \
  --with-np=8 \
  --with-external-packages-dir=${EXTERNAL_PACKAGES_DIR} \
  --download-petsc4py=yes \
  "
export nopackage="\
  --with-packages-dir=${EXTERNAL_PACKAGES_DIR} \
  "
mkdir -p %{INSTALL_DIR}/externalpackages
mkdir -p %{MODULE_DIR}

export PLAPACK_STRING=plapack
export PLAPACKOPTIONS="--with-plapack=1 --download-plapack"
%if "%{is_mvapich2}" == "1"
export PLAPACK_STRING=
export PLAPACKOPTIONS=
%endif

##
## configure install loop
##
export logdir=%{_topdir}/../apps/petsc/logs
mkdir -p ${logdir}; rm -rf ${logdir}/*
export dynamiccc="uni unidebug debug i64 i64debug complexi64 complexi64debug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

export EXTENSIONS="single ${dynamiccc} ${dynamiccxx}"
#export EXTENSIONS="single ${dynamiccc}"

##
## start of for ext loop, installation only
##
for ext in "" ${EXTENSIONS} ; do
#for ext in "" ; do

echo "configure install for ${ext}"
export versionextra=

if [ -z "${ext}" ] ; then
  export architecture=haswell
  export modulefilename=%{pkg_version}
else
  export architecture=haswell-${ext}
  export modulefilename=%{pkg_version}-${ext}
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

#
# Chaco
#
%if "%{comp_fam}" == "intel"
export CHACO_STRING=chaco
export CHACO_OPTIONS="--with-chaco=1 --download-chaco"
%endif

#
# hdf5
# not available with gcc right now
export hdf5string=
export hdf5download=
export hdf5versionextra=

# %if "%{comp_fam}" == "intel"
# %if "%{is_cmpich}" == "1"
#     module load phdf5
#     export hdf5download="--with-hdf5=1 --with-hdf5-dir=${TACC_HDF5_DIR}"
#     export hdf5versionextra="; hdf5 support"
#     export hdf5string="hdf5"
# %endif
# %endif

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
export MUMPS_STRING=mumps
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
# Sundials
#
export SUNDIALS_OPTIONS="--with-sundials=1 --download-sundials"
export SUNDIALS_STRING="sundials"

#
# SuperLU
#
export SUPERLU_OPTIONS="\
    --with-superlu_dist=1 --download-superlu_dist=${SRC_DIR}/git.superlu_dist.tgz \
    --with-superlu=1 --download-superlu=${SRC_DIR}/git.superlu.tgz \
    ${PARMETIS_OPTIONS}"
export SUPERLU_STRING="superlu and superlu_dist"

##
## 64-bit indices
##
INDEX_OPTIONS=
case "${ext}" in
*i64* ) INDEX_OPTIONS=--with-64-bit-indices ;
        CHACO_OPTIONS= ;   CHACO_STRING= ;
        MUMPS_OPTIONS= ;   MUMP_STRING= ;
	ML_OPTIONS= ;      ML_STRING= ;
	PLAPACK_OPTIONS= ; PLAPACK_STRING= ;
        SPAI_OPTIONS= ;    SPAITRING= ;
	SPOOLES_OPTIONS= ; SPOOLES_STRING= ;
	SUNDIALS_OPTIONS= ; SUNDIALS_STRING= ;
	SUPERLU_OPTIONS= ; SUPERLU_STRING= ;
        SUITESPARSE_OPTIONS= ; SUITESPARSE_STRING= ;
                ;;
esac

# disabled
%if "%{comp_fam}" == "gcc"
  export CHACO_OPTIONS=
  export CHACO_STRING=
#  export ML_OPTIONS=
#  export ML_STRING=
  export PLAPACK_OPTIONS=
  export PLAPACK_STRING=
#  export SUNDIALS_OPTIONS=
#  export SUNDIALS_STRING=
#  export SUPERLU_OPTIONS= 
#  export SUPERLU_STRING=
%endif

##
## define packages; some are real & complex, others real only.
##
%define complexpackages ${hdf5string} ${MUMPS_STRING} scalapack ${SPOOLES_STRING} ${SUITESPARSE_STRING} ${SUPERLU_STRING}
export PETSC_COMPLEX_PACKAGES="\
  ${hdf5download} \
  ${MUMPS_OPTIONS}\
  ${SCALAPACK_OPTIONS} ${SPOOLES_OPTIONS} \
  ${SUITESPARSE_OPTIONS} ${SUPERLU_OPTIONS} \
  "
%define realonlypackages \
${CHACO_STRING} ${HYPRE_STRING} ${ML_STRING} parmetis spai \
${PLAPACK_STRING} ${SUNDIALS_STRING} 
# ml

export PETSC_REALONLY_PACKAGES="\
  ${CHACO_OPTIONS} \
  ${HYPRE_OPTIONS} ${ML_OPTIONS} \
  ${MATLABOPTIONS} ${ML_OPTIONS} \
  ${PLAPACKOPTIONS} ${SPAI_OPTIONS} ${SUNDIALS_OPTIONS} \
  "

export packages="${PETSC_REALONLY_PACKAGES} ${PETSC_COMPLEX_PACKAGES}"

## VLE let's see if this causes the problem
## export packages=
export scalar="--with-scalar-type=real"
case "${ext}" in
*complex* ) export packages="${PETSC_COMPLEX_PACKAGES}"
           export scalar="--with-scalar-type=complex --with-fortran-kernels=1"
           ;;
esac

#
# blas/lapack
#
export BLAS_LAPACK_OPTIONS="\
  ${BLAS_LAPACK_LOAD} \
  "
#
# cuda
#
export CUDA_OPTIONS=
%if "%{comp_fam}" == "gcc"
module load cuda
export CUDA_OPTIONS="--with-cuda=1 --with-cuda-dir=${TACC_CUDA_DIR} \
	--with-cudac=${TACC_CUDA_BIN}/nvcc \
	--with-cusp-dir=${TACC_CUDA_DIR} --with-thrust-dir=${TACC_CUDA_DIR}/include/ \
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
  export PETSC_MPICH_HOME=/opt/cray/mpt/7.3.0/gni/mpich-intel/14.0
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
    export packages= ;;
esac

##
## here we go
##
#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

#TACC_INTEL_LIB=/opt/intel/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64
if [ "%{comp_fam}" = "gcc" ] ; then
  echo ${LIBS}
  export LIBS="${LIBS} /opt/apps/intel/16.0.0.109/compilers_and_libraries_2016.0.109/linux/compiler/lib/intel64_lin/libirc.so"
else
  export LIBS="${LIBS} ${TACC_INTEL_LIB}/libirc.so"
fi

export PETSC_ARCH=${architecture}
noprefix=--prefix=%{INSTALL_DIR}/${architecture}
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

##
## Make!
PETSC_DIR=`pwd` PETSC_ARCH=${architecture} make MAKE_NP=8 V=1
##
##

# as of 3.7 the object files are kept. I don't think we need them
/bin/rm -rf $PETSC_ARCH/obj/src
find $PETSC_ARCH -name \*.o -exec rm -f {} \;

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

# Write out the modulefile associated with the application
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

prepend_path("PATH",            pathJoin(petsc_dir,"bin") )
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

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

rm -rf ${architecture}/obj
rm -rf externalpackages/${architecture}/git.hypre

##
## end of for ext loop
##
done 

# this contains binary crap that messes up the packaging
find . -name git.hypre -exec pwd \; -exec ls -ld {} \;
#find . -name .git -exec rm -rf {} \;

cp -r config include lib makefile src \
                    $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r haswell*      $RPM_BUILD_ROOT/%{INSTALL_DIR}

popd # leave the BUILD directory
umount %{INSTALL_DIR}  

echo "Directory to package up: $RPM_BUILD_ROOT/%{INSTALL_DIR}"
echo "listing:"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}/.tacc_install_canary
  %{INSTALL_DIR}/config
  %{INSTALL_DIR}/include
  %{INSTALL_DIR}/lib
  %{INSTALL_DIR}/makefile
  %{INSTALL_DIR}/src
  %{INSTALL_DIR}/haswell
  %{INSTALL_DIR}/haswell-debug
  %{INSTALL_DIR}/haswell-single 
  %{INSTALL_DIR}/haswell-i64
  %{INSTALL_DIR}/haswell-i64debug
  %{INSTALL_DIR}/haswell-uni
  %{INSTALL_DIR}/haswell-unidebug

%files %{PACKAGE}-xx
  %{INSTALL_DIR}/haswell-cxx 
  %{INSTALL_DIR}/haswell-cxxdebug 
  %{INSTALL_DIR}/haswell-complex 
  %{INSTALL_DIR}/haswell-complexdebug 
  %{INSTALL_DIR}/haswell-cxxcomplex 
  %{INSTALL_DIR}/haswell-cxxcomplexdebug 
  %{INSTALL_DIR}/haswell-cxxi64
  %{INSTALL_DIR}/haswell-cxxi64debug
  %{INSTALL_DIR}/haswell-complexi64
  %{INSTALL_DIR}/haswell-complexi64debug

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%preun %{PACKAGE}-xx
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Aug 16 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: adding petsc4py UNRELEASED
* Sat Jul 28 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: 3.9.3, also adding complexi64
* Thu Jun 14 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: point update to 3.9.2, going back to instant download,
             gcc libirc fix, going to 3 rpms.
* Tue Apr 24 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release of 3.9
