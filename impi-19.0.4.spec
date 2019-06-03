#
# W. Cyrus Proctor
# 2015-11-12
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name impi
%define MODULE_VAR    IMPI

# Create some macros (spec file variables)
%define major_version 19
%define minor_version 0
%define micro_version 4

%define lib_version 2019.4.243

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define underscore_version %{major_version}_%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   3%{?dist}
License:   proprietary
Group:     MPI
URL:       https://software.intel.com/en-us/intel-mpi-library
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
This is specifically an rpm for the Intel MPI modulefile
used on Frontera.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
This is specifically an rpm for the Intel MPI modulefile
used on Frontera.

%description
This is specifically an rpm for the Intel MPI modulefile
used on Frontera.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================

###%if "%{comp_fam_name}" == "Intel"
###  # gfortran "use mpi" statements are busted
###  # fix intel's mess
###  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
###  ln -s /opt/intel/compilers_and_libraries_%{lib_version}/linux/mpi/intel64/bin/mpiicc $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
###  ln -s /opt/intel/compilers_and_libraries_%{lib_version}/linux/mpi/intel64/bin/mpiicpc $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
###  ln -s /opt/intel/compilers_and_libraries_%{lib_version}/linux/mpi/intel64/bin/mpiifort $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
###  ln -s /opt/intel/compilers_and_libraries_%{lib_version}/linux/mpi/intel64/bin/mpiifort $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
###%endif
###
### 
###%if "%{comp_fam_name}" == "GNU"
###  # gfortran "use mpi" statements are busted
###  # fix intel's mess
###  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
###  cp %{_sourcedir}/mpif90.18 $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
###  chmod +rx $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
###%endif
  
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

# Default Intel
%define myCC  icc
%define myCXX icpc
%define myFC  ifort

# GCC module
%if "%{comp_fam_name}" == "GNU"
%define myCC  gcc
%define myCXX g++
%define myFC  gfortran
%endif

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
Intel MPI Library %{pkg_version} focuses on making applications perform better on Intel
architecture-based clusters -- implementing the high performance Message Passing
Interface Version 3.0 specification on multiple fabrics. It enables you to
quickly deliver maximum end user performance even if you change or upgrade to
new interconnects, without requiring changes to the software or operating
environment.

This module loads the Intel MPI environment built with
Intel compilers. By loading this module, the following commands
will be automatically available for compiling MPI applications:
mpif77       (F77 source)
mpif90       (F90 source)
mpicc        (C   source)
mpicxx       (C++ source)

The %{MODULE_VAR} module also defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

Version %{version}
]]

--help(help_msg)
help(help_msg)

-- Create environment variables.
local base_dir           = "/opt/intel/compilers_and_libraries_%{lib_version}/linux/mpi"

whatis("Name: Intel MPI"                                                    )
whatis("Version: %{version}"                                                )
whatis("Category: library, Runtime Support"                                 )
whatis("Description: Intel MPI Library (C/C++/Fortran for x86_64)"          )
whatis("URL: http://software.intel.com/en-us/articles/intel-mpi-library"    )
prepend_path( "PATH"                   , pathJoin( base_dir , "intel64/bin"      ) )
prepend_path( "PATH"                   , pathJoin( "%{INSTALL_DIR}" , "bin"      ) )
prepend_path( "LD_LIBRARY_PATH"        , pathJoin( base_dir , "intel64/lib"      ) )
prepend_path( "MANPATH"                , pathJoin( base_dir , "man"              ) )
prepend_path( "MODULEPATH"             ,"/opt/apps/%{comp_fam_ver}/impi%{underscore_version}/modulefiles" )
prepend_path( "I_MPI_ROOT"             , base_dir                                )
setenv(       "MPICH_HOME"             , base_dir                                )
setenv(       "TACC_MPI_GETMODE"       , "impi_hydra"                            )
setenv(       "TACC_IMPI_DIR"          , base_dir                                )
setenv(       "TACC_IMPI_BIN"          , pathJoin( base_dir , "intel64/bin"      ) )
setenv(       "TACC_IMPI_LIB"          , pathJoin( base_dir , "intel64/lib"      ) )
setenv(       "TACC_IMPI_INC"          , pathJoin( base_dir , "intel64/include"  ) )
setenv(       "I_MPI_JOB_FAST_STARTUP" , "1"                                     )
setenv(       "I_MPI_CC"               , "%{myCC}"                               )
setenv(       "I_MPI_CXX"              , "%{myCXX}"                              )
setenv(       "I_MPI_FC"               , "%{myFC}"                               )
setenv(       "I_MPI_F77"              , "%{myFC}"                               )
setenv(       "I_MPI_F90"              , "%{myFC}"                               )
family(       "MPI"                                                              )


if (os.getenv("TACC_SYSTEM") == "frontera") then
  depends_on("libfabric")
  local libfabric_lib = os.getenv("TACC_LIBFABRIC_LIB")
  setenv(     "I_MPI_OFI_LIBRARY"      , pathJoin(libfabric_lib,"libfabric.so" ) )
--  setenv(     "FI_PSM2_LAZY_CONN"      , "1"                                     )
--  setenv(     "FI_PROVIDER"            , "psm2"                                  )
--  setenv(     "FI_PROVIDER_PATH"       , pathJoin(base_dir, "intel64/libfabric/lib/prov") )
  setenv(     "I_MPI_FABRICS"          , "shm:ofi"                               )
  setenv(     "I_MPI_STARTUP_MODE"     , "pmi_shm_netmod"                        )
end

EOF

 
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  ### don't check the hidden one!
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

