Summary: Trilinos install

# Give the package a base name
%define pkg_base_name trilinos
%define MODULE_VAR    TRILINOS

# Create some macros (spec file variables)
%define major_version git
%define minor_version 20180802

%define pkg_version %{major_version}%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 2%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-git%{minor_version}.tar.gz
URL: http://trilinos.sandia.gov/
Vendor: Sandia National Labs
Packager: TACC -- eijkhout@tacc.utexas.edu

# # Refer to: https://www.redhat.com/archives/rpm-list/2003-May/msg00471.html
# Source1: find_requires_no_python.sh
# define __find_requires %{Source1}
# # This does not seem to work; http://ftp.rpm.org/max-rpm/s1-rpm-depend-auto-depend.html
# AutoReqProv: no

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Trilinos is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries
%package %{PACKAGE}-sources
Summary: Trilinos is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Trilinos is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}-sources
Trilinos sources: demos & packages directories

%description %{PACKAGE}
The Trilinos Project is an effort to develop algorithms and enabling
technologies within an object-oriented software framework for the
solution of large-scale, complex multi-physics engineering and
scientific problems. A unique design feature of Trilinos is its focus
on packages.

Each Trilinos package is a self-contained, independent piece of
software with its own set of verzoekments, its own development team
and group of users. Because of this, Trilinos itself is designed to
respect the autonomy of packages. Trilinos offers a variety of ways
for a particular package to interact with other Trilinos packages. It
also offers a set of tools that can assist package developers with
builds across multiple platforms, generating documentation and
regression testing across a set of target platforms. At the same time,
what a package must do to be called a Trilinos package is minimal, and
varies with each package.
%description %{MODULEFILE}
The Trilinos Project is an effort to develop algorithms and enabling
technologies within an object-oriented software framework for the
solution of large-scale, complex multi-physics engineering and
scientific problems. A unique design feature of Trilinos is its focus
on packages.

Each Trilinos package is a self-contained, independent piece of
software with its own set of verzoekments, its own development team
and group of users. Because of this, Trilinos itself is designed to
respect the autonomy of packages. Trilinos offers a variety of ways
for a particular package to interact with other Trilinos packages. It
also offers a set of tools that can assist package developers with
builds across multiple platforms, generating documentation and
regression testing across a set of target platforms. At the same time,
what a package must do to be called a Trilinos package is minimal, and
varies with each package.

%prep

%setup -n trilinos-git

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include compiler-load.inc
%include mpi-load.inc

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

module load boost cmake swig/3.0.12
## VLE stopgap!
export BOOST_ROOT=${TACC_BOOST_DIR}

%if "%{comp_fam}" == "gcc"
  which gcc
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif

export COPTFLAGS="-g -xhost -O2"

export HAS_HDF5=ON
export HAS_NETCDF=ON
export HAS_MUELU=ON
export HAS_PYTHON=ON
export HAS_STK=ON
export HAS_SUPERLU=ON
%if "%{comp_fam}" == "gcc"
  export HAS_HDF5=OFF
  export HAS_NETCDF=OFF
  # VLE is this fixed?
  export HAS_SUPERLU=ON
%endif

export HAS_SEACAS=${HAS_NETCDF}
if [ "${HAS_HDF5}" = "ON" ] ; then
  module load phdf5
fi
if [ "${HAS_NETCDF}" = "ON" ] ; then
  module load parallel-netcdf phdf5
fi
if [ "${HAS_PYTHON}" = "ON" ] ; then
  module load python2/2.7.15
fi
if [ "${HAS_SUPERLU}" = "ON" ] ; then
  module load superlu_seq
fi

#module use -a /opt/apps/intel16/modulefiles # for boost
#module load boost

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

##
## start of configure install loop
##

rm -rf CMakeCache.txt CMakeFiles
echo "cmaking in" `pwd`

####
#### Cmake
####

export VERSION=git
export TRILINOS_LOCATION=%{_topdir}/BUILD/

rm -rf /tmp/trilinos-build
mkdir -p /tmp/trilinos-build
pushd /tmp/trilinos-build

##  export VERBOSE=1
export SOURCEVERSION=%{version}
export PREFIXPATH=%{INSTALL_DIR}
source %{SPEC_DIR}/trilinos-git.cmake || /bin/true
echo ${trilinos_extra_libs}

####
#### Compilation
####

#make -j 1             # debug mode....
## parallel make; "j 8" seems to run out of memory
make -j 4             # Trilinos can compile in parallel

#make -j 4 tests           # (takes forever...)

####
#### Testing
####
#ctest -VV

####
#### Install permanently
####

make install
#/opt/apps/intel18/python2/2.7.15/lib/libpython2.7.so
( cd %{INSTALL_DIR} && \
  find . -name \*.cmake \
    -exec sed -i -e '/STKDoc_testsConfig.cmake/d' \
            -e '/COMPILER_FLAGS/s/mkl/mkl -L/opt/apps/intel18/python2/2.7.15/lib -lpython2.7/' \
            -e '/EXTRA_LD_FLAGS/s?""?"/opt/apps/intel18/python2/2.7.15/lib/libpython2.7.so"?' \
            -e '/SET.*TPL_LIBRARIES/s?""?"/opt/apps/intel18/python2/2.7.15/lib/libpython2.7.so"?' \
            -e '/SET.*TPL_LIBRARIES/s?so"?so;/opt/apps/intel18/python2/2.7.15/lib/libpython2.7.so"?' \
                   {} \; \
         -print \
)

echo "are we still in /tmp/trilinos-build?"
pwd
popd

( pwd ; ls ; \
  ls -l \
    packages/seacas/libraries/ioss/html \
    packages/seacas/libraries/exodus/topology \
    packages/seacas/libraries/exodus/html \
  ; \
  rm -f \
    packages/seacas/libraries/ioss/html \
    packages/seacas/libraries/exodus/topology \
    packages/seacas/libraries/exodus/html \
)

# prevent trouble with #!${PYTHON_EXECUTABLE}
find packages -name \*.py.in -exec rm -f {} \;

cp -r demos packages %{INSTALL_DIR}
echo "contents of the tmpfs INSTALL_DIR:"
ls %{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The trilinos module defines the following environment variables:
TACC_TRILINOS_DIR, TACC_TRILINOS_BIN, and
TACC_TRILINOS_LIB for the location
of the Trilinos distribution, documentation, binaries,
and libraries.

Version %{version}
external packages installed: ${trilinos_extra_libs}
]] )

whatis( "Name: Trilinos" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/trilinos/trilinos-as/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             trilinos_arch =    "${architecture}"
local             trilinos_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(trilinos_dir,trilinos_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(trilinos_dir,trilinos_arch,"lib") )

setenv("TRILINOS_ARCH",            trilinos_arch)
setenv("TRILINOS_DIR",             trilinos_dir)
setenv("TACC_TRILINOS_DIR",        trilinos_dir)
setenv("TACC_TRILINOS_BIN",        pathJoin(trilinos_dir,trilinos_arch,"bin") )
setenv("TACC_TRILINOS_INC",        pathJoin(trilinos_dir,trilinos_arch,"include") )
setenv("TACC_TRILINOS_LIB",        pathJoin(trilinos_dir,trilinos_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module1.0#################################################
##
## version file for Trilinos %version
##

set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

##
## end of configure install section
##

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

echo "Directory to package up: $RPM_BUILD_ROOT/%{INSTALL_DIR}"
echo "listing:"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}
echo "original requires:"
find $RPM_BUILD_ROOT | /usr/lib/rpm/find-requires
echo "filtered requires:"
#find $RPM_BUILD_ROOT | %{SPEC_DIR}/../SOURCES/find_requires_no_python.sh
#find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name \*.so -print -exec ldd {} \; 

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

%files %{PACKAGE}-sources
  %defattr(-,root,install,)
  %{INSTALL_DIR}/demos
  %{INSTALL_DIR}/packages
  %{INSTALL_DIR}/*.txt

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}/bin
  %{INSTALL_DIR}/include
  %{INSTALL_DIR}/lib

#bin
#demos
#include
#lib
#packages

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

# ########################################
# ## Fix Modulefile During Post Install ##
# ########################################
# %post %{PACKAGE}
# export PACKAGE_POST=1
# %include post-defines.inc

# %post %{MODULEFILE}
# export MODULEFILE_POST=1
# %include post-defines.inc

# %preun %{PACKAGE}
# export PACKAGE_PREUN=1
# %include post-defines.inc
# ########################################
# ############ Do Not Remove #############
# ########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog

* Fri Aug 24 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: UNRELEASED activating hdf5/netcdf
             now in three rpms
* Fri Aug 03 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: try to use python 2.7.15 throughout
  TRYING: with python, no Domi
* Mon Jul 31 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release, no pytrilinos

