#
# Spec file for Arpack
#
Summary: Arpack (including PArpack) local binary install

%define pkg_base_name arpack
%define MODULE_VAR ARPACK

%define major_version 3
%define minor_version 7
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

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
License: GPL
Vendor: https://github.com/opencollab/arpack-ng
# used to be: http://forge.scilab.org/index.php/p/arpack-ng/
Group: System Environment/Base
Source: arpack-ng_%{version}.tar.gz
## Patch1: arpack-3.0.2.patch
Packager: eijkhout@tacc.utexas.edu

%define debug_package %{nil}
%global _python_bytecompile_errors_terminate_build 0

#---------------------------------------
%package %{PACKAGE}
#---------------------------------------
Summary: Arpack (including PArpack) local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Arpack (including PArpack) local binary install
Group: System Environment/Base

#---------------------------------------
%description
#---------------------------------------
%description %{PACKAGE}
ARPACK is a collection of Fortran77 subroutines designed to solve large scale eigenvalue problems.
%description %{MODULEFILE}
ARPACK is a collection of Fortran77 subroutines designed to solve large scale eigenvalue problems.

#---------------------------------------
%prep
#---------------------------------------
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

#---------------------------------------
%setup -n arpack-ng-%{version}
#---------------------------------------
##%patch1 -p0

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

export LIBRARY_PATH=$TACC_MKL_LIB
%if "%{comp_fam}" == "intel"
  CFLAGS="-O3 -fPIC"
  FFLAGS="-O3 -fPIC"
%endif

%if "%{comp_fam}" == "intel"
  BLASLIB="-Wl,-rpath,$TACC_MKL_LIB -L$TACC_MKL_LIB -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread -lm"
  LAPACKLIB=$BLASLIB
%endif

%if "%{comp_fam}" == "gcc"
  %define NOT_USING_INTEL 1
  module load mkl
  BLASLIB="-Wl,-rpath,$TACC_MKL_LIB -L$TACC_MKL_LIB -lmkl_gf_lp64 -lmkl_sequential -lmkl_core -lpthread -lm"
  LAPACKLIB=$BLASLIB
%endif


%if "%{comp_fam}" == "pgi"
  CFLAGS="-O3 -tp barcelona-64 -fPIC"
  FFLAGS="-O3 -tp barcelona-64 -fPIC"
%endif


module load autotools

CFLAGS="$CFLAGS" FFLAGS="$FFLAGS" ./configure --prefix=%{INSTALL_DIR} --with-blas="$BLASLIB" --with-lapack="$LAPACKLIB" --enable-mpi
make

#### %include mpi-env-vars.inc

make DESTDIR=$RPM_BUILD_ROOT install



cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
The ARPACK modulefile defines the following environment variables:
TACC_ARPACK_DIR, TACC_ARPACK_LIB, and TACC_ARPACK_INC 
for the location of the ARPACK %{version} distribution, and 
libraries respectively.

Add the following options to the link step:

      -Wl,-rpath,$TACC_ARPACK_LIB -L$TACC_ARPACK_LIB -larpack

This is a fortran 77 library. It has no include files.

Version %{version}
]])

whatis("ARPACK/PARPACK: Arnoldi package")
whatis("Version: %{version}")
whatis("Category: library, mathematics")
whatis("Keywords: library, mathematics")
whatis("Description: eigenvalue computations based on restarted Arnoldi method")
whatis("URL: http://www.caam.rice.edu/software/ARPACK/")


-- Create environment variables.

local arpack_dir="%{INSTALL_DIR}"

setenv(          "TACC_ARPACK_DIR",      arpack_dir)
setenv(          "TACC_ARPACK_LIB",      pathJoin(arpack_dir,"lib"))

--  Append path


prepend_path(    "LD_LIBRARY_PATH",      pathJoin(arpack_dir,"lib"))

%if "%{NOT_USING_INTEL}" == "1"
prereq("mkl")
%endif
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{pkg_name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(755,build,install)
%{INSTALL_DIR}
%{MODULE_DIR}


%post
%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Apr 22 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release

