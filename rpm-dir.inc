# -*-rpm-spec-*-
#
#-------------------------------------------------------------------
# Define local build root and top level dir for rpm builds
#-------------------------------------------------------------------

Buildroot:       /var/tmp/%{name}-%{version}-buildroot
%define _topdir  /admin/build/admin/rpms/maverick2
%define APPS     /opt/apps
%define MODULES  modulefiles
%define SPEC_DIR %{_topdir}/SPECS
%define TACC_OPT %{nil}

%define defined()      %{expand:%%{?%{1}:1}%%{!?%{1}:0}}
%define undefined()    %{expand:%%{?%{1}:0}%%{!?%{1}:1}}
