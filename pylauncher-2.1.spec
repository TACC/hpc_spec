#
# Spec file for Pylauncher
#
%define pylauncherversion 2.1

Summary: Pylauncher local binary install
Name: pylauncher
Version: %{pylauncherversion}
Release: 1
License: GPL
Vendor: https://bitbucket.org/VictorEijkhout/pylauncher
Group: TACC
Source: pylauncher-%{version}.tgz
Packager: eijkhout@tacc.utexas.edu 
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define pylauncher_install_dir %{APPS}/%{name}/%{version}
%define modulefileroot  %{APPS}/%{MODULES}/%{name}


%package -n %{name}-%{version}
Summary: Pylauncher local binary install
Group: Numerical library

%description
%description -n %{name}-%{version}
PYLAUNCHER is a python-based flexible launcher

%prep 
rm -rf $RPM_BUILD_ROOT/%{pylauncher_install_dir}
mkdir -p $RPM_BUILD_ROOT/%{pylauncher_install_dir}

%setup 
#-n pylauncher-bitbucket

%build

%install

if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
  module purge
  clearMT
   export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
fi

# give us a clean module environment with only binutils and such
module purge
module --expert load TACC

#
# configure/install loop; also modulefiles
#
export PYLAUNCHER_DIR=`pwd`
mkdir -p $RPM_BUILD_ROOT/%{pylauncher_install_dir}
mkdir -p $RPM_BUILD_ROOT/%{modulefileroot}

cp -r pylauncher.py hostlist.py examples docs $RPM_BUILD_ROOT/%{pylauncher_install_dir}/

cat > $RPM_BUILD_ROOT/%{modulefileroot}/%{version} << EOF
#%Module1.0##################################################################
#
# This module file sets up the environment variables and path for the
# pylauncher distribution.
#
#############################################################################

proc ModulesHelp { } {
puts stderr "The PYLAUNCHER modulefile defines the following environment variables:"
puts stderr "TACC_PYLAUNCHER_DIR, TACC_PYLAUNCHER_DOC"
puts stderr "for the location of the PYLAUNCHER %{version} distribution"
puts stderr "and documentation"
puts stderr ""
puts stderr "\nVersion %{version}"
}

module-whatis "Name: pylauncher"
module-whatis "Version: %{version}"
module-whatis "Category: utility, system"
module-whatis "URL: https://bitbucket.org/VictorEijkhout/pylauncher"
module-whatis "Description: flexible parametric job launcher"

#
# Create environment variables.
#

set		pylauncher_dir		%{pylauncher_install_dir}

setenv		TACC_PYLAUNCHER_DIR	\$pylauncher_dir
setenv		TACC_PYLAUNCHER_DOC	\$pylauncher_dir/docs

prepend-path	PYTHONPATH		\$pylauncher_dir

EOF

cat > $RPM_BUILD_ROOT/%{modulefileroot}/.version.%{version} << EOF
#%Module1.0##################################################
##
## version file for pylauncher
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{modulefileroot}/%{version}

%files -n %{name}-%{version}
%defattr(755,root,install)
%{pylauncher_install_dir}
%{modulefileroot}

%post
%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Apr 02 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial build
