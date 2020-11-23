#
#-----------------------------------------
# Compiler Designations for TACC Clusters
#-----------------------------------------

%define comp_fam error

%if "%{is_xl131}" == "1"
  %define comp_fam xl
  %define comp_fam_ver xl13_1
  %define comp_fam_name XL
  %define is_xl 1
  %define comp_module xl/13.1.6
%endif
%if "%{is_xl161}" == "1"
  %define comp_fam xl
  %define comp_fam_ver xl16
  %define comp_fam_name XL
  %define is_xl 1
  %define comp_module xl/16.1.1
%endif
%if "%{is_gcc48}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_8
  %define comp_fam_name GNU
  %define is_gcc 1
  %define comp_module gcc/4.8.5
%endif
%if "%{is_gcc49}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_9
  %define comp_fam_name GNU
  %define is_gcc 1
  %define comp_module gcc/4.9.3
%endif
%if "%{is_gcc51}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc5_1
  %define comp_fam_name GNU
  %define is_gcc 1
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
  %define is_gcc 1
  %define comp_module gcc/5.4.0
%endif
%if "%{is_gcc63}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc6_3
  %define comp_fam_name GNU
  %define is_gcc 1
  %define comp_module gcc/6.3.0
%endif
%if "%{is_gcc71}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc7_1
  %define comp_fam_name GNU
  %define is_gcc 1
  %define comp_module gcc/7.1.0
%endif
%if "%{is_gcc73}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc7_3
  %define comp_fam_name GNU
  %define is_gcc 1
  %define comp_module gcc/7.3.0
%endif
%if "%{is_gcc91}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc9_1
  %define comp_fam_name GNU
  %define is_gcc 1
  %define comp_module gcc/9.1.0
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
%if "%{is_intel18}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel18
  %define comp_fam_name Intel
  %define is_intel 1
  %define comp_module intel/18.0.2
%endif
%if "%{is_pgi19}" == "1"
  %define comp_fam pgi
  %define comp_fam_ver pgi19
  %define comp_fam_name PGI
  %define is_pgi 1
  %define comp_module pgi/19.10.0
%endif
%if "%{is_pgi20}" == "1"
  %define comp_fam pgi
  %define comp_fam_ver pgi20
  %define comp_fam_name PGI
  %define is_pgi 1
  %define comp_module pgi/20.7.0
%endif


%if "%{comp_fam}" == "pgi"
  %define TACC_OPT           -tp=pwr9  -fast 
  %define TACC_OPT_VEC       -tp=pwr9  -fast -Mvect=simd  
  %define TACC_OPT_NOVEC     -tp=pwr9  -fast -Mvect=nosimd              
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  exit
%endif

%if "%{comp_fam}" == "gcc"
  %define TACC_OPT -mcpu=power9 -mtune=power9
%endif

