Summary: Trilinos install

# Give the package a base name
%define pkg_base_name trilinos
%define MODULE_VAR    TRILINOS

# Create some macros (spec file variables)
%define major_version git
%define minor_version 20181024

%define pkg_version %{major_version}%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 6%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-git%{minor_version}.tar.gz
URL: http://trilinos.sandia.gov/
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

module load cmake boost swig
## VLE stopgap!
export BOOST_ROOT=${TACC_BOOST_DIR}

%if "%{comp_fam}" == "gcc"
  which gcc
  module load mkl
%else
  export MKLFLAG="-mkl"
%endif

export COPTFLAGS="-g %{TACC_OPT} -O2"

export HAS_HDF5=ON
export HAS_NETCDF=ON
export HAS_MUELU=ON
export HAS_PYTHON=ON
export HAS_STK=ON
export HAS_SUPERLU=ON
%if "%{comp_fam}" == "gcc"
  #export HAS_NETCDF=OFF
  #export HAS_HDF5=OFF
  # VLE is this fixed?
  export HAS_SUPERLU=ON
%endif

export HAS_SEACAS=${HAS_NETCDF}
if [ "${HAS_HDF5}" = "ON" ] ; then
  module load phdf5
fi
if [ "${HAS_NETCDF}" = "ON" ] ; then
  module load parallel-netcdf
fi
if [ "${HAS_PYTHON}" = "ON" ] ; then
  module load python
fi
if [ "${HAS_SUPERLU}" = "ON" ] ; then
  module load superlu_seq
fi

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

##
## start of configure install stage
##

rm -rf CMakeCache.txt CMakeFiles
echo "Cmaking in" `pwd`

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
##
## cmake script!
##
source %{SPEC_DIR}/trilinos-git.cmake

cat >sedheader.script <<EOF
/header =/i\
    header = os.path.join(MPI_BASE_DIR, "include", "mpi.h")
/header =/d
EOF

sed -i \
    -e '/header/s/\/include\/mpi.h/\/opt\/intel\/compilers_and_libraries_2018.2.199\/linux\/mpi\/intel64\/include\/mpi.h/' \
    /tmp/trilinos-build/packages/PyTrilinos/src/gen_teuchos_rcp.py

#os.path.join(MPI_BASE_DIR, "intel64", "include", "mpi.h")/'

#-f sedheader.script
grep "header =" \
    /tmp/trilinos-build/packages/PyTrilinos/src/gen_teuchos_rcp.py

####
#### Compilation
####

#make -j 1             # debug mode....
## parallel make; "j 8" seems to run out of memory
make -j 4             # Trilinos can compile in parallel

#make -j 4 tests           # (takes forever...)

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

( cd %{INSTALL_DIR} && \
  find . -name \*.cmake \
         -exec sed -i -e '/STKDoc_testsConfig.cmake/d' \
                      -e '/COMPILER_FLAGS/s/mkl/mkl -L\${TACC_PYTHON_LIB} -lpython2.7/' \
                      -e '/EXTRA_LD_FLAGS/s?""?"/opt/apps/intel17/python/2.7.13/lib/libpython2.7.so"?' \
                      -e '/SET.*TPL_LIBRARIES/s?""?"/opt/apps/intel17/python/2.7.13/lib/libpython2.7.so"?' \
                      -e '/SET.*TPL_LIBRARIES/s?so"?so;/opt/apps/intel17/python/2.7.13/lib/libpython2.7.so"?' \
                   {} \; \
         -print \
)
## SET(Zoltan_TPL_LIBRARIES "")
export nosed="\
    "

echo "are we still in /tmp/trilinos-build?"
pwd
popd

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

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

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

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Tue Aug 28 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 6: rebuild for intel18
* Wed Jul 18 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 5: recompile with fixed superlu_seq
* Wed Jun 20 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 4: superlu correctly included
* Mon Feb 26 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: just to satisfy losf
* Sat Nov 04 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: adding superlu
* Fri Sep 01 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
