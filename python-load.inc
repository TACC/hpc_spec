#
#-----------------------------------------
# Load Desired Python Stack for RPM Builds
#-----------------------------------------

%if %{undefined python_fam}
  %define python_fam error
%endif

########################################################################
#  Pushing all decisions to python-defines.inc so this file remains simple
########################################################################

module unload $TACC_FAMILY_PYTHON

%if ! %{undefined python_module}
  module load %{python_module}
%endif

%if "%{python_fam}" == "error"
  %{error: You must define which Python stack you are trying to load!}
  exit
%endif


