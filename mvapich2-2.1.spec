#
# $Id: mvapich2-2.1.spec 1656 2014-11-26 15:29:50Z carlos $
#
# Release 5 - using barebones intel 15.0.0 to avoid issues with C++11 dependencies
#
# Release 2 - using modulefile for intel 15.0.2 that includes ICC_LIB corectly
# version used for install path

%define myversion 2.1

%if "%{is_debug}" == "1"
   %define dbg -dbg
   %define pkg_version %{myversion}_dbg
%else
   %define dbg %{nil}
   %define pkg_version %{myversion}
%endif

Summary: OSU MVAPICH2 MPI implementation
Name:    mvapich2
Version: 2.1
Release: 5
License: freely distributable
Group:   Development/Libraries
Source:  mvapich2-%{version}.tar.gz
Packager: TACC - karl@tacc.utexas.edu, mclay@tacc.utexas.edu, carlos@tacc.utexas.edu, viennej@tacc.utexas.edu

BuildRoot: %{_tmppath}/%{name}-%{version}-root

#---------------------------------------------------------------------------
# Changelog
# * [4/5/2013] Making a hecura build with profile patch from Krishna applie
#---------------------------------------------------------------------------

%define mpi_fam mvapich2
%define mpi_fam_ver mvapich2_2_1

%include rpm-dir.inc
%include compiler-defines.inc

# local config takes precedent over includes above

%define APPS /opt/apps
%define MODULES modulefiles
%define OFED_DIR    /usr
%define with_cma 1

%if "%{is_intel15}" == "1"
  %define comp_fam intel
  %define comp_fam_ver intel15
  %define comp_fam_name Intel
%endif


%define __spec_install_post /usr/lib/rpm/brp-compress
%define __spec_install_post /usr/lib/rpm/brp-strip
%define debug_package %{nil}

%package -n %{name}-%{comp_fam_ver}%{dbg}
Summary: OSU IB MPI-2 implementation
Group: Development/Libraries

%description
%description -n %{name}-%{comp_fam_ver}%{dbg}
MPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.
MPICH includes all of the routines in MPI 1.2, along with the I/O routines
from MPI-2 and some additional routines from MPI-2, including those supporting
MPI Info and some of the additional datatype constructors.  MPICH  was
developed by Argonne National Laboratory. See www.mcs.anl.gov/mpi/mpich for
more information.

%prep

%setup -n mvapich2-%{version}  mvapich2-%{version}

##
## BUILD
##

%build

echo pkg_version: -%{pkg_version}-
echo dbg:         -%{dbg}-

%include system-load.inc
%include compiler-load.inc

# There is no intel 15.0.0 installed here, so I am hacking this in
# from the installation in my account - CRF 2015.06.23 
%if "%{is_intel15}" == "1"

module unload intel
module list
source ~carlos/intel/composer_xe_2015.0.090/bin/iccvars.sh intel64
source ~carlos/intel/composer_xe_2015.0.090/bin/ifortvars.sh intel64
which icc
which ifort
export CC=icc
export CXX=icpc
export FC=ifort
export F77=ifort
export ICC_LIB=~carlos/intel/composer_xe_2015.0.090/lib/intel64
export IFC_LIB=~carlos/intel/composer_xe_2015.0.090/lib/intel64

%define comp_fam intel
%define comp_fam_ver intel15
%define comp_fam_name Intel

%endif

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{pkg_version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define SUBMODULES  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}

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

%if "%{is_sun}" == "1"

  export FLDFLAGS="-L$TACC_SUN_LIB -Wl,-rpath,$TACC_SUN_LIB"
  export CLDFLAGS="-Wl,-rpath,$TACC_SUN_LIB"

  export CLINKER="$CC $IBLDFLAGS $CLDFLAGS"
  export CCLINKER="$CXX $IBLDFLAGS $CLDFLAGS"
  export FLINKER="$FC $IBLDFLAGS $FLDFLAGS"
  export F90LINKER="$F90 $IBLDFLAGS $FLDFLAGS"

  export CFLAGS="$CFLAGS "
  export CXXFLAGS="$CXXFLAGS "
%endif

%if "%{is_pgi10}" == "1"

#  export CFLAGS_TACC_BUILD_ONLY="-Msignextend -DPGI -B $CFLAGS_TACC_BUILD_ONLY"
  export CFLAGS_TACC_BUILD_ONLY="-Msignextend -DPGI $CFLAGS_TACC_BUILD_ONLY"
  export FFLAGS_TACC_BUILD_ONLY="-Msignextend -DPGI $CFLAGS_TACC_BUILD_ONLY"

%endif


export LDFLAGS="$LDFLAGS -Wl,-rpath,%{OFED_DIR}/lib64 -L%{OFED_DIR}/lib64"

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

# jv 12/03/14
# removed —-with-rdma=gen2 because it is a default value
# removed --with-cma because it is a default value
# added --enable-hybrid to support hybrid mode (RC/UD)

./configure --prefix=$INSTALL_DIR   \
        --with-ib-libpath=%{OFED_DIR}/lib64/         \
        --with-ib-include=%{OFED_DIR}/include/       \
        --enable-cxx --enable-romio                  \
        $OPT_LEVEL                                   \
        $DEBUG_OPTIONS                               \
        --enable-sharedlibs=gcc  --enable-shared     \
        --with-ch3-rank-bits=32                      \
        --with-file-system=lustre                    \
        --enable-mcast                               \
        --enable-hybrid


# adio with new mpich is broken (ks 12/9/13)
#        --with-file-system=lustre                    \
#       --enable-cuda --with-cuda=/opt/apps/cuda/5.0/ \
#       --enable-hybrid
#        --with-pm=no --with-pmi=slurm
#        --disable-weak-symbols \
#       --with-limic2-include=%{limic_dir}/include \
#       --with-limic2-libpath=%{limic_dir}/lib  \

# Disabling lustre-specific adio to avoid corruption (ks 4/1/2011)
# Disabling hybrid (rtm 1/30/2013)

make -j 4


###
### INSTALL
###

%install

%include system-load.inc
%include compiler-load.inc

# There is no intel 15.0.0 installed here, so I am hacking this in
# from the installation in my account - CRF 2015.06.23 
%if "%{is_intel15}" == "1"

module unload intel
module list
source ~carlos/intel/composer_xe_2015.0.090/bin/iccvars.sh intel64
source ~carlos/intel/composer_xe_2015.0.090/bin/ifortvars.sh intel64
which icc
which ifort
export CC=icc
export CXX=icpc
export FC=ifort
export F77=ifort
export ICC_LIB=~carlos/intel/composer_xe_2015.0.090/lib/intel64
export IFC_LIB=~carlos/intel/composer_xe_2015.0.090/lib/intel64

%define comp_fam intel
%define comp_fam_ver intel15
%define comp_fam_name Intel
%endif

make DESTDIR=$RPM_BUILD_ROOT install

export CFLAGS_TACC_BUILD_ONLY="-pipe -fno-strict-aliasing"
export FFLAGS_TACC_BUILD_ONLY=$CFLAGS_TACC_BUILD_ONLY
for i in $CFLAGS_TACC_BUILD_ONLY $FFLAGS_TACC_BUILD_ONLY; do
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
done

# Fix for Intel11 to avoid feupdateenv warning

%if "%{is_intel13}" == "1"

   perl -pi -e 's/^WRAPPER_LDFLAGS=\"(.+)\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
   perl -pi -e 's/^WRAPPER_LDFLAGS=\"(.+)\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
   perl -pi -e 's/^WRAPPER_LDFLAGS=\"(.+)\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
   perl -pi -e 's/^WRAPPER_LDFLAGS=\"(.+)\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90

##    perl -pi -e 's/^WRAPPER_LDFLAGS=\"\s+(\S+)\s+\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
##    perl -pi -e 's/^WRAPPER_LDFLAGS=\"\s+(\S+)\s+\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
##    perl -pi -e 's/^WRAPPER_LDFLAGS=\"\s+(\S+)\s+\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
##    perl -pi -e 's/^WRAPPER_LDFLAGS=\"\s+(\S+)\s+\"/WRAPPER_LDFLAGS=\"$1 -limf\"/' $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90

%endif



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
module-whatis "Description: MPI-2 implementation for Infiniband"
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

#JV added the 12/03/2014
# by default bcast optimizations are disabled due to a bug in 1.9a
# the following command re-enable these optimizations
setenv MV2_USE_OLD_BCAST 0


#JV added the 04/16/2015
# by default UD is enable with -enable-hybrid
# the following command disable this option to use only RC
setenv MV2_USE_UD_HYBRID 0

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

