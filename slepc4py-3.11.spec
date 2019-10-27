#
# Spec file for Slepc4py
#

Summary: Slepc4py install

# Give the package a base name
%define pkg_base_name slepc4py
%define MODULE_VAR    SLEPC4PY

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 11

# package version is the slepc version
%define pkg_version %{major_version}.%{minor_version}
# source tarball has patch level in it; we ignore this.
%define wgetversion 3.11.0

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include python-defines.inc

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

Release: 1%{?dist}
License: GPL
Vendor: Lisandro Dalcin
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
URL: https://bitbucket.org/slepc/slepc4py/
Source0: %{pkg_base_name}-%{wgetversion}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Slepc4py local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Slepc4py local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
SLEPC4PY is the python interface to slepc
%description %{MODULEFILE}
SLEPC4PY is the python interface to slepc

%prep 

%setup -n slepc4py-%{wgetversion}

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
%include python-defines.inc

%include compiler-load.inc
%include mpi-load.inc
%include python-load.inc

echo %{PYTHON_INSTALL_DIR}
if [ -z "%{PYTHON_INSTALL_DIR}" ] ; then
  echo "No PYTHON INSTALL DIR defined"
  exit 1
fi

module avail slepc

export SLEPC4PY_DIR=`pwd`
rm -rf $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}
echo "tmpfs on python install dir: %{PYTHON_INSTALL_DIR}"
mount -t tmpfs tmpfs %{PYTHON_INSTALL_DIR}

export LIBDIRNAME="lib"
# %if "%{comp_fam}" == "intel"
#   export LIBDIRNAME="lib64"
# %endif

export PYTHONDIRNAME=%{python_fam}%{python_major_version}.%{python_minor_version}
export PYTHONPROG=%{python_fam}%{python_major_version}

# PYTHONPATH : 
# pathJoin( %{PYTHON_INSTALL_DIR},"${LIBDIRNAME}","python${TACC_PYTHON_VER}","site-packages") )

# same extensions as in slepc
export dynamiccc="i64 debug i64debug complexi64 complexi64debug uni unidebug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

export noext="\
  "

for ext in \
  "" \
  single ${dynamiccc} ${dynamiccxx} \
  ; do

export architecture=skylake
if [ -z "${ext}" ] ; then
  export moduleversion=%{version}
else
  export architecture=${architecture}-${ext}
  export moduleversion=%{version}-${ext}
fi
module unload petsc slepc petsc4py
module load petsc/${moduleversion} slepc/${moduleversion} 
module use /opt/apps/intel18/impi18_0/python%{python_major_version}_%{python_minor_version}/modulefiles
module load petsc4py/${moduleversion}

# where are we installing?
export PREFIXDIR=%{PYTHON_INSTALL_DIR}/${architecture}
# or should that be
#export PREFIXDIR=${RPM_BUILD_DIR}/%{PYTHON_INSTALL_DIR}

pwd

${PYTHONPROG} setup.py build
echo "installing in prefix: ${PREFIXDIR}"
${PYTHONPROG} setup.py install --prefix=${PREFIXDIR}
echo "just checking:"
ls ${PREFIXDIR}
ls ${PREFIXDIR}/lib
ls ${PREFIXDIR}/${LIBDIRNAME}

mkdir -p              $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/${architecture}
cp -r ${PREFIXDIR}/*  $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/${architecture}/

## Module files for slepc4py

mkdir -p %{PYTHON_MODULE_DIR}

echo "writing module file for python ${TACC_PYTHON_VER}, slepc ${moduleversion}"

cat > $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/${moduleversion}.lua << EOF
help( [[
The SLEPC4PY modulefile defines the following environment variables:
TACC_SLEPC4PY_DIR
for the location of the SLEPC4PY %{version} distribution;
it also updates PYTHONPATH.

Version ${moduleversion}
]] )

whatis( "Name: Slepc4py" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${moduleversion}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://bitbucket.org/slepc/slepc4py/" )
whatis( "Description: python interface to Slepc" )

local             slepc_arch =    "${architecture}"
local             slepc4py_dir =     "%{PYTHON_INSTALL_DIR}"

prepend_path("PYTHONPATH", pathJoin(slepc4py_dir,"${architecture}","${LIBDIRNAME}","python${TACC_PYTHON_VER}","site-packages") )

setenv(          "TACC_SLEPC4PY_DIR",        slepc4py_dir)

depends_on("petsc/${moduleversion}")
depends_on("petsc4py/${moduleversion}")
depends_on("slepc/${moduleversion}")
EOF

cat > $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/.version.${moduleversion} << EOF
#%Module1.0##################################################
##
## version file for slepc4py
##
 
set     ModulesVersion      "${moduleversion}"
EOF

###%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{modulefileroot}/${moduleversion}.lua

done

cp -r demo docs ${LIBDIR} src test *.rst  $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/

umount %{PYTHON_INSTALL_DIR}

%files %{PACKAGE}
  %defattr(755,root,install)
  %{PYTHON_INSTALL_DIR}

%files %{MODULEFILE}
  %defattr(755,root,install)
  %{PYTHON_MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jun 20 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial build
