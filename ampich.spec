#
# W. Cyrus Proctor
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
%define pkg_base_name ampich
%define MODULE_VAR    AMPICH

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 2

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-hidden-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   3
License:   BSD
Group:     MPI
URL:       http://www.mpich.org
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
This is specifically an rpm for the Intel MPI modulefile
used on LS5.

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
ml purge
ml %{comp_module}
ml

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  mount -t tmpfs tmpfs %{INSTALL_DIR}
    
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
 
 
export ampich=`pwd`
export ampich_install=%{INSTALL_DIR}
export ncores=16
export ampich_major=%{major_version}
export ampich_minor=%{minor_version}
export ampich_version=${ampich_major}.${ampich_minor}
if [ "%{comp_fam}" == "gcc" ]; then
  echo "GCC Build"
  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export CFLAGS="-march=core-avx-i -mtune=core-avx2"
  export CXXFLAGS="-march=core-avx-i -mtune=core-avx2"
  export FCFLAGS="-march=core-avx-i -mtune=core-avx2"
  export LDFLAGS="-march=core-avx-i -mtune=core-avx2"
elif [ "%{comp_fam}" == "intel" ]; then
  echo "Intel Build"
  export CC=icc
  export CXX=icpc
  export FC=ifort
  export CFLAGS="-xCORE-AVX-I -axCORE-AVX2"
  export CXXFLAGS="-xCORE-AVX-I -axCORE-AVX2"
  export FCFLAGS="-xCORE-AVX-I -axCORE-AVX2"
  export LDFLAGS="-xCORE-AVX-I -axCORE-AVX2"
else
  echo "Unrecognized compiler! Exiting!"
  exit -1
fi

cd ${ampich}

wget http://www.mpich.org/static/downloads/${ampich_version}/mpich-${ampich_version}.tar.gz
tar xvfz mpich-${ampich_version}.tar.gz
cd mpich-${ampich_version}

${ampich}/mpich-${ampich_version}/configure \
--prefix=${ampich_install}                  \
--with-slurm=/opt/slurm/default

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
MPICH is a high-performance and widely portable implementation of the Message
Passing Interface (MPI) standard (MPI-1, MPI-2 and MPI-3). The goals of MPICH
are: (1) to provide an MPI implementation that efficiently supports different
computation and communication platforms including commodity clusters (desktop
systems, shared-memory systems, multicore architectures), high-speed networks
(10 Gigabit Ethernet, InfiniBand, Myrinet, Quadrics) and proprietary high-end
computing systems (Blue Gene, Cray) and (2) to enable cutting-edge research in
MPI through an easy-to-extend modular framework for other derived
implementations. 

This module loads the Argonne MPICH environment built with
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


whatis("Name: Argonne MPICH"                                                 )
whatis("Version: %{version}"                                                 )
whatis("Category: MPI library, Runtime Support"                              )
whatis("Description: Argonne MPICH MPI Library (C/C++/Fortran for x86_64) "  )
whatis("URL: http://www.mpich.org "  )


-- Create environment variables
local base = "%{INSTALL_DIR}"
prepend_path( "MPICH_HOME"            , base )
prepend_path( "PATH"                  , pathJoin( base, "bin" ))
prepend_path( "LD_LIBRARY_PATH"       , pathJoin( base, "lib" ))
prepend_path( "MANPATH"               , pathJoin( base, "share/man" ))
prepend_path( "MODULEPATH"            , "%{MODULE_PREFIX}/%{comp_fam_ver}/ampich_3_2/modulefiles")

setenv(       "TACC_MPICH_DIR"        , base )
setenv(       "TACC_MPICH_BIN"        , pathJoin( base, "bin" ))
setenv(       "TACC_MPICH_LIB"        , pathJoin( base, "lib" ))
setenv(       "TACC_MPICH_INC"        , pathJoin( base, "include" ))

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

