#
# W. Cyrus Proctor
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
  # Compiler Specific Only
  %else
    %define pkg_name       %{name_prefix}-%{pkg_base_name}-%{comp_fam_ver}
    %define MODULE_SUFFIX  %{comp_fam_ver}/modulefiles/%{pkg_base_name}
    %define INSTALL_SUFFIX %{comp_fam_ver}/%{pkg_base_name}/%{pkg_version}
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

# Add canary to let post-defines know this is a relocatable rpm
%define RELOC 1

# Add canary to let post-defines know this is a hidden module
%define VISIBLE  0

# Module macros
%define MODULE_PREFIX   /tmpmod 
%define MODULE_DIR      %{MODULE_PREFIX}/%{MODULE_SUFFIX}
%define MODULE_FILENAME .%{version}.lua

# Install macros
%define INSTALL_PREFIX  /tmprpm
%define INSTALL_DIR     %{INSTALL_PREFIX}/%{INSTALL_SUFFIX}

# Subpackage macros
%define PACKAGE             package
%define MODULEFILE          modulefile
%define BUILD_PACKAGE       %( if [ ${NO_PACKAGE:=0}    = 0 ]; then echo "1"; else echo "0"; fi )
%define BUILD_MODULEFILE    %( if [ ${NO_MODULEFILE:=0} = 0 ]; then echo "1"; else echo "0"; fi )
%define RPM_PACKAGE_NAME    %{name}-%{PACKAGE}-%{version}-%{release}
%define RPM_MODULEFILE_NAME %{name}-%{MODULEFILE}-%{version}-%{release}

#---------------------------------------
#---------------------------------------
#---------------------------------------
# Default installation prefixes
# May be overridden at install
# with:
# rpm --relocate /foo=/bar <rpm-name>.rpm 
Prefix:    %{MODULE_PREFIX}
Prefix:    %{INSTALL_PREFIX}
#---------------------------------------
#---------------------------------------
#---------------------------------------
