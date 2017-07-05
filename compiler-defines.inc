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
%if "%{is_gcc54}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc5_4
  %define comp_fam_name GNU
  %define comp_module gcc/5.4.0
%endif
%if "%{is_gcc63}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc6_3
  %define comp_fam_name GNU
  %define comp_module gcc/6.3.0
%endif
%if "%{is_gcc71}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc7_1
  %define comp_fam_name GNU
  %define comp_module gcc/7.1.0
%endif
%if "%{is_intel16}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel16
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/16.0.3
%endif
%if "%{is_intel17}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel17
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/17.0.4
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  exit
%endif

%if "%{comp_fam}" == "gcc"
  %define TACC_OPT -march=broadwell -mtune=knl
%endif
%if "%{comp_fam}" == "intel"
  %define TACC_OPT -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512
%endif
