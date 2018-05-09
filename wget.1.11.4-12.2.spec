#
# spec file for package wget (Version 1.11.4)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

# norootforbuild


Name:           wget
BuildRequires:  libpng-devel openssl-devel
Url:            http://www.gnu.org/software/wget/
License:        GPLv3+
Group:          Productivity/Networking/Web/Utilities
AutoReqProv:    on
Version:        1.11.4
Release:        12.2.2
Summary:        A Tool for Mirroring FTP and HTTP Servers
Packager:       TACC - cproctor@tacc.utexas.edu
Source:         %name-%version.tar.bz2
Patch1:         wgetrc.patch
Patch2:         wget-nullcerts.patch
Patch100:       certs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
PreReq:         %install_info_prereq
PreReq:         tacc-openssl

%description
Wget enables you to retrieve WWW documents or FTP files from a server.
This can be done in script files or via the command line.



Authors:
--------
    Hrvoje Niksic <hniksic@srce.hr>

%prep
%setup -q
%patch1
%patch2
%patch100

%build
./autogen.sh
export PATH=/opt/openssl/1.0.2o/usr/bin:$PATH
export LD_LIBRARY_PATH=/opt/openssl/1.0.2o/usr/lib:$LD_LIBRARY_PATH
export LDFLAGS="-Wl,-rpath=/opt/openssl/1.0.2o/usr/lib -L/opt/openssl/1.0.2o/usr/lib"
export CPPFLAGS="-I/opt/openssl/1.0.2o/usr/include"
%configure --with-libssl-prefix=/opt/openssl/1.0.2o
make %{?jobs:-j%jobs}

%install
make DESTDIR=$RPM_BUILD_ROOT install
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT;

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README MAILING-LIST 
%doc doc/sample.wgetrc util/rmold.pl
%{_mandir}/*/wget*
%{_infodir}/wget*
%config(noreplace) %{_sysconfdir}/wgetrc
%{_bindir}/*

%changelog
* Wed Dec 16 2009 jengelh@medozas.de
- Enable parallel building
* Tue Aug 11 2009 max@suse.de
- Fix vulnerability against SSL certificates with a zero byte in
  the common name field (wget-nullcerts.patch, bnc#528298).
* Mon Sep  1 2008 max@suse.de
- New version 1.11.4:
  * Fixed a problem in authenticating over HTTPS through a proxy.
    (Regression in 1.11 over 1.10.2.)
  * The combination of -r or -p with -O, which was disallowed in 1.11,
    has been downgraded to a warning in 1.11.2.
  * Further improvements to progress bar displays in non-English
    locales (too many spaces could be inserted, causing the display to
    scroll).
  * Successive invocations of Wget on FTP URLS, with
  - -no-remove-listing and --continue, was causing Wget to append,
    rather than replace, information in the .listing file, and thereby
    download the same files multiple times. Fixed in 1.11.2.
  * Wget 1.11 no longer allowed ".." to persist at the beginning of
    URLs, for improved conformance with RFC 3986. However, this
    behavior presents problems for some FTP setups, and so they are now
    preserved again, for FTP URLs only.
  * Downgraded -N with -O to a warning, rather than an error.
  * Fixed a crash on some systems, due to Wget casting a
    pointer-to-long to a pointer-to-time_t.
  * Fixed an issue (apparently a regression) where -O would refuse to
    download when -nc was given, even though the file didn't exist.
  * Fixed a situation where Wget could abort with --continue if the
    remote server gives a content-length of zero when the file exists
    locally with content.
* Wed Apr 30 2008 max@suse.de
- Let the resolver (/etc/gai.conf) decide whether to prefer IPv4
  or IPv6 if a host has addresses of both kinds (bnc#310224).
- Passive FTP is the default now, so we don't need to set it
  explicitly anymore.
* Wed Apr 23 2008 max@suse.de
- New version 1.11.1:
  * Migration to the GPLv3+ license.
  * Improvements to the HTTP password authentication code, bringing
    it a little closer to RFC compliance (more is needed).
  * Basic support for respecting filenames specified via
    `Content-Disposition' headers (turned on with --content-disposition,
    but please read the documentation).
  * An --ignore-case option to make wildcard- and suffix-matching
    case-sensitive.
  * Progress bar now displays correctly in non-English locales (and a
    related assertion failure was fixed).
  * Added option --auth-no-challenge, to support broken pre-1.11
    authentication-before-server-challenge, which turns out to still
    be useful for some limited cases.
  * Documentation of accept/reject lists in the manual's "Types of
    Files" section now explains various aspects of their behavior that
    may be surprising, and notes that they may change in the future.
  * Documentation of --no-parents now explains how a trailing slash,
    or lack thereof, in the specified URL, will affect behavior.
- Purged lots of obsolete patches and cleaned up the spec file.
* Sun Feb 24 2008 crrodriguez@suse.de
- make use of find_lang macro
* Wed Mar 28 2007 max@suse.de
- Fixes a null pointer dereference (#231063, CVE-2006-6719)
* Thu Jun 22 2006 max@suse.de
- Removed the unneeded fix for CAN-2004-1487
  (bugs #179369 and #185214).
- Filter escape responses from the HTTP server (CAN-2004-1488,
  bug #185265).
* Wed Feb  1 2006 max@suse.de
- Fixed (hacked) restart of interrupted FTP transactions (#144410).
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 16 2006 mmj@suse.de
- Compile with -fstack-protector
* Fri Oct 14 2005 mmj@suse.de
- Update to wget 1.10.2
* Mon Sep 19 2005 mmj@suse.de
- Fix strict aliasing issues
* Tue Aug 30 2005 mmj@suse.de
- Update to wget-1.10.1 which is a bugfix release [#113682]
* Mon Jun 13 2005 mmj@suse.de
- Update to wget-1.10 which has LFS and non-experimental IPv6,
  among many other improvements and bugfixes
* Tue Apr 26 2005 mmj@suse.de
- Fix the way fnmatch matches [#75791]
* Fri Apr  8 2005 mmj@suse.de
- Add sanitizing URLs patch
- Add other patches
* Thu Mar 31 2005 mmj@suse.de
- Don't double UTF-8 encode german messages [#74544]
* Fri Feb 11 2005 mmj@suse.de
- Roll back to wget-1.9.1 since the wget tree with LFS support is
  too buggy. We rather want a functioning wget. [#47965]
* Mon Jan 31 2005 ro@suse.de
- texi2html changed behaviour, adapt filelist
* Thu Dec  2 2004 mmj@suse.de
- Update to 20041113 wget-LFS snapshot
- Fix NULL pointer assertion [#48748]
* Mon Nov 15 2004 mmj@suse.de
- Use another version of the fix below
* Sun Nov 14 2004 mmj@suse.de
- Add fix for using proxies [#47965]
* Mon Oct 18 2004 mmj@suse.de
- locale no should correctly be nb so rename po/no* to po/nb*
* Mon Sep 27 2004 mmj@suse.de
- Use LFS patch from Leonid Petrov [#37967] [#45084]
* Mon Jun 28 2004 mmj@suse.de
- Fix what appears to be a copy/paste error in the dual-family
  IPv4+IPv6 patch [#42503].
* Thu Apr  1 2004 mmj@suse.de
- Enable download of files > 2 GB [#37967]
- Remove old crufty comments
* Fri Feb 20 2004 pth@suse.de
- Correctly set the charset for de.po to utf-8. Fixes #34708.
* Sun Feb  1 2004 mmj@suse.de
- Update to 1.9.1 which is a bugfix release
* Sat Jan 10 2004 adrian@suse.de
- build as user
* Tue Oct 28 2003 mmj@suse.de
- Add patch for dual-family IPv4+IPv6 support from Ari Edelkind
* Mon Oct 27 2003 mmj@suse.de
- Update to version 1.9 and remove patches, which was included
  upstream. 1.9 news:
  o specify what POST method be used for HTTP
  o IPv6 support is available, although it's still experimental
  o The `--timeout' option now also affects DNS lookup and
    establishing the TCP connection
  o Download speed shown by the progress bar is based on the data
    recently read, rather than the average speed of the entire
    download
  o It is now possible to connect to FTP servers through FWTK
    firewalls
  o The new option `--retry-connrefused' makes Wget retry
    downloads even in the face of refused connections
  o The new option `--dns-cache=off' may be used to prevent Wget
    from caching DNS lookups
  o Wget no longer escapes characters in local file names based
    on whether they're appropriate in URLs
  o Handling of HTML comments has been dumbed down to conform to
    what users expect and other browsers do: instead of being
    treated as SGML declaration, a comment is terminated at the
    first occurrence of "-->"
  o Wget now correctly handles relative URIs that begin with "//"
  o Boolean options in `.wgetrc' and on the command line now
    accept values "yes" and "no" along with the traditional "on"
    and "off"
  o It is now possible to specify decimal values for timeouts,
    waiting periods, and download rate.
* Tue Jul 15 2003 pthomas@suse.de
- Add security fix to unconditionally terminate the filename
  in url.c(compose_file_name).
* Thu Apr 24 2003 ro@suse.de
- fix install_info --delete call and move from preun to postun
* Tue Apr  1 2003 schwab@suse.de
- Define _GNU_SOURCE to fix missing declarations.
* Fri Mar  7 2003 ro@suse.de
- fix build with current autoconf
* Thu Mar  6 2003 pthomas@suse.de
- Add missing change log entry.
* Wed Mar  5 2003 pthomas@suse.de
- Add security fix that makes wget check for '..' and '/' in
  file names.
* Wed Feb 12 2003 kukuk@suse.de
- Remove ps and pdf documenation, info, man and html are enough.
  [Bug #23592]
* Tue Feb 11 2003 mmj@suse.de
- Use %%install_info macro [#23468]
- Don't remove $RPM_BUILD_ROOT without checking it's not "/"
* Thu Oct 24 2002 pthomas@suse.de
- Change wgetrc to make wget use passive_ftp per default.
* Wed Aug  7 2002 mmj@suse.de
- Update to 1.8.2 which is a bugfix release.
* Wed Jul 10 2002 okir@suse.de
- added patch for IPv6 support
* Tue May 14 2002 meissner@suse.de
- replaced assert msecs>=0 by if (msecs<0) msecs=0. (stupid assert)
* Fri Feb  1 2002 ro@suse.de
- changed neededforbuild <libpng> to <libpng-devel-packages>
* Mon Jan 14 2002 bk@suse.de
- marked wgetrc as noreplace, format is compatible to older versions
* Mon Jan  7 2002 pthomas@suse.de
- Upgrade to 1.8.1
* Thu Dec 13 2001 pthomas@suse.de
- Upgrade to 1.8
- Regenerate pdf_doc.diff
- Drop ppc specific patch as it's not needed anymore.
- Install all HTML pages and not only the table of contents.
- Pass DESTDIR on from the toplevel Makefile.
* Mon Aug 20 2001 olh@suse.de
- add wget-1.7.ppc.diff to fix segfault on ppc
* Fri Jun  8 2001 pthomas@suse.de
- Upgrade to 1.7.
- Add a target to doc/Makefile to build a PDF version of the
  documentation.
- Compile with SSL support (for HTTPS).
* Fri May 25 2001 bjacke@suse.de
- apply and enable IPv6 patch
- add Debian's manpage
* Thu May 10 2001 mfabian@suse.de
- bzip2 sources
* Fri Mar 30 2001 pthomas@suse.de
- Apply my patch accepted for wget 1.7 that replaces ctype.h
  with safe-ctype.h, a locale independent version of ctype.h
  taken from libiberty. This makes setting LC_CTYPE safe.
* Thu Mar  8 2001 ke@suse.de
- Build and install a printable manual (PDF).
* Thu Mar  1 2001 pthomas@suse.de
- Set LC_CTYPE along with LC_MESSAGES to correctly display
  messages in locales other then C/POSIX.
* Wed Feb 14 2001 schwab@suse.de
- Fix large file support (#2647).
* Mon Jan 22 2001 ke@suse.de
- Update to version 1.6.
- wget.spec: Use proper rpm macros.
- Add README.SuSE
- Drop security patch (cf. 1999-02-09 and README.SuSE); not needed any
  longer.
- Lost large file support (cf. README.SuSE); reopen #2647.
* Fri Jun  9 2000 schwab@suse.de
- Change all values that count bytes from long to unsigned long (#2647).
* Sun Feb 20 2000 ke@suse.de
- General spec file cleanup:
- add group tag.
- use various macros (%%{version}, %%{_infodir}).
- ./configure -> %%build.
* Sat Oct  2 1999 ke@suse.de
- Add more PO files from
  http://www.iro.umontreal.ca/~pinard/po/HTML/domain-wget.html.
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Tue Feb  9 1999 ke@suse.de
- Security fix (proposed by marc).
* Sun Jan 17 1999 ke@suse.de
- apply patch (new de.po).
- fix BuildRoot.
* Thu Sep 24 1998 ke@suse.de
- Update: wget-1.5.3 (bug fix release).
* Fri Jun 26 1998 ke@suse.de
- Update: wget-1.5.2 (bug fix release).
- Make BuildRoot work.
* Tue May 12 1998 ke@suse.de
- update: wget-1.5.1 (bug fix release).
* Fri Apr 24 1998 ke@suse.de
- enable NLS.
* Thu Apr 23 1998 ke@suse.de
- update: wget-1.5.0.
* Sat Jun 21 1997 Karl Eichwalder  <ke@suse.de>
  * patch from Hrvoje Niksic to prevent crashes if you are using
  proxy authorization.
* Mon May 19 1997 Karl Eichwalder  <ke@suse.de>
  * new package: wget-1.4.5
