#
# Spec file for visit
#

Summary:  visit common files local binary install
Name:     visit-common
Version:  1.0
Release:  3
License:  GPL
Vendor:   wci.llnl.gov/codes/visit/
Group:    Visualization 
Packager:  pnav@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps


%define is_intel15 1
%include compiler-defines.inc
%define is_mvapich2 1
%define mpiV 2_1
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/visit

%define VISIT_SRC visit.common.%{mpi_fam_ver}.%{release}.tar.gz

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: visit %{version} local binary install
Group: Visualization

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
VisIt is a free interactive parallel visualization and graphical analysis tool.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd $RPM_BUILD_ROOT/%{INSTALL_DIR}
tar xvzf $RPM_SOURCE_DIR/%{VISIT_SRC}

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(755,root,install)
%{INSTALL_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT
