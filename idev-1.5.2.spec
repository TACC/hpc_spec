Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name idev
%define MODULE_VAR    IDEV

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 5
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include name-defines-noreloc.inc

Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   1%{?dist}
License:   GPL
Group:     Development/Tools
URL:       https:/github.com/tacc/idev
Packager:  TACC - milfeld@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
#
# Spec file for idev
#
Summary:   idev: interactive access to production nodes
#Release:   1

%define APPS   /opt/apps
%define USER   /usr/bin
%define MODULES modulefiles


%define INSTALL_DIR %{USER}
%define  MODULE_DIR %{APPS}/%{MODULES}/%{pkg_base_name}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
idev submits a batch job and provides interactive access
to a compute node for interactive execution of ibrun, openmp executables,
and cuda programs. 

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Modulefile give basic information about idev.  Not needed for execution.

%description 
idev submits a batch job and provides interactive access
to a compute node for interactive execution of ibrun, openmp executables,
and cuda programs. 

%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -c -n idev-%{pkg_version}
#setup -c
echo `pwd` > /tmp/whereami1_a

%install
echo `pwd` > /tmp/whereami2_a
mkdir -p      $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp idev       $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp idev_utils $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat    > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The idev modulefile defines the following environment variables:
TACC_IDEV_DIR (for the location of the idev command and idev_utilities).
#
The latest version (%{version}) of  idev is in the %{INSTALL_DIR} directory.
At TACC %{INSTALL_DIR} is in the default PATH.  It is NOT necessary
to have the idev module loaded to use idev.

Purpose: For developing MPI or GPU code interactively.
Features:
Allows user to work directly on a compute node:
  You can execute the MPI ibrun command interactively.
  You can execute cuda code interactively (Stampede/Lonestar/Longhorn).

Usage:
        idev

(First time: users with multiple accounts  must select default account.)


Idev works for bash and tcsh shells (may not work for zsh).
Idev uses a job submission to obtain a node(s) for an interactive session.
Exiting the idev shell on the compute node will delete the job.
You can run multiple idev sessions.
Command line options allow you to change the default resources 
for the batch job (number of cores, time, queue, etc.) .

For details, execute: 

        idev -help

See help for setting defaults for account, queue and time.
]]

help(help_message,"\n")

whatis("Name: idev")
whatis("Version: %{version}")
whatis("Category: utility, development")
whatis("URL: http://www.tacc.utexas.edu")
whatis("Description: Interactive Access to Compute Node(s) for Development via Batch System")


local idev_dir="%{INSTALL_DIR}"

setenv("TACC_IDEV_DIR",idev_dir)

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for idev
##
 
set     ModulesVersion      "%{version}"
EOF

%files
%defattr(755,root,install)
%{INSTALL_DIR}/%{pkg_base_name}
%{INSTALL_DIR}/%{pkg_base_name}_utils
%{MODULE_DIR}

%post
%clean
#rm -rf $RPM_BUILD_ROOT
