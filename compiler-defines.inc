# -*-rpm-spec-*-
#
#-----------------------------------------
# Compiler Designations for TACC Clusters
#-----------------------------------------

%define comp_fam error

%if "%{is_intel11}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel11_1
  %define comp_fam_name Intel
  %define is_intel 1
%endif

%if "%{is_pgi10}" == "1"
  %define comp_fam pgi
  %define comp_fam_ver pgi10
  %define comp_fam_name PGI
  %define is_pgi 1
%endif

%if "%{is_pgi12}" == "1"
  %define comp_fam pgi
  %define comp_fam_ver pgi12
  %define comp_fam_name PGI
  %define is_pgi 1
%endif

# System gcc: change your INSTALL_DIR and MODULE_DIR to
# /opt/apps/name instead of /opt/apps/compiler/name
%if "%{is_gcc}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_1
  %define comp_fam_name GNU
%endif

%if "%{is_gcc41}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_1
  %define comp_fam_name GNU
%endif

%if "%{is_gcc44}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_4
  %define comp_fam_name GNU
%endif

%if "%{is_gcc46}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_6
  %define comp_fam_name GNU
%endif

%if "%{is_gcc47}" == "1"
  %define comp_fam gcc
  %define comp_fam_ver gcc4_7
  %define comp_fam_name GNU
%endif

%if "%{comp_fam}" == "error"
  %{error: You must define which compiler you are using!}
  exit
%endif


