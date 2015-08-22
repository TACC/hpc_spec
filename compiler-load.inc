# -*-rpm-spec-*-
#
#
#-----------------------------------------
# Load Desired Compiler for RPM Builds
#-----------------------------------------

%define comp_fam error

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles:/share/apps/modulefiles
  . $BASH_ENV
  module unload $TACC_FAMILY_COMPILER
  module unload pgi
fi

%if "%{is_intel10}" == "1"
  %define comp_fam intel
  %define comp_version 10.1
  module load intel/10.1

  CC=icc
  CXX=icpc
  FC=ifort
  F77=ifort
  F90=ifort

%endif

%if "%{is_intel11}" == "1"
  %define comp_fam intel
  %define comp_version 11.1
  module load intel/11.1

  export CC=icc
  export CXX=icpc
  export FC=ifort
  export F77=ifort
  export F90=ifort
%endif

%if "%{is_intel12}" == "1"
  %define comp_fam     intel
  %define comp_version 12.1
  module try-load %{comp_fam}/%{comp_version}
  module try-load %{comp_fam}/.%{comp_version}

  export CC=icc
  export CXX=icpc
  export FC=ifort
  export F77=ifort
%endif

%if "%{is_pgi10}" == "1"
  %define comp_fam pgi
  module load pgi/10.8-0

  export CC=pgcc
  export CXX=pgCC
  export FC=pgf90
  export F77=pgf77
  export F90=pgf90
%endif

%if "%{is_pgi11}" == "1"
  %define comp_fam pgi
  module load pgi/11.8
  %define comp_version 11.8

  export CC=pgcc
  export CXX=pgCC
  export FC=pgf90
  export F77=pgf77
  export FC=pgf90
%endif

%if "%{is_pgi12}" == "1"
  %define comp_fam pgi
  module load pgi/12.5
  %define comp_version 12.5

  export CC=pgcc
  export CXX=pgCC
  export FC=pgf90
  export F77=pgf77
# following required for mvapich2
#  export F77=pgf90
%endif

%if "%{is_gcc}" == "1"
  %define comp_fam gcc

  %{error: ** gcc compiler not supported!}
  exit

  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export F77=gfortran
  export F90=gfortran
%endif

%if "%{is_gcc41}" == "1"
  %define comp_fam gcc
  %define comp_version 4.1.2
  module load %{comp_fam}/%{comp_version}

  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export F77=gfortran
  export F90=gfortran
%endif

%if "%{is_gcc44}" == "1"
  %define comp_fam gcc
  %define comp_version 4.4.5
  module load %{comp_fam}/%{comp_version}

  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export F77=gfortran
  export F90=gfortran
%endif

%if "%{is_gcc46}" == "1"
  %define comp_fam gcc
  %define comp_version 4.6.3
  module load %{comp_fam}/%{comp_version}

  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export F77=gfortran
  export F90=gfortran
%endif

%if "%{is_gcc47}" == "1"
  %define comp_fam gcc
  %define comp_version 4.7.1
  module load %{comp_fam}/%{comp_version}

  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export F77=gfortran
  export F90=gfortran
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are trying to load!}
  exit
%endif


