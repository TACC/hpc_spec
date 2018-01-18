Summary: Shell Startup tracing tool 
Name: tacc-shell_startup_debug
Version: 1.9
Release: 1%{?dist}
License:   LGPL
Group: System Environment/Base
Group: tacc-stampede2-base
URL: www.tacc.utexas.edu
Packager: TACC - mclay@tacc.utexas.edu, cproctor@tacc.utexas.edu
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: tacc-bash
Requires: tacc-login-scripts

%define debug_package %{nil}
%include rpm-dir.inc

%define pkg_base_name shell_startup_debug
%define name_prefix   tacc
%define pkg_name      %{name_prefix}-%{pkg_base_name}
%define PKG_BASE    /opt/apps/%{pkg_base_name}
%define INSTALL_DIR %{PKG_BASE}/%{version}

%package %{pkg_name}
Summary: shell startup debug: tracking shell startup behavior
Group: System

%description
%description %{pkg_name}
Shell startup tracing tool.  

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-%{version}

%build

%install

# shell startup scripts need lua 
# So we search for lua # the old fashion way

for i in /usr/bin /opt/apps/lua/lua/bin /opt/local/bin; do
  if [ -x $i/lua ]; then
    luaPath=$i
    break
  fi
done


PATH=$luaPath:$PATH
export PATH

./configure --prefix=/opt/apps
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{INSTALL_DIR}/../shell_startup_debug

echo "done with install"

%files -n %{pkg_name}
%defattr(-,root,root,)
%{INSTALL_DIR}

%post -n %{pkg_name}

cd %{PKG_BASE}

if [ -d %{pkg_base_name} ]; then
  rm -f %{pkg_base_name}
fi
ln -s %{version} %{pkg_base_name}

%postun -n %{pkg_name}

cd %{PKG_BASE}

if [ -h %{pkg_base_name} ]; then
  lv=`readlink %{pkg_base_name}`
  if [ ! -d $lv ]; then
    rm %{pkg_base_name} 
  fi
fi

%clean -n %{pkg_name}
rm -rf $RPM_BUILD_ROOT
