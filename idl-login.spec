#
# idl-login.spec, v 7.0.6, 2013-01-09 12:50:00 pnav
#                          

Summary:    IDL
Name:       idl-login
Version:    7.0.6
Release:    0
License:    Exelis
Vendor:     Exelis
Group:      Visualization / Data Analysis
Source:     %{name}-%{version}.tar.gz
Packager:   pnav@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

AutoReqProv: no
%define MySrc %{name}-%{version}.tar.gz

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/idl/%{version}
%define MODULE_DIR %{APPS}/%{MODULES}/idl

#%package 
#Summary: IDL %{version} local binary install
#Group: Visualization / Data Analysis

%description 
IDL is the trusted scddientific programming language used
 across disciplines to create meaningful visualizations out of complex
 numerical data. From small scale analysis programs to widely deployed
 applications, IDL provides the comprehensive computing environment
 you need to effectively get information from your data.

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
This module loads idl environment.
The command directory is added to PATH.
The library directory is added to LD_LIBRARY_PATH.
Following environment variable are defined:

ITT_DIR
IDL_DIR
TACC_IDL_DIR

Version %{version}
]]

local no_bin_message = [[

NOTE: The IDL binaries are only installed on the largemem and vis partitions.
Please use one of these srun templates to get an interactive IDL session:

srun -p largemem -n 16 -t <timeframe> -A <account> --pty /bin/bash -l
srun -p vis -n 16 -t <timeframe> -A <account> --pty /bin/bash -l

]]

whatis("Name: idl")
whatis("Version: %{version}")
whatis("Category: visualization")
whatis("Description: IDL interactive graphing and visualization toolkit")
whatis("URL: http://www.ittvis.com/ProductServices/IDL.aspx")

help(help_message, "\n")

LmodMessage(no_bin_message, "\n")

setenv("ITT_DIR",      "%{INSTALL_DIR}")
setenv("IDL_DIR",      "%{INSTALL_DIR}/idl")
setenv("TACC_IDL_DIR", "%{INSTALL_DIR}")

prepend_path("PATH", "%{INSTALL_DIR}/idl/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for idl version %{version}
##
set ModulesVersion "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{name}

# Define files permisions, user and group
%defattr(-,root,install)
%{MODULE_DIR}


%clean
rm -rf $RPM_BUILD_ROOT
