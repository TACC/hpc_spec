Summary: Libmesh install

# Give the package a base name
%define pkg_base_name libmesh
%define MODULE_VAR    LIBMESH

# Create some macros (spec file variables)
%define major_version git20181008
%define minor_version 0
%define micro_version 0

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
Source: %{pkg_base_name}-%{pkg_version}.tgz
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

module load boost python

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

rm -rf /tmp/libmesh-build
mkdir -p /tmp/libmesh-build
pushd /tmp/libmesh-build

export PYLIB=${TACC_PYTHON_LIB}/libpython2.7.so

export LIBS=${PYLIB} ; \
export libmesh_LDFLAGS="${TACC_PYTHON_LIB}/libpython2.7.so"
${LIBMESH_DIR}/configure --prefix=${LIBMESH_INSTALLATION} \
    --with-trilinos=${TACC_TRILINOS_DIR} \
    --with-boost=${TACC_BOOST_DIR} \
    2>&1 | tee ${softdir}/configure.log

make 2>&1 | tee ${softdir}/make.log
make install

echo "are we still in /tmp/libmesh-build?"
pwd
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
* Mon Oct 08 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
