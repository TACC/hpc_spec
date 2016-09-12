Summary:    IDL
Name:       idl
Version:    8.4
Release:    0
License:    Exelis
Vendor:     Exelis
Group:      Visualization / Data Analysis
Source:     idl84envi52linux.x86_64.gz
Packager:   gda@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

AutoReqProv: no

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR %{APPS}/%{MODULES}/%{name}

%define PACKAGE_NAME tacc-%{name}

%package -n %{PACKAGE_NAME}
Summary: idl %{version} local binary install
Group: Visualization

%description 
%description -n %{PACKAGE_NAME}
IDL is the trusted scientific programming language used
 across disciplines to create meaningful visualizations out of complex
 numerical data. From small scale analysis programs to widely deployed
 applications, IDL provides the comprehensive computing environment
 you need to effectively get information from your data.

%prep
%setup -c -n %{name}-%{version}

%build

%install

cat > setup_answers << 'EOF'
y
INSTALLDIR
y
y
y
n
n
n
y
y
y
y
y
n
n
EOF

sed "s?INSTALLDIR?%{APPS}/%{name}/%{version}?" < setup_answers  | ./install.sh -s

cp %{_sourcedir}/idl8.4_license_221797-TACC.dat %{INSTALL_DIR}/license/license.dat
mkdir -p $RPM_BUILD_ROOT/%{APPS}/%{name}
cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{APPS}/%{name}

# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0####################################################################
##
## idl
##
proc ModulesHelp { } {
	puts stderr "\tThis module loads idl environment.\n"
        puts stderr "\t{ The command directory is added to PATH.                } \n"
        puts stderr "\t{ The library directory is added to LD_LIBRARY_PATH.     } \n"
        puts stderr "\t{ Following environment variable are defined:            } \n"
        puts stderr "\t{ TACC_IDL_DIR                                           } \n"
	puts stderr "\tVersion %{version}\n"
}

module-whatis "Name: idl"
module-whatis "Version: %{version}"
module-whatis "Category: visualization"
module-whatis "data analysis, data visualization, and software application development"
module-whatis "URL: http://www.ittvis.com/ProductServices/IDL.aspx"

setenv ITT_DIR	    %{INSTALL_DIR}/
setenv IDL_DIR 	    %{INSTALL_DIR}/idl
setenv TACC_IDL_DIR %{INSTALL_DIR}

prepend-path PATH %{INSTALL_DIR}/idl/bin

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for idl version %{version}
##
set ModulesVersion "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%files -n %{PACKAGE_NAME}

# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

# 
%post -n %{PACKAGE_NAME}
%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{INSTALL_DIR}
