Summary: Valgrind memory checker
Name: valgrind
Version: 3.17.0
Release: 1%{?dist}
License: GPL
Vendor: http://valgrind.org/
Group: System Environment/Base
Source: valgrind-%{version}.tar.bz2
Packager: mclay@tacc.utexas.edu, bbarth@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define pkg_base_name valgrind
%define name_prefix   tacc
%define pkg_name      %{name_prefix}-%{pkg_base_name}

%define APPS           /opt/apps
%define PKG_BASE       /opt/apps/%{pkg_base_name}
%define INSTALL_DIR    %{PKG_BASE}/%{version}
%define MODULES        modulefiles
%define MODULE_DIR     %{APPS}/%{MODULES}/%{pkg_base_name}

%package -n %{pkg_name}
Summary: Valgrind memory checker
Group: System

%description
%description -n %{pkg_name}
Valgrind is a tool for helping you deal with memory use problems.
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{version}

%build
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

module purge
#module load gcc

./configure --prefix=%{INSTALL_DIR} --enable-only64bit
make 


%install

make DESTDIR=$RPM_BUILD_ROOT install

## Module for valgrind
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local msg = [[
The %{INSTALL_NAME} modulefile defines the following environment via

TACC_VALGRIND_DIR, TACC_VALGRIND_LIB, and TACC_VALGRIND_INC
for the location of the Valgrind %{version} distribution, 
libraries, and include files respectively

To use the valgrind utility on an executable called a.out:

valgrind ./a.out

Version %{version}
]]
help(msg)
whatis("Name: Valgrind")
whatis("Version: %{version}")
whatis("Category: utility, runtime support")
whatis("Keywords: Utility, Debugging")
whatis("URL: http://valgrind.org")
whatis("Description: Dynamic memory testing and debugging tools")

-- Create environment variables.

local           valgrind_dir  =      "%{INSTALL_DIR}"

setenv(         "TACC_VALGRIND_DIR",  valgrind_dir)
setenv(         "TACC_VALGRIND_LIB",  pathJoin(valgrind_dir,"lib/valgrind/amd64-linux"))
setenv(         "TACC_VALGRIND_INC",  pathJoin(valgrind_dir,"include"))

prepend_path(   "PATH",               pathJoin(valgrind_dir,"bin"))
append_path(    "MANPATH",            pathJoin(valgrind_dir,"man"))
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Valgrind
##

set     ModulesVersion      "%version"
EOF


%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}

%files -n %{pkg_name}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}


%post
%clean -n %{pkg_name}
rm -rf $RPM_BUILD_ROOT
