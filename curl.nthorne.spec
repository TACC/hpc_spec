#
# spec file for package curl (Version 7.20.1)
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%bcond_without openssl
%bcond_with mozilla_nss
#%bcond_without testsuite
%bcond_with testsuite

Name:           curl
BuildRequires:  libidn-devel openldap2-devel pkg-config zlib-devel
%if %{with openssl}
BuildRequires:  openssl-devel
%endif
%if %{with mozilla_nss}
BuildRequires:  mozilla-nss-devel
%endif
%if 0%{suse_version} > 930
BuildRequires:  krb5-devel
%else
BuildRequires:  heimdal-devel
%endif
BuildRequires:  libssh2-devel openssh
%if 0%{?_with_stunnel:1}
# used by the testsuite
BuildRequires:  stunnel
%endif
#define cvs_suffix -20090302
Version:        7.20.1
Release:        3.4.1

AutoReqProv:    on
# bug437293
%ifarch ppc64
Obsoletes:      curl-64bit
%endif
#
License:        BSD3c(or similar) ; MIT License (or similar)
Group:          Productivity/Networking/Web/Utilities
Summary:        A Tool for Transferring Data from URLs
Url:            http://curl.haxx.se/
Packager:       TACC - cproctor@tacc.utexas.edu
Source:         curl-%version%{?cvs_suffix}.tar.bz2
Source2:        baselibs.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
PreReq:         tacc-openssl

%description
Curl is a client to get documents and files from or send documents to a
server using any of the supported protocols (HTTP, HTTPS, FTP, FTPS,
TFTP, DICT, TELNET, LDAP, or FILE). The command is designed to work
without user interaction or any kind of interactivity.

%package -n libcurl4
License:        BSD3c(or similar) ; MIT License (or similar)
Summary:        cURL shared library version 4
Group:          Productivity/Networking/Web/Utilities

%description -n libcurl4
cURL shared library version 4.

%package -n libcurl-devel
License:        BSD3c(or similar) ; MIT License (or similar)
Summary:        A Tool for Transferring Data from URLs
Group:          Development/Libraries/C and C++
Requires:       libcurl4 = %{version} glibc-devel
# curl-devel (v 7.15.5) was last used in 10.2
Provides:       curl-devel <= 7.15.5
Obsoletes:      curl-devel < 7.16.2

%description -n libcurl-devel
Curl is a client to get documents and files from or send documents to a
server using any of the supported protocols (HTTP, HTTPS, FTP, GOPHER,
DICT, TELNET, LDAP, or FILE). The command is designed to work without
user interaction or any kind of interactivity.

%prep
%setup -q -n curl-%version%{?cvs_suffix}

%build
# local hack to make curl-config --libs stop printing libraries it depends on
# (currently, libtool sets link_all_deplibs=(yes|unknown) everywhere,
# will hopefully change in the future)
sed -i 's/link_all_deplibs=unknown/link_all_deplibs=no/' configure
export CFLAGS="$RPM_OPT_FLAGS"
export PATH=/opt/openssl/1.0.2o/usr/bin:$PATH
export LD_LIBRARY_PATH=/opt/openssl/1.0.2o/usr/lib:$LD_LIBRARY_PATH
export LDFLAGS="-Wl,-rpath=/opt/openssl/1.0.2o/usr/lib -L/opt/openssl/1.0.2o/usr/lib"
export CPPFLAGS="-I/opt/openssl/1.0.2o/usr/include"

./configure \
	--prefix=%{_prefix} \
	--enable-ipv6 \
%if %{with openssl}
	--with-ssl=/opt/openssl/1.0.2o \
	--with-ca-path=/etc/ssl/certs/ \
%else
	--without-ssl \
%if %{with mozilla_nss}
	--with-nss \
%endif
%endif
%if %suse_version > 930
	--with-gssapi=/usr/lib/mit \
%else
	--with-gssapi=/usr/lib/heimdal \
%endif
	--with-libssh2\
	--libdir=%{_libdir} \
	--enable-hidden-symbols \
	--disable-static
: if this fails, the above sed hack did not work
./libtool --config | grep -q link_all_deplibs=no
# enable-hidden-symbols needs gcc4 and causes that curl exports only its API
make %{?jobs:-j%jobs}

%if %{with testsuite}

%check
cd tests
make
# make sure the testsuite runs don't race on MP machines in autobuild
if test -z "$BUILD_INCARNATION" -a -r /.buildenv; then
	. /.buildenv
fi
if test -z "$BUILD_INCARNATION"; then
	BUILD_INCARNATION=0
fi
base=$((8990 + $BUILD_INCARNATION * 20))
perl ./runtests.pl -a -b$base || {
%if 0%{?curl_testsuite_fatal:1}
	exit
%else
	echo "WARNING: runtests.pl failed with code $?, continuing nevertheless"
%endif
}
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
rm $RPM_BUILD_ROOT%_libdir/libcurl.la
install -d $RPM_BUILD_ROOT/usr/share/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT/usr/share/aclocal/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libcurl4 -p /sbin/ldconfig

%postun -n libcurl4 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README RELEASE-NOTES
%doc docs/{BUGS,FAQ,FEATURES,MANUAL,RESOURCES,TODO,TheArtOfHttpScripting}
%doc lib/README.curl_off_t
%{_prefix}/bin/curl
%doc %{_mandir}/man1/curl.1.gz

%files -n libcurl4
%defattr(-,root,root)
%{_libdir}/libcurl.so.4*

%files -n libcurl-devel
%defattr(-,root,root)
%{_prefix}/bin/curl-config
%{_prefix}/include/curl
%{_prefix}/share/aclocal/libcurl.m4
%{_libdir}/libcurl.so
%{_libdir}/pkgconfig/libcurl.pc
%doc %{_mandir}/man1/curl-config.1.gz
%doc %{_mandir}/man3/*
%doc docs/libcurl/symbols-in-versions

%changelog
* Wed Jun  2 2010 lnussel@suse.de
- allowing switching to nss instead of openssl via bcond
* Mon May 10 2010 crrodriguez@opensuse.org
- disable c-ares support while bnc598574 is fixed.
* Sat Apr 24 2010 coolo@novell.com
- buildrequire pkg-config to fix provides
* Fri Apr 23 2010 crrodriguez@opensuse.org
- Update to libcurl 7.20.1
  * off-by-one in the chunked encoding trailer parser
  * CURLOPT_CERTINFO memory leak
  * threaded resolver double free when closing curl handle
  * url_multi_remove_handle() caused use after free
  * SSL possible double free when reusing curl handle
  * alarm()-based DNS timeout bug
* Wed Mar 24 2010 crrodriguez@opensuse.org
- enable libssh2 support unconditionally.
* Wed Mar 10 2010 crrodriguez@opensuse.org
- enable libcares support unconditionally.
* Sat Feb 13 2010 dimstar@opensuse.org
- Update to version 7.20.0:
  * support SSL_FILETYPE_ENGINE for client certificate
  * curl-config can now show the arguments used when building curl
  * non-blocking TFTP
  * send Expect: 100-continue for POSTs with unknown sizes
  * added support for IMAP(S), POP3(S), SMTP(S) and RTSP
  * added new curl_easy_setopt() options for SMTP and RTSP
  * added --mail-from and --mail-rcpt for SMTP
  * VMS build system enhancements
  * added support for the PRET ftp command
  * curl supports --ssl and --ssl-reqd
  * added -J/--remote-header-name for using server-provided
    filename with -O
  * enhanced asynchronous DNS lookups
  * symbol CURL_FORMAT_OFF_T is obsoleted
  * many bugfixes
* Tue Jan 26 2010 mmarek@suse.cz
- updated to 7.19.7
  * -T. is now for non-blocking uploading from stdin
  * SYST handling on FTP for OS/400 FTP server cases
  * libcurl refuses to read a single HTTP header longer than 100K
  * added the --crlfile option to curl
  * many bugfixes
* Mon Jan 11 2010 meissner@suse.de
- add baselibs.conf as source
* Thu Aug 13 2009 mmarek@suse.cz
- updated to 7.19.6
  * CURLOPT_FTPPORT (and curl's -P/--ftpport) support port ranges
  * Added CURLOPT_SSH_KNOWNHOSTS, CURLOPT_SSH_KEYFUNCTION,
    CURLOPT_SSH_KEYDATA
  * CURLOPT_QUOTE, CURLOPT_POSTQUOTE and CURLOPT_PREQUOTE can be
    told to ignore error responses when used with FTP
  * fixed CVE-2009-2417 (matching certificates with embedded NUL
    bytes)
  * many other bugfixes
* Tue May 19 2009 mmarek@suse.cz
- remove the Obsoletes: curl-ca-bundle, it breaks parallel
  installation of older libcurl packages (bnc#484044).
* Tue May 19 2009 mmarek@suse.cz
- updated to 7.19.5
  * libcurl now closes all dead connections whenever you attempt to
    open a new connection
  * libssh2's version number can now be figured out run-time
    instead of using the build-time fixed number
  * CURLOPT_SEEKFUNCTION may now return CURL_SEEKFUNC_CANTSEEK
  * curl can now upload with resume even when reading from a pipe
  * a build-time configured curl_socklen_t is now used instead of
    socklen_t
- by default, don't abort if the testsuite fails.
* Thu Mar  5 2009 mmarek@suse.cz
- don't run autoreconf -fi as it breaks on older distros and
  upstream uses recent autotools already.
* Mon Mar  2 2009 mmarek@suse.cz
- updated to 7.19.4
  * don't follow redirects to file:// and scp:// by default; add
    new curl_easy_setopt options CURLOPT_PROTOCOLS and
    CURLOPT_REDIR_PROTOCOLS to specify which protocols are allowed
    and which protocols are allowed to redirect to (bnc#475103,
    CVE-2009-0037)
  * Added CURLOPT_NOPROXY and the corresponding --noproxy
  * the OpenSSL-specific code disables TICKET (rfc5077) which is
    enabled by default in openssl 0.9.8j
  * Added CURLOPT_TFTP_BLKSIZE
  * Added CURLOPT_SOCKS5_GSSAPI_SERVICE and
    CURLOPT_SOCKS5_GSSAPI_NEC - with the corresponding curl options
  - -socks5-gssapi-service and --socks5-gssapi-nec
  * Improved IPv6 support when built with with c-ares >= 1.6.1
  * Added CURLPROXY_HTTP_1_0 and --proxy1.0
  * Added docs/libcurl/symbols-in-versions
  * Added CURLINFO_CONDITION_UNMET
  * Added support for Digest and NTLM authentication using GnuTLS
  * CURLOPT_FTP_CREATE_MISSING_DIRS can now be set to 2 to retry
    the CWD even when MKD fails
  * GnuTLS initing moved to curl_global_init()
  * CURLAUTH_DIGEST_IE bit added for CURLOPT_HTTPAUTH and
    CURLOPT_PROXYAUTH
  * pkg-config can now show supported_protocols and
    supported_features
  * Added CURLOPT_CERTINFO and CURLINFO_CERTINFO
  * Added CURLOPT_POSTREDIR
  * Better detect HTTP 1.0 servers and don't do HTTP 1.1 requests
    on them
  * configure --disable-proxy disables proxy support
  * Added CURLOPT_USERNAME and CURLOPT_PASSWORD
  * --interface now works with IPv6 connections on glibc systems
  * Added CURLOPT_PROXYUSERNAME and CURLOPT_PROXYPASSWORD
* Wed Dec 10 2008 olh@suse.de
- use Obsoletes: -XXbit only for ppc64 to help solver during distupgrade
  (bnc#437293)
* Thu Oct 30 2008 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Mon Sep 15 2008 mmarek@suse.cz
- only buildrequire stunnel when built --with stunnel
* Thu Sep 11 2008 mmarek@suse.cz
- test 279 no longer fails with runtests.pl -b <num>
* Tue Sep  2 2008 mmarek@suse.cz
- updated to 7.19.0
  * curl_off_t gets its size/typedef somewhat differently than
    before. This _may_ cause an ABI change for you. See
    /usr/share/doc/packages/curl/README.curl_off_t for a full
    explanation. (Should not affect our package as it has LFS
    enabled)
  * Added CURLINFO_PRIMARY_IP
  * Added CURLOPT_CRLFILE and CURLE_SSL_CRL_BADFILE
  * Added CURLOPT_ISSUERCERT and CURLE_SSL_ISSUER_ERROR
  * curl's option parser for boolean options reworked
  * Added --remote-name-all
  * Added CURLINFO_APPCONNECT_TIME
  * Added test selection by key word in runtests.pl
  * the curl tool's -w option support the %%{ssl_verify_result}
    variable
  * Added CURLOPT_ADDRESS_SCOPE and scope parsing of the URL
    according to RFC4007
  * Support --append on SFTP uploads (not with OpenSSH, though)
  * Added curlbuild.h and curlrules.h to the external library
    interface
  * lots of bugfixes
* Wed Jun  4 2008 mmarek@suse.cz
- updated to 7.18.2
  * CURLFORM_STREAM was added
  * CURLOPT_NOBODY is now supported over SFTP
  * curl can now run on Symbian OS
  * curl -w redirect_url and CURLINFO_REDIRECT_URL
  * added curl_easy_send() and curl_easy_recv()
  * some bugfixes
* Sat May 17 2008 coolo@suse.de
- fix renaming of xxbit packages
* Mon Apr 28 2008 mmarek@suse.cz
- disable c-ares support again until bnc#381709 is fixed
- build with libssh2 support in the devel:libraries:c_c++ project
* Fri Apr 11 2008 mmarek@suse.cz
- build with c-ares support
- fixed build for older dists
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Wed Apr  2 2008 mmarek@suse.de
- obsolete curl-ca-bundle by the library package
* Mon Mar 31 2008 mmarek@suse.cz
- updated to 7.18.1
  * minor fixes since last update
* Fri Mar 21 2008 mmarek@suse.cz
- updated to cvs snapshot 20080321
  * added support for HttpOnly cookies
  * we no longer distribute or install a ca cert bundle
  * SSLv2 is now disabled by default for SSL operations
  * the test509-style setting URL in callback is officially no
    longer supported
  * support a full chain of certificates in a given PKCS12
    certificate
  * resumed transfers work with SFTP
  * added type checking macros for curl_easy_setopt() and
    curl_easy_getinfo(), watch out for new warnings in code using
    libcurl (needs gcc-4.3 and currently only works in C mode)
  * curl_easy_setopt(), curl_easy_getinfo(), curl_share_setopt()
    and curl_multi_setopt() uses are now checked to use exactly
    three arguments
* Mon Mar 10 2008 mmarek@suse.cz
- clean up curl-config --libs output, thanks to Cristian Rodríguez
  for pointing it out
* Fri Mar  7 2008 mmarek@suse.cz
- build with gssapi support (thanks to Michael Calmer)
* Mon Feb 18 2008 mmarek@suse.cz
- removed Requires: openssl-certs - doesn't exist on older dists
  and is required by libopenssl otherwise
- allow to build the package even if the testsuite fails
* Fri Feb  8 2008 mmarek@suse.cz
- use /etc/ssl/certs instead of own curl-ca-bundle.crt
  * more up-to-date ca cert collection (bnc#334690)
  * allows for easier updates of ca certs
* Tue Jan 29 2008 mmarek@suse.cz
- updated to 7.18.0
  * --data-urlencode
  * CURLOPT_PROXY_TRANSFER_MODE
  * --no-keepalive - now curl does connections with keep-alive
    enabled by default
  * --socks4a added (proxy type CURLPROXY_SOCKS4A for libcurl)
  * --socks5-hostname added (CURLPROXY_SOCKS5_HOSTNAME for libcurl)
  * curl_easy_pause()
  * CURLOPT_SEEKFUNCTION and CURLOPT_SEEKDATA
  * --keepalive-time
  * curl --help output was re-ordered
  * bugfixes
- fixed test553 to work with different port number
* Thu Jan 10 2008 mmarek@suse.cz
- only print -lcurl in curl-config to reduce dependencies
* Tue Dec 11 2007 mmarek@suse.cz
- backported the CURLOPT_PROXY_TRANSFER_MODE patch [#306272#c26]
* Fri Nov 16 2007 mmarek@suse.cz
- fixed the testsuite on hosts that have no IPv6 support [#341994]
  curl-testsuite-safely-skip-http-ipv6.patch
  curl-testsuite-remember-broken-servers.patch
- added stunnel to BuildRequires to enable SSL tests
* Tue Oct 30 2007 mmarek@suse.cz
- updated to 7.17.1
  * automatically append ";type=<a|i>" when using HTTP proxies for
    FTP urls [#306272]
  * improved NSS support
  * added --proxy-negotiate
  * added --post301 and CURLOPT_POST301
  * builds with c-ares 1.5.0
  * added CURLOPT_SSH_HOST_PUBLIC_KEY_MD5 and --hostpubmd5
  * renamed CURLE_SSL_PEER_CERTIFICATE to
    CURLE_PEER_FAILED_VERIFICATION
  * added CURLOPT_OPENSOCKETFUNCTION and CURLOPT_OPENSOCKETDATA
  * CULROPT_COOKIELIST supports "FLUSH"
  * added CURLOPT_COPYPOSTFIELDS
  * added --static-libs to curl-config
  * many bugfixes, inc. fix for bug #332917
* Thu Oct 11 2007 mszeredi@suse.de
- Add missing dependency (openldap2-devel) for libcurl-devel
* Mon Oct  8 2007 mmarek@suse.cz
- updated to 7.17.0
  * curl_easy_setopt() now allocates strings passed to it
  * LDAP libraries are now linked "regularly" and not with dlopen
    (the strict-aliasing patch can go away)
  * HTTP transfers have the download size info "available" earlier
  * FTP transfers have the download size info "available" earlier
  * several error codes and options were marked as obsolete and
    subject to future removal (set CURL_NO_OLDIES to see if your
    application is using them)
  * some bugfixes (see /usr/share/doc/packages/curl/RELEASE-NOTES)
- added fixes for some post-7.17 bugs
- removed some less useful %%%%doc files
* Fri Sep 14 2007 mmarek@suse.cz
- set transfer mode (binary/ascii) when retrieving ftp:// urls via
  an http proxy (curl-ftp-httpproxy.patch) [#306272]
* Wed Aug 29 2007 mmarek@suse.cz
- s/openssl-devel/libopenssl-devel/ [#305815]
* Fri Aug  3 2007 mmarek@suse.cz
- updated to 7.16.4
  * added CURLOPT_NEW_FILE_PERMS and CURLOPT_NEW_DIRECTORY_PERMS
  * improved hashing of sockets for the multi_socket API
  * ftp kerberos5 support added
  * some bugfixes (see /usr/share/doc/packages/curl/RELEASE-NOTES)
- fixed libcurl-devel Provides: [#293401]
* Mon Jul  9 2007 mmarek@suse.cz
- updated to 7.16.3
  * many bugfixes
  * support for running multiple testsuites in paralell
- removed lfs patch leftover
* Mon Jun  4 2007 mmarek@suse.cz
- install libcurl.m4 [#275462]
* Fri Jun  1 2007 dmueller@suse.de
- fix obsoletes for alpha3 update
- fix ldconfig call
* Wed May 23 2007 bk@suse.de
- updated to 7.16.2 (lots of fixes, fixes a segfault in git-http)
* Fri May  4 2007 mmarek@suse.cz
- also avoid non-versioned obsoletes
* Mon Apr 16 2007 mmarek@suse.de
- avoid non-versioned provides
- removed old curl_ssl provides/obsoletes from 7.1 times
* Mon Apr  2 2007 rguenther@suse.de
- split off libcurl4 and curl-ca-bundle packages, rename curl-devel
  to libcurl-devel
* Sat Mar 31 2007 rguenther@suse.de
- add zlib-devel BuildRequires
* Fri Feb 16 2007 mmarek@suse.cz
- better patch for #246179
* Fri Feb 16 2007 mmarek@suse.cz
- fix CURLOPT_RANGE reset for ftp transfers
  [#246179] (ftp_range.patch)
- updated to 7.16.1 (other bugfixes)
* Fri Jan 26 2007 mmarek@suse.cz
- remove libcurl.a and libcurl.la (rationale: there are security
  updates of curl from time to time, so statically linking it is
  not acceptable)
* Thu Jan 25 2007 mmarek@suse.cz
- fixed strict aliasing warnings
* Tue Dec 19 2006 mmarek@suse.cz
- updated to 7.16.0
  * removed CURLOPT_SOURCE_* options and --3p* command line option
    (breaks python-curl atm)
  * for a complete list of changes, see
    /usr/share/doc/packages/curl/RELEASE-NOTES
* Tue Aug 15 2006 mmarek@suse.cz
- configure with --enable-hidden-symbols to compile libcurl with
  - fvisibility=hidden, exporting only symbols from the API
* Tue Aug 15 2006 mmarek@suse.cz
- updated to version 7.15.5
  * added --ftp-ssl-reqd
  * modified the prototype for the socket callback set with
    CURLMOPT_SOCKETFUNCTION
  * added curl_multi_assign()
  * added CURLOPT_FTP_ALTERNATIVE_TO_USER and --ftp-alternative-to-user
  * added a vcproj file for building libcurl
  * added curl_formget()
  * added CURLOPT_MAX_SEND_SPEED_LARGE and CURLOPT_MAX_RECV_SPEED_LARGE
  * Made -K on a file that couldn't be read cause a warning to be displayed
  * some bugfixes
- dropped epsv-firewall.patch which was intergrated in 7.15.2
* Sat Jul  1 2006 cthiel@suse.de
- update to version 7.15.4, changes & fixes for this version:
  * NTLM2 session response support
  * CURLOPT_COOKIELIST set to "SESS" clears all session cookies
  * CURLINFO_LASTSOCKET returned sockets are now checked more before
    returned
  * curl-config got a --checkfor option to compare version numbers
  * line end conversions for FTP ASCII transfers
  * curl_multi_socket() API added (still mostly untested)
  * conversion callback options for EBCDIC <=> ASCII conversions
  * added CURLINFO_FTP_ENTRY_PATH
  * less blocking for the multi interface during (Open)SSL connect
    negotiation
  * builds fine on cygwin
  * md5-sess with Digest authentication
  * dict with letters such as space in a word
  * dict with url-encoded words in the URL
  * libcurl.m4 when default=yes but no libcurl was found
  * numerous bugs fixed in the TFTP code
  * possible memory leak when adding easy handles to multi stack
  * TFTP works in a more portable fashion (== on more platforms)
  * WSAGetLastError() is now used (better) on Windows
  * GnuTLS non-block case that could cause data trashing
  * deflate code survives lack of zlib header
  * CURLOPT_INTERFACE works with hostname
  * configure runs fine with ICC
  * closed control connection with FTP when easy handle was removed from
    multi
  * curl --trace crash when built with VS2005
  * SSL connect time-out
  * improved NTLM functionality
  * following redirects with more than one question mark in source URL
  * fixed debug build crash with -d
  * generates a fine AIX Toolbox RPM spec
  * treat FTP AUTH failures properly
  * TFTP transfers could trash data
  * -d + -G combo crash
* Wed Jun 14 2006 mmarek@suse.cz
- fixed syntax error in configure
* Sun May 28 2006 cthiel@suse.de
- update to version 7.15.3, changes & fixes for this version:
  * added docs for --ftp-method and CURLOPT_FTP_FILEMETHOD
  * TFTP Packet Buffer Overflow Vulnerability (CVE-2006-1061)
  * properly detecting problems with sending the FTP command USER
  * wrong error message shown when certificate verification failed
  * multi-part formpost with multi interface crash
  * the CURLFTPSSL_CONTROL setting for CURLOPT_FTP_SSL is acknowledged
  * "SSL: couldn't set callback" is now treated as a less serious problem
  * Interix build fix
  * fixed curl "hang" when out of file handles at start
  * prevent FTP uploads to URLs with trailing slash
- changes & fixes in 7.15.2
  * Support for SOCKS4 proxies (added --socks4)
  * CURLOPT_CONNECT_ONLY and CURLINFO_LASTSOCKET added
  * CURLOPT_LOCALPORT and CURLOPT_LOCALPORTRANGE (--local-port) added
  * Dropped support for the LPRT ftp command
  * Gopher is now officially abandoned as a protocol (lib)curl tries to
    support
  * curl_global_init() and curl_global_cleanup() are now using a refcount so
    that it is now legal to call them multiple times. See updated info for
    details
  * two bugs concerning using curl_multi_remove_handle() before the transfer
    was complete
  * multi-pass authentication and compressed content
  * minor format string mistake in the GSS/Negotiate code
  * cached DNS entries could remain in the cache too long
  * improved GnuTLS check in configure
  * re-used FTP connections when the second request didn't do a transfer
  * plain --limit-rate [num] means bytes
  * re-creating a dead connection is no longer counted internally as a
    followed redirect and thus prevents a weird error that would occur if a
    FTP connection died on an attempted re-use
  * Try PASV after failing to connect to the port the EPSV response
    contained
  * -P [IP] with non-local address with ipv6-enabled curl
  * -P [hostname] with ipv6-disabled curl
  * libcurl.m4 was updated
  * configure no longer warns if the current path contains a space
  * test suite kill race condition
  * FTP_SKIP_PASV_IP and FTP_USE_EPSV when doing FTP over HTTP proxy
  * Doing a second request with FTP on the same bath path, would make
    libcurl confuse what current working directory it had
  * FTP over HTTP proxy now sends the second CONNECT properly
  * numerous compiler warnings and build quirks for various compilers have
    been addressed
  * supports name and passwords up to 255 bytes long, embedded in URLs
  * the HTTP_ONLY define disables the TFTP support
- removed curl-7.15.1-CVE-2006-1061.patch, included upstream
- removed curl-7.15.1-aliasing.patch
* Tue Mar 14 2006 mmarek@suse.cz
- fix buffer overflow in TFTP code
  [#157874] (CVE-2006-1061.patch)
* Wed Feb 15 2006 ro@suse.de
- added libidn-devel to requires of devel package
* Mon Feb 13 2006 mmarek@suse.cz
- build with libidn support
  [#150313]
* Fri Jan 27 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 23 2006 mmarek@suse.cz
- fallback to PASV if some firewall doesn't let an EPSV connection
  trough
* Thu Jan 12 2006 mmarek@suse.cz
- build with -fstack-protector
- add dependency on curl = %%%%{version} to curl-devel
* Tue Jan 10 2006 mmarek@suse.cz
- remove non-existent path /usr/ssl, which caused -L/usr/ssl/lib to
  appeared in curl-config output
- use make -j
* Tue Dec 13 2005 mmarek@suse.cz
- updated to 7.15.1, fixing previous vulnerabilities
* Thu Oct 13 2005 mmarek@suse.cz
- fix stack buffer overflow in lib/http_ntlm.c [#128065]
* Mon Oct 10 2005 mmarek@suse.cz
- updated to 7.14.1
- updated curl-7.14.1-aliasing.patch
* Mon Jun 20 2005 anicka@suse.cz
- update to 7.14.0
- remove obsolete patch curl-ntlm.patch
* Tue Apr 12 2005 tcrhak@suse.cz
- packaged curl-ca-bundle.crt (bug #64301)
* Thu Feb 24 2005 meissner@suse.de
- enable make test. fixed test 241 to use ::1 directly.
* Tue Feb 22 2005 mcihar@suse.cz
- fix buffer overflow in NTLM (bug #65752)
* Tue Feb  8 2005 mcihar@suse.cz
- update to 7.13.0
* Wed Aug 11 2004 tcrhak@suse.cz
- update to 7.12.0
* Wed Apr 28 2004 tcrhak@suse.cz
- strict aliasing fix
* Tue Mar 16 2004 tcrhak@suse.cz
- fix for lfs for in transfer.c (bug #36040)
* Wed Feb 25 2004 tcrhak@suse.cz
- ignore leading slashes of url-path in URLs like
  ftp://user@name//url-path, i.e don't change to the
  root directory (RFC 1738, bug #34471)
* Tue Feb 10 2004 tcrhak@suse.cz
- update to version 7.11.0
* Sat Jan 10 2004 adrian@suse.de
- add %%defattr and %%run_ldconfig
* Wed Nov  5 2003 tcrhak@suse.cz
- added large file support, patch lfs [bug #32411]
* Thu Sep  4 2003 tcrhak@suse.cz
- require zlib-devel, openssl-devel and glibc-devel in curl-devel [bug #29881]
* Fri Aug  8 2003 tcrhak@suse.cz
- terminate array of directory components by NULL (bug #28351, patch dirs)
* Wed Jul 23 2003 tcrhak@suse.cz
- update to version 7.10.5
* Mon Jun  2 2003 ro@suse.de
- remove unpackaged files from buildroot
* Wed Nov 27 2002 tcrhak@suse.cz
- update to version 7.10.2
- moved curl-config.1.gz to the devel subpackage [bug #21966]
* Sat Jul 13 2002 tcrhak@suse.cz
- update to version 7.9.8
- added automake
* Fri Jan 18 2002 tcrhak@suse.cz
- used macros %%{_lib} and %%{_libdir}
- update to 7.9.2
* Fri Oct 19 2001 ro@suse.de
- do not pack shared library into both, main and devel package
* Mon Oct  8 2001 tcrhak@suse.cz
- update to version 7.9
* Fri Sep 21 2001 adostal@suse.cz
- fix manual in man.patch
* Tue Aug 21 2001 adostal@suse.cz
- update to version 7.8.1
* Wed Jul 18 2001 adostal@suse.cz
- files devel fixed
* Mon Jul  2 2001 adostal@suse.cz
- update to version 7.8
* Wed Jun 13 2001 ro@suse.de
- fixed to compile with new autoconf
* Mon Apr  9 2001 cihlar@suse.cz
- update to version 7.7.1
* Tue Mar  6 2001 cihlar@suse.cz
- update to version 7.6.1
* Wed Jan  3 2001 cihlar@suse.cz
- fixed Provides and Obsoletes also for curl-devel
* Tue Dec 19 2000 cihlar@suse.cz
- fixed name
- added Obsoletes: curl_ssl
* Mon Dec 18 2000 cihlar@suse.cz
- changed to ssl support
* Thu Nov 16 2000 cihlar@suse.cz
- renamed curldev -> curl-devel
- update to version 7.4.2
* Tue Oct 17 2000 cihlar@suse.cz
- update to version 7.4.1 - security bug fixed
* Wed Aug 30 2000 cihlar@suse.cz
- package created
