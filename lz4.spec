#
# spec file for package lz4
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           lz4
%define lname	liblz4-1
Version:        1.8.0
Release:        lp150.1.10
Summary:        Hash-based Predictive Lempel–Ziv compressor
License:        GPL-2.0+ and BSD-2-Clause
Group:          Productivity/Archiving/Compression
Url:            http://lz4.org/

#Git-Clone:	https://github.com/lz4/lz4
Source:         https://github.com/lz4/lz4/archive/v%version.tar.gz
Source99:       baselibs.conf
Patch1:         lz4-use-shlib.diff
Patch2:         lz-export.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  pkg-config

%description
LZ4 is a lossless data compression algorithm that is focused on
compression and decompression speed. It belongs to the LZ77
(Lempel–Ziv) family of byte-oriented compression schemes. It is a
LZP2 fork and provides better compression ratio for text files.

This subpackage provides a GPL command-line utility to make use of
the LZ4 algorithm.

%package -n %lname
Summary:        Hash-based predictive Lempel-Ziv compressor
License:        BSD-2-Clause
Group:          System/Libraries

%description -n %lname
LZ4 is a lossless data compression algorithm that is focused on
compression and decompression speed. It belongs to the LZ77
(Lempel–Ziv) family of byte-oriented compression schemes. It is a

This subpackage contains the (de)compressor code as a shared library.

%package -n liblz4-devel
Summary:        Development files for the LZ4 compressor
License:        BSD-2-Clause
Group:          Development/Libraries/C and C++
Requires:       %lname = %version

%description -n liblz4-devel
LZ4 is a lossless data compression algorithm that is focused on
compression and decompression speed. It belongs to the LZ77
(Lempel–Ziv) family of byte-oriented compression schemes. It is a

This subpackage contains libraries and header files for developing
applications that want to make use of liblz4.

%prep
%setup -q
%patch -P 1 -P 2 -p1

%build
# Goddammit, lz4
perl -i -pe 's{^\t@}{\t}g' Makefile */Makefile
# don't bother building here, because make install builds it again - unconditionally :-(

%install
make install CFLAGS="%optflags" DESTDIR="%buildroot" \
	PREFIX="%_prefix" LIBDIR="%_libdir"
rm -f "%buildroot/%_libdir"/*.a
mkdir -p "%buildroot/%_mandir/man1"
# duh, it was right in 1.7.5
mv "%buildroot/%_mandir"/*.1 "%buildroot/%_mandir/man1/"

%check
LD_LIBRARY_PATH="%buildroot/%_libdir" ldd -r "%buildroot/%_bindir/lz4"

%post   -n %lname -p /sbin/ldconfig
%postun -n %lname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_bindir/lz4*
%_bindir/unlz4
%_mandir/man1/*.1*

%files -n %lname
%defattr(-,root,root)
%_libdir/liblz4.so.1*

%files -n liblz4-devel
%defattr(-,root,root)
%_includedir/lz4*.h
%_libdir/liblz4.so
%_libdir/pkgconfig/*.pc

%changelog
* Fri Aug 25 2017 jengelh@inai.de
- Update to new upstream release 1.8.0
  * cli: fix: do not modify /dev/null's permissions.
  * cli: added POSIX separator "--" for specifying that all
    following arguments are non-options.
  * cli: restored -BX command enabling block checksum.
  * API: added LZ4_compress_HC_destSize() and
    LZ4F_resetDecompressionContext().
  * API: lz4frame: negative compression levels trigger fast
    acceleration.
  * API: lz4frame: ability to control block checksum and
    dictionary ID.
  * API: fix: expose obsolete decoding functions
  * API: experimental: lz4frame_static.h:
    new dictionary compression API
  * doc: Updated LZ4 Frame format to v1.6.0, restoring
    Dictionary ID field in header.
- Add lz-export.diff
* Tue Aug 15 2017 ddiss@suse.com
- Use official upstream repository; (boo#1053910)
* Wed Jul  5 2017 jengelh@inai.de
- Update to new upstrema release 1.7.5 (2017-01-03)
  * back to the old version scheme
  * lz4hc: new compression levels 10-12
- Remove lz4-soversion.diff (not needed),
  lz4-killdate.diff (no longer needed)
* Mon Jan 16 2017 dimstar@opensuse.org
- Add baselibs.conf: provide liblz4-1_7 as -32bit compatibility
  package, required by systemd-32bit.
* Sat Apr  2 2016 jengelh@inai.de
- Update to new upstream release 131 (library 1.7) (boo#973735)
  * slightly improved decoding speed
  * lz4frame API is included in liblz4
  * new -m command line option to compress multiple files
  * new lz4 and lz4hc compression API (old one retained)
* Fri Nov 28 2014 jengelh@inai.de
- Update to version 1.4+svn124
  * LZ4F_compressBound() may be called with NULL preferencesPtr
  * LZ4_loadDict now returns the dictionary size instead of 1
  on success
- Add lz4-soversion.diff to address ABI changes
* Wed Oct  1 2014 jengelh@inai.de
- Update to version 1.3.1+svn123
  * Added a pkgconfig file
  * Fix a LZ4HC streaming bug
  * Updated the framing specificaiton to 1.4.1
* Wed Jul 16 2014 jengelh@inai.de
- Update to svn revision 119, set version to 1.2.0 (based upon
  Makefile contents; it's still odd to see the 1.4 Windows release)
  * Provide LZ4 as a shared library
- Remove lz4-automake.diff (no longer deemed necessary)
- Add lz4-use-shlib.diff
* Mon Nov 25 2013 dsterba@suse.com
- update to svn 108, set version to 1.4 (current windows release)
  - added manpage
  - minor code updates
* Tue Sep  3 2013 jengelh@inai.de
- Update to new snapshot svn102; set version as 1.3.3 in accordance
  with latest Windows releases.
  * Add lz4-killdate.diff (kill the ungodly __DATE__s)
* Thu Feb 21 2013 jengelh@inai.de
- I hate %%makeinstall (it fails all the SLES builds), kill it!
* Sat Mar 17 2012 jengelh@medozas.de
- Initial package for build.opensuse.org
