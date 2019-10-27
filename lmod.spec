#
# $Id: lmod.spec 1934 2013-10-12 14:10:48Z karl $
#
%define name_prefix tacc
%define base_name lmod

Prefix:    /opt/apps
Summary:   lmod: Lua based Modules
Name:      %{name_prefix}-%{base_name}
Version:   8.1.6
Release:   1
License:   MIT
Vendor:    Robert McLay
Group:     System Environment/Base
Source:    Lmod-%{version}.tar.bz2
Packager:  TACC - mclay@tacc.utexas.edu
Buildroot: /var/tmp/%{base_name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS           /opt/apps
%define PKG_BASE       /opt/apps/%{base_name}
%define INSTALL_DIR    %{PKG_BASE}/%{version}
%define GENERIC_IDIR   %{PKG_BASE}/lmod
%define MODULES        tools/modulefiles
%define MODULE_DIR     %{APPS}/%{MODULES}
%define MODULE_LMOD    %{APPS}/%{MODULES}/lmod.lua
%define MODULE_SETTARG %{APPS}/%{MODULES}/settarg.lua
%define ZSH_SITE_FUNC  /opt/apps/zsh/site-functions

%description

Lua Based Modules

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR} $RPM_BUILD_ROOT/%{ZSH_SITE_FUNC}

##
## SETUP
##

%setup -n Lmod-%{version}

##
## BUILD
##

%build

%install

myhost=$(hostname -f)
myhost=${myhost%.tacc.utexas.edu}
first=${myhost%%.*}
SYSHOST=${myhost#*.}

if [ "$SYSHOST" = "ls5" ]; then
EXTRA="--with-tmodPathRule=yes --with-syshost=ls5 --with-siteName=TACC --with-silentShellDebugging=yes"
CACHE_DIR="--with-spiderCacheDescript=cacheDescript.txt"

cat > cacheDescript.txt << EOF
/home1/moduleData/cacheDir/tacc:/home1/moduleData/cacheDir/tacc_cache_timestamp.txt
EOF
fi

# Lmod needs lua but should not require that a working module
# system be in place to install lmod.  So we search for lua
# the old fashion way

for i in /opt/apps/lua/lua/bin /usr/bin /usr/local/bin /opt/local/bin ; do
  if [ -x $i/lua ]; then
    luaPath=$i
    break
  fi
done
PATH=$luaPath:$PATH

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR} $RPM_BUILD_ROOT/%{ZSH_SITE_FUNC}

./configure --prefix=%{APPS} $CACHE_DIR --with-settarg=FULL $EXTRA
make DESTDIR=$RPM_BUILD_ROOT install
cp contrib/TACC/*.lua $RPM_BUILD_ROOT/%{INSTALL_DIR}/libexec
sed -e '/^scDescriptT = {/,/^}/d' < $RPM_BUILD_ROOT/%{INSTALL_DIR}/init/lmodrc.lua > $RPM_BUILD_ROOT/%{INSTALL_DIR}/init/lmodrc_cray_world.lua

rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/../lmod

#-----------------
# Modules Section
#-----------------

#-----------------
# Lmod modulefile
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_LMOD} << 'EOF'
-- -*- lua -*-
help(
[[
This module is for Lmod.  Normal user will probably not need to
load this module.  It is only required if one is using the tools
that are part of Lmod.

Version %{version}
]])

local version = "%{version}"
whatis("Name: Lmod")
whatis("Version: " .. version)
whatis("Category: System Software")
whatis("Keywords: System, Utility, Tools")
whatis("Description: An environment module system")
whatis("URL: http://www.tacc.utexas.edu/tacc-projects/lmod")

prepend_path( "PATH",            "%{GENERIC_IDIR}/libexec" )
EOF

#--------------------
# Settarg modulefile
#--------------------

sed -e "s|@PKG@|%{GENERIC_IDIR}|g"     \
    -e "s|@settarg_cmd@|settarg_cmd|g" \
    -e "s|@path_to_lua@|$luaPath|g"    \
    < MF/settarg.version.lua > $RPM_BUILD_ROOT/%{MODULE_SETTARG}

%files
%defattr(-,root,root,)
%{INSTALL_DIR}
%{MODULE_LMOD}
%{MODULE_SETTARG}
%{ZSH_SITE_FUNC}

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
