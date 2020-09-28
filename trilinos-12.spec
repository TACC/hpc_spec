Summary: Trilinos install

# Give the package a base name
%define pkg_base_name trilinos
%define MODULE_VAR    TRILINOS

# Create some macros (spec file variables)
%define major_version 12
%define minor_version 18
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
#### %include python-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home2.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 11%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tar.gz
URL: https://github.com/trilinos/Trilinos
Vendor: Sandia National Labs
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Trilinos is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Trilinos is a large suite of numerical algorithms from Sandia National Laboratories
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
The Trilinos Project is an effort to develop algorithms and enabling
technologies within an object-oriented software framework for the
solution of large-scale, complex multi-physics engineering and
scientific problems. A unique design feature of Trilinos is its focus
on packages.

Each Trilinos package is a self-contained, independent piece of
software with its own set of requirements, its own development team
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
software with its own set of requirements, its own development team
and group of users. Because of this, Trilinos itself is designed to
respect the autonomy of packages. Trilinos offers a variety of ways
for a particular package to interact with other Trilinos packages. It
also offers a set of tools that can assist package developers with
builds across multiple platforms, generating documentation and
regression testing across a set of target platforms. At the same time,
what a package must do to be called a Trilinos package is minimal, and
varies with each package.

%prep

%setup -n trilinos-%{version}

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
#### %include python-load.inc

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
##cp -r * %{INSTALL_DIR}
##pushd %{INSTALL_DIR}

module load cmake boost swig
## VLE stopgap!
export BOOST_ROOT=${TACC_BOOST_DIR}

%if "%{comp_fam}" == "gcc"
  which gcc
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif
export MKLLIBS=mkl_intel_lp64\;mkl_sequential\;mkl_core\;pthread

export COPTFLAGS="-g %{TACC_OPT} -O2"
  export HAS_HDF5=ON
  export HAS_NETCDF=ON
  export HAS_PYTHON=ON
  export HAS_MUELU=ON
  export HAS_STK=ON
  export HAS_SUPERLU=ON

export HAS_SEACAS=${HAS_NETCDF}
if [ "${HAS_HDF5}" = "ON" ] ; then
  module load phdf5
fi
if [ "${HAS_NETCDF}" = "ON" ] ; then
  module load parallel-netcdf
fi

export HAS_MUMPS=ON
# https://github.com/trilinos/Trilinos/issues/6339
if [ "${HAS_MUMPS}" = "ON" ] ; then
  module load mumps 
  export MUMPSLIBS="-L${TACC_MUMPS_LIB} -ldmumps -lmumps_common -lpord -lmkl_scalapack_lp64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -liomp5 -lmkl_blacs_intelmpi_lp64 -lpthread -lifcore"
  export MUMPSLIBNAMES=dmumps\;mumps_common\;pord\;mkl_scalapack_lp64\;mkl_intel_lp64\;mkl_intel_thread\;mkl_core\;iomp5\;mkl_blacs_intelmpi_lp64\;pthread\;ifcore
  export PARMETISLIBS=${TACC_PARMETIS_LIB}/libptscotchparmetis.a\;${TACC_PARMETIS_LIB}/libparmetis.so
  export MKLLIBS=${MKLLIBS}\;libmkl_scalapack_lp64\;libmkl_blacs_intelmpi_lp64
else
  export MUMPSLIBS=NO_MUMPS_LOADED
  export PARMETISLIBS=NO_PARMETIS_LOADED
fi

export HAS_PYTHON=OFF
export removed_from_cmake="\
  -D Trilinos_EXTRA_LINK_FLAGS=${PYTHON_LIB_SO} \
  -D Trilinos_EXTRA_LD_FLAGS=${PYTHON_LIB_SO} \
  "
export HAS_SUPERLU=OFF

if [ "${HAS_SUPERLU}" = "ON" ] ; then
  module load superlu_seq
else
  export TACC_SUPERLUSEQ_DIR=/home/foo
  export TACC_SUPERLUSEQ_LIB=/home/foo
fi

##
## start of configure install loop
##

rm -rf CMakeCache.txt CMakeFiles
echo "cmaking in" `pwd`

rm -rf /tmp/trilinos-build
mkdir -p /tmp/trilinos-build
pushd /tmp/trilinos-build

export TRILINOS_LOCATION=%{_topdir}/BUILD/

%if "%{comp_fam}" == "gcc"
  echo "%%%% MueLu stats %%%%"
  gcc -v
  uname -a
  export VERBOSE=1
%endif

export SOURCEVERSION=%{version}
export VERSION=%{version}
# %if "%{python_major_version}" == "3"
#   export PYTHON_LIB_SO=${TACC_PYTHON3_LIB}/libpython%{python_major_version}.%{python_minor_version}m.so
# %else
#   export PYTHON_LIB_SO=${TACC_PYTHON2_LIB}/libpython%{python_major_version}.%{python_minor_version}.so
# %endif

%include %{SPEC_DIR}/victor_scripts/trilinos.cmake
echo ${trilinos_extra_libs}

####
#### Compilation
####
make -j 8             # Trilinos can compile in parallel
# make -j 4 tests           # (takes forever...)
#make runtests-serial # (requires queue submission)
#make runtests-mpi    # (requires queue submission)

####
#### Testing
####
#ctest -VV

####
#### Install permanently
####

make install

## TACC_FAMILY_PYTHON_VERSION is 2.7.16 and such

####
#### this is hard to get to work.
#### let's build without python for a while
####
# ( cd %{INSTALL_DIR} && \
#   find . -name \*.cmake \
#          -exec sed -i -e '/STKDoc_testsConfig.cmake/d' \
#                       -e '/COMPILER_FLAGS/s/mkl/mkl -L\${TACC_PYTHON_LIB} -lpython${TACC_PYTHON_VER}/' \
#                       -e '/EXTRA_LD_FLAGS/s?""?"\${TACC_PYTHON_LIB}/libpython${TACC_PYTHON_VER}.so"?' \
#                       -e '/SET.*TPL_LIBRARIES/s?""?"\${TACC_PYTHON_LIB}/libpython${TACC_PYTHON_VER}.so"?' \
#                       -e '/SET.*TPL_LIBRARIES/s?so"?so;\${TACC_PYTHON_LIB}/libpython${TACC_PYTHON_VER}.so"?' \
#                    {} \; \
#          -print \
# )

## SET(Zoltan_TPL_LIBRARIES "")

echo "are we still in /tmp/trilinos-build?"
pwd
popd

cp -r demos packages %{INSTALL_DIR}

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
whatis( "URL: https://github.com/trilinos/Trilinos" )
whatis( "Description: Sandia computational engineering package" )

local             trilinos_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(trilinos_dir,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(trilinos_dir,"lib") )

setenv("TRILINOS_DIR",             trilinos_dir)
setenv("TACC_TRILINOS_DIR",        trilinos_dir)
setenv("TACC_TRILINOS_BIN",        pathJoin(trilinos_dir,"bin") )
setenv("TACC_TRILINOS_INC",        pathJoin(trilinos_dir,"include") )
setenv("TACC_TRILINOS_LIB",        pathJoin(trilinos_dir,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module1.0#################################################
##
## version file for Trilinos %version
##

set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

#module unload python ### VLE why?

cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/
ls %{INSTALL_DIR}
ls ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

umount %{INSTALL_DIR} # tmpfs # $INSTALL_DIR

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Tue Apr 28 2020 eijkhout <eijkhout@tacc.utexas.edu>
- UNRELEASED : fix in .version file
* Sun Nov 24 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 11: adding mumps, update to 12.18.1
* Thu Nov 14 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 10: without python
* Mon Sep 16 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 9: making python handling more portable
* Sun Jun 09 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 8: fix URLs, architecture, lib directory
* Tue May 28 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 7: upgrade to 12.14.1
  for now without python, superluseq
* Mon Apr 23 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: upgrade to 12.12.1 NEVER RELEASED?
* Wed Jan 17 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: giving up on SuperLU for now, fixed module help
* Wed Aug 16 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: adding FEI
* Mon Jul 31 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: disable STK for gcc
* Fri Jun 30 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: fix broken stuff that trips up dealII
             also enabling python for gcc
* Fri May 12 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
