# -*-rpm-spec-*-
#
#
#-----------------------------------------
# Load Desired MPI Stack for RPM Builds
#-----------------------------------------

%if %{undefined mpi_fam}
  %define mpi_fam error
%endif

########################################################################
#  Pushing all decisions to mpi-defines.inc so this file remains simple
########################################################################

module unload $TACC_FAMILY_MPI

%if ! %{undefined mpi_module}
  module load %{mpi_module}
%endif

%if "%{mpi_fam}" == "error"
  %{error: You must define which MPI stack you are trying to load!}
  exit
%endif


