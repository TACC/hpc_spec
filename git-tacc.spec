# $Id$

Summary: GIT
Name: git-tacc
Version: 2.7.0
Release: 1
License: GPLv2
Group: System Environment/Base
Source0:  git-%{version}.tar.gz
Packager: alamas@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME git
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_GIT

%description
A fast distributed version control system.

%prep

%setup -n %{PNAME}-%{version}

%build


if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
 # module purge
  clearMT
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

module purge
module load autotools
module use -a /work/03078/cproctor/apps/modulefiles
module load wrangler/cygcc/4.9.1

#module load python
#module load gcc

if [ ! -f ./configure ]; then
  autoconf
fi
module list
which gcc
which as

./configure CC=gcc --prefix=%{INSTALL_DIR} #--with-python=$TACC_PYTHON_BIN/python
make 

%install

if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi
module purge
module load gcc
make DESTDIR=$RPM_BUILD_ROOT install
#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_DOC, %{MODULE_VAR}_BIN, for the
location of the %{PNAME} distribution,  documentation, binaries, respectively.

Version %{version}
]]
)

whatis("Name: Git")
whatis("Version: %{version}")
whatis("Category: library, tools")
whatis("Keywords: System, Source Control Management, Tools")
whatis("URL: http://git-scm.com")
whatis("Description: Fast Version Control System")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

EOF

#--------------
#  Version file. 
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

module unload python

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
