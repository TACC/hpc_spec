# -*-rpm-spec-*-
#
#-----------------------------------------
# Compiler Designations for TACC Clusters
#-----------------------------------------

%define comp_fam error
#define comp_mic_support 0

%if "%{is_intel13}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel13
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel
# prep for new default version
#  %define comp_module intel/13.1.1.163
%endif

%if "%{is_intel14}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel14
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/14.0.1.106
%endif

%if "%{is_intel15}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel15
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/15.0.3
%endif

%if "%{is_intel18}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel18
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/18.0.2
%endif

%if "%{is_gcc44}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_4
  %define comp_fam_name GNU
  %define comp_module gcc/4.4.6
%endif

%if "%{is_gcc46}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_6
  %define comp_fam_name GNU
  %define comp_module gcc/4.6.3
%endif

%if "%{is_gcc47}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_7
  %define comp_fam_name GNU
  %define comp_module gcc/4.7.1
%endif

%if "%{is_gcc49}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_9
  %define comp_fam_name GNU
  %define comp_module gcc/4.9.1
%endif

%if "%{is_gcc73}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc7_3
  %define comp_fam_name GNU
  %define comp_module gcc/7.3.0
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  #exit
%endif
