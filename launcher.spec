#
# $Id: launcher.spec,v 1.4 2011/1/21 15:40:02 lwilson Exp $
#
 
Summary: Local TACC parametric-launcher install.
 
#
#
#

Name: launcher
Version: 3.1.1
Release: 2
Vendor: TACC
License: none
Group: Utility
Source: %{name}-%{version}.tar.gz
Packager: lwilson@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%description

%define PKG_INSTALL_DIR /opt/apps/%{name}/%{name}-%{version}
%define MODULEFILES_INSTALL_DIR /opt/apps/modulefiles
%define CREATE_MODULE_FILE 1
%define MODULE_VAR TACC_LAUNCHER

%prep
rm   -rf $RPM_BUILD_ROOT/%{PKG_INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{PKG_INSTALL_DIR}/
mkdir -p $RPM_BUILD_ROOT/%{MODULEFILES_INSTALL_DIR}/%{name}

 
##
## SETUP
##
%setup 
 
##
## BUILD
##

%build

%install

find . | cpio -pduv  $RPM_BUILD_ROOT/%{PKG_INSTALL_DIR}

## Module for launcher
mkdir -p $RPM_BUILD_ROOT/%{MODULEFILES_INSTALL_DIR}/%{name}
cat > $RPM_BUILD_ROOT/%{MODULEFILES_INSTALL_DIR}/%{name}/%{version}.lua << 'EOF'

local help_message=[[
The %{name} module file defines the environment variable:
$%{MODULE_VAR}_DIR for the location of the TACC Parametric 
Job Launcher which is a simple utility for submitting multiple
serial applications simultaneously.

For more information on using the Launcher, please consult
the README.launcher file located in $%{MODULE_VAR}_DIR

Version %{version}
]]

help(help_message,"\n")

whatis ("Name: TACC Parametric Job Launcher")
whatis ("Version: %{version}")
whatis ("Category: utility, runtime support")
whatis ("Keywords: System, Utility, Tools")
whatis ("Description: Utility for starting parametric job sweeps")

local launcher_dir="%{PKG_INSTALL_DIR}"
local launcher_plugin_dir="%{PKG_INSTALL_DIR}/plugins"
setenv("TACC_LAUNCHER_DIR", launcher_dir)
setenv("LAUNCHER_DIR", launcher_dir)
setenv("LAUNCHER_PLUGIN_DIR", launcher_plugin_dir)
setenv("LAUNCHER_RMI", "SLURM")

EOF

mkdir -p $RPM_BUILD_ROOT/%{MODULEFILES_INSTALL_DIR}/%{name}
cat > $RPM_BUILD_ROOT/%{MODULEFILES_INSTALL_DIR}/%{name}/.version << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}%{version}
##
 
set     ModulesVersion      "2.0"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULEFILES_INSTALL_DIR}/%{name}/%{version}.lua

%files
%defattr(755,root,install)

%{PKG_INSTALL_DIR}
%{MODULEFILES_INSTALL_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT

