# -*-rpm-spec-*-
#
#
#-------------------------------------------------------------------
# Define local build root and top level dir for rpm builds
#-------------------------------------------------------------------

Buildroot:      /var/tmp/%{name}-%{version}-buildroot
%define _topdir /home1/0000/build/admin/rpms/lonestar42/
%define APPS    /opt/apps
%define MODULES modulefiles


%define defined()      %{expand:%%{?%{1}:1}%%{!?%{1}:0}}
%define undefined()    %{expand:%%{?%{1}:0}%%{!?%{1}:1}}

