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

%if "%{is_openmpi}" == "1" 
  %if %{undefined mpiV}
    %define mpi_label 2_x
    %define mpi_module_version 2.x-dev_686_g5616e12
  %endif
  %if "%{mpiV}" == "2_x"
    %define mpi_label 2_x
    %define mpi_module_version 2.x-dev_686_g5616e12
  %endif
  %define mpi_fam     openmpi
  %define mpi_fam_ver openmpi_%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{is_impi}" == "1"
  %if %{undefined mpiV}
    %define mpi_label 5_1
    %define mpi_module_version 5.1.1
  %endif
  %if "%{mpiV}" == "5_1"
    %define mpi_label 5_1
    %define mpi_module_version 5.1.1
  %endif
  %define mpi_fam     impi
  %define mpi_fam_ver impi_%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{is_mvapich2}" == "1"
  %if %{undefined mpiV}
    %define mpi_label 2_1
    %define mpi_module_version 2.1
  %endif
  %if "%{mpiV}" == "2_1"
    %define mpi_label 2_1
    %define mpi_module_version 2.1
  %endif
  %if "%{mpiV}" == "2_3"
    %define mpi_label 2_3
    %define mpi_module_version 2.3.1
  %endif

  %define mpi_fam     mvapich2-largemem
  %define mpi_fam_ver mvapich2-largemem_%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{is_cmpich}" == "1"
  %if %{undefined mpiV}
    %define mpi_label 7_7
    %define mpi_module_version 7.7.3
  %endif
  %if "%{mpiV}" == "7_2"
    %define mpi_label 7_2
    %define mpi_module_version 7.2.4
  %endif
  %if "%{mpiV}" == "7_3"
    %define mpi_label 7_3
    %define mpi_module_version 7.3.0
  %endif
  %if "%{mpiV}" == "7_3_0"
    %define mpi_label 7_3
    %define mpi_module_version 7.3.0
  %endif
  %if "%{mpiV}" == "7_3_2"
    %define mpi_label 7_3
    %define mpi_module_version 7.3.2
  %endif
  %if "%{mpiV}" == "7_7_0"
    %define mpi_label 7_7
    %define mpi_module_version 7.7.0
  %endif
  %if "%{mpiV}" == "7_7_3"
    %define mpi_label 7_7
    %define mpi_module_version 7.7.3
  %endif
  %define mpi_fam     cray_mpich
  %define mpi_fam_ver cray_mpich_%{mpi_label}
  %define mpi_module  %{mpi_fam}/%{mpi_module_version}
%endif

%if "%{is_ampich}" == "1"
  %if %{undefined mpiV}
    %define mpi_label 3_2
    %define mpi_module_version 3.2
  %endif
  %if "%{mpiV}" == "3_2"
    %define mpi_label 3_2
    %define mpi_module_version 3.2
  %endif
  %define mpi_fam     argonne_mpich
  %define mpi_fam_ver argonne_mpich_%{mpi_label}
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


