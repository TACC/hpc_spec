#
# Adapted from Bar.spec by Victor Eijkhout 2015/11/30
# split software into two rpm
#

Summary: Dealii install

# Give the package a base name
%define pkg_base_name dealii
%define MODULE_VAR    DEALII

# Create some macros (spec file variables)
%define major_version 9
%define minor_version 0
%define micro_version 0

%define dealiipetscversion 3.9
%define dealiitrilinosversion git20180802

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc

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

Release: 1%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tar.gz
URL: http://www.dealii.org/
Vendor: TAMU
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Dealii is an open source finite element package
Group: Development/Numerical-Libraries
%package %{PACKAGE}-sources
Summary: Dealii is an open source finite element package
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Dealii is an open source finite element package
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
The main aim of deal.II is to enable rapid development of modern
finite element codes, using among other aspects adaptive meshes and a
wide array of tools classes often used in finite element
program. Writing such programs is a non-trivial task, and successful
programs tend to become very large and complex. We believe that this
is best done using a program library that takes care of the details of
grid handling and refinement, handling of degrees of freedom, input of
meshes and output of results in graphics formats, and the
like. Likewise, support for several space dimensions at once is
included in a way such that programs can be written independent of the
space dimension without unreasonable penalties on run-time and memory
consumption.
%description %{PACKAGE}-sources
The main aim of deal.II is to enable rapid development of modern

%description %{MODULEFILE}
The main aim of deal.II is to enable rapid development of modern
finite element codes, using among other aspects adaptive meshes and a
wide array of tools classes often used in finite element
program. Writing such programs is a non-trivial task, and successful
programs tend to become very large and complex. We believe that this
is best done using a program library that takes care of the details of
grid handling and refinement, handling of degrees of freedom, input of
meshes and output of results in graphics formats, and the
like. Likewise, support for several space dimensions at once is
included in a way such that programs can be written independent of the
space dimension without unreasonable penalties on run-time and memory
consumption.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_full_version}

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
%include compiler-load.inc
%include mpi-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#
# Set Up Installation Directory and tmp file system
#
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

export modulefilename=%{pkg_version}

# Insert necessary module commands
module list
for m in boost cmake \
    parallel-netcdf phdf5 \
    petsc/%{dealiipetscversion} slepc/%{dealiipetscversion} \
    p4est trilinos/%{dealiitrilinosversion} \
    ; do
  module --ignore_cache load $m ;
done
# VLE missing so far: metis
#module load phdf5 parallel-netcdf python swig
#module load mumps 
#module load parmetis-petsc

%if "%{comp_fam}" == "gcc"
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

##
## start of configure install
##

export LOGDIR=`pwd`
mkdir -p %{INSTALL_DIR}/build
pushd %{INSTALL_DIR}/build

rm -f CMakeCache.txt

echo "Installing deal with Petsc: ${PETSC_DIR}/${PETSC_ARCH}"

  cmake -VV \
    -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} \
    -DCMAKE_C_COMPILER="mpicc" \
    -DCMAKE_CXX_COMPILER="mpicxx" \
    -DDEAL_II_WITH_CXX11=ON \
    -DCMAKE_Fortran_COMPILER=mpif90 \
    -DDEAL_II_CXX_FLAGS_DEBUG="-std=c++14" \
    -DDEAL_II_CXX_FLAGS_RELEASE="-std=c++14" \
    -DDEAL_II_WITH_MPI=ON \
    ` if [ ${TACC_FAMILY_COMPILER} = "gcc" ] ; then echo " \
        -DMPI_CXX_INCLUDE_PATH=${MPICH_HOME}/include \
        -DMPI_CXX_LIBRARIES=${MPICH_HOME}/lib \
    " ; fi ` \
    -DDEAL_II_COMPONENT_MESH_CONVERTER=ON \
    -DBOOST_DIR=${TACC_BOOST_DIR} \
    -DHDF5_DIR=${TACC_HDF5_DIR} \
    ` if [ ${TACC_FAMILY_COMPILER} = "intel" ] ; then echo " \
      -DMUMPS_DIR=${TACC_MUMPS_DIR} \
      -DMETIS_DIR=${TACC_METIS_DIR} \
      -DSLEPC_DIR=${TACC_SLEPC_DIR} \
    " ; fi ` \
    -DNETCDF_DIR=${TACC_NETCDF_DIR} \
    -DDEAL_II_WITH_PETSC=ON -DDEAL_II_WITH_SLEPC=ON \
        -DPETSC_DIR=${PETSC_DIR} -DPETSC_ARCH=${PETSC_ARCH} \
    -DDEAL_II_WITH_P4EST=ON \
        -DP4EST_DIR=${P4ESTDIR} \
    -DDEAL_II_WITH_TRILINOS=ON \
        -DTRILINOS_DIR=${TACC_TRILINOS_DIR} \
    ${DEALDIR}/dealii-${DEALVERSION} \
    \
    %{_topdir}/BUILD/dealii-%{version} \
    2>&1 | tee ${LOGDIR}/dealii_cmake.log

make 2>&1 | tee ${LOGDIR}/dealii_compile.log

make install
### fails with gcc because it uses mpiexec:
### make test

popd # back out of INSTALL_DIR

mkdir -p %{INSTALL_DIR}/examples
cp -r examples/step* %{INSTALL_DIR}/examples

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

##
## start of module file section
##

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
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The dealii module defines the following environment variables:
TACC_DEALII_DIR, TACC_DEALII_BIN, and
TACC_DEALII_LIB for the location
of the Dealii distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Dealii" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/dealii/dealii-as/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             dealii_arch =    "${architecture}"
local             dealii_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(dealii_dir,dealii_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(dealii_dir,dealii_arch,"lib") )

setenv("DEALII_ARCH",            dealii_arch)
setenv("DEALII_DIR",             dealii_dir)
setenv("TACC_DEALII_DIR",        dealii_dir)
setenv("TACC_DEALII_BIN",        pathJoin(dealii_dir,dealii_arch,"bin") )
setenv("TACC_DEALII_LIB",        pathJoin(dealii_dir,dealii_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Dealii %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

cp -r %{INSTALL_DIR}/{include,lib,share} \
    ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
cp -r %{INSTALL_DIR}/{LICENSE,README.md,examples} \
    ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
umount %{INSTALL_DIR}

#------------------------
%if %{?BUILD_PACKAGE}
  # RPM package contains files within these directories
#------------------------

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}/.tacc_install_canary
  %{INSTALL_DIR}/include
  %{INSTALL_DIR}/lib
  %{INSTALL_DIR}/share

%files %{PACKAGE}-sources
  %defattr(-,root,install,)
  %{INSTALL_DIR}/LICENSE
  %{INSTALL_DIR}/README.md
#  %{INSTALL_DIR}/build
  %{INSTALL_DIR}/examples
							
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

%changelog
#
* Mon Aug 20 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
