# $Id$

Summary: TACC TIPS
Name: tacc_tips
Version: 0.5
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Base
Source0:  %{name}-%{version}.tar.bz2
Packager: mclay@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define PKG_BASE    %{APPS}/%{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_TIPS

%description
A fortune like program to report a tip to a user each time they log-in.

%prep

%setup -n %{name}-%{version}

%build
%install

if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi
#module load gcc

make DESTDIR=$RPM_BUILD_ROOT DIR=%{INSTALL_DIR}/bin install

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The binary is called showTip.  You can do:

   $ showTip -n 14

to see tip 14 again.

To show all tips do:

   $ showTip -a

To disable do:

   $ touch ~/.no.tips

Version %{version}
]]
)

whatis("Name: Tacc Tips")
whatis("Version: %{version}")
whatis("Category: User training")
whatis("Keywords: Training ")
whatis("URL: http://tacc.utexas.edu")
whatis("Description: Tips generated at each login.")


prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")

EOF

#--------------
#  Version file. 
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT
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
