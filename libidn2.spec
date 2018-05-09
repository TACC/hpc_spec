#
# spec file for package libidn2
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


%define lname	libidn2-0
Name:           libidn2
Version:        2.0.4
Release:        3.1
Summary:        Support for Internationalized Domain Names (IDN) based on IDNA2008
License:        GPL-3.0+
Group:          Development/Libraries/C and C++
BuildRoot:      /var/tmp/%{name}-%{version}-buildroot
Url:            https://www.gnu.org/software/libidn/#libidn2
Source0:        https://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
Source1:        https://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz.sig
Source3:        baselibs.conf
BuildRequires:  libunistring-devel
BuildRequires:  pkgconfig
Requires(post): %{install_info_prereq}
%define         INSTALL_DIR /opt/%{name}/%{version}
%define         _prefix /usr
%define         _bindir %{_prefix}/bin
%define         _libdir %{_prefix}/lib
%define         _datadir %{_prefix}/share
%define         _infodir %{_prefix}/share/info
%define         _mandir %{_prefix}/share/man

%description
An implementation of the IDNA2008 specifications (RFCs 5890, 5891, 5892, 5893)

%package tools
Summary:        Command line utility to convert Int. Domain Names
Group:          Productivity/Networking/DNS/Utilities

%description tools
An implementation of the IDNA2008 specifications (RFCs 5890, 5891, 5892, 5893)

%package -n %{lname}
Summary:        Support for Internationalized Domain Names (IDN)
Group:          System/Libraries

%description -n %{lname}
An implementation of the IDNA2008 specifications (RFCs 5890, 5891, 5892, 5893)

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/C and C++
Requires:       %{lname} = %{version}

%description devel
An implementation of the IDNA2008 specifications (RFCs 5890, 5891, 5892, 5893)

%prep
%setup -q

%build
./configure \
    --prefix=%{INSTALL_DIR}/%{_prefix} \
    --disable-rpath \
    --disable-silent-rules \
    --disable-static \
    --disable-gtk-doc

make %{?_smp_mflags}

%install
##%define buildroot /var/tmp/%{name}-%{version}-buildroot 
###%make_install
make DESTDIR=%{buildroot} install
##find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name "*.la" -delete -print
# Do not bother with partial gtkdoc
##rm -rf %{buildroot}/%{_datadir}/gtk-doc/
rm -rf %{buildroot}/%{INSTALL_DIR}/%{_datadir}/gtk-doc/
rm -rf %{buildroot}/%{INSTALL_DIR}/%{_infodir}/dir

%check
make check %{?_smp_mflags}

%post tools
%install_info --info-dir=%{INSTALL_DIR}%{_infodir} %{INSTALL_DIR}%{_infodir}/libidn2.info.*

%preun tools
%install_info_delete --info-dir=%{INSTALL_DIR}%{_infodir} %{INSTALL_DIR}%{_infodir}/libidn2.info.*

%post -n %{lname} -p /sbin/ldconfig
%postun -n %{lname} -p /sbin/ldconfig

%files tools
%doc AUTHORS COPYING* ChangeLog NEWS README.md
%{INSTALL_DIR}%{_infodir}/libidn*
%{INSTALL_DIR}%{_bindir}/idn2
%{INSTALL_DIR}%{_mandir}/man1/idn2.1*

%files -n %{lname}
%{INSTALL_DIR}%{_libdir}/libidn2.so.*

%files devel
%{INSTALL_DIR}%{_libdir}/libidn2.so
%{INSTALL_DIR}%{_libdir}/pkgconfig/libidn2.pc
%{INSTALL_DIR}%{_includedir}/*.h
%{INSTALL_DIR}%{_mandir}/man3/*


##%{INSTALL_DIR}/bin/idn2
##%{INSTALL_DIR}/include/idn2.h
##%{INSTALL_DIR}/lib/libidn2.so
##%{INSTALL_DIR}/lib/libidn2.so.0
##%{INSTALL_DIR}/lib/libidn2.so.0.3.3
##%{INSTALL_DIR}/lib/pkgconfig/libidn2.pc
##%{INSTALL_DIR}/share/gtk-doc/html/libidn2/*
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/api-index-full.html
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/home.png
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/index.html
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/left-insensitive.png
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/left.png
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/libidn2-idn2.html
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/libidn2.devhelp2
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/libidn2.html
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/right-insensitive.png
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/right.png
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/style.css
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/up-insensitive.png
####%{INSTALL_DIR}/share/gtk-doc/html/libidn2/up.png
##%{INSTALL_DIR}/share/info/dir
##%{INSTALL_DIR}/share/info/libidn2.info
##%{INSTALL_DIR}/share/man/man1/idn2.1
##%{INSTALL_DIR}/share/man/man3/*
####%{INSTALL_DIR}/share/man/man3/idn2_check_version.3
####%{INSTALL_DIR}/share/man/man3/idn2_free.3
####%{INSTALL_DIR}/share/man/man3/idn2_lookup_u8.3
####%{INSTALL_DIR}/share/man/man3/idn2_lookup_ul.3
####%{INSTALL_DIR}/share/man/man3/idn2_register_u8.3
####%{INSTALL_DIR}/share/man/man3/idn2_register_ul.3
####%{INSTALL_DIR}/share/man/man3/idn2_strerror.3
####%{INSTALL_DIR}/share/man/man3/idn2_strerror_name.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_ascii_4i.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_ascii_4z.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_ascii_8z.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_ascii_lz.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_unicode_44i.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_unicode_4z4z.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_unicode_8z4z.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_unicode_8z8z.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_unicode_8zlz.3
####%{INSTALL_DIR}/share/man/man3/idn2_to_unicode_lzlz.3


%changelog
* Wed Aug 30 2017 astieger@suse.com
- update to 2.0.4:
  * Fix integer overflow in bidi.c/_isBidi() bsc#1056451
  * Fix integer overflow in puny_decode.c/decode_digit()
    bsc#1056450
  * Fix idna_free() to idn_free()
- enable documentation again
* Mon Jul 24 2017 astieger@suse.com
- update to 2.0.3:
  * %%IDN2_USE_STD3_ASCII_RULES disabled by default.
    Previously libidn2 was eliminating non-STD3 characters from
    domain strings such as _443._tcp.example.com, or IPs such as
    1.2.3.4/24 provided to libidn2 functions. That was an
    unexpected regression for applications switching from libidn
    and thus it is no longer applied by default.
    Use %%IDN2_USE_STD3_ASCII_RULES to enable that behavior again.
- disable documentation, does not build correctly
* Sat May 20 2017 astieger@suse.com
- update to 2.0.2:
  * Fix TR46 transitional mode
  * Fix several documentation issues
* Tue Apr 25 2017 pmonrealgonzalez@suse.com
- Sources updated from http://alpha.gnu.org to https://ftp.gnu.org
* Mon Apr 24 2017 pmonrealgonzalez@suse.com
- Update to version 2.0.1
- Version 2.0.1 (released 2017-04-22)
  * idn2 utility now using IDNA2008 + TR46 by default
- Version 2.0.0 (released 2017-03-29) [alpha]
  * Version numbering scheme changed
  * Added to ASCII conversion functions corresponding to libidn1
    functions:
  - idn2_to_ascii_4i		- idn2_to_ascii_4z
  - idn2_to_ascii_8z		- idn2_to_ascii_lz
  * Added to unicode conversion functions corresponding to libidn1
    functions:
  - idn2_to_unicode_8z4z	- idn2_to_unicode_4z4z
  - idn2_to_unicode_44i	- idn2_to_unicode_8z8z
  - idn2_to_unicode_8zlz	- idn2_to_unicode_lzlz
  * Including idn2.h will provide libidn1 compatibility functions
  unless IDN2_SKIP_LIBIDN_COMPAT is defined. That allows converting
  applications from libidn1 (which offers IDNA2003) to libidn2 (which
  offers IDNA2008) by replacing idna.h to idn2.h in the applications'
  source.
- Dropped patch not needed after revision
  * libidn2-no-examples-build.patch
* Thu Jan 19 2017 shshyukriev@suse.com
- Update to version 0.16
  * build: Fix idn2_cmd.h build rule.
  * API and ABI is backwards compatible with the previous version.
- Update to version 0.15 (released 2017-01-14)
  * Fix out-of-bounds read.
  * Fix NFC input conversion (regression).
  * Shrink TR46 static mapping data.
  * API and ABI is backwards compatible with the previous version.
- Update to version 0.14 (released 2016-12-30)
  * build: Fix gentr46map build.
  * API and ABI is backwards compatible with the previous version.
- Update to version 0.13:
  * build: Doesn't download external files during build.
  * doc: Clarify license.
  * build: Generate ChangeLog file properly.
  * doc: API documentation related to TR46 flags.
  * API and ABI is backwards compatible with the previous version.
- Update to version 0.12:
  * Builds/links with libunistring.
  * Fix two possible crashes with unchecked NULL pointers.
  * Memleak fix.
  * Binary search for codepoints in tables.
  * Do not taint output variable on error in idn2_register_u8().
  * Do not taint output variable on error in idn2_lookup_u8().
  * Update to Unicode 6.3.0 IDNA tables.
  * Add TR46 / UTS#46 support to API and idn2 utility.
  * Add NFC quick check.
  * Add make target 'check-coverage' for test coverage report.
  * Add tests to increase test code coverage.
  * API and ABI is backwards compatible with the previous version.
* Thu Dec  8 2016 astieger@suse.com
- update to 0.11:
  * Fix stack underflow in 'idn2' command line tool. [boo#1014473]
  * Fix gdoc script to fix texinfo syntax error.
  * API and ABI is backwards compatible with the previous version.
* Fri Oct 21 2016 tchvatal@suse.com
- Convert to libidn2 package started to being used, namely by curl
- Alternative implementation based on new specification from 2008
  + completely different codebase with no ties to libidn
* Wed Jul 20 2016 astieger@suse.com
- libidn 1.33:
  * bnc#990189 CVE-2015-8948 CVE-2016-6262
  * bnc#990190 CVE-2016-6261
  * bnc#990191 CVE-2016-6263
  * libidn: Fix out-of-bounds stack read in idna_to_ascii_4i.
  * idn: Solve out-of-bounds-read when reading one zero byte as input.
  * libidn: stringprep_utf8_nfkc_normalize reject invalid UTF-8.
* Thu Aug 13 2015 mpluskal@suse.com
- Update to 1.32
  * libidn: Fix crash in idna_to_unicode_8z8z and
    idna_to_unicode_8zlz. This problem was introduced in 1.31.
  * API and ABI is backwards compatible with the previous version.
- Update gpg keyring
* Thu Jul  9 2015 tchvatal@suse.com
- Add Apache-2.0 license to the license line. Under this is the
  java code, but we don't build it -> just the sources license
* Thu Jul  9 2015 tchvatal@suse.com
- Version bump to 1.31:
  * Fixes bnc#923241 CVE-2015-2059 out-of-bounds read with stringprep on
    invalid UTF-8
  * Few other triv changes
* Fri Mar 13 2015 tchvatal@suse.com
- Version bump to 1.30:
  * punycode.{c,h} files were reimported
- Cleanup with spec-cleaner
* Mon Oct 20 2014 i@marguerite.su
- update version 1.29:
  * libidn: Mark internal variable "g_utf8_skip" as static.
  * idn: Flush stdout to simplify for tools that buffer too heavily.
  * i18n: Added Brazilian Portuguese translation.
  * Update gnulib files.
  * API and ABI is backwards compatible with the previous version.
* Thu Dec 19 2013 coolo@suse.com
- disable gpg-offline again to avoid build cycles
* Wed Dec 18 2013 mvyskocil@suse.com
- Verify source tarball via gpg-offline
* Sat Dec 14 2013 uweigand@de.ibm.com
- Fix gnulib test failure due to SUSE_ASNEEDED.
* Mon Sep 23 2013 tchvatal@suse.com
- Version bump to 1.28:
  * java buildfixes
  * translation updates
  * improved unit-tests
  * for more read NEWS file
* Fri Sep 21 2012 jengelh@inai.de
- Employ shared library package naming
* Tue Jun  5 2012 vdziewiecki@suse.com
-Update to 1.25:
  * MSVC: Build fixes related to _GL_ATTRIBUTE_CONST and
    _GL_ATTRIBUTE_PURE.
    Reported by Bartosz Brachaczek <b.brachaczek@gmail.com>.
  * examples: Fix compiler warning about ignoring return value from
    fgets.
  * tests: Ship with a valgrind suppressions file for the strlen
    issue.
  * Update gnulib files and translations.
  * API and ABI is backwards compatible with the previous version.
* Sun May 13 2012 Nico.Laus.2001@gmx.de
- Upgrade to version 1.24
  * Libraries are re-licensed from LGPLv2+ to dual-GPLv2+|LGPLv3+.
  * build: Fix parallel Windows builds.
    Reported by René Berber
  * libidn: Fix potential infloop in pr29 code.
    Reported by Jon Nelson <address@hidden> in
    http://lists.gnu.org/archive/html/help-libidn/2012-01/msg00008.html
  * libidn: Add 'const' keyword to 'stringprep_ucs4_nfkc_normalize' function.
  * Sync glib NFKC code and improve copyright/license statements.
  * Update gnulib files and translations.
  * API and ABI is backwards compatible with the previous version.
* Mon Dec 26 2011 jengelh@medozas.de
- Remove redundant tags/sections
* Mon Dec 26 2011 crrodriguez@opensuse.org
- fix URL
* Mon Dec 26 2011 crrodriguez@opensuse.org
- Update to version 1.23
- Run spec cleaner
* Sat Oct  1 2011 crrodriguez@opensuse.org
- Do not build gtk-docs
- make check hangs in qemu-arm, workaround the bugs.
* Fri Jun 10 2011 andrea.turrini@gmail.com
- Fixed typo in description of libidn.spec
* Sat May  7 2011 crrodriguez@opensuse.org
- Upgrade to version 1.22
  * Fix memory leak when idna_to_ascii_4i fails
  * Fix ToUnicode case-insensitivity bug
  * Avoid some warnings to make it build with modern gcc on amd64.
* Tue Dec 15 2009 jengelh@medozas.de
- add baselibs.conf as a source
* Tue Oct  6 2009 crrodriguez@opensuse.org
- update to version 1.15
  * support GCC visibility features
* Wed Jan  7 2009 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Tue Oct 14 2008 crrodriguez@suse.de
- disable static libraries
* Tue Oct  7 2008 stbinner@suse.de
- update to 1.10:
  * idn: accept -n as short form for --nfkc.
  * Fix compiler warnings, updated gnulib files and translations
* Mon Jul 21 2008 stbinner@suse.de
- update to 1.9:
  * idn: fix error message when NFKC fails, and other translations
  * Remove more non-free text from doc/specifications/rfc3454.txt.
* Thu Apr 24 2008 stbinner@suse.de
- update to 1.8: no functional changes
* Mon Apr 14 2008 stbinner@suse.de
- update to 1.7:
  * new parameter --nfkc to process string with Unicode v3.2 NFKC
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Tue Mar 25 2008 stbinner@suse.de
- update to 1.6:
  * Remove non-free portions of doc/specifications/rfc3454.txt.
  * Doc fixes in IDNA to clarify that some functions operate on
    just one domain labels and some operate on domain name (which
    can contain several domain labels).
* Tue Mar 18 2008 crrodriguez@suse.de
- remove "la" file with empty dependency_libs
* Wed Feb 27 2008 stbinner@suse.de
- update to 1.5:
  * Don't include wchar.h in idn-int.h.
  * Added appendix 'On Label Separators' to the manual.
  * Improved rendering of non-ASCII in the info manual.
  * Fix non-portable use of brace expansion in makefiles.
  * Update translations.
* Sun Jan 27 2008 stbinner@suse.de
- update to 1.4: updated translations and fix of --version/--help
* Fri Aug  3 2007 stbinner@suse.de
- update to 1.0:
  * Command-line tools, examples, etc are now licensed under GPLv3
  * The library is still licensed under LGPL v2.1 for compatibility
    reasons (it is included in glibc).
  * Updated gnulib files and translations
* Tue Jul 17 2007 stbinner@suse.de
- update to 0.6.14:
  * Documentation fixes
  * Install images for the manual in $infodir
  * Updated gnulib files
  * Use AM_JAVACFLAGS instead of JAVACFLAGS in java/misc/Makefile.am
* Thu Mar 29 2007 rguenther@suse.de
- add emacs site-lisp directories.
* Wed Mar 14 2007 stbinner@suse.de
- update to 0.6.11:
  * The C# Libidn port was updated.
  * The Java code has been fixed to properly translate any
    non-ASCII dot into ".".
* Thu Oct 19 2006 stbinner@suse.de
- update to 0.6.8:
  * The gnulib directory is separated into two directories.
  * Update gnulib files.
  * Some minor cleanups, like assuming locale.h and setlocale().
  * API and ABI is backwards compatible with the previous version.
* Thu Sep 14 2006 stbinner@suse.de
- update to 0.6.7:
  * Fix build failure of idn-int.h on C99 platforms.
  * The manual includes GPL license, for the command-line tools.
  * The function, variable and concept index is moved to the end
    of the manual.
  * Update of gnulib files and translations
* Wed Aug 23 2006 stbinner@suse.de
- update to 0.6.6
  * Instead of AX_CREATE_STDINT_H, use the stdint gnulib module,
    for idn-int.h.
  * Update gnulib files.
  * Updated translations.
* Thu Aug 17 2006 aj@suse.de
- Remove unneccasary BuildRequires.
* Mon Jul 10 2006 stbinner@suse.de
- update to 0.6.5
  * links the library with an external libintl for gettext
  * updates the doxygen configuration file to version 1.4.7
  * translation of error messages was fixed
  * warnings on 64-bit platforms were fixed
* Mon May 22 2006 stbinner@suse.de
- update to 0.6.3
  * Fix objdir != srcdir builds for the Java documentation.
  * Update of gnulib files.
  * Make it possible to cross-compile to mingw32.
  * Minor changes in how the C# code is built.
* Thu Jan 26 2006 sbrabec@suse.cz
- Added %%install_info_prereq.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Sat Dec  3 2005 coolo@suse.de
- update to 0.6.0
* Wed Aug  3 2005 coolo@suse.de
- move .la file to -devel package
* Fri Jan 21 2005 coolo@suse.de
- update to 0.5.9
* Thu Oct 14 2004 coolo@suse.de
- update to 0.5.8
* Fri Aug  6 2004 coolo@suse.de
- update to 0.5.3 (integrating schwab's patch)
* Thu Aug  5 2004 coolo@suse.de
- update to 0.5.2
* Sat Jul  3 2004 schwab@suse.de
- Fix invalid free.
* Tue Jun  1 2004 coolo@suse.de
- update to 0.4.8
* Thu Mar  4 2004 coolo@suse.de
- fixing file list and requires
* Wed Feb  4 2004 coolo@suse.de
- update to 0.3.7
* Thu Oct 16 2003 coolo@suse.de
- build as user
* Fri Sep 26 2003 coolo@suse.de
- update to 0.3
* Wed Aug 20 2003 coolo@suse.de
- update to 0.2.2
* Wed Jul 23 2003 coolo@suse.de
- update to 0.2.1
* Tue Jun  3 2003 coolo@suse.de
- Initial package
