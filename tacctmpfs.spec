# $Id$

Summary: tacctmpfs
Name: tacctmpfs
Version: 3.1
Release: 1
License: GDP
Group: System Environment/Base
Source0:  %{name}-%{version}.tar.gz
Packager: djames@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME tacctmpfs

%define INSTALL_DIR /usr/local/bin

%description
Allows build login to execute tmpfs trick

%prep

%setup

%build

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
module load intel
make 

%install

make INSTALL_DIR=$RPM_BUILD_ROOT/%{INSTALL_DIR} install

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}/%{PNAME}

%clean
rm -rf $RPM_BUILD_ROOT

%post

chmod 4755 %{INSTALL_DIR}/%{PNAME}

