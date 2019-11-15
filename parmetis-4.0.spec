#
# $Id: parmetis.spec,v 1.5 2007/05/29 14:15:00 karl Exp $
#
 
Summary: Local ParMETIS binary install
 
%define name_prefix tacc
%define base_name pmetis

#
#
#

Name: %{name_prefix}-%{base_name}
Version: 4.0.3
Release: 1
License: GPL
Vendor: George Karypis
Group: System Environment/Base
Source: parmetis-%{version}.tar.gz
Packager: TACC - mclay@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles
%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{base_name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{base_name}
 
%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: parmetis 4.0
Group: System Environment/Base

%description 
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
ParMETIS is an MPI-based parallel library that implements a variety of
algorithms for partitioning unstructured graphs, meshes, and for
computing fill-reducing orderings of sparse matrices. ParMETIS extends
the functionality provided by METIS and includes routines that are
especially suited for parallel AMR computations and large scale
numerical simulations. The algorithms implemented in ParMETIS are
based on the parallel multilevel k-way graph-partitioning, adaptive
repartitioning, and parallel multi-constrained partitioning schemesl.


%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
 
##
## SETUP
##
%setup -n parmetis-%{version}
 
##
## BUILD
##
%build

%include compiler-load.inc
%include mpi-load.inc

%if "%{mpi_fam}" != "none"
   CC=mpicc
   CXX=mpicxx
   FC=mpif90
   F77=mpif77
   F90=$FC
   PARALLEL="--enable-parallel"
%endif


%if "%{mpi_fam}" == "impi"
   CC=mpiicc
   CXX=mpiicxx
   FC=mpiifort
   F77=mpiifort
   F90=$FC
   PARALLEL="--enable-parallel"
%endif


export CFLAGS="-O3 -fPIC"
export FFLAGS="-O3 -fPIC"
echo CC=$CC


# must have make 3.81 which is a module on ranger but
# is installed on the lonestar and newer.
module try-add gmake
module load cmake 

module list

gmake --version
cmake --version

METIS_H=metis/include/metis.h

cp  $METIS_H ${METIS_H}.orig
cat ${METIS_H}.orig | sed -e 's/REALTYPEWIDTH 32/REALTYPEWIDTH 64/' > $METIS_H

make config cc=$CC prefix=%{INSTALL_DIR}
make
make install DESTDIR=$RPM_BUILD_ROOT
make distclean
make config shared=1 cc=$CC prefix=%{INSTALL_DIR} 
make

%install

make install DESTDIR=$RPM_BUILD_ROOT
cp metis/include/metis.h $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/manual
cp manual/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/manual


rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The pmetis module defines the following environment variables:
TACC_PMETIS_DIR, TACC_PMETIS_DOC, TACC_PMETIS_BIN, 
TACC_PMETIS_LIB, and TACC_PMETIS_INC for the location
of the ParMetis distribution, documentation, binaries,
libraries, and include files.


To use the parmetis library, include compilation and link directives
of the form: -L$TACC_PMETIS_LIB -I$TACC_PMETIS_INC -lparmetis -lmetis

Here is an example command to compile pmetis_test.c:

icc -I$TACC_PMETIS_INC pmetis_test.c -L$TACC_PMETIS_LIB -lparmetis

Version %{version}
]]

help(help_message,"\n")

whatis("Name: ParMETIS: Parallel Graph Partitioning")
whatis("Version: %{version}")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Parallel, Mathematics, Graph Partitioning")
whatis("Description: Parallel graph partitioning and fill-reduction matrix ordering routines")
whatis("URL: http://glaros.dtc.umn.edu/gkhome/views/metis")
whatis("Packager: %{packager}")

local pmetis_dir = "%{INSTALL_DIR}"

setenv(      "TACC_PMETIS_DIR", pmetis_dir)
setenv(      "TACC_PMETIS_BIN", pathJoin(pmetis_dir,"bin"))
setenv(      "TACC_PMETIS_DOC", pathJoin(pmetis_dir,"manual"))
setenv(      "TACC_PMETIS_INC", pathJoin(pmetis_dir,"include"))
setenv(      "TACC_PMETIS_LIB", pathJoin(pmetis_dir,"lib"))

prepend_path("PATH",            pathJoin(pmetis_dir,"bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin(pmetis_dir,"lib"))
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for %{base_name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(755,root,install)


%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
