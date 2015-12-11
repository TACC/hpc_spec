
%define name_prefix tacc
%define base_name shell_startup_debug

Summary: Shell Startup tracing tool 
Name: %{name_prefix}-%{base_name}
Version: 1.6
Release: 2
License:   LGPL
Group: System Environment/Base
URL: www.tacc.utexas.edu
Source0: %{base_name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{base_name}-%{version}-%{release}-root
%include rpm-dir.inc



%define PKG_BASE %{APPS}/%{base_name} 
%define INSTALL_DIR %{PKG_BASE}/%{version}

%description
Shell startup tracing tool.  

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n %{base_name}-%{version}

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

if [ -d %{base_name} ]; then
  rm -f %{base_name}
fi
ln -s %{version} %{base_name}

%postun

cd %{PKG_BASE}

if [ -h %{base_name} ]; then
  lv=`readlink %{base_name}`
  if [ ! -d $lv ]; then
    rm %{base_name} 
  fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan 12 2011 root <root@build.ls4.tacc.utexas.edu> - 
- Initial build.

