# -*-rpm-spec-*-
#
#
#-------------------------------
# MPI Stack Family Definitions
#-------------------------------

# see rpm-dir.inc for the definition of "undefined"

%if %{undefined mpi_fam}
  %define mpi_fam error
%endif

%if "%{is_mvapich2}" == "1" 
  %define mpi_fam     mvapich2
  %if %{undefined mpiV} || "%{compV}" == "44" || "%{mpiV}" == "1_6"
    %define mpi_label 1_6
    %define mpi_module_version 1.6
  %endif
  %if "%{is_intel12}" == "1" || "%{is_gcc41}" == "1" || "%{is_gcc46}" == "1" 
    %define mpi_label 1_8
    %define mpi_module_version 1.8
  %endif
%endif

%if "%{is_mvapich2a}" == "1"  || "%{is_mvapich2}" == "1_7" 
  %define mpi_fam mvapich2
  %define mpi_label 1_7
  %define mpi_module_version 1.7
%endif

%if "%{is_mvapich2_1_8}" == "1"  || "%{is_mvapich2}" == "1_8"
  %define mpi_fam mvapich2
  %define mpi_label 1_8
  %define mpi_module_version 1.8
%endif

%if "%{is_mvapich2_2_0}" == "1"  || "%{is_mvapich2}" == "2_0" || "%{mpiV}" =="2_0"
  %define mpi_fam mvapich2
  %define mpi_label 2_0
  %define mpi_module_version 2.0b
%endif


%if "%{is_openmpi}" == "1"
  %define mpi_fam openmpi
  %define mpi_label 1_4
  %define mpi_module_version 1.4.3
%endif


%if "%{mpi_fam}" == "error"
  %{error: You must define which MPI you are using!}
  exit
%endif


%if ! %{undefined mpi_module_version}
  %define mpi_fam_ver %{mpi_fam}_%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif
