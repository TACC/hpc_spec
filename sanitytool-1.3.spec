# $Id: sanitytool.spec, v 1.3, 2016/04/01 siliu $ 

Summary: Sanity Tool
Name: sanitytool
Version: 1.3
Release: 1
License: TACC
Vendor: TACC
Group: TACC-HPC-TOOL
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
Sanity Tool 1.3

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

help( [[
The module loads TACC Sanitytool for you.
Version: 1.3

You can run the command "sanitycheck" to examine your current environment settings on Stampede, Lonestar, or Maverick.
If you encounter any problems, please send an email to siliu@tacc.utexas.edu with your user id and error messages.
Please also contact siliu@tacc.utexas.edu, if you have any other concerns or require additional tests.
]] )

whatis "Name: Sanity Tool"
whatis "Version: 1.3"
whatis "Category: System tools"

local sanitypath = "/opt/apps/sanitytool/1.3/"

append_path("PATH",sanitypath)
setenv("TACC_SANITYTOOL_DIR", "/opt/apps/sanitytool/1.3/")

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

