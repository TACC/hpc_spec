Prefix:    /opt/apps
Summary:   Provide lua module such as strict.lua
Name:      luatools
Version:   2
Release:   1%{?dist}
License:   MIT
Vendor:    Robert McLay
Group:     System Environment/Base
Source:    luatools-%{version}.tar.bz2
Packager:  TACC - mclay@tacc.utexas.edu
#Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define pkg_base_name luatools
%define name_prefix   tacc
%define pkg_name      %{name_prefix}-%{pkg_base_name}


%define APPS           /opt/apps
%define PKG_BASE       /opt/apps/%{pkg_base_name}
%define INSTALL_DIR    %{PKG_BASE}/%{version}
%define MODULES        modulefiles
%define MODULE_DIR     %{APPS}/%{MODULES}/luatools
%define MODULE         %{MODULE_DIR}/2.lua

%package -n %{pkg_name}
Summary: lua modules such as strict.lua
Group: System
%description
%description -n %{pkg_name}

Lua Modules such as strict.lua

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR} 

##
## SETUP
##

%setup -n luatools-%{version}

##
## BUILD
##

%build

%install


# luatools needs lua but should not require that a working module
# system be in place to install lmod.  So we search for lua
# the old fashion way

for i in /usr/bin /opt/apps/lua/lua/bin /usr/local/bin /opt/local/bin ; do
  if [ -x $i/lua ]; then
    luaPath=$i
    break
  fi
done
PATH=$luaPath:$PATH

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR} 

./configure --prefix=%{INSTALL_DIR} 
make
make CC=gcc DESTDIR=$RPM_BUILD_ROOT install

#-----------------
# Modules Section
#-----------------

#-----------------
# Lmod modulefile
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE} << 'EOF'
-- -*- lua -*-
help(
[[
This module is for luatools.  These are lua modulefiles that provide the strict.lua package.
Version %{version}
]])

local version = "%{version}"
whatis("Name: luatools")
whatis("Version: " .. version)
whatis("Category: System Software")
whatis("Keywords: System, Utility, Tools")
whatis("Description: tools for lua")

if (os.getenv("LUA_PATH") == nil) then
   prepend_path("LUA_PATH",";",";")
end
if (os.getenv("LUA_CPATH") == nil) then
   prepend_path("LUA_CPATH",";",";")
end

prepend_path("LUA_PATH", "%{INSTALL_DIR}/share/lua/5.1/?/init.lua", ";")
prepend_path("LUA_PATH", "%{INSTALL_DIR}/share/lua/5.1/?.lua",      ";")
prepend_path("LUA_CPATH","%{INSTALL_DIR}/lib/lua/5.1/?.so",         ";")

EOF

%files -n %{pkg_name}
%defattr(-,root,root,)
%{INSTALL_DIR}
%{MODULE}

%clean -n %{pkg_name}
rm -rf $RPM_BUILD_ROOT
