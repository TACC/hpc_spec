Summary: Libmesh install

# Give the package a base name
%define pkg_base_name libmesh
%define MODULE_VAR    LIBMESH

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 6
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define use_petsc 1
%define petscversion 3.14
%define use_trilinos 0
%define trilinosversion 12.18.1
%define python_version 3

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
URL: https://github.com/libMesh
Vendor: CFDlab UT Austin
Packager: TACC -- eijkhout@tacc.utexas.edu

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Libmesh is a C++ Finite Element library
Group: Development/Numerical-Libraries
%package %{MODULEFILE}
Summary: Libmesh is a C++ Finite Element library
Group: Development/Numerical-Libraries

%description
%description %{PACKAGE}
C++ FE
%description %{MODULEFILE}
C++ FE

%prep

%setup -n libmesh-%{version}

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

export COPTFLAGS="-g %{TACC_OPT} -O2"

module load boost python%{python_version}
%if "%{use_petsc}" == "1"
module load petsc/%{petscversion}
%endif
%if "%{use_trilinos}" == "1"
module load trilinos/%{trilinosversion}
export TRILINOS_CONFIGURE_STRING=--with-trilinos=${TACC_TRILINOS_DIR:?NO_TRILINOS_DIR}
%endif

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

##
## start of configure install loop
##

export LIBMESH_HOME=%{_topdir}/BUILD
export softdir=%{_topdir}/SPECS

export LIBMESH_VERSION=%{version}
export LIBMESH_DIR=${LIBMESH_HOME}/libmesh-${LIBMESH_VERSION}
export LIBMESH_BUILD=${LIBMESH_HOME}/build-${LIBMESH_VERSION}
export LIBMESH_INSTALLATION=%{INSTALL_DIR}
export LIBMESH_BIN=${LIBMESH_INSTALLATION}/bin

%if "%{comp_fam}" == "intel"
# ./include/libmesh/fe_abstract.h(443): error: more than one operator "+" matches these operands:
#             built-in operator "arithmetic + arithmetic"
#             function "operator+(const PetscInt={int} &, const PetscComplex &)"
#             operand types are: const libMesh::OrderWrapper + const unsigned int
#     Order get_order()  const { return static_cast<Order>(fe_type.order + _p_level); }
sed -i src/fe/fe.C \
    -e 's/this->fe_type.order +/static_cast<unsigned int>(this->fe_type.order) +/'
sed -i src/fe/fe_base.C \
    -e 's/(fe_type.order +/(static_cast<unsigned int>(fe_type.order) +/' \
    -e 's/(temp_fe_type.order +/(static_cast<unsigned int>(temp_fe_type.order) +/'

for f in include/fe/fe_abstract.h \
         src/systems/system_projection.C \
         include/systems/generic_projector.h \
         src/error_estimation/patch_recovery_error_estimator.C \
         src/error_estimation/weighted_patch_recovery_error_estimator.C ; do 
  sed -i $f \
    -e 's/fe_type.order +/static_cast<unsigned int>(fe_type.order) +/'
done
sed -i src/base/dof_map.C \
    -e 's/- base_fe_type.order/- static_cast<unsigned int>(base_fe_type.order)/' \
    -e 's/+ base_fe_type.order/+ static_cast<unsigned int>(base_fe_type.order)/'
for f in src/fe/fe_hierarchic_shape_1D.C src/fe/fe_bernstein_shape_1D.C \
        src/fe/fe_lagrange_shape_1D.C src/fe/fe_lagrange_shape_2D.C src/fe/fe_lagrange_shape_3D.C \
        src/fe/fe_monomial_shape_1D.C src/fe/fe_monomial_shape_2D.C src/fe/fe_monomial_shape_3D.C \
	; do
  sed -i $f \
    -e 's/(fet.order +/(static_cast<unsigned int>(fet.order) +/'
done
sed -i src/fe/fe_interface.C \
    -e 's/(fe_t.order +/(static_cast<unsigned int>(fe_t.order) +/'
sed -i src/fe/fe_interface.C \
    -e 's/(p_refined_fe_t.order +/(static_cast<unsigned int>(p_refined_fe_t.order) +/'
for f in src/fe/fe_szabab_shape_1D.C \
         src/fe/fe_subdivision_2D.C \
         ; do \
    sed -i $f \
      -e 's/(fet.order +/(static_cast<unsigned int>(fet.order) +/' \
      -e 's/(fet.order+/(static_cast<unsigned int>(fet.order) +/'
done
%endif

rm -rf /tmp/libmesh-build
mkdir -p /tmp/libmesh-build
pushd /tmp/libmesh-build

if [ "$TACC_FAMILY_PYTHON" = "python2" ] ; then
  export PYLIB=${TACC_PYTHON_LIB}/libpython${TACC_PYTHON_VER:=2.7}.so
else
  export TACC_PYTHON_LIB=$TACC_PYTHON_LIB
  export PYLIB=${TACC_PYTHON_LIB}/libpython${TACC_PYTHON_VER:=3.7}m.so
fi
if [ ! -f $PYLIB ] ; then
  echo "Could find pylib=$PYLIB" 
  exit 1
fi
export LIBS=${PYLIB}
export libmesh_LDFLAGS=$PYLIB
#"${TACC_PYTHON_LIB:?NO_PYTHON_LIB}/libpython${TACC_PYTHON_VER}.so"

CXX=mpicxx \
CC=mpicc \
${LIBMESH_DIR}/configure --prefix=${LIBMESH_INSTALLATION} \
    ${TRILINOS_CONFIGURE_STRING} \
    --with-boost=${TACC_BOOST_DIR} \
    --enable-parmesh --disable-metaphysicl \
    --enable-fortran --enable-dirichlet --enable-nodeconstraint \
    2>&1 | tee ${softdir}/configure.log

###./configure --enable-mpi --enable-fortran --enable-exceptions --enable-amr --enable-vsmoother --enable-periodic  --enable-parmesh --enable-ghosted --enable-pfem  --enable-ifem   --enable-examples  --enable-petsc   --enable-trilinos --enable-slepc --enable-boost --enable-laspack --enable-bzip2 --enable-tecio --enable-tecplot --enable-parmetis --enable-tetgen --enable-triangle --enable-vtk --enable-eigen --enable-glpk --enable-netcdf --enable-exodus --enable-nemesis --enable-fparser --with-cxx=g++ --with-fc=gfortran --with-cc=gcc MPI_INCLUDES_PATH=${PETSC_DIR}/${PETSC_ARCH}/include MPI_LIBS_PATH=${PETSC_DIR}/${PETSC_ARCH}/lib

make -j 8 2>&1 | tee ${softdir}/make.log

# small sanity check
make check -C examples SUBDIRS=introduction/introduction_ex1 || /bin/true

make install
# this should be fixed in 1.3.1
#sed -i -e '/make_dependencies/s/@/-@/' ${LIBMESH_INSTALLATION}/contrib/utils/Makefile.in

popd

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
The libmesh module defines the following environment variables:
TACC_LIBMESH_DIR, TACC_LIBMESH_BIN, and
TACC_LIBMESH_LIB for the location
of the Libmesh distribution, documentation, binaries,
and libraries.

Version %{version}
external packages installed: ${libmesh_extra_libs}
]] )

whatis( "Name: Libmesh" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://github.com/libMesh" )
whatis( "Description: C++ Finite Element Library" )

local             libmesh_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(libmesh_dir,libmesh_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(libmesh_dir,libmesh_arch,"lib") )

setenv("TACC_LIBMESH_DIR",        libmesh_dir)
setenv("TACC_LIBMESH_BIN",        pathJoin(libmesh_dir,libmesh_arch,"bin") )
setenv("TACC_LIBMESH_INC",        pathJoin(libmesh_dir,libmesh_arch,"include") )
setenv("TACC_LIBMESH_LIB",        pathJoin(libmesh_dir,libmesh_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module1.0#################################################
##
## version file for Libmesh %version
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
* Tue Mar 09 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
