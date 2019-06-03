#
# W. Cyrus Proctor
# 2015-11-20 Need to investigate relocation -- use /opt/apps for now
# 2015-11-20
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
%define pkg_base_name ompi
%define pkg_full_name openmpi
%define MODULE_VAR    OMPI

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 1
%define micro_version 4

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pkg_version_dash %{major_version}_%{minor_version}

%define ucx_version 1.5.1
%define ucx_install /opt/apps/ucx/%{ucx_version}

%define pmix_version 3.1.2
%define pmix_install /opt/apps/pmix/%{pmix_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   3%{?dist}
License:   BSD
Group:     MPI
URL:       https://www.open-mpi.org
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_full_name}-%{pkg_version}.tar.bz2

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
Open-MPI development library.


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

%setup -n %{pkg_full_name}-%{pkg_version}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
ml purge
%include compiler-load.inc
ml ucx
ml pmix
ml hwloc/1.11.12
ml

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
    
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

#sed -i '30i#include "orte/mca/errmgr/errmgr.h"' ./oshmem/mca/memheap/base/memheap_base_mkey.c
 
 
export ncores=96

./configure                        \
--prefix=%{INSTALL_DIR}            \
--disable-static                   \
--enable-builtin-atomics           \
--with-ucx=${TACC_UCX_DIR}         \
--with-pmix=${TACC_PMIX_DIR}       \
--with-libevent=external           \
--with-hwloc=${TACC_HWLOC_DIR}     \
--with-slurm                       \
--enable-mpi-cxx                   

#--disable-dlopen                   \


#--enable-orterun-prefix-by-default \
#--enable-mpirun-prefix-by-default  \
#--with-ompi-pmix-rte               \
#--disable-oshmem                   \
#--with-libevent=/usr               \
#--without-verbs                    \
#--with-slurm                       \
#--enable-static=yes                \
#--enable-shared=no

#sed -i 's#$(OSHMEM_TOP_BUILDDIR)/ompi/libmpi.la#$(OSHMEM_TOP_BUILDDIR)/ompi/libmpi.la $(top_srcdir)/orte/libopen-rte.la#g' ./oshmem/Makefile

#--with-pic                         \
#--with-ucx=%{ucx_install}          \
#--with-pmix=%{pmix_install}        \
## --with-slurm
## 29 ${openmpi}/openmpi-${version}/configure \
##  30 --prefix=${openmpi_install}             \
##  31 --without-libfabric                     \
##  32 --with-psm2=/usr                        \
##  33 --with-cma                              \
##  34 --enable-orterun-prefix-by-default      \
##  35 --with-slurm                            \
##  36 --with-pmi                              \
##  37 --with-pic                              \
##  38 --disable-dlopen                        \
##  41 
##  42 #--with-verbs=/usr                       \
##  43 #--with-psm                              \


make V=1 -j ${ncores}
make DESTDIR=$RPM_BUILD_ROOT -j ${ncores} install

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
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
The Open MPI Project is an open source Message Passing Interface implementation
that is developed and maintained by a consortium of academic, research, and
industry partners. Open MPI is therefore able to combine the expertise,
technologies, and resources from all across the High Performance Computing
community in order to build the best MPI library available. Open MPI offers
advantages for system and software vendors, application developers and computer
science researchers.

This module loads the openmpi environment built with
Intel compilers. By loading this module, the following commands
will be automatically available for compiling MPI applications:
mpif77       (F77 source)
mpif90       (F90 source)
mpicc        (C   source)
mpiCC/mpicxx (C++ source)

The %{MODULE_VAR} module also defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

Version %{version}
]]

--help(help_msg)
help(help_msg)


whatis("Name: OpenMPI"                                                       )
whatis("Version: %{version}"                                                 )
whatis("Category: MPI library, Runtime Support"                              )
whatis("Description: OpenMPI Library (C/C++/Fortran for x86_64)"             )
whatis("URL: https://www.open-mpi.org"                                       )


-- Create environment variables
local base = "%{INSTALL_DIR}"
prepend_path( "MPICH_HOME"            , base )
prepend_path( "PATH"                  , pathJoin( base, "bin" ))
prepend_path( "LD_LIBRARY_PATH"       , pathJoin( base, "lib" ))
prepend_path( "MANPATH"               , pathJoin( base, "share/man" ))
prepend_path( "MODULEPATH"            , "%{MODULE_PREFIX}/%{comp_fam_ver}/ompi_%{pkg_version_dash}/modulefiles")

setenv(       "TACC_OPENMPI_DIR"        , base )
setenv(       "TACC_OPENMPI_BIN"        , pathJoin( base, "bin" ))
setenv(       "TACC_OPENMPI_LIB"        , pathJoin( base, "lib" ))
setenv(       "TACC_OPENMPI_INC"        , pathJoin( base, "include" ))

family("MPI")

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

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
