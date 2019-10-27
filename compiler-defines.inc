#
#-----------------------------------------
# Compiler Designations for TACC Clusters
#-----------------------------------------

%define comp_fam error

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
%if "%{is_gcc81}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc8_1
  %define comp_fam_name GNU
  %define is_gcc 1
  %define comp_module gcc/8.1.0
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

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  exit
%endif

%if "%{comp_fam}" == "gcc"
  %define TACC_OPT -march=broadwell -mtune=knl
  %define TACC_OPT_CORE_AVX2 -march=broadwell -mtune=broadwell -ftree-vectorize
  %define TACC_OPT_CORE_AVX2_NOVEC_NOSIMD -march=broadwell -mtune=broadwell -fno-tree-vectorize
  %define TACC_OPT_COMMON_AVX512 -march=broadwell -mtune=skylake-avx512 -mavx512f -mavx512cd -ftree-vectorize
  %define TACC_OPT_CORE_AVX512 -march=skylake-avx512 -mtune=skylake-avx512 -ftree-vectorize
  %define TACC_OPT_MIC_AVX512 -march=knl -mtune=knl -free-vectorize
%endif
%if "%{comp_fam}" == "intel"
  %define TACC_OPT -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512
  %define TACC_OPT_CORE_AVX2 -xCORE-AVX2
  %define TACC_OPT_CORE_AVX2_NOVEC_NOSIMD -xCORE-AVX2 -no-vec -no-simd
  %define TACC_OPT_COMMON_AVX512_ZMM -xCOMMON-AVX512 -qopt-zmm-usage=high
  %define TACC_OPT_CORE_AVX512_ZMM -xCORE-AVX512 -qopt-zmm-usage=high
  %define TACC_OPT_MIC_AVX512_ZMM -xMIC-AVX512 -qopt-zmm-usage=high
  %define TACC_OPT_COMMON_AVX512 -xCOMMON-AVX512
  %define TACC_OPT_CORE_AVX512 -xCORE-AVX512
  %define TACC_OPT_MIC_AVX512 -xMIC-AVX512
%endif
%{!?suf: %define suf default}
%if "%{suf}" == "default"
  %define TACC_VEC_OPT %{TACC_OPT}
  %define dovec 0
%endif
%if "%{suf}" == "avx2"
  %define TACC_VEC_OPT %{TACC_OPT_CORE_AVX2}
  %define dovec 0
%endif
%if "%{suf}" == "avx2-novec-nosimd"
  %define TACC_VEC_OPT %{TACC_OPT_CORE_AVX2_NOVEC_NOSIMD}
  %define dovec 0
%endif
%if "%{suf}" == "common-avx512-zmm"
  %define TACC_VEC_OPT %{TACC_OPT_COMMON_AVX512_ZMM}
  %define dovec 1
%endif
%if "%{suf}" == "core-avx512-zmm"
  %define TACC_VEC_OPT %{TACC_OPT_CORE_AVX512_ZMM}
  %define dovec 1
%endif
%if "%{suf}" == "mic-avx512-zmm"
  %define TACC_VEC_OPT %{TACC_OPT_MIC_AVX512_ZMM}
  %define dovec 1
%endif
%if "%{suf}" == "common-avx512"
  %define TACC_VEC_OPT %{TACC_OPT_COMMON_AVX512}
  %define dovec 1
%endif
%if "%{suf}" == "core-avx512"
  %define TACC_VEC_OPT %{TACC_OPT_CORE_AVX512}
  %define dovec 1
%endif
%if "%{suf}" == "mic-avx512"
  %define TACC_VEC_OPT %{TACC_OPT_MIC_AVX512}
  %define dovec 1
%endif
