# $Id: matlab.spec, v 2016b, 2016/12/31 siliu $ 

Summary: Matlab Compiler Runtime (MCR)
Name: mcr
Version: v910
Release: 1
License: Mathworks License
Vendor: Mathworks
Group: Matlab
Source:  %{name}-%{version}.tar.gz
Packager: siliu@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define PKG_BASE    %{APPS}/%{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_TIPS

%description
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

%prep
#Nothing necessary here

%build
#Nothing necessary here

%install

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

Version v91
]]
)

whatis("Name: MCR")
whatis("Version: v91")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab v91 Compiler Runtime from MathWorks")

prepend_path("PATH", "/opt/apps/mcr/v91/bin")
prepend_path("LD_LIBRARY_PATH", "/opt/apps/mcr/v91/bin/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/opt/apps/mcr/v91/runtime/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/opt/apps/mcr/v91/bin/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/opt/apps/mcr/v91/sys/os/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/opt/apps/mcr/v91/sys/java/jre/glnxa64/jre/lib/amd64/native_threads")
prepend_path("LD_LIBRARY_PATH", "/opt/apps/mcr/v91/sys/java/jre/glnxa64/jre/lib/amd64/server")
prepend_path("LD_LIBRARY_PATH", "/opt/apps/mcr/v91/sys/java/jre/glnxa64/jre/lib/amd64")

setenv ("TACC_MCR_DIR", "/opt/apps/mcr/v91")
setenv ("XAPPLRESDIR", "/opt/apps/mcr/v91/X11/app-defaults")


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
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

