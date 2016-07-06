# $Id: matlab.spec, v 2016a, 2016/04/30 siliu $ 

Summary: Matlab
Name: matlab
Version: 2016a
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
MATLAB is a high-level language and interactive environment 
that enables you to perform computationally intensive tasks faster 
than with traditional programming languages such as C, C++, and Fortran.

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
MATLAB interpreter and compiler MATLAB is a high-level language
and interactive environment that enables you to perform computationally
intensive tasks faster than with traditional programming languages
such as C, C++, and Fortran.

UT Austin students, researchers and faculty have access to UT Austin license.
Please contact the TACC help desk with your department/college information.

All other students, researchers and faculty: Matlab usage on TACC systems
follows a Bring-Your-Own-License format. To use Matlab on TACC resources
you must have a matlab license server with a floating network license.
Furthermore the license server has to be accessible from the compute nodes
on TACC systems. You can test this with:
telnet hostname port_number

The TACC helpdesk staff can provide ip-ranges to your license admin to
add exceptions in your firewall rules for license checkout.

Version 2016a
]]
)

whatis("Name: MATLAB")
whatis("Version: 2016a")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab 2016a from MathWorks")

prepend_path("PATH", "/opt/apps/matlab/2016a/bin")

append_path("LD_LIBRARY_PATH", "/opt/apps/matlab/2016a/bin/glnxa64")
append_path("LD_LIBRARY_PATH", "/opt/apps/matlab/2016a/runtime/glnxa64")
append_path("LD_LIBRARY_PATH", "/opt/apps/matlab/2016a/sys/java/jre/glnxa64/jre/lib/amd64/server/")

setenv ("TACC_MATLAB_DIR", "/opt/apps/matlab/2016a")
setenv ("DVS_CACHE","off")

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

