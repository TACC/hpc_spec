
%define name_prefix tacc
%define base_name lua

Summary:   Local Lua binary install
Name:      %{name_prefix}-%{base_name}
Version:   5.1.4
Release:   1
License:   MIT
Vendor:    lua.org
Group:     System Environment/Base
Source:    lua-5.1.4.8.tar.gz
Packager:  TACC - mclay@tacc.utexas.edu
Buildroot: /var/tmp/%{base_name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS        /opt/apps
%define PKG_BASE    %{APPS}/%{base_name}
%define MODULES     tools/modulefiles

%define INSTALL_DIR %{PKG_BASE}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{base_name}

#----------------------------------------------


%description

Lua is a powerful, fast, light-weight, embeddable scripting language.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, runs by interpreting bytecode for a
register-based virtual machine, and has automatic memory management
with incremental garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.
"Lua" (pronounced LOO-ah) means "Moon" in Portuguese. As such, it is
neither an acronym nor an abbreviation, but a noun. More specifically,
"Lua" is a name, the name of the moon of the Earth and the name of the
language. Like most names, it should be written in lower case with an
initial capital, that is, "Lua". Please do not write it as "LUA",
which is both ugly and confusing, because then it becomes an acronym
with different meanings for different people. So, please, write "Lua"
right!

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n %{base_name}-%{version}.8
 
##
## BUILD
##

%build

CC=gcc ./configure --prefix=%{INSTALL_DIR}
make
make DESTDIR=$RPM_BUILD_ROOT install
 
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The lua modulefile defines the following environment variables
TACC_LUA_BIN, TACC_LUA_LIB, and TACC_LUA_INC for the location of the Lua distribution,
documentation, binaries, libraries, and include files, respectively.

To use the Lua library, include compilation directives
of the form: -L$TACC_LUA_LIB -I$TACC_LUA_INC -llua

Here is an example command to compile lua_test.c:
icc -I$TACC_LUA_INC lua_test.c -L$TACC_LUA_LIB -llua

Version %{version}
]])

whatis("Name: Lua")
whatis("Version: %{version}")
whatis("Category: library, scripting language")
whatis("Keywords: System, Library, Scripting Language")
whatis("Description: Lua is a powerful, fast, light-weight, embeddable scripting language. ")
whatis("URL: http://www.lua.org")

setenv( "TACC_LUA_DIR", "%{INSTALL_DIR}")
setenv( "TACC_LUA_BIN", "%{INSTALL_DIR}/bin")
setenv( "TACC_LUA_LIB", "%{INSTALL_DIR}/lib")
setenv( "TACC_LUA_INC", "%{INSTALL_DIR}/include")

-- Append path

prepend_path("PATH", "%{INSTALL_DIR}/bin")
prepend_path("PKG_CONFIG_PATH", "%{INSTALL_DIR}/lib/pkgconfig")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for %{base_name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%files 
%defattr(755,root,root,)

%{INSTALL_DIR}
%{MODULE_DIR}

%post

cd %{PKG_BASE}

if [ -d  %{base_name} ]; then
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

