#
# $Id: metis.spec 949 2012-01-27 17:24:06Z karl $
#
 
Summary: Local METIS binary install
 
%define name_prefix tacc
%define base_name metis5

#
#
#

Name: %{name_prefix}-%{base_name}
Version: 5.0.2
Release: 2
License: University of Minnesota
Vendor: George Karypis
Group: System Environment/Base
Source: metis-%{version}.tar.gz
Packager: TACC - mclay@tacc.utexas.edu
BuildRoot: %{_tmppath}/%{base_name}-%{version}-%{release}-root

%define debug_package %{nil}
%include rpm-dir.inc
%include compiler-defines.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define PNAME       metis
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{PNAME}

%package -n %{name}-%{comp_fam_ver}
Summary: Local METIS binary install
Group:   applications

%description
%description -n %{name}-%{comp_fam_ver}

METIS is a set of serial programs for partitioning graphs,
partitioning finite element meshes, and producing fill reducing
orderings for sparse matrices. The algorithms implemented in METIS are
based on the multilevel recursive-bisection, multilevel k-way, and
multi-constraint partitioning schemes.

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
 
##
## SETUP
##

%setup -n metis-%{version}
 
##
## BUILD
##

%build

%include compiler-load.inc

module load cmake

cmake --version

cp  include/metis.h include/metis.h.orig
cat include/metis.h.orig | sed -e 's/REALTYPEWIDTH 32/REALTYPEWIDTH 64/' > include/metis.h

make config shared=1 cc=$CC prefix=%{INSTALL_DIR}
make
 
%install

make install DESTDIR=$RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/manual
cp manual/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/manual

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[
The metis modulefile defines the following environment variables:
TACC_METIS_DIR, TACC_METIS_DOC, TACC_METIS_BIN, TACC_METIS_LIB, 
and TACC_METIS_INC for the location of the Metis distribution, 
documentation, binaries, libraries, and include files, respectively.

To use the metis library, include compilation directives
of the form: -L$TACC_METIS_LIB -I$TACC_METIS_INC -lmetis

An example command to compile metis_test.c is as follows:

icc -I$TACC_METIS_INC metis_test.c -L$TACC_METIS_LIB -lmetis"

Version %{version}
]]
)

whatis("Name: METIS: Multilevel Partitioning Algorithms")
whatis("Version: %{version}")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics")
whatis("Description: Serial graph partitioning and fill-reduction matrix ordering routines")
whatis("URL: http://glaros.dtc.umn.edu/gkhome/views/metis")
whatis("Packager: %{packager}")


setenv(         "TACC_METIS_DIR",        "%{INSTALL_DIR}")
setenv(         "TACC_METIS_BIN",        "%{INSTALL_DIR}/bin")
setenv(         "TACC_METIS_DOC",        "%{INSTALL_DIR}/manual")
setenv(         "TACC_METIS_LIB",        "%{INSTALL_DIR}/lib")
setenv(         "TACC_METIS_INC",        "%{INSTALL_DIR}/include")

--
-- prepend path
--

prepend_path(   "PATH",                  "%{INSTALL_DIR}")
prepend_path(   "LD_LIBRARY_PATH",       "%{INSTALL_DIR}/lib")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for %{name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT

