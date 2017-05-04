# $Id: mcr.spec, v2016b, 2017/03/07 siliu $ 
Summary: Matlab Compiler Runtime (MCR)
Name: mcr
Version: v92
Release: 1
License: Mathworks License
Vendor: Mathworks
Group: Matlab
Source: %{name}-%{version}.tar.gz
Packager:  siliu@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps/
%define MODULES modulefiles

# Note: this is a binary distribution and there is nothing to compile!
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%description
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

%prep
##rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
##mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##
##setup -n %{name}-%{version}

##
## BUILD
##
%build

%install

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

Version v92
]]
)

whatis("Name: MCR")
whatis("Version: v92")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab v92 Compiler Runtime from MathWorks")

prepend_path("PATH", "/home1/apps/mcr/v92/bin")
prepend_path("LD_LIBRARY_PATH", "/home1/apps/mcr/v92/bin/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/home1/apps/mcr/v92/runtime/glnxa64")

prepend_path("LD_LIBRARY_PATH", "/home1/apps/mcr/v92/bin/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/home1/apps/mcr/v92/sys/os/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/home1/apps/mcr/v92/sys/java/jre/glnxa64/jre/lib/amd64/server")
prepend_path("LD_LIBRARY_PATH", "/home1/apps/mcr/v92/sys/java/jre/glnxa64/jre/lib/amd64")

setenv ("TACC_MCR_DIR", "/home1/apps/mcr/v92")
setenv ("XAPPLRESDIR", "/home1/apps/mcr/v92/X11/app-defaults")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

%files
%defattr(-,root,install)
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
