#
# W. Cyrus Proctor
# 2016-01-06
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
%define pkg_base_name mvapich2
%define MODULE_VAR    MVAPICH2

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 1

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
#%include name-defines-noreloc.inc
%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1
License:   Freely Distributable
Group:     MPI
URL:       http://mvapich.cse.ohio-state.edu
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

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
MPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.

MPICH includes all of the routines in MPI 1.2, along with the I/O routines from
MPI-2 and some additional routines from MPI-3, including those supporting MPI
Info and some of the additional datatype constructors.  MPICH  was developed by
Argonne National Laboratory. See www.mcs.anl.gov/mpi/mpich for more
information.



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
module purge
# Load Compiler
%include compiler-load.inc
ml hwloc
# Load MPI Library
#%include mpi-load.inc

# Insert further module commands

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
  
##################################################
export         mv2=`pwd`
export mv2_install=%{INSTALL_DIR}
##################################################

export   mv2_major=2
export   mv2_minor=1
export mv2_version=${mv2_major}.${mv2_minor}

export   CFLAGS="-L/opt/slurm/default/lib64 -lpmi2 -xAVX -axCORE-AVX2"
export CXXFLAGS="-L/opt/slurm/default/lib64 -lpmi2 -xAVX -axCORE-AVX2"
export  FCFLAGS="-L/opt/slurm/default/lib64 -lpmi2 -xAVX -axCORE-AVX2"
export   FFLAGS="-L/opt/slurm/default/lib64 -lpmi2 -xAVX -axCORE-AVX2"
export  LDFLAGS="-L/opt/slurm/default/lib64 -lpmi2 -xAVX -axCORE-AVX2"
export   CFLAGS="-xAVX -axCORE-AVX2"
export CXXFLAGS="-xAVX -axCORE-AVX2"
export  FCFLAGS="-xAVX -axCORE-AVX2"
export   FFLAGS="-xAVX -axCORE-AVX2"
export  LDFLAGS="-xAVX -axCORE-AVX2"
export       CC=icc
export      CXX=icpc
export       FC=ifort
export       FF=ifort
export   ncores=16

cd ${mv2}
wget http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-${mv2_version}.tar.gz
tar xvfz mvapich2-${mv2_version}.tar.gz
cd mvapich2-${mv2_version}

${mv2}/mvapich2-${mv2_version}/configure \
--prefix=${mv2_install}                  \
--with-pmi=pmi2                          \
--with-pm=slurm                          \
--with-slurm=/opt/slurm/default          \
--enable-romio                           \
--with-file-system=lustre+nfs            \
--disable-mcast

make -j ${ncores}
make -j ${ncores} install


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/


  
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
This module loads the MVAPICH2 MPI environment built with %{comp_fam_name} compilers. 
By loading this module, the following commands will be automatically available
for compiling MPI applications:

mpif77       (F77 source)
mpif90       (F90 source)
mpicc        (C   source)
mpiCC/mpicxx (C++ source)

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

Version %{pkg_version}
]]

--help(help_msg)
help(help_msg)

-- Create environment variables.
local base           = "%{INSTALL_DIR}"
whatis("Name: MVAPICH2")
whatis("Version: %{pkg_version}")
whatis("Category: library, runtime support ")
whatis("Keywords: System, Library ")
whatis("Description: MPI-2 implementation for Infiniband ")
whatis("URL: http://mvapich.cse.ohio-state.edu/overview/mvapich2")
setenv("MPICH_HOME",base)
setenv("TACC_MPI_GETMODE","mvapich2_ssh")
prepend_path("PATH"            , pathJoin(base, "bin")        )
prepend_path("MANPATH"         , pathJoin(base, "share/man")  )
prepend_path("INFOPATH"        , pathJoin(base, "doc")        )
prepend_path("LD_LIBRARY_PATH" , pathJoin(base, "lib/shared") )
prepend_path("LD_LIBRARY_PATH" , pathJoin(base, "lib")        )
setenv("MV2_USE_OLD_BCAST","0")
setenv("MV2_USE_UD_HYBRID","0")
family("MPI")

-- prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/bar1_1/modulefiles")

setenv( "TACC_%{MODULE_VAR}_DIR",                base )
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(base, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(base, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(base, "bin"))
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

