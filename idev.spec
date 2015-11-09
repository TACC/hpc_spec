#
# Spec file for idev
#
Summary:   idev: interactive access to production nodes
Name:      idev
Version:   1.0
Release:   11
License:   TACC
Vendor:    tacc.utexas.edu
Group:     System Environment/Base
Source:    idev-%{version}.tar.gz
Packager:  TACC- milfeld@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS   /opt/apps
%define USER   /opt/apps/tacc/bin
%define MODULES modulefiles


%define INSTALL_DIR %{USER}
%define  MODULE_DIR %{APPS}/%{MODULES}/%{name}

%description 
idev submits a batch job and provides interactive access
to a compute node for interactive execution of ibrun, 
openmp executables, MIC executables and cuda programs. 

%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup

%install

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

User Guide at:

        portal.tacc.utexas.edu/software/idev

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
%{INSTALL_DIR}/%{name}
%{INSTALL_DIR}/%{name}_utils
%{MODULE_DIR}

%post
%clean
#rm -rf $RPM_BUILD_ROOT
