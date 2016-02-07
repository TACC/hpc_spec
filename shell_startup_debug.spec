Summary: Shell Startup tracing tool 
Name: shell_startup_debug
Version: 1.6
Release: 1
License:   LGPL
Group: System Environment/Base
URL: www.tacc.utexas.edu
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%include rpm-dir.inc



%define PKG_BASE %{APPS}/%{name} 
%define INSTALL_DIR %{PKG_BASE}/%{version}

%description
Shell startup tracing tool.  

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n %{name}-%{version}

%build

%install

# shell startup scripts need lua 
# So we search for lua # the old fashion way

luaPath=/opt/apps/lua/lua/bin

for i in /usr/bin /opt/apps/lua/lua/bin /opt/local/bin; do
  if [ -x $i/lua ]; then
    luaPath=$i
    break
  fi
done


PATH=$luaPath:$PATH
export PATH

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

./configure --prefix=%{APPS}
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/../shell_startup_debug

%files
%defattr(755,root,root,)

%{INSTALL_DIR}

%post

cd %{PKG_BASE}

if [ -d %{name} ]; then
  rm -f %{name}
fi
ln -s %{version} %{name}

%postun

cd %{PKG_BASE}

if [ -h %{name} ]; then
  lv=`readlink %{name}`
  if [ ! -d $lv ]; then
    rm %{name} 
  fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan 12 2011 root <root@build.ls4.tacc.utexas.edu> - 
- Initial build.

