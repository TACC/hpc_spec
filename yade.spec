Summary: Yade install

# Give the package a base name
%define pkg_base_name yade
%define MODULE_VAR    YADE

# Create some macros (spec file variables)
%define major_version git2017dec
%define minor_version 1
%define micro_version 1

%define pkg_version %{major_version}
#.%{minor_version}.%{micro_version}

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

Release: 1%{?dist}
License: GPLv2
Group: Development/Numerical-Libraries
Source: %{pkg_base_name}-%{pkg_version}.tar.gz
URL: https://yade-dem.org/doc/
Vendor: Yade
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Open Source Discrete Element Method
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Open Source Discrete Element Method
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
Yade is an extensible open-source framework for discrete numerical models, focused on Discrete Element Method. The computation parts are written in c++ using flexible object model, allowing independent implementation of new alogrithms and interfaces. Python is used for rapid and concise scene construction, simulation control, postprocessing and debugging.
%description %{MODULEFILE}
Yade is an extensible open-source framework for discrete numerical models, focused on Discrete Element Method. The computation parts are written in c++ using flexible object model, allowing independent implementation of new alogrithms and interfaces. Python is used for rapid and concise scene construction, simulation control, postprocessing and debugging.

%prep

%setup -n yade-%{version}

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

export COPTFLAGS="-g %{TACC_OPT} -O2"
%if "%{comp_fam}" == "gcc"
  export HAS_HDF5=ON
  export HAS_NETCDF=ON
  export HAS_PYTHON=ON
  export HAS_MUELU=ON
  export HAS_STK=OFF
%else
  export HAS_HDF5=ON
  export HAS_NETCDF=ON
  export HAS_PYTHON=ON
  export HAS_MUELU=ON
  export HAS_STK=ON
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

##
## start of configure install loop
##

rm -rf CMakeCache.txt CMakeFiles
echo "cmaking in" `pwd`

rm -rf /tmp/yade-build
mkdir -p /tmp/yade-build
pushd /tmp/yade-build

export YADE_LOCATION=%{_topdir}/BUILD/

%if "%{comp_fam}" == "gcc"
  echo "%%%% MueLu stats %%%%"
  gcc -v
  uname -a
  export VERBOSE=1
%endif

export SOURCEVERSION=%{version}
export VERSION=%{version}
source %{SPEC_DIR}/yade.cmake
echo ${yade_extra_libs}

####
#### Compilation
####
make -j 8             # Yade can compile in parallel
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
#SET(Yade_CXX_COMPILER_FLAGS " -mkl -DMPICH_SKIP_MPICXX -std=c++11 -O3 -DNDEBUG")
#SET(Yade_C_COMPILER_FLAGS " -mkl -O3 -DNDEBUG")

echo "are we still in /tmp/yade-build?"
pwd
popd

cp -r demos packages %{INSTALL_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
The yade module defines the following environment variables:
TACC_YADE_DIR, TACC_YADE_BIN, and
TACC_YADE_LIB for the location
of the Yade distribution, documentation, binaries,
and libraries.

Version %{version}
external packages installed: ${yade_extra_libs}
]] )

whatis( "Name: Yade" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://yade-dem.org/doc/" )
whatis( "Description: Open Source Discrete Element Method" )

local             yade_arch =    "${architecture}"
local             yade_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(yade_dir,yade_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(yade_dir,yade_arch,"lib") )

setenv("YADE_ARCH",            yade_arch)
setenv("YADE_DIR",             yade_dir)
setenv("TACC_YADE_DIR",        yade_dir)
setenv("TACC_YADE_BIN",        pathJoin(yade_dir,yade_arch,"bin") )
setenv("TACC_YADE_INC",        pathJoin(yade_dir,yade_arch,"include") )
setenv("TACC_YADE_LIB",        pathJoin(yade_dir,yade_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Yade %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua 

##
## end of configure install section
##

module unload python
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

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
* Wed Mat 21 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
