Summary: Valgrind memory checker
Name: valgrind
Version: 3.12.0
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
module load gcc

./configure --prefix=%{INSTALL_DIR} --enable-only64bit
make 


%install

make DESTDIR=$RPM_BUILD_ROOT install

## Module for valgrind
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0##################################################################
#
# This module file sets up the environment variables and path for the
# valgrind distribution.
#
#############################################################################

proc ModulesHelp { } {
puts stderr "The %{INSTALL_NAME} modulefile defines the following environment va
riables:"
puts stderr "TACC_VALGRIND_DIR, TACC_VALGRIND_LIB, and TACC_VALGRIND_INC"
puts stderr "for the location of the Valgrind %{version} distribution, "
puts stderr "libraries, and include files respectively.\n"

puts stderr "To use the valgrind utility on an executable called a.out:"
puts stderr ""
puts stderr "valgrind ./a.out"

puts stderr "\nVersion %{version}"
}
module-whatis "Name: Valgrind"
module-whatis "Version: %{version}"
module-whatis "Category: utility, runtime support"
module-whatis "Keywords: Utility, Debugging"
module-whatis "URL: http://valgrind.org"
module-whatis "Description: Dynamic memory testing and debugging tools"

#
# Create environment variables.
#

set             valgrind_dir        %{INSTALL_DIR}

setenv          TACC_VALGRIND_DIR        $valgrind_dir
setenv          TACC_VALGRIND_LIB        $valgrind_dir/lib/valgrind/amd64-linux
setenv          TACC_VALGRIND_INC        $valgrind_dir/include

#
# Append path
#

append-path     PATH                       $valgrind_dir/bin
append-path     MANPATH                    $valgrind_dir/man
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
