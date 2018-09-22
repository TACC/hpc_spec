#
#-----------------------------------------
# Load Desired Compiler for RPM Builds
#-----------------------------------------

if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  MP="/opt/apps/tools/modulefiles:/opt/apps/modulefiles"

  if [ -z "$MODULEPATH" ]; then
    export MODULEPATH=$(/opt/apps/lmod/lmod/libexec/addto --append MODULEPATH ${MP//:/ })
  fi
fi

%if %{undefined comp_fam}
  %define comp_fam error
%endif

########################################################################
#  The idea is to make all decisions in the compiler-define.inc file
#  Then use the results here.  This file should only have to modified
#  if we add a new compiler.      
########################################################################

%if "%{comp_fam}" == "xl"
  export CC=xlc
  export CXX=xlc++
  export FC=xlf
  export F77=xlf
%endif

%if "%{comp_fam}" == "intel"
  export CC=icc
  export CXX=icpc
  export FC=ifort
  export F77=ifort
%endif

%if "%{comp_fam}" == "gcc"
  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export F77=gfortran
  export FC=gfortran
%endif

%if "%{comp_fam}" == "pgi"
  export CC=pgcc
  export CXX=pgCC
  export FC=pgf90
  export F77=pgf77
  export F90=pgf90
%endif

module load %{comp_module}


%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are trying to load!}
  exit
%endif
