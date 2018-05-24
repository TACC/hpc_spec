#
# $Id: mvapich2-2.3b 2017-09-01 13:29:50 Jerome $
#
%define myversion 2.3

%if "%{is_debug}" == "1"
   %define dbg -dbg
   %define pkg_version %{myversion}_dbg
%else
   %define dbg %{nil}
   %define pkg_version %{myversion}
%endif

Summary: OSU MVAPICH2 MPI implementation
Name:    mvapich2
Version: 2.3rc1
Release: 2%{?dist}
License: BSD License
Group:   Development/Libraries
Packager: TACC - viennej@tacc.utexas.edu
Source: http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.3rc1.tar.gz 
BuildRoot: /var/tmp/%{name}-%{version}-root

#---------------------------------------------------------------------------
# Changelog
#---------------------------------------------------------------------------


%define mpi_fam mvapich2
%define mpi_fam_ver mvapich2-2_3rc1

%include rpm-dir.inc
%include compiler-defines.inc

# local config takes precedent over includes above

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{pkg_version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define SUBMODULES  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}

%define __spec_install_post /usr/lib/rpm/brp-compress
%define __spec_install_post /usr/lib/rpm/brp-strip
%define debug_package %{nil}

%package -n %{name}-%{comp_fam_ver}%{dbg}
Summary: OSU MPI-3 implementation
Group: Development/Libraries

%description
%description -n %{name}-%{comp_fam_ver}%{dbg}
MVAPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.
MVAPICH includes all of the routines in MPI 3.1.
MVAPICH is developed at the Ohio State University. See whttp://mvapich.cse.ohio-state.edu/

%prep

%setup -n mvapich2-%{version}  mvapich2-%{version}
##
## BUILD
##

%build

echo pkg_version: -%{pkg_version}-
echo dbg:         -%{dbg}-

%include compiler-defines.inc
%include compiler-load.inc
module load intel/17.0.4
module list

export MPIINSTALL_OPTS="-noman"
export RSHCOMMAND=ssh

# We will define an extra variable to decide what gets
# removed from the final mpi wrappers.

export CFLAGS=" "
export CFLAGS_TACC_BUILD_ONLY="-pipe"
export CXXFLAGS=$CFLAGS
export FFLAGS=$CFLAGS
export FCFLAGS=$FFLAGS

%if "%{comp_fam}" == "intel"

  export CFLAGS="$CFLAGS -Wl,-rpath,$IFC_LIB -Wl,-rpath,$ICC_LIB"
#  export CFLAGS="$CFLAGS -Wl,-rpath,$IFC_LIB -Wl,-rpath,$ICC_LIB -i-dynamic"
  export CFLAGS_TACC_BUILD_ONLY="$CFLAGS_TACC_BUILD_ONLY -fno-strict-aliasing"
  export FFLAGS_TACC_BUILD_ONLY=$CFLAGS_TACC_BUILD_ONLY

  export CXXFLAGS=$CFLAGS
  export FFLAGS=$CFLAGS
  export FCFLAGS=$FFLAGS

%endif

%if "%{comp_fam}" == "gcc"
  export LDFLAGS="$LDFLAGS -Wl,-rpath,$GCC_LIB"
  export CFLAGS_TACC_BUILD_ONLY="$CFLAGS_TACC_BUILD_ONLY"
  export FFLAGS_TACC_BUILD_ONLY=$CFLAGS_TACC_BUILD_ONLY

  export CXXFLAGS=$CFLAGS
  export FFLAGS=$CFLAGS
  export FCFLAGS=$FFLAGS

%endif

# Add the BUILD_ONLY flags into default flags; will be removed
# from mpi wrapper scripts after the build is complete.

export CFLAGS="$CFLAGS $CFLAGS_TACC_BUILD_ONLY"
export FFLAGS="$FFLAGS $FFLAGS_TACC_BUILD_ONLY"
export CXXFLAGS="$CXXFLAGS $CFLAGS_TACC_BUILD_ONLY"

OPT_LEVEL="--enable-fast=O3"
DEBUG_OPTIONS="--enable-g=dbg"
%if "%{is_debug}" == "1"
  module load valgrind
  OPT_LEVEL="--disable-fast"
  DEBUG_OPTIONS="--enable-g=dbg,mem,meminit --with-valgrind=$TACC_VALGRIND_INC --enable-debuginfo  --enable-error-messages=all"
%endif

INSTALL_DIR=%{INSTALL_DIR}


# Removed from config:
# --enable-sharedlibs=gcc  --enable-shared

./configure --prefix=$INSTALL_DIR   \
        --with-device=ch3:psm  \
        --with-ch3-rank-bits=32	\
	--enable-cxx --enable-romio \
        $OPT_LEVEL                  \
        $DEBUG_OPTIONS               \
        --with-file-system=lustre     \

make -j 16


###
### INSTALL
###

%install

%include compiler-load.inc
module load intel/17.0.4

make DESTDIR=$RPM_BUILD_ROOT install

export CFLAGS_TACC_BUILD_ONLY="-pipe -fno-strict-aliasing"
export FFLAGS_TACC_BUILD_ONLY=$CFLAGS_TACC_BUILD_ONLY
for i in $CFLAGS_TACC_BUILD_ONLY $FFLAGS_TACC_BUILD_ONLY; do
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
done


# Add the appropriate module files.

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}%{dbg} << 'EOF'
#%Module1.0#####################################################################
##
## MVAPICH2
##
proc ModulesHelp { } {
global version MPICHhome

puts stderr " "
puts stderr "Mvapich2 2.3RC1 "
puts stderr " " 
puts stderr "This module loads the MVAPICH2 MPI environment built with"
puts stderr "%{comp_fam_name} compilers. By loading this module, the following commands"
puts stderr "will be automatically available for compiling MPI applications:"
puts stderr "\n"
puts stderr "mpif77       (F77 source)"
puts stderr "mpif90       (F90 source)"
puts stderr "mpicc        (C   source)"
puts stderr "mpiCC/mpicxx (C++ source)"
puts stderr "\n"
puts stderr "Version $version\n"
}

module-whatis "MVAPICH2"
module-whatis "Version: %{version}"
module-whatis "Category: library, runtime support"
module-whatis "Keywords: System, Library"
module-whatis "Description: MPI-3.1 implementation for Infiniband"
module-whatis "URL: http://mvapich.cse.ohio-state.edu/overview/mvapich2/"

# for Tcl script use only
set     version         %version
set     MPICHhome       %{INSTALL_DIR}

# Export to User.

setenv MPICH_HOME       $MPICHhome
setenv TACC_MPI_GETMODE mvapich2_ssh


prepend-path    PATH            $MPICHhome/bin
prepend-path    MANPATH         $MPICHhome/share/man
prepend-path    INFOPATH        $MPICHhome/doc
prepend-path    LD_LIBRARY_PATH $MPICHhome/lib/shared

prepend-path    LD_LIBRARY_PATH $MPICHhome/lib

prepend-path    MODULEPATH      %{SUBMODULES}
prepend-path    PKG_CONFIG_PATH $MPICHhome/lib/pkgconfig

%if "%{is_debug}" == "1"
setenv  MPICH_TRMEM_VALIDATE YES
setenv  MPICH_TRMEM_INITZERO YES
%endif

family "MPI"

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version}%{dbg} << 'EOF'
#%Module1.0#################################################
##
## version file for MVAPICH %version for intel
##

set     ModulesVersion      "%version"
EOF

##
## FILES
##

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}%{dbg}

%files -n %{name}-%{comp_fam_ver}%{dbg}
%{INSTALL_DIR}
%{MODULE_DIR}

#%postun

##
## CLEAN
##
%clean
rm -rf $RPM_BUILD_ROOT
#
