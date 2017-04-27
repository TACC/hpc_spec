#
# Adapted from Bar.spec by Victor Eijkhout 2015/11/30
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
%define minor_version 6
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

Release:   6
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
%description package
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

# Insert necessary module commands
#module purge

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

module load cmake metis pmetis
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
export COPTFLAGS="-xhost -O2" ; export CXXOPTFLAGS="-xhost -O2" ; export FOPTFLAGS="-xhost -O2"
export CNOOPTFLAGS="-O0 -g" ; export CXXNOOPTFLAGS="-O0 -g" ; export FNOOPTFLAGS="-O0 -g"
export CHACOSTRING=chaco
export CHACO_OPTIONS="--with-chaco=1 --download-chaco"
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

export EXTENSIONS="single ${dynamiccc} ${dynamiccxx}"
export noext="\
  reinstate: \
  \
  ${dynamiccxx} \
  tau \
  ${static} we don't do static anymore \
  nono"

##
## start of for ext loop, installation only
##
for ext in "" ${EXTENSIONS} ; do

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

##
## hdf5
# not available with gcc right now
export hdf5string=
export hdf5download=
export hdf5versionextra=

# %if "%{comp_fam}" == "intel" && "%{comp_fam_ver}" != "intel15"
    export hdf5string="hdf5"
# %endif

if [ ! -z "${hdf5string}" ] ; then
    module load phdf5
    export hdf5download="--with-hdf5=1 --with-hdf5-dir=${TACC_HDF5_DIR}"
    export hdf5versionextra="; hdf5 support"
fi

# ## totally disabled for now
# export hdf5string=
# export hdf5download=
# export hdf5versionextra=

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
export mumpsstring="mumps"
export SUPERLU_OPTIONS="--with-superlu_dist=1 --download-superlu_dist \
   --with-superlu=1 --download-superlu ${PARMETIS_OPTIONS}"
export superlustring="superlu (distributed/sequential)"
export SCALAPACK_OPTIONS="--with-scalapack=1 --download-scalapack --with-blacs=1 --download-blacs"
export scalapackstring="scalapack/blacs"
# disabled
export SUPERLU_OPTIONS= 
export superlustring=

#
# Spai
#
export SPAI_OPTIONS="--with-spai=1 --download-spai"
export SPAI_STRING=spai

#
# Spooles
#
export SPOOLES_OPTIONS="--with-spooles=1 --download-spooles"
export spoolesstring=spooles

##
## 64-bit indices
##
INDEX_OPTIONS=
case "${ext}" in
*i64* ) INDEX_OPTIONS=--with-64-bit-indices ;
        CHACO_OPTIONS= ;   CHACOSTRING= ;
        MUMPS_OPTIONS= ;   mumpsstring= ;
	ML_OPTIONS= ;      ML_STRING= ;
	PLAPACK_OPTIONS= ; PLAPACK_STRING= ;
        SPAI_OPTIONS= ;    SPAITRING= ;
	SPOOLES_OPTIONS= ; spoolesstring= ;
	SUPERLU_OPTIONS= ; SUPERLU_STRING= ;
                ;;
esac

##
## define packages; some are real & complex, others real only.
##
export complexpackages="${mumpsstring} ${scalapackstring} ${spoolesstring} ${superlustring}"
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
export packageslisting="${complexpackages} ${realonlypackages}"
export scalar="--with-scalar-type=real"

case "${ext}" in
*complex* ) export packages="${PETSC_COMPLEX_PACKAGES}"
           export packageslisting="${complexpackages}"
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

export PETSC_MPICH_HOME=/opt/cray/mpt/7.2.4/gni/mpich2-intel/14.0
export PETSC_MPICH_HOME=/opt/cray/mpt/7.3.0/gni/mpich-intel/14.0
#/opt/apps/intel16/cray_mpich/7.2.4
export mpi="--with-mpi-compilers=1 --with-mpi-dir=${PETSC_MPICH_HOME}"
# --with-cc=/opt/apps/intel/16/compilers_and_libraries_2016.0.109/linux/bin/intel64/icc"
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
module list
echo $TACC_CRAY_MPT_INC
  RPM_BUILD_ROOT=tmpfs PETSC_DIR=`pwd` ./configure \
    ${PETSC_CONFIGURE_OPTIONS} \
    ${mpi} ${clanguage} ${scalar} ${dynamicshared} ${precision} ${packages} \
    --with-debugging=${usedebug} \
    ${BLAS_LAPACK_OPTIONS} ${MPI_EXTRA_OPTIONS} ${CUDA_OPTIONS} ${INDEX_OPTIONS} \
    --CFLAGS="${CFLAGS}" --FFLAGS="${FFLAGS}" --CXXFLAGS="${CXXFLAGS}"
fi

##
## Make!
PETSC_DIR=`pwd` PETSC_ARCH=${architecture} make MAKE_NP=4
##
##

# as of 3.6 the object files are kept. I don't think we need them
/bin/rm -rf $PETSC_ARCH/obj/src

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

##
## end of for ext loop
##
done 

cp -r bin config externalpackages include lib makefile src    \
                    $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r haswell*      $RPM_BUILD_ROOT/%{INSTALL_DIR}

popd
  
umount %{INSTALL_DIR}

#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

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
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Mar 30 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: recompile with apparently moved intel compiler
* Thu Jul 07 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: update packages listing in modulefile
* Tue Dec 22 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: new cray mpich version
* Thu Dec 10 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: all packages
* Tue Dec 08 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: no longer relocatable
* Mon Dec 07 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: no packages
