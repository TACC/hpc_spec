# Si Liu
# Updated for ls6
# 2021-09-30
#
#
#-------------------------------
# MPI Stack Family Definitions
#-------------------------------

# see rpm-dir.inc for the definition of "undefined"

%if %{undefined mpi_fam}
  %define mpi_fam error
%endif

%if %{undefined mpi_label}
  %define mpi_label error
%endif

########################################################################
##  The idea is to make all decisions in the here then mpi-load.inc 
##  is simple.
########################################################################

%if "%{is_impi}" == "1"
  %if %{undefined mpiV}
    %define mpi_label 17_0
    %define mpi_module_version 17.0.3
  %endif
  %if "%{mpiV}" == "5_1"
    %define mpi_label 5_1
    %define mpi_module_version 5.1.3
  %endif
  %if "%{mpiV}" == "17_0"
    %define mpi_label 17_0
    %define mpi_module_version 17.0.3
  %endif
  %if "%{mpiV}" == "18_0"
    %define mpi_label 18_0
    %define mpi_module_version 18.0.2
  %endif
  %if "%{mpiV}" == "19_0"
    %define mpi_label 19_0
    %define mpi_module_version 19.0.9
  %endif
  %define mpi_fam     impi
  %define mpi_fam_ver impi%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{is_mvapich2}" == "1"
  %if %{undefined mpiV}
    %define mpi_label 2_3
    %define mpi_module_version 2.3rc2
  %endif
  %if "%{mpiV}" == "2_3"
    %define mpi_label 2_3
    %define mpi_module_version 2.3rc2
  %endif
  %define mpi_fam     mvapich2
  %define mpi_fam_ver mvapich2-%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{mpi_fam}" == "error"
  %{error: You must define which MPI you are using!}
  exit
%endif

%if "%{mpi_label}" == "error"
  %{error: Illegal MPI version syntax! Use e.g. --mpich=7_2}
  exit
%endif


