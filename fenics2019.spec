Summary: Fenics install

# Give the package a base name
%define pkg_base_name fenics
%define MODULE_VAR    FENICS

# Create some macros (spec file variables)
%define major_version 2019
%define minor_version 1
%define micro_version 0
%define versionpatch %{major_version}.%{minor_version}.%{micro_version}

%define pkg_version %{major_version}

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
License: BSD-like; see src/docs/website/documentation/copyright.html
Vendor: https://fenicsproject.org/
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{versionpatch}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Fenics local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Fenics local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
FEniCS is a popular open-source (LGPLv3) computing platform for solving partial differential equations (PDEs).
%description %{MODULEFILE}
FEniCS is a popular open-source (LGPLv3) computing platform for solving partial differential equations (PDEs).

%prep

%setup -n fenics-%{versionpatch}

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
module purge
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
# nothing here! cp -r * %{INSTALL_DIR}
pushd %{INSTALL_DIR}
export FENICS_DIR=`pwd`

module load cmake python3
%if "%{comp_fam}" == "gcc"
  module load mkl
%endif

# fenics-specific modules
module load pybind11

####
#### time saving: disable some rebuilds
####
# INSTALL_FFC=0
# DOWNLOAD_FENICS=1
# INSTALL_DOLFIN=1
# INSTALL_MSHR=1
# INSTALL_PYTHON=1

################################################################
####
#### setup
####
################################################################

####
#### compilers
####
#module load intel/18.0.2
export CC=`which mpicc`
export CXX=`which mpicxx`
export FC=`which mpif90`\

####
#### python stuff
####
export PYTHONLEVEL=3
module load cmake
export BOOSTMODULE=boost/1.65
module load ${BOOSTMODULE} # 1.68 is too new!
export BOOST_ROOT=${TACC_BOOST_DIR}
module load python${PYTHONLEVEL}
# note that gcc + python3.6 gives a non-functional pip3
export PIP=pip${PYTHONLEVEL}
module load swig

####
#### required: petsc, slepc
####
PETSCVERSION=3.9
export PETSCMODULE=petsc/${PETSCVERSION}
export SLEPCMODULE=slepc/${PETSCVERSION}
module load ${PETSCMODULE} ${SLEPCMODULE}

####
#### required: eigen
####
EIGEN_VERSION=3.3.4
module load eigen/${EIGEN_VERSION}
EIGEN_DIR=${TACC_EIGEN_DIR}
EIGEN_INSTALL_DIR=${TACC_EIGEN_DIR}

####
#### optional: hdf5
####
export HDF5MODULE=phdf5/1.8.16
module load ${HDF5MODULE}

################################################################
####
#### installation
####
################################################################

####
#### go to the install place
####
FENICS_DIR=%{INSTALL_DIR}
LOGDIR=`pwd`
cd ${FENICS_DIR}

####
#### declare paths
####
export FENICS_PYTHON=${FENICS_DIR}/python
mkdir -p ${FENICS_PYTHON}
export FENICS_PYTHON_PACKAGES=${FENICS_PYTHON}/lib/python${TACC_PYTHON_VER}/site-packages/

####
#### FFC
####

# Stable version
# To install the Python components of FEniCS:

echo ; echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" ; echo
echo ; echo "                Installing FFC"  ; echo 
echo ; echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" ; echo

echo "Using pip: ${PIP}"
echo "Python version: ${TACC_PYTHON_VER}"

( \
  FFC_DIR=/tmp/ffc \
  && rm -rf ${FFC_DIR} \
  && mkdir -p ${FFC_DIR} \
  && cd ${FFC_DIR} \
  && ${PIP} install fenics-ffc \
    --upgrade \
    --prefix=${FENICS_PYTHON} \
  && echo "VLE this fix should go away" \
  && cd ${FENICS_PYTHON_PACKAGES}/FIAT \
  && sed -i '49s/AttributeError/(AttributeError, ValueError)/' \
	 expansions.py \
)

export PYTHONPATH=${PYTHONPATH}:${FENICS_PYTHON_PACKAGES}

####
#### Dolfin and Mshr
####

FENICS_INSTALL=${FENICS_DIR}
# /fenics-installation

# To install DOLFIN, and optionally mshr and/or Python interface of
# DOLFIN/mshr:

FENICS_VERSION=$(python3 -c"import ffc; print(ffc.__version__)")
( \
  git clone --branch=$FENICS_VERSION https://bitbucket.org/fenics-project/dolfin \
  && cd dolfin \
  && cp cmake/templates/dolfin.pc.in dolfin.pc.bak \
  && git checkout origin/master -- cmake/templates/dolfin.pc.in \
  && diff dolfin.pc.bak cmake/templates/dolfin.pc.in || /bin/true \
)
( \
  git clone --branch=$FENICS_VERSION https://bitbucket.org/fenics-project/mshr \
  && cd mshr/python \
  && sed -i \
       -e 's/include_dirs = /include_dirs = [ "\/opt\/apps\/intel18\/boost\/1.65\/include" ] +/' \
	   setup.py \
)

if [ -z "${EIGEN_INSTALL_DIR}" -o ! -d "${EIGEN_INSTALL_DIR}" ] ; then
  echo "Could not find EIGEN_INSTALL_DIR: ${EIGEN_INSTALL_DIR}"
  exit 1
fi
if [ -z "${PETSC_DIR}" -o ! -d "${PETSC_DIR}" ] ; then
  echo "Could not find PETSC_DIR: ${PETSC_DIR}"
  exit 1
fi

echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
echo "                Installing DOLFIN" 
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

rm -rf dolfin/build && mkdir -p dolfin/build 
( \
  cd dolfin/build \
  && cmake \
     -D CMAKE_INSTALL_PREFIX=${FENICS_INSTALL} \
     -D DOLFIN_SKIP_BUILD_TESTS:BOOL=TRUE \
     -D CMAKE_C_COMPILER:FILEPATH=${CC} \
     -D CMAKE_CXX_COMPILER:FILEPATH=${CXX} \
     -D BOOST_ROOT:FILEPATH="${TACC_BOOST_DIR}" \
     -D EIGEN3_INCLUDE_DIR:FILEPATH="${EIGEN_INSTALL_DIR}/include/eigen3" \
     -D PETSC_DIR:PATH=${PETSC_DIR} \
     -D DOLFIN_ENABLE_SUNDIALS=OFF \
     .. \
  && make install \
) 

echo  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" 
echo  "                Installing MSHR"   
echo  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" 
rm -rf mshr/build && mkdir -p mshr/build
( cd mshr/build \
  && cmake \
     -D CMAKE_INSTALL_PREFIX=${FENICS_INSTALL} \
     -D CMAKE_C_COMPILER:FILEPATH=${CC} \
     -D CMAKE_CXX_COMPILER:FILEPATH=${CXX} \
     -D BOOST_ROOT:FILEPATH="${TACC_BOOST_DIR}" \
     -D EIGEN3_INCLUDE_DIR:FILEPATH="${EIGEN_INSTALL_DIR}/include/eigen3" \
     -D PETSC_DIR:PATH=${PETSC_DIR} \
     .. \
  && make install \
) 

export CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:${FENICS_INSTALL}/share/dolfin/cmake

export CXXFLAGS="-I${TACC_BOOST_INC}"

echo  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" 
echo  "                Installing PYTHON"   
echo  "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" 
( \
  cd dolfin/python \
  && ${PIP} install . \
     --prefix=${FENICS_PYTHON} \
) 

( \
  cd mshr/python \
  && ${PIP} install . \
     --prefix=${FENICS_PYTHON} \
) 

# It may be useful to add cmake flag -DCMAKE_INSTALL_PREFIX=<prefix> and pip3 flag --user or --prefix=<prefix> to install to a user location.

##cp ${LOGDIR}/fenicssetup.sh ${FENICS_DIR}
cat >fenicssetup.sh <<EOF
export FENICS_DIR=%{INSTALL_DIR}

# set PATH and LD_LIBRARY_PATH
source \${FENICS_DIR}/fenics-installation/share/dolfin/dolfin.conf

# set PYTHONPATH
export PYTHONPATH=\${PYTHONPATH}:\${FENICS_DIR}/python/lib/python${TACC_PYTHON_VER}/site-packages:\${FENICS_DIR}/dolfin/python
EOF

chmod -R g+rX,o+rX ${FENICS_DIR}

##
## modulefile
##

export modulefilename=%{version}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The fenics module defines the Fenics variable
TACC_FENICS_DIR for the location
of the Fenics distribution. It also updates PYTHONPATH.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Fenics" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://fenicsproject.org/" )
whatis( "Description: Portable Extendible Toolkit for Scientific Computing, Numerical library for sparse linear algebra" )

local             fenics_dir =     "%{INSTALL_DIR}/"

prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"dolfin","python") )
prepend_path("PYTHONPATH",      pathJoin(fenics_dir,"dolfin","python","src") )
prepend_path("PYTHONPATH",
      pathJoin(fenics_dir,"python","lib","python${TACC_PYTHON_VER}","site-packages") )

setenv("FENICS_DIR",             fenics_dir)
setenv("TACC_FENICS_DIR",        fenics_dir)

prereq("${BOOSTMODULE}")
prereq("python${PYTHONLEVEL}")
prereq("${PETSCMODULE}")
prereq("${SLEPCMODULE}")
prereq("${HDF5MODULE}")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Fenics %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua 

cp -r %{INSTALL_DIR}/* \
    $RPM_BUILD_ROOT/%{INSTALL_DIR}

popd
umount %{INSTALL_DIR}

echo "Directory to package up: $RPM_BUILD_ROOT/%{INSTALL_DIR}"
echo "listing:"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(-,root,install,)
  %{MODULE_DIR}

%files %{PACKAGE}
  %defattr(-,root,install,)
  %{INSTALL_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
%changelog
* Mon Jan 28 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
