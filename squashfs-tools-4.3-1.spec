Summary: Utility for the creation of squashfs filesystems
Name: squashfs-tools
Version: 4.3
Release: 1
License: BSD-3
URL: http://squashfs.sourceforge.net
Source: squashfs%{version}.tar.gz
ExclusiveOS: linux
Group: System Utilities
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{name}-%{version}-%{release}-root

%include rpm-dir.inc

%description
Squashfs is a highly compressed read-only filesystem for Linux.  This package contains the utilities for manipulating squashfs filesystems.

%prep

%setup -q -n squashfs%{version}

%build

%install

cd squashfs-tools
# Make install directory
mkdir -p ${RPM_BUILD_ROOT}/usr/local/bin
# Compile
make INSTALL_DIR=${RPM_BUILD_ROOT}/usr/local/bin
# Install
make INSTALL_DIR=${RPM_BUILD_ROOT}/usr/local/bin install

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/local/bin/mksquashfs
/usr/local/bin/unsquashfs

%changelog
