# $Id$

Summary: XALT
Name: xalt
Version: 1.7
Release: 6
License: LGPLv2
Group: System Environment/Base
Source0:  xalt-%{version}-devel.tar.bz2
Packager: mclay@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME xalt
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_XALT

%description
A method to collect system usage data.

%prep

%setup -n %{PNAME}-%{version}-devel

%build
%install


if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/xsede/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

module --latest load intel
module load python

CXX=/usr/bin/g++ CC=/usr/bin/gcc ./configure CXX=/usr/bin/g++ CC=/usr/bin/gcc --prefix=%{INSTALL_DIR} --with-syshostConfig=nth_name:2 --with-config=Config/TACC_config.py --with-transmission=syslog --with-trackMPIOnly=yes --with-omnipathProfileBug=yes

make CXX=/usr/bin/g++ CC=/usr/bin/gcc DESTDIR=$RPM_BUILD_ROOT install Inst_TACC
rm -f $RPM_BUILD_ROOT/%{INSTALL_DIR}/sbin/xalt_db.conf

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The xalt module collects system usage data.

Version %{version}
]]
)

whatis("Name: XALT")
whatis("Version: %{version}")
whatis("Category: tools")
whatis("Keywords: System, TOOLS")
whatis("URL: http://xalt.sf.net")
whatis("Description: Collects system usage data")

prepend_path{"PATH",                     "%{INSTALL_DIR}/bin", priority = 100}
prepend_path("LD_PRELOAD",               "%{INSTALL_DIR}/lib64/libxalt_init.so")
setenv (     "%{MODULE_VAR}_DIR",        "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BIN",        "%{INSTALL_DIR}/bin")
setenv (     "XALT_EXECUTABLE_TRACKING", "yes")

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

%files
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
