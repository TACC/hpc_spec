# $Id$

Summary: iRODS
Name: irods
Version: 4.2.1
Release: 1
License: Private
Group: DMC
Source0:  %{name}-%{version}.tar.gz
Packager: siva@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR  TACC_IRODS

%description

This is icommand installation RPM for UT repository users for iRODS 3.3.1 version.

%prep

echo "*** in prep section ***"
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version}


%build

echo "*** in build section ***"

%install
echo "*** in install section ***"
if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi

module purge
#module --expert load TACC





mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}

 cp   -rp  bin $RPM_BUILD_ROOT%{INSTALL_DIR}
chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT%{INSTALL_DIR}


#-----------------
# Modules Section 
#-----------------
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_BIN, and for
the location of the %{PNAME} distribution and its binaries.

Version %{version}
]]
)

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: Data Storage")
whatis("Keywords: icommands,data storage")
whatis("URL: http://www.tacc.utexas.edu")
whatis("Description: IRODS")


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
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

%files
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

#%clean
#rm -rf $RPM_BUILD_ROOT
                                                                                                                                                                                      



