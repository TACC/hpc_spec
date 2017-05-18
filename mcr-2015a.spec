# $Id: mcr.spec, v 2015a(v85), 2015/05/28 siliu $ 
 
Summary: Matlab Compiler Runtime (MCR)

Name: mcr
Version: v85
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
 
## SETUP
##setup -n %{name}-%{version}
 
## BUILD
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

Version v85
]]
)

whatis("Name: MCR")
whatis("Version: v85")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab v85 Compiler Runtime from MathWorks")

prepend_path("PATH", "/work/apps/mcr/v85/bin")
prepend_path("LD_LIBRARY_PATH", "/work/apps/mcr/v85/bin/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/work/apps/mcr/v85/runtime/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/work/apps/mcr/v85/bin/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/work/apps/mcr/v85/sys/os/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/work/apps/mcr/v85/sys/java/jre/glnxa64/jre/lib/amd64/native_threads")
prepend_path("LD_LIBRARY_PATH", "/work/apps/mcr/v85/sys/java/jre/glnxa64/jre/lib/amd64/server")
prepend_path("LD_LIBRARY_PATH", "/work/apps/mcr/v85/sys/java/jre/glnxa64/jre/lib/amd64")

setenv ("TACC_MCR_DIR", "/work/apps/mcr/v85")
setenv ("XAPPLRESDIR", "/work/apps/mcr/v85/X11/app-defaults")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
 
set     ModulesVersion      "%{version}"
EOF

%files
%defattr(-,root,install)
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
