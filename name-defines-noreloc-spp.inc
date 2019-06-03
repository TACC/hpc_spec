#
# W. Cyrus Proctor
# 2019-02-25 Add python
# 2015-12-05 Add hidden and non-relocatable version
# 2015-08-25

%define name_prefix tacc

# Compiler Specific?
%if "%{?comp_fam_ver}"
  # Compiler *and* MPI Specific
  %if "%{?mpi_fam_ver}"
    %define pkg_name       %{name_prefix}-%{pkg_base_name}-%{comp_fam_ver}-%{mpi_fam_ver}
    %define MODULE_SUFFIX  %{comp_fam_ver}/%{mpi_fam_ver}/modulefiles/%{pkg_base_name}
    %define INSTALL_SUFFIX %{comp_fam_ver}/%{mpi_fam_ver}/%{pkg_base_name}/%{pkg_version}
    # Compiler *and* MPI *and* Python Specific
    %if "%{?python_fam_ver}"
      %define pkg_name              %{name_prefix}-%{pkg_base_name}-%{comp_fam_ver}-%{mpi_fam_ver}-%{python_fam_ver}
      %define PYTHON_MODULE_SUFFIX  %{comp_fam_ver}/%{mpi_fam_ver}/%{python_fam_ver}/modulefiles/%{pkg_base_name}
      %define PYTHON_INSTALL_SUFFIX %{comp_fam_ver}/%{mpi_fam_ver}/%{python_fam_ver}/%{pkg_base_name}/%{pkg_version}
    %endif
  # Compiler Specific Only
  %else
    %define pkg_name       %{name_prefix}-%{pkg_base_name}-%{comp_fam_ver}
    %define MODULE_SUFFIX  %{comp_fam_ver}/modulefiles/%{pkg_base_name}
    %define INSTALL_SUFFIX %{comp_fam_ver}/%{pkg_base_name}/%{pkg_version}
    # Compiler *and* Python Specific
    %if "%{?python_fam_ver}"
      %define pkg_name              %{name_prefix}-%{pkg_base_name}-%{comp_fam_ver}-%{python_fam_ver}
      %define PYTHON_MODULE_SUFFIX  %{comp_fam_ver}/%{python_fam_ver}/modulefiles/%{pkg_base_name}
      %define PYTHON_INSTALL_SUFFIX %{comp_fam_ver}/%{python_fam_ver}/%{pkg_base_name}/%{pkg_version}
    %endif
  %endif
# Compiler Non-specific
%else
  %define pkg_name       %{name_prefix}-%{pkg_base_name}
  %define MODULE_SUFFIX  modulefiles/%{pkg_base_name}
  %define INSTALL_SUFFIX %{pkg_base_name}/%{pkg_version}
%endif


# NOTES:
# Leave MODULE_PREFIX and INSTALL_PREFIX as /tmpmod and /tmprpm!
# These are temporary placeholders that allow for install-time
# relocation via rpm. They must be unique and *not* nested. 
# /tmpmod and /tmprpm should *never* be the final install locations.

# Add canary to let post-defines know this is a non-relocatable rpm
%define RELOC 0

# Add canary to let post-defines know this is a visible module
%define VISIBLE  1

# Module macros
%define MODULE_PREFIX   /opt/apps/spp
%define MODULE_DIR      %{MODULE_PREFIX}/%{MODULE_SUFFIX}
%define MODULE_FILENAME %{version}.lua
%if "%{?python_fam_ver}"
  %define PYTHON_MODULE_DIR %{MODULE_PREFIX}/%{PYTHON_MODULE_SUFFIX}
  %if "%{?unified_directories}"
    %define MODULE_SUFFIX %{PYTHON_MODULE_SUFFIX}
    %define MODULE_DID    %{PYTHON_MODULE_DIR}
  %endif
%endif

# Install macros
%define INSTALL_PREFIX  /opt/apps/spp
%define INSTALL_DIR     %{INSTALL_PREFIX}/%{INSTALL_SUFFIX}
%if "%{?python_fam_ver}"
  %define PYTHON_INSTALL_DIR %{INSTALL_PREFIX}/%{PYTHON_INSTALL_SUFFIX}
  %if "%{?unified_directories}"
    %define INSTALL_SUFFIX %{PYTHON_INSTALL_SUFFIX}
    %define INSTALL_DIR    %{PYTHON_INSTALL_DIR}
  %endif
%endif

# Subpackage macros
%define PACKAGE             package
%define MODULEFILE          modulefile
%define BUILD_PACKAGE       %( if [ ${NO_PACKAGE:=0}    = 0 ]; then echo "1"; else echo "0"; fi )
%define BUILD_MODULEFILE    %( if [ ${NO_MODULEFILE:=0} = 0 ]; then echo "1"; else echo "0"; fi )
%if "%{?python_fam_ver}"
  %define WITH_PYTHON 1
%else
  %define WITH_PYTHON 0
%endif
%define RPM_PACKAGE_NAME    %{name}-%{PACKAGE}-%{version}-%{release}
%define RPM_MODULEFILE_NAME %{name}-%{MODULEFILE}-%{version}-%{release}

