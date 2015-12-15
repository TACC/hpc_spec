
Summary:    Slurm Examples for Lonestar 5
Name:       tacc-slurm_examples
Version:    1.0
Release:    2
License:    GPL
Vendor:     TACC
Group:      System/Info
Source:     slurm_examples-%{version}.tar.gz
Packager:   TACC - alamas@tacc.utexas.edu
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
#Summary: Slurm examples for Lonestar 5
#Group:   System/Info

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}
Slurm examples for Lonestar 5

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/tacc/doc/slurm

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep -n slurm_examples-%{version}.tar.gz

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/<name>-<version>
%setup -n slurm_examples-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
# Use mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}

#-----------------------------
# Build parallel version
#-----------------------------

# Build Utilities
cp ./*.slurm %{INSTALL_DIR}

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

 mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}

#  Kluge, the make install, installs in /tmp/carlos
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount                                   %{INSTALL_DIR}


#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}

# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the source files from /tmp/BUILD
rm -rf /tmp/BUILD/%{name}-%{version}

# Remove the installation files now that the RPM has been generated
rm -rf /var/tmp/%{name}-%{version}-buildroot

rm -rf $RPM_BUILD_ROOT
