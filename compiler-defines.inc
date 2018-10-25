#
#-----------------------------------------
# Compiler Designations for TACC Clusters
#-----------------------------------------

%define comp_fam error

%if "%{is_gcc49}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_9
  %define comp_fam_name GNU
  %define comp_module gcc/4.9.3
%endif
%if "%{is_gcc51}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc5_1
  %define comp_fam_name GNU
  %define comp_module gcc/5.1.0
%endif
%if "%{is_gcc52}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc5_2
  %define comp_fam_name GNU
  %define comp_module gcc/5.2.0
%endif
%if "%{is_gcc73}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc7_3
  %define comp_fam_name GNU
  %define comp_module gcc/7.3.0
%endif
%if "%{is_intel16}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel16
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/16.0.1
%endif
%if "%{is_intel18}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel18
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/18.0.2
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  exit
%endif

%if "%{comp_fam}" == "gcc"
  %define TACC_OPT -march=ivybridge -mtune=haswell
%endif
%if "%{comp_fam}" == "intel"
  %define TACC_OPT -xCORE-AVX-I -axCORE-AVX2
%endif
%{!?suf: %define suf default}
%if "%{suf}" == "default"
  %define TACC_VEC_OPT %{TACC_OPT}
  %define dovec 0
%endif

