
Summary:    Startup Scripts (Defaults/Examples) for Lonestar 5
Name:       tacc-startup_scripts
Version:    1.0
Release:    1
License:    GPL
Vendor:     TACC
Group:      System/Info
Source:     startup_scripts-%{version}.tar.gz
Packager:   TACC - djames@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
%define dbg           %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
#%include compiler-defines.inc
# MPI Family Definitions
#%include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
#%package -n %{name}
#Summary: Startup Files (defaults/examples) for Lonestar 5
#Group:   System/Info

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}
Default/example startup files for Lonestar 5.
Also includes a script user can run to copy these files safely to user account.
These are NOT currently the master files used by create_user scripts.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/tacc/doc/startup_scripts

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
#### %prep -n startup_scripts-%{version}.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/<name>-<version>
#### %setup -n startup_scripts-%{version}
%setup

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

### Nothing necessary here; all we have are some files to copy

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

# Just copy files from exploded tarball to temporary install
cp ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}

# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}
%attr(755, root, root)  install_default_scripts
%attr(644, root, root)  dot.*
%attr(644, root, root)  transition.txt

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post

# Nothing necessary here

%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the source files from /tmp/BUILD
rm -rf /tmp/BUILD/%{name}-%{version}

# Remove the installation files now that the RPM has been generated
rm -rf /var/tmp/%{name}-%{version}-buildroot

rm -rf $RPM_BUILD_ROOT
