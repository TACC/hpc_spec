# -*-rpm-spec-*-
#
#-----------------------------------------
# Compiler Designations for TACC Clusters
#-----------------------------------------

%define comp_fam error
#define comp_mic_support 0

%if "%{is_intel15}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel15
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/15.0.3
%endif

%if "%{is_gcc49}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_9
  %define comp_fam_name GNU
  %define comp_module gcc/4.9.1
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  exit
%endif
