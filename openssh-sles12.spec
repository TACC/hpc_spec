%include rpm-dir.inc
# TACC tag version
%define tacc_tag v3.19.1-tacc-5
#
# spec file for package openssh
#
# Copyright (c) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


%if 0%{suse_version} >= 1100
%define has_fw_dir 1
%else
%define has_fw_dir 0
%endif

%if 0%{suse_version} >= 1110
%define has_libselinux 1
%else
%define has_libselinux 0
%endif

%if 0%{?suse_version} >= 1130
%define needs_all_dirs 1
%else
%define needs_all_dirs 0
%endif

%if 0%{?suse_version} >= 1140
%define needs_libedit 1
%else
%define needs_libedit 0
%endif

%define has_krb_mini 0
#%if 0%{?suse_version} > 1140
#%define has_krb_mini 1
#%else
#%define has_krb_mini 0
#%endif

%if 0%{?suse_version} > 1220
%define uses_systemd 1
%else
%define uses_systemd 0
%endif

%define sandbox_seccomp 0
%if 0%{?suse_version} > 1220
%define sandbox_seccomp 1
%endif

%define _fwdir   %{_sysconfdir}/sysconfig/SuSEfirewall2.d
%define _fwdefdir   %{_fwdir}/services
%define _appdefdir  %( grep "configdirspec=" $( which xmkmf ) | sed -r 's,^[^=]+=.*-I(.*)/config.*$,\\1/app-defaults,' )
%{!?_initddir:%global _initddir %{_initrddir}}

Name:           openssh
BuildRequires:  audit-devel
BuildRequires:  autoconf
BuildRequires:  groff
%if %{has_krb_mini}
BuildRequires:  krb5-mini-devel
%else
BuildRequires:  krb5-devel
%endif
%if %{needs_libedit}
BuildRequires:  libedit-devel
%endif
%if %{has_libselinux}
BuildRequires:  libselinux-devel
%endif
BuildRequires:  openldap2-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
%if %{uses_systemd}
BuildRequires:  pkgconfig(systemd)
%{?systemd_requires}
%endif
BuildRequires:  tcpd-devel
PreReq:         pwdutils %{fillup_prereq} coreutils
%if ! %{uses_systemd}
PreReq:         %{insserv_prereq}
%endif
Version:        7.5p1
Release:        1%{?dist}
Summary:        Secure Shell Client and Server (Remote Login Program)
License:        BSD-2-Clause and MIT
Group:          Productivity/Networking/SSH
Packager:       TACC - cproctor@tacc.utexas.edu
Url:            http://www.openssh.com/
##Source:         http://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source0:        tacc-openssh-hpn-isshd-%{tacc_tag}.tar.gz
Source1:        sshd.init
Source2:        sshd.pamd
Source3:        README.SUSE
Source4:        README.kerberos
Source5:        ssh.reg
Source6:        ssh-askpass
Source7:        sshd.fw
Source8:        sysconfig.ssh
Source9:        sshd-gen-keys-start
Source10:       sshd.service
Source11:       README.FIPS
Source12:       cavs_driver-ssh.pl
Patch00:        openssh-7.2p2-allow_root_password_login.patch
Patch01:        openssh-7.2p2-allow_DSS_by_default.patch
Patch02:        openssh-7.2p2-X11_trusted_forwarding.patch
Patch03:        openssh-7.2p2-lastlog.patch
Patch04:        openssh-7.2p2-enable_PAM_by_default.patch
Patch05:        openssh-7.2p2-dont_use_pthreads_in_PAM.patch
Patch06:        openssh-7.2p2-eal3.patch
Patch07:        openssh-7.2p2-blocksigalrm.patch
Patch08:        openssh-7.2p2-send_locale.patch
Patch09:        openssh-7.2p2-hostname_changes_when_forwarding_X.patch
Patch10:        openssh-7.2p2-remove_xauth_cookies_on_exit.patch
Patch11:        openssh-7.2p2-pts_names_formatting.patch
Patch12:        openssh-7.2p2-pam_check_locks.patch
Patch13:        openssh-7.2p2-disable_short_DH_parameters.patch
Patch14:        openssh-7.2p2-seccomp_getuid.patch
Patch15:        openssh-7.2p2-seccomp_geteuid.patch
Patch16:        openssh-7.2p2-seccomp_stat.patch
Patch17:        openssh-7.2p2-additional_seccomp_archs.patch
Patch18:        openssh-7.2p2-fips.patch
Patch19:        openssh-7.2p2-seed-prng.patch
Patch20:        openssh-7.2p2-gssapi_key_exchange.patch
Patch21:        openssh-7.2p2-audit.patch
Patch22:        openssh-7.2p2-audit_fixes.patch
Patch23:        openssh-7.2p2-audit_seed_prng.patch
Patch24:        openssh-7.2p2-login_options.patch
Patch25:        openssh-7.2p2-disable_openssl_abi_check.patch
Patch26:        openssh-7.2p2-no_fork-no_pid_file.patch
Patch27:        openssh-7.2p2-host_ident.patch
Patch28:        openssh-7.2p2-sftp_homechroot.patch
Patch29:        openssh-7.2p2-sftp_force_permissions.patch
Patch30:        openssh-7.2p2-X_forward_with_disabled_ipv6.patch
Patch31:        openssh-7.2p2-ldap.patch
Patch32:        openssh-7.2p2-IPv6_X_forwarding.patch
Patch33:        openssh-7.2p2-ignore_PAM_with_UseLogin.patch
Patch34:        openssh-7.2p2-prevent_timing_user_enumeration.patch
Patch35:        openssh-7.2p2-limit_password_length.patch
Patch36:        openssh-7.2p2-keep_slogin.patch
Patch37:        openssh-7.2p2-kex_resource_depletion.patch
Patch38:        openssh-7.2p2-verify_CIDR_address_ranges.patch
Patch39:        openssh-7.2p2-disable_preauth_compression.patch
Patch40:        openssh-7.2p2-restrict_pkcs11-modules.patch
Patch41:        openssh-7.2p2-prevent_private_key_leakage.patch
Patch42:        openssh-7.2p2-secure_unix_sockets_forwarding.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Conflicts:      nonfreessh
Recommends:     audit
Recommends:     xauth
Recommends:     %{name}-helpers = %{version}-%{release}
Conflicts:      %{name}-fips < %{version}-%{release} , %{name}-fips > %{version}-%{release}
%define CHECKSUM_SUFFIX .hmac
%define CHECKSUM_HMAC_KEY "HMAC_KEY:OpenSSH-FIPS@SLE"

%description
SSH (Secure Shell) is a program for logging into and executing commands
on a remote machine. It is intended to replace rsh (rlogin and rsh) and
provides openssl (secure encrypted communication) between two untrusted
hosts over an insecure network.

xorg-x11 (X Window System) connections and arbitrary TCP/IP ports can
also be forwarded over the secure channel.


%package helpers
Summary:        OpenSSH AuthorizedKeysCommand helpers
Group:          Productivity/Networking/SSH
Requires:       %{name} = %{version}-%{release}

%description helpers
Helper applications for OpenSSH which retrieve keys from various sources.


%package fips
Summary:        OpenSSH FIPS cryptomodule HMACs
Group:          Productivity/Networking/SSH
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < %{version}-%{release} , %{name} > %{version}-%{release}
Obsoletes:      %{name}-hmac

%description fips
Hashes that together with the main package form the FIPS certifiable
cryptomodule.


%package cavs
Summary:        OpenSSH FIPS cryptomodule CAVS tests
Group:          Productivity/Networking/SSH
Requires:       %{name} = %{version}-%{release}

%description cavs
FIPS140 CAVS tests related parts of the OpenSSH package


%prep
##%setup -q
%setup -q -n tacc-openssh-hpn-isshd-%{tacc_tag}
%patch00 -p2
%patch01 -p2
%patch02 -p2
%patch03 -p2
%patch04 -p2
%patch05 -p2
%patch06 -p2
%patch07 -p2
%patch08 -p2
%patch09 -p2
%patch10 -p2
%patch11 -p2
%patch12 -p2
%patch13 -p2
%patch14 -p2
%patch15 -p2
%patch16 -p2
%patch17 -p2
%patch18 -p2
%patch19 -p2
%patch20 -p2
%patch21 -p2
%patch22 -p2
%patch23 -p2
%patch24 -p2
%patch25 -p2
%patch26 -p2
%patch27 -p2
%patch28 -p2
%patch29 -p2
%patch30 -p2
%patch31 -p2
%patch32 -p2
%patch33 -p2
%patch34 -p2
%patch35 -p2
%patch36 -p2
%patch37 -p2
%patch38 -p2
%patch39 -p2
%patch40 -p2
%patch41 -p2
%patch42 -p2
cp %{SOURCE3} %{SOURCE4} %{SOURCE11} .

%build
# set libexec dir in the LDAP patch
sed -i.libexec 's,@LIBEXECDIR@,%{_libexecdir}/ssh,' \
    $( grep -Rl @LIBEXECDIR@ \
        $( grep "^+++" %{PATCH31} | sed -r 's@^.+/([^/\t ]+).*$@\1@' )
    )

autoreconf -fiv
%ifarch s390 s390x %sparc
PIEFLAGS="-fPIE"
%else
PIEFLAGS="-fpie"
%endif
CFLAGS="%{optflags} $PIEFLAGS -fstack-protector"
CXXFLAGS="%{optflags} $PIEFLAGS -fstack-protector"
LDFLAGS="-pie -Wl,--as-needed"
#CPPFLAGS="%{optflags} -DUSE_INTERNAL_B64"
export LDFLAGS CFLAGS CXXFLAGS CPPFLAGS
%configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --sysconfdir=%{_sysconfdir}/ssh \
    --libexecdir=%{_libexecdir}/ssh \
    --with-tcp-wrappers \
%if %{has_libselinux}
    --with-selinux \
%endif
%if %{uses_systemd}
    --with-pid-dir=/run \
%endif
    --with-ssl-engine \
    --with-pam \
    --with-kerberos5=%{_prefix} \
    --with-privsep-path=/var/lib/empty \
%if %{sandbox_seccomp}
    --with-sandbox=seccomp_filter \
%else
    --with-sandbox=rlimit \
%endif
%ifnarch s390 s390x
    --with-opensc \
%endif
    --disable-strip \
    --with-audit=linux \
    --with-ldap \
    --with-xauth=%{_bindir}/xauth \
%if %{needs_libedit}
    --with-libedit \
%endif
    --with-ssh1 \
    --target=%{_target_cpu}-suse-linux \
    --with-nerscmod              

### configure end
make %{?_smp_mflags}

#make %{?_smp_mflags} -C converter

%install
make install DESTDIR=%{buildroot}
#make install DESTDIR=%{buildroot} -C converter

install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -d -m 755 %{buildroot}/var/lib/sshd
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/sshd
install -d -m 755 %{buildroot}%{_sysconfdir}/slp.reg.d/
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/slp.reg.d/
install -d -m 755 %{buildroot}%{_initddir}
%if %{uses_systemd}
install -m 0755 %{SOURCE1} .
install -D -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}/sshd.service
ln -s /sbin/service %{buildroot}%{_sbindir}/rcsshd
%else
install -D -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/sshd
install -m 0644 %{SOURCE10} .
ln -s ../..%{_initddir}/sshd %{buildroot}%{_sbindir}/rcsshd
%endif
install -d -m 755 %{buildroot}/var/adm/fillup-templates
install -m 644 %{SOURCE8} %{buildroot}/var/adm/fillup-templates
# install shell script to automate the process of adding your public key to a remote machine
install -m 755 contrib/ssh-copy-id %{buildroot}%{_bindir}
install -m 644 contrib/ssh-copy-id.1 %{buildroot}%{_mandir}/man1
sed -i -e s@/usr/libexec@%{_libexecdir}@g %{buildroot}%{_sysconfdir}/ssh/sshd_config

%if %{has_fw_dir}
#install firewall definitions format is described here:
#%{_datadir}/SuSEfirewall2/services/TEMPLATE
mkdir -p %{buildroot}%{_fwdefdir}
install -m 644 %{SOURCE7} %{buildroot}%{_fwdefdir}/sshd
%endif

# askpass wrapper
sed -e "s,@LIBEXECDIR@,%{_libexecdir},g" < %{SOURCE6} > %{buildroot}%{_libexecdir}/ssh/ssh-askpass
sed -e "s,@LIBEXECDIR@,%{_libexecdir},g" < %{SOURCE12} > %{buildroot}%{_libexecdir}/ssh/cavs_driver-ssh.pl
rm -f %{buildroot}%{_datadir}/Ssh.bin
# sshd keys generator wrapper
install -D -m 0755 %{SOURCE9} %{buildroot}%{_sbindir}/sshd-gen-keys-start

# the hmac hashes - taken from openssl
#
# re-define the __os_install_post macro: the macro strips
# the binaries and thereby invalidates any hashes created earlier.
#
# this shows up earlier because otherwise the %expand of
# the macro is too late.
%{expand:%%global __os_install_post {%__os_install_post
for b in \
        %{_bindir}/ssh \
        %{_sbindir}/sshd \
        %{_libexecdir}/ssh/sftp-server \
        ; do
    openssl dgst -sha256 -binary -hmac %{CHECKSUM_HMAC_KEY} < %{buildroot}$b > %{buildroot}$b%{CHECKSUM_SUFFIX}
done

}}

%pre
getent group sshd >/dev/null || %{_sbindir}/groupadd -r sshd
getent passwd sshd >/dev/null || %{_sbindir}/useradd -r -g sshd -d /var/lib/sshd -s /bin/false -c "SSH daemon" sshd
%if %{uses_systemd}
%service_add_pre sshd.service
%endif

%post
%if %{uses_systemd}
%{fillup_only -n ssh sshd}
%service_add_post sshd.service
%else
%{fillup_and_insserv -n ssh sshd}
%endif

%preun
%if %{uses_systemd}
%service_del_preun sshd.service
%else
%stop_on_removal sshd
%endif

%postun
# The openssh-fips trigger script for openssh will normally restart sshd once
# it gets installed, so only restart the service here is openssh-fips is not
# present
rpm -q openssh-fips >& /dev/null && DISABLE_RESTART_ON_UPDATE=yes
%if %{uses_systemd}
%service_del_postun sshd.service
%else
%restart_on_update sshd
%{insserv_cleanup}
%endif

%triggerin -n openssh-fips -- %{name} = %{version}-%{release}
%restart_on_update sshd

%files
%defattr(-,root,root)
%exclude %{_bindir}/ssh%{CHECKSUM_SUFFIX}
%exclude %{_sbindir}/sshd%{CHECKSUM_SUFFIX}
%exclude %{_libexecdir}/ssh/sftp-server%{CHECKSUM_SUFFIX}
%exclude %{_libexecdir}/ssh/cavs*
%dir %attr(755,root,root) /var/lib/sshd
%doc README.SUSE README.kerberos README.FIPS ChangeLog OVERVIEW README TODO LICENCE CREDITS
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%verify(not mode) %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%verify(not mode) %attr(0640,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/sshd
%if %{uses_systemd}
%doc sshd.init
%attr(0644,root,root) %config %{_unitdir}/sshd.service
%else
%attr(0755,root,root) %config %{_initddir}/sshd
%doc sshd.service
%endif
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%attr(0755,root,root) %dir %{_libexecdir}/ssh
%exclude %{_libexecdir}/ssh/ssh-ldap*
%attr(0755,root,root) %{_libexecdir}/ssh/*
%attr(0444,root,root) %doc %{_mandir}/man1/*
%attr(0444,root,root) %doc %{_mandir}/man5/*
%attr(0444,root,root) %doc %{_mandir}/man8/*
%dir %{_sysconfdir}/slp.reg.d
%config %{_sysconfdir}/slp.reg.d/ssh.reg
/var/adm/fillup-templates/sysconfig.ssh
%if %{has_fw_dir}
%if %{needs_all_dirs}
%dir %{_fwdir}
%dir %{_fwdefdir}
%endif
%config %{_fwdefdir}/sshd
%endif

%files helpers
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%verify(not mode) %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ldap.conf
%attr(0755,root,root) %dir %{_libexecdir}/ssh
%attr(0755,root,root) %{_libexecdir}/ssh/ssh-ldap*
%doc HOWTO.ldap-keys openssh-lpk-openldap.schema openssh-lpk-sun.schema

%files fips
%defattr(-,root,root)
%attr(0444,root,root) %{_bindir}/ssh%{CHECKSUM_SUFFIX}
%attr(0444,root,root) %{_sbindir}/sshd%{CHECKSUM_SUFFIX}
%attr(0444,root,root) %{_libexecdir}/ssh/sftp-server%{CHECKSUM_SUFFIX}

%files cavs
%defattr(-,root,root)
%attr(0755,root,root) %{_libexecdir}/ssh/cavs*

%changelog
* Tue Jan 24 2017 pcerny@suse.com
- Adding missing pieces for user matching (bsc#1021626)
* Thu Jan  5 2017 pcerny@suse.com
- Properly verify CIDR masks in configuration
  (bsc#1005893)
  [openssh-7.2p2-verify_CIDR_address_ranges.patch]
- Remove pre-auth compression support from the server to prevent
  possible cryptographic attacks.
  (CVE-2016-10012, bsc#1016370)
  [openssh-7.2p2-disable_preauth_compression.patch]
- limit directories for loading PKCS11 modules
  (CVE-2016-10009, bsc#1016366)
  [openssh-7.2p2-restrict_pkcs11-modules.patch]
- Prevent possible leaks of host private keys to low-privilege
  process handling authentication
  (CVE-2016-10011, bsc#1016369)
  [openssh-7.2p2-prevent_private_key_leakage.patch]
- Do not allow unix socket forwarding when running without
  privilege separation
  (CVE-2016-10010, bsc#1016368)
  [openssh-7.2p2-secure_unix_sockets_forwarding.patch]
* Tue Nov  8 2016 pcerny@suse.com
- prevent resource depletion during key exchange
  (bsc#1005480, CVE-2016-8858)
  [openssh-7.2p2-kex_resource_depletion.patch]
- fix suggested command for removing conflicting server keys from
  the known_hosts file (bsc#1006221)
* Thu Oct 13 2016 pcerny@suse.com
- enable geteuid{,32} syscalls on mainframes, since it may be
  called from libica/ibmica on machines with hardware crypto
  accelerator (bsc#1004258)
  [openssh-7.2p2-seccomp_geteuid.patch]
- fix regression of (bsc#823710)
  [openssh-7.2p2-audit_fixes.patch]
- add slogin (removed upstreams)
  [openssh-7.2p2-keep_slogin.patch]
* Thu Sep 29 2016 pcerny@suse.com
- remaining patches that were still missing
  since the update to 7.2p2 (FATE#319675):
- allow X forwarding over IPv4 when IPv6 sockets is not available
  [openssh-7.2p2-X_forward_with_disabled_ipv6.patch]
- do not write PID file when not daemonizing
  [openssh-7.2p2-no_fork-no_pid_file.patch]
- use correct options when invoking login
  [openssh-7.2p2-login_options.patch]
- helper application for retrieving users' public keys from
  an LDAP server
  [openssh-7.2p2-ldap.patch]
- allow forcing permissions over sftp
  [openssh-7.2p2-sftp_force_permissions.patch]
- do not perform run-time checks for OpenSSL API/ABI change
  [openssh-7.2p2-disable_openssl_abi_check.patch]
- suggest commands for cleaning known hosts file
  [openssh-7.2p2-host_ident.patch]
- sftp home chroot patch
  [openssh-7.2p2-sftp_homechroot.patch]
- ssh sessions auditing
  [openssh-7.2p2-audit.patch]
- enable seccomp sandbox on additional architectures
  [openssh-7.2p2-additional_seccomp_archs.patch]
- fix forwarding with IPv6 addresses in DISPLAY (bnc#847710)
  [openssh-7.2p2-IPv6_X_forwarding.patch]
- ignore PAM environment when using login
  (bsc#975865, CVE-2015-8325)
  [openssh-7.2p2-ignore_PAM_with_UseLogin.patch]
- limit accepted password length (prevents possible DoS)
  (bsc#992533, CVE-2016-6515)
  [openssh-7.2p2-limit_password_length.patch]
- Prevent user enumeration through the timing of password
  processing (bsc#989363, CVE-2016-6210)
  [openssh-7.2p2-prevent_timing_user_enumeration.patch]
- Add auditing for PRNG re-seeding
  [openssh-7.2p2-audit_seed_prng.patch]
* Fri Sep 16 2016 pcerny@suse.com
- FIPS compatibility (no selfchecks, only crypto restrictions)
  [openssh-7.2p2-fips.patch]
- PRNG re-seeding
  [openssh-7.2p2-seed-prng.patch]
- preliminary version of GSSAPI KEX
  [openssh-7.2p2-gssapi_key_exchange.patch]
* Tue Jun  7 2016 pcerny@suse.com
- enable support for SSHv1 protocol and discourage its usage
  (bsc#983307)
- enable DSA by default for backward compatibility and discourage
  its usage (bsc#983784)
* Mon May 30 2016 pcerny@suse.com
- enable trusted X11 forwarding by default
  [openssh-7.2p2-X11_trusted_forwarding.patch]
- set UID for lastlog properly
  [openssh-7.2p2-lastlog.patch]
- enable use of PAM by default
  [openssh-7.2p2-enable_PAM_by_default.patch]
- copy command line arguments properly
  [openssh-7.2p2-saveargv-fix.patch]
- do not use pthreads in PAM code
  [openssh-7.2p2-dont_use_pthreads_in_PAM.patch]
- fix paths in documentation
  [openssh-7.2p2-eal3.patch]
- prevent race consitions triggered by SIGALRM
  [openssh-7.2p2-blocksigalrm.patch]
- do send and accept locale environment variables by default
  [openssh-7.2p2-send_locale.patch]
- handle hostnames changes during X forwarding
  [openssh-7.2p2-hostname_changes_when_forwarding_X.patch]
- try to remove xauth cookies on exit
  [openssh-7.2p2-remove_xauth_cookies_on_exit.patch]
- properly format pts names for ?tmp? log files
  [openssh-7.2p2-pts_names_formatting.patch]
- check locked accounts when using PAM
  [openssh-7.2p2-pam_check_locks.patch]
- chenge default PermitRootLogin to 'yes' to prevent unwanted
  surprises on updates from older versions.
  See README.SUSE for details
  [openssh-7.2p2-allow_root_password_login.patch]
- Disable DH parameters under 2048 bits by default and allow
  lowering the limit back to the RFC 4419 specified minimum
  through an option (bsc#932483, bsc#948902)
  [openssh-7.2p2-disable_short_DH_parameters.patch]
- Add getuid() and stat() syscalls to the seccomp filter
  (bsc#912436)
  [openssh-7.2p2-seccomp_getuid.patch,
  openssh-7.2p2-seccomp_stat.patch]
* Sun Apr 17 2016 pcerny@suse.com
- upgrade to 7.2p2 (FATE#319675)
  upstream package without any SUSE patches
  Distilled upstream log:
- OpenSSH 6.7
  Potentially-incompatible changes:
  * sshd(8): The default set of ciphers and MACs has been
    altered to remove unsafe algorithms. In particular, CBC
    ciphers and arcfour* are disabled by default.
    The full set of algorithms remains available if configured
    explicitly via the Ciphers and MACs sshd_config options.
  * sshd(8): Support for tcpwrappers/libwrap has been removed.
  * OpenSSH 6.5 and 6.6 have a bug that causes ~0.2%% of
    connections using the curve25519-sha256@libssh.org KEX
    exchange method to fail when connecting with something that
    implements the specification correctly. OpenSSH 6.7 disables
    this KEX method when speaking to one of the affected
    versions.
  New Features:
  * ssh(1), sshd(8): Add support for Unix domain socket
    forwarding. A remote TCP port may be forwarded to a local
    Unix domain socket and vice versa or both ends may be a Unix
    domain socket.
  * ssh(1), ssh-keygen(1): Add support for SSHFP DNS records for
    ED25519 key types.
  * sftp(1): Allow resumption of interrupted uploads.
  * ssh(1): When rekeying, skip file/DNS lookups of the hostkey
    if it is the same as the one sent during initial key exchange
  * sshd(8): Allow explicit ::1 and 127.0.0.1 forwarding bind
    addresses when GatewayPorts=no; allows client to choose
    address family
  * sshd(8): Add a sshd_config PermitUserRC option to control
    whether ~/.ssh/rc is executed, mirroring the no-user-rc
    authorized_keys option
  * ssh(1): Add a %%C escape sequence for LocalCommand and
    ControlPath that expands to a unique identifer based on a
    hash of the tuple of (local host, remote user, hostname,
    port). Helps avoid exceeding miserly pathname limits for Unix
    domain sockets in multiplexing control paths
  * sshd(8): Make the "Too many authentication failures" message
    include the user, source address, port and protocol in a
    format similar to the authentication success / failure
    messages
  Bugfixes:
  * sshd(8): Fix remote forwarding with the same listen port but
    different listen address.
  * ssh(1): Fix inverted test that caused PKCS#11 keys that were
    explicitly listed in ssh_config or on the commandline not to
    be preferred.
  * ssh-keygen(1): Fix bug in KRL generation: multiple
    consecutive revoked certificate serial number ranges could be
    serialised to an invalid format. Readers of a broken KRL
    caused by this bug will fail closed, so no
    should-have-been-revoked key will be accepted.
  * ssh(1): Reflect stdio-forward ("ssh -W host:port ...")
    failures in exit status. Previously we were always returning 0
  * ssh(1), ssh-keygen(1): Make Ed25519 keys' title fit properly
    in the randomart border
  * ssh-agent(1): Only cleanup agent socket in the main agent
    process and not in any subprocesses it may have started (e.g.
    forked askpass). Fixes agent sockets being zapped when
    askpass processes fatal()
  * ssh-add(1): Make stdout line-buffered; saves partial output
    getting lost when ssh-add fatal()s part-way through (e.g.
    when listing keys from an agent that supports key types that
    ssh-add doesn't)
  * ssh-keygen(1): When hashing or removing hosts, don't choke on
    @revoked markers and don't remove @cert-authority markers
  * ssh(1): Don't fatal when hostname canonicalisation fails and
    a ProxyCommand is in use; continue and allow the ProxyCommand
    to connect anyway (e.g. to a host with a name outside the DNS
    behind a bastion)
  * scp(1): When copying local->remote fails during read, don't
    send uninitialised heap to the remote end.
  * sftp(1): Fix fatal "el_insertstr failed" errors when
    tab-completing filenames with  a single quote char somewhere
    in the string
  * ssh-keyscan(1): Scan for Ed25519 keys by default.
  * ssh(1): When using VerifyHostKeyDNS with a DNSSEC resolver,
    down-convert any certificate keys to plain keys and attempt
    SSHFP resolution.  Prevents a server from skipping SSHFP
    lookup and forcing a new-hostkey dialog by offering only
    certificate keys.
- OpenSSH 6.8
  Potentially-incompatible changes:
  * sshd(8): UseDNS now defaults to 'no'. Configurations that
    match against the client host name (via sshd_config or
    authorized_keys) may need to re-enable it or convert to
    matching against addresses.
  New Features:
  * Add FingerprintHash option to ssh(1) and sshd(8), and
    equivalent command-line flags to the other tools to control
    algorithm used for key fingerprints. The default changes from
    MD5 to SHA256 and format from hex to base64.
    Fingerprints now have the hash algorithm prepended. An
    example of the new format:
    SHA256:mVPwvezndPv/ARoIadVY98vAC0g+P/5633yTC4d/wXE Please
    note that visual host keys will also be different.
  * ssh(1), sshd(8): Experimental host key rotation support. Add
    a protocol extension for a server to inform a client of all
    its available host keys after authentication has completed.
    The client may record the keys in known_hosts, allowing it to
    upgrade to better host key algorithms and a server to
    gracefully rotate its keys.
    The client side of this is controlled by a UpdateHostkeys
    config option (default off).
  * ssh(1): Add a ssh_config HostbasedKeyType option to control
    which host public key types are tried during host-based
    authentication.
  * ssh(1), sshd(8): fix connection-killing host key mismatch
    errors when sshd offers multiple ECDSA keys of different
    lengths.
  * ssh(1): when host name canonicalisation is enabled, try to
    parse host names as addresses before looking them up for
    canonicalisation. fixes bz#2074 and avoiding needless DNS
    lookups in some cases.
  * ssh-keygen(1), sshd(8): Key Revocation Lists (KRLs) no longer
    require OpenSSH to be compiled with OpenSSL support.
  * ssh(1), ssh-keysign(8): Make ed25519 keys work for host based
    authentication.
  * sshd(8): SSH protocol v.1 workaround for the Meyer, et al,
    Bleichenbacher Side Channel Attack. Fake up a bignum key
    before RSA decryption.
  * sshd(8): Remember which public keys have been used for
    authentication and refuse to accept previously-used keys.
    This allows AuthenticationMethods=publickey,publickey to
    require that users authenticate using two _different_ public
    keys.
  * sshd(8): add sshd_config HostbasedAcceptedKeyTypes and
    PubkeyAcceptedKeyTypes options to allow sshd to control what
    public key types will be accepted. Currently defaults to all.
  * sshd(8): Don't count partial authentication success as a
    failure against MaxAuthTries.
  * ssh(1): Add RevokedHostKeys option for the client to allow
    text-file or KRL-based revocation of host keys.
  * ssh-keygen(1), sshd(8): Permit KRLs that revoke certificates
    by serial number or key ID without scoping to a particular
    CA.
  * ssh(1): Add a "Match canonical" criteria that allows
    ssh_config Match blocks to trigger only in the second config
    pass.
  * ssh(1): Add a -G option to ssh that causes it to parse its
    configuration and dump the result to stdout, similar to
    "sshd -T".
  * ssh(1): Allow Match criteria to be negated.
    E.g. "Match !host".
  * The regression test suite has been extended to cover more
    OpenSSH features. The unit tests have been expanded and now
    cover key exchange.
  Bugfixes:
  * ssh-keyscan(1): ssh-keyscan has been made much more robust
    again servers that hang or violate the SSH protocol.
  * ssh(1), ssh-keygen(1): Fix regression: Key path names were
    being lost as comment fields.
  * ssh(1): Allow ssh_config Port options set in the second
    config parse phase to be applied (they were being ignored).
  * ssh(1): Tweak config re-parsing with host canonicalisation - make
    the second pass through the config files always run when host name
    canonicalisation is enabled (and not whenever the host name
    changes)
  * ssh(1): Fix passing of wildcard forward bind addresses when
    connection multiplexing is in use
  * ssh-keygen(1): Fix broken private key conversion from
    non-OpenSSH formats.
  * ssh-keygen(1): Fix KRL generation bug when multiple CAs are
    in use.
  * Various fixes to manual pages
- OpenSSH 6.9
  Security:
  * ssh(1): when forwarding X11 connections with
    ForwardX11Trusted=no, connections made after
    ForwardX11Timeout expired could be permitted and no longer
    subject to XSECURITY restrictions because of an ineffective
    timeout check in ssh(1) coupled with "fail open" behaviour in
    the X11 server when clients attempted connections with
    expired credentials. This problem was reported by Jann Horn.
  * ssh-agent(1): fix weakness of agent locking (ssh-add -x) to
    password guessing by implementing an increasing failure
    delay, storing a salted hash of the password rather than the
    password itself and using a timing-safe comparison function
    for verifying unlock attempts. This problem was reported by
    Ryan Castellucci.
  New Features:
  * ssh(1), sshd(8): promote chacha20-poly1305@openssh.com to be
    the default cipher
  * sshd(8): support admin-specified arguments to
    AuthorizedKeysCommand
  * sshd(8): add AuthorizedPrincipalsCommand that allows
    retrieving authorized principals information from a
    subprocess rather than a file.
  * ssh(1), ssh-add(1): support PKCS#11 devices with external PIN
    entry devices
  * sshd(8): allow GSSAPI host credential check to be relaxed for
    multihomed hosts via GSSAPIStrictAcceptorCheck option
  * ssh-keygen(1): support "ssh-keygen -lF hostname" to search
    known_hosts and print key hashes rather than full keys.
  * ssh-agent(1): add -D flag to leave ssh-agent in foreground
    without enabling debug mode
  Bugfixes:
  * ssh(1), sshd(8): deprecate legacy
    SSH2_MSG_KEX_DH_GEX_REQUEST_OLD message and do not try to use
    it against some 3rd-party SSH implementations that use it
    (older PuTTY, WinSCP).
  * Many fixes for problems caused by compile-time deactivation
    of SSH1 support (including bz#2369)
  * ssh(1), sshd(8): cap DH-GEX group size at 4Kbits for Cisco
    implementations as some would fail when attempting to use
    group sizes >4K
  * ssh(1): fix out-of-bound read in EscapeChar configuration
    option parsing
  * sshd(8): fix application of PermitTunnel, LoginGraceTime,
    AuthenticationMethods and StreamLocalBindMask options in
    Match blocks
  * ssh(1), sshd(8): improve disconnection message on TCP reset;
    bz#2257
  * ssh(1): remove failed remote forwards established by
    muliplexing from the list of active forwards
  * sshd(8): make parsing of authorized_keys "environment="
    options independent of PermitUserEnv being enabled
  * sshd(8): fix post-auth crash with permitopen=none
  * ssh(1), ssh-add(1), ssh-keygen(1): allow new-format private
    keys to be encrypted with AEAD ciphers
  * ssh(1): allow ListenAddress, Port and AddressFamily
    configuration options to appear in any order
  * sshd(8): check for and reject missing arguments for
    VersionAddendum and ForceCommand
  * ssh(1), sshd(8): don't treat unknown certificate extensions
    as fatal
  * ssh-keygen(1): make stdout and stderr output consistent
  * ssh(1): mention missing DISPLAY environment in debug log when
    X11 forwarding requested
  * sshd(8): correctly record login when UseLogin is set
  * sshd(8): Add some missing options to sshd -T output and fix
    output of VersionAddendum and HostCertificate. bz#2346
  * Document and improve consistency of options that accept a
    "none" argument" TrustedUserCAKeys, RevokedKeys (bz#2382),
    AuthorizedPrincipalsFile (bz#2288)
  * ssh(1): include remote username in debug output
  * sshd(8): avoid compatibility problem with some versions of
    Tera Term, which would crash when they received the hostkeys
    notification message (hostkeys-00@openssh.com)
  * sshd(8): mention ssh-keygen -E as useful when comparing
    legacy MD5 host key fingerprints
  * ssh(1): clarify pseudo-terminal request behaviour and use
    make manual language consistent
  * ssh(1): document that the TERM environment variable is not
    subject to SendEnv and AcceptEnv
- OpenSSH 7.0:
  This focuses primarily on deprecating weak, legacy and/or
  unsafe cryptography.
  Security:
  * sshd(8): OpenSSH 6.8 and 6.9 incorrectly set TTYs to be
    world- writable. Local attackers may be able to write
    arbitrary messages to logged-in users, including terminal
    escape sequences.  Reported by Nikolay Edigaryev.
  * sshd(8): Portable OpenSSH only: Fixed a privilege separation
    weakness related to PAM support. Attackers who could
    successfully compromise the pre-authentication process for
    remote code execution and who had valid credentials on the
    host could impersonate other users.  Reported by Moritz
    Jodeit.
  * sshd(8): Portable OpenSSH only: Fixed a use-after-free bug
    related to PAM support that was reachable by attackers who
    could compromise the pre-authentication process for remote
    code execution. Also reported by Moritz Jodeit.
  * sshd(8): fix circumvention of MaxAuthTries using keyboard-
    interactive authentication. By specifying a long, repeating
    keyboard-interactive "devices" string, an attacker could
    request the same authentication method be tried thousands of
    times in a single pass. The LoginGraceTime timeout in sshd(8)
    and any authentication failure delays implemented by the
    authentication mechanism itself were still applied. Found by
    Kingcope.
  Potentially-incompatible Changes:
  * Support for the legacy SSH version 1 protocol is disabled by
    default at compile time.
  * Support for the 1024-bit diffie-hellman-group1-sha1 key
    exchange is disabled by default at run-time. It may be
    re-enabled using the instructions in README.legacy or
    http://www.openssh.com/legacy.html
  * Support for ssh-dss, ssh-dss-cert-* host and user keys is
    disabled by default at run-time. These may be re-enabled
    using the instructions at http://www.openssh.com/legacy.html
  * Support for the legacy v00 cert format has been removed.
  * The default for the sshd_config(5) PermitRootLogin option has
    changed from "yes" to "prohibit-password".
  * PermitRootLogin=without-password/prohibit-password now bans
    all interactive authentication methods, allowing only
    public-key, hostbased and GSSAPI authentication (previously
    it permitted keyboard-interactive and password-less
    authentication if those were enabled).
  New Features:
  * ssh_config(5): add PubkeyAcceptedKeyTypes option to control
    which public key types are available for user authentication.
  * sshd_config(5): add HostKeyAlgorithms option to control which
    public key types are offered for host authentications.
  * ssh(1), sshd(8): extend Ciphers, MACs, KexAlgorithms,
    HostKeyAlgorithms, PubkeyAcceptedKeyTypes and
    HostbasedKeyTypes options to allow appending to the default
    set of algorithms instead of replacing it. Options may now be
    prefixed with a '+' to append to the default, e.g.
    "HostKeyAlgorithms=+ssh-dss".
  * sshd_config(5): PermitRootLogin now accepts an argument of
    'prohibit-password' as a less-ambiguous synonym of 'without-
    password'.
  Bugfixes:
  * ssh(1), sshd(8): add compatability workarounds for Cisco and
    more PuTTY versions.
  * Fix some omissions and errors in the PROTOCOL and
    PROTOCOL.mux documentation relating to Unix domain socket
    forwarding
  * ssh(1): Improve the ssh(1) manual page to include a better
    description of Unix domain socket forwarding
  * ssh(1), ssh-agent(1): skip uninitialised PKCS#11 slots,
    fixing failures to load keys when they are present.
  * ssh(1), ssh-agent(1): do not ignore PKCS#11 hosted keys that
    wth empty CKA_ID
  * sshd(8): clarify documentation for UseDNS option
- OpenSSH 7.1:
  Security:
  * sshd(8): OpenSSH 7.0 contained a logic error in
    PermitRootLogin= prohibit-password/without-password that
    could, depending on compile-time configuration, permit
    password authentication to root while preventing other forms
    of authentication. This problem was reported by Mantas
    Mikulenas.
  Bugfixes:
  * ssh(1), sshd(8): add compatability workarounds for FuTTY
  * ssh(1), sshd(8): refine compatability workarounds for WinSCP
  * Fix a number of memory faults (double-free, free of
    uninitialised memory, etc) in ssh(1) and ssh-keygen(1).
    Reported by Mateusz Kocielski.
- OpenSSH 7.1p2:
  * SECURITY: ssh(1): The OpenSSH client code between 5.4 and 7.1
    contains experimential support for resuming SSH-connections
    (roaming).
    The matching server code has never been shipped, but the
    client code was enabled by default and could be tricked by a
    malicious server into leaking client memory to the server,
    including private client user keys.
    The authentication of the server host key prevents
    exploitation by a man-in-the-middle, so this information leak
    is restricted to connections to malicious or compromised
    servers.
    MITIGATION: For OpenSSH >= 5.4 the vulnerable code in the
    client can be completely disabled by adding 'UseRoaming no'
    to the gobal ssh_config(5) file, or to user configuration in
    ~/.ssh/config, or by passing -oUseRoaming=no on the command
    line.
    PATCH: See below for a patch to disable this feature
    (Disabling Roaming in the Source Code).
    This problem was reported by the Qualys Security Advisory
    team.
  * SECURITY: Eliminate the fallback from untrusted
    X11-forwarding to trusted forwarding for cases when the X
    server disables the SECURITY extension. Reported by Thomas
    Hoger.
  * SECURITY: Fix an out of-bound read access in the packet
    handling code. Reported by Ben Hawkes.
  * PROTOCOL: Correctly interpret the 'first_kex_follows' option
    during the intial key exchange. Reported by Matt Johnston.
  * Further use of explicit_bzero has been added in various
    buffer handling code paths to guard against compilers
    aggressively doing dead-store removal.
  Potentially-incompatible changes:
  * This release disables a number of legacy cryptographic
    algorithms by default in ssh:
    + Several ciphers blowfish-cbc, cast128-cbc, all arcfour
    variants and the rijndael-cbc aliases for AES.
    + MD5-based and truncated HMAC algorithms.
- OpenSSH 7.2:
  Security:
  * ssh(1), sshd(8): remove unfinished and unused roaming code
    (was already forcibly disabled in OpenSSH 7.1p2).
  * ssh(1): eliminate fallback from untrusted X11 forwarding to
    trusted forwarding when the X server disables the SECURITY
    extension.
  * ssh(1), sshd(8): increase the minimum modulus size supported
    for diffie-hellman-group-exchange to 2048 bits.
  * sshd(8): pre-auth sandboxing is now enabled by default
    (previous releases enabled it for new installations via
    sshd_config).
  New Features:
  * all: add support for RSA signatures using SHA-256/512 hash
    algorithms based on draft-rsa-dsa-sha2-256-03.txt and
    draft-ssh-ext-info-04.txt.
  * ssh(1): Add an AddKeysToAgent client option which can be set
    to 'yes', 'no', 'ask', or 'confirm', and defaults to 'no'.
    When enabled, a private key that is used during
    authentication will be added to ssh-agent if it is running
    (with confirmation enabled if set to 'confirm').
  * sshd(8): add a new authorized_keys option "restrict" that
    includes all current and future key restrictions
    (no-*-forwarding, etc.).  Also add permissive versions of the
    existing restrictions, e.g.  "no-pty" -> "pty". This
    simplifies the task of setting up restricted keys and ensures
    they are maximally-restricted, regardless of any permissions
    we might implement in the future.
  * ssh(1): add ssh_config CertificateFile option to explicitly
    list certificates. bz#2436
  * ssh-keygen(1): allow ssh-keygen to change the key comment for
    all supported formats.
  * ssh-keygen(1): allow fingerprinting from standard input, e.g.
    "ssh-keygen -lf -"
  * ssh-keygen(1): allow fingerprinting multiple public keys in a
    file, e.g. "ssh-keygen -lf ~/.ssh/authorized_keys" bz#1319
  * sshd(8): support "none" as an argument for sshd_config
    Foreground and ChrootDirectory. Useful inside Match blocks to
    override a global default. bz#2486
  * ssh-keygen(1): support multiple certificates (one per line)
    and reading from standard input (using "-f -") for
    "ssh-keygen -L"
  * ssh-keyscan(1): add "ssh-keyscan -c ..." flag to allow
    fetching certificates instead of plain keys.
  * ssh(1): better handle anchored FQDNs (e.g. 'cvs.openbsd.org')
    in hostname canonicalisation - treat them as already
    canonical and remove the trailing '.' before matching
    ssh_config.
  Bugfixes:
  * sftp(1): existing destination directories should not
    terminate recursive uploads (regression in openssh 6.8)
  * ssh(1), sshd(8): correctly send back SSH2_MSG_UNIMPLEMENTED
    replies to unexpected messages during key exchange.
  * ssh(1): refuse attempts to set ConnectionAttempts=0, which
    does not make sense and would cause ssh to print an
    uninitialised stack variable.
  * ssh(1): fix errors when attempting to connect to scoped IPv6
    addresses with hostname canonicalisation enabled.
  * sshd_config(5): list a couple more options usable in Match
    blocks.
  * sshd(8): fix "PubkeyAcceptedKeyTypes +..." inside a Match
    block.
  * ssh(1): expand tilde characters in filenames passed to -i
    options before checking whether or not the identity file
    exists. Avoids confusion for cases where shell doesn't expand
    (e.g. "-i ~/file" vs. "-i~/file").
  * ssh(1): do not prepend "exec" to the shell command run by
    "Match exec" in a config file, which could cause some
    commands to fail in certain environments.
  * ssh-keyscan(1): fix output for multiple hosts/addrs on one
    line when host hashing or a non standard port is in use
  * sshd(8): skip "Could not chdir to home directory" message
    when ChrootDirectory is active.
  * ssh(1): include PubkeyAcceptedKeyTypes in ssh -G config dump.
  * sshd(8): avoid changing TunnelForwarding device flags if they
    are already what is needed; makes it possible to use tun/tap
    networking as non-root user if device permissions and
    interface flags are pre-established
  * ssh(1), sshd(8): RekeyLimits could be exceeded by one packet.
  * ssh(1): fix multiplexing master failure to notice client
    exit.
  * ssh(1), ssh-agent(1): avoid fatal() for PKCS11 tokens that
    present empty key IDs.
  * sshd(8): avoid printf of NULL argument.
  * ssh(1), sshd(8): allow RekeyLimits larger than 4GB.
  * ssh-keygen(1): sshd(8): fix several bugs in (unused) KRL
    signature support.
  * ssh(1), sshd(8): fix connections with peers that use the key
    exchange guess feature of the protocol.
  * sshd(8): include remote port number in log messages.
  * ssh(1): don't try to load SSHv1 private key when compiled
    without SSHv1 support.
  * ssh-agent(1), ssh(1): fix incorrect error messages during key
    loading and signing errors.
  * ssh-keygen(1): don't leave empty temporary files when
    performing known_hosts file edits when known_hosts doesn't
    exist.
  * sshd(8): correct packet format for tcpip-forward replies for
    requests that don't allocate a port
  * ssh(1), sshd(8): fix possible hang on closed output.
  * ssh(1): expand %%i in ControlPath to UID.
  * ssh(1), sshd(8): fix return type of openssh_RSA_verify.
  * ssh(1), sshd(8): fix some option parsing memory leaks.
  * ssh(1): add a some debug output before DNS resolution; it's a
    place where ssh could previously silently stall in cases of
    unresponsive DNS servers.
  * ssh(1): remove spurious newline in visual hostkey.
  * ssh(1): fix printing (ssh -G ...) of HostKeyAlgorithms=+...
  * ssh(1): fix expansion of HostkeyAlgorithms=+...
  Documentation:
  * ssh_config(5), sshd_config(5): update default algorithm lists
    to match current reality.
  * ssh(1): mention -Q key-plain and -Q key-cert query options.
  * sshd_config(8): more clearly describe what
    AuthorizedKeysFile=none does.
  * ssh_config(5): better document ExitOnForwardFailure.
  * sshd(5): mention internal DH-GEX fallback groups in manual.
  * sshd_config(5): better description for MaxSessions option.
  Portability:
  * sshd(8): fix multiple authentication using S/Key.
- OpenSSH 7.2p2:
  Security:
  * sshd(8): sanitise X11 authentication credentials to avoid
    xauth command injection when X11Forwarding is enabled.
- (removing patches from previous version:
  openssh-6.6p1-X11-forwarding.patch
  openssh-6.6p1-X_forward_with_disabled_ipv6.patch
  openssh-6.6p1-audit1-remove_duplicit_audit.patch
  openssh-6.6p1-audit2-better_audit_of_user_actions.patch
  openssh-6.6p1-audit3-key_auth_usage-fips.patch
  openssh-6.6p1-audit3-key_auth_usage.patch
  openssh-6.6p1-audit4-kex_results-fips.patch
  openssh-6.6p1-audit4-kex_results.patch
  openssh-6.6p1-audit5-session_key_destruction.patch
  openssh-6.6p1-audit6-server_key_destruction.patch
  openssh-6.6p1-audit7-libaudit_compat.patch
  openssh-6.6p1-audit8-libaudit_dns_timeouts.patch
  openssh-6.6p1-blocksigalrm.patch
  openssh-6.6p1-curve25519-6.6.1p1.patch
  openssh-6.6p1-default-protocol.patch
  openssh-6.6p1-disable-openssl-abi-check.patch
  openssh-6.6p1-disable_roaming.patch
  openssh-6.6p1-eal3.patch
  openssh-6.6p1-fingerprint_hash.patch
  openssh-6.6p1-fips-checks.patch
  openssh-6.6p1-fips.patch
  openssh-6.6p1-gssapi_key_exchange.patch
  openssh-6.6p1-gssapimitm.patch
  openssh-6.6p1-host_ident.patch
  openssh-6.6p1-key-converter.patch
  openssh-6.6p1-lastlog.patch
  openssh-6.6p1-ldap.patch
  openssh-6.6p1-login_options.patch
  openssh-6.6p1-no_fork-no_pid_file.patch
  openssh-6.6p1-pam-check-locks.patch
  openssh-6.6p1-pam-fix2.patch
  openssh-6.6p1-pam-fix3.patch
  openssh-6.6p1-pts.patch
  openssh-6.6p1-saveargv-fix.patch
  openssh-6.6p1-seccomp_getuid.patch
  openssh-6.6p1-seccomp_stat.patch
  openssh-6.6p1-seed-prng.patch
  openssh-6.6p1-send_locale.patch
  openssh-6.6p1-sftp_force_permissions.patch
  openssh-6.6p1-sftp_homechroot.patch
  openssh-6.6p1-xauth.patch
  openssh-6.6p1-xauthlocalhostname.patch)
* Thu Apr  7 2016 pcerny@suse.com
- Correctly parse GSSAPI KEX algorithms (bsc#961368)
- Sanitise input for xauth(1) (bsc#970632, CVE-2016-3115)
  [-sanitise_xauth_input]
- prevent X11 SECURITY circumvention when forwarding X11
  connections (bsc#962313, CVE-2016-1908)
  [-untrusted_X_forwarding]
- more verbose FIPS mode/CC related documentation in README.FIPS
  (bsc#965576, bsc#960414)
- fix PRNG re-seeding (bsc#960414, bsc#729190)
- Disable DH parameters under 2048 bits by default and allow
  lowering the limit back to the RFC 4419 specified minimum
  through an option (bsc#932483, bsc#948902)
  [-disable_DH_under_1536b -> -disable_short_DH_parameters]
- ignore PAM environment when using login
  (bsc#975865, CVE-2015-8325)
  [-ignore_PAM_with_UseLogin]
* Tue Mar  8 2016 pcerny@suse.com
- fix minor problems (bsc#945493)
- fix postun script of main package (bsc#945484)
- fix crashes when /proc is not available (bsc#947458)
- rename and comment the roaming patch
  (CVE-2016-077-7_8 to -disable_roaming)
* Wed Jan 13 2016 jsegitz@novell.com
- CVE-2016-0777, bsc#961642, CVE-2016-0778, bsc#961645
  Added CVE-2016-077-7_8.patch to disable the roaming code to prevent
  information leak and buffer overflow
* Fri Jul 31 2015 pcerny@suse.com
- Maintenance update
  * better timeouting of X11 forwards (CVE-2015-5352/bsc#936695)
    [-X11_forwarding_timeout] and hardening of ssh-agent(1)
    locking (bsc#936695) [-agent_locking_hardening]
  * removing and disabling short DH parameters (bsc#932483)
    [-disable_DH_under_1536b, -remove_moduli_under_1536b]
  * disable accdess to procfs from sftp (bsc#903649)
    [-sftp_procfs_restrictions]
  * Allow each keyboard authentication method to be used only
    once per login (CVE-2015-5600/bsc#938746)
    [-use_each_kbd_method_just_once]
  * Don't resend username to PAM, it can be misused for privilege
    escalation (CVE-2015-6563/bsc#943010)
    [-pam_privsep_dont_resend_username]
  * Prevent possible use-after-free in PAM authentication monitor
    (CVE-2015-6564/bsc#943006)
    [-pam_privsep_auth_uaf]
* Thu May 14 2015 pcerny@suse.com
- use %%restart_on_update in the trigger script
* Fri Apr 10 2015 pcerny@suse.com
- Fix dependencies of the main package and the -fips subpackage
  to include exact build number, so that mismatching hashes are
  removed on upgrade.
  (bsc#924476)
* Tue Feb 10 2015 pcerny@suse.com
- CAVS test for KDF (bsc#916905)
  [-cavstest-kdf.patch]
- CAVS related parts now reside in the -cavs subpackage
- changing license to 2-clause BSD and MIT, since that reflects
  better what the code is licenced under
* Fri Feb  6 2015 pcerny@suse.com
- Change FIPS integrity tests to use HMAC instead of plain hash
  (bsc#916473)
* Tue Jan 13 2015 pcerny@suse.com
- Add hmac-sha1-etm to MACs available inthe FIPS 140-2 mode
  (bsc#912489)
- allow stat() syscall pulled in by OpenSSL certification
  (bsc#912436, bsc#855676)
  [-seccomp_stat patch]
- enable building without auditing support
* Tue Oct 28 2014 pcerny@suse.com
- key exchange modifications for FIPS
* Thu Aug  7 2014 pcerny@suse.com
- change FIPS checksum files and subpackage naming (bnc#856316)
* Fri Jul 25 2014 pcerny@suse.com
- ssh(1) - correct FIPS checks to prevent connection fails when
  protocol version is not explicitly requested (bnc#876704)
- ssh-keygen(1) - do not create DSA and RSA1 keys in FIPS mode
  when generating all server keys (bnc#886845)
- fix SUSE spelling (bnc#889014)
* Fri Jul  4 2014 pcerny@suse.com
- Prevent other possible crashes in audit code due to abnormal
  execution paths (generalized previous fix for bnc#832628)
* Fri Jun 13 2014 pcerny@suse.com
- exit sshd normally when port is already in use (bnc#832628)
- fix forwarding with IPv6 addresses in DISPLAY (bnc#847710)
  [-IPv6_X_forwarding.patch]
- check SSHFP DNS records even for server certificates
  (bnc#870532, CVE-2014-2653)
  [-check_sshfp_for_certs.patch]
- removing the key converter (which hasn't been built since
  the update to 6.5p1) patch from sources
  [-key-converter.patch]
* Thu Apr 24 2014 pcerny@suse.com
- curve25519 key exchange fix (-curve25519-6.6.1p1.patch)
- patch re-ordering (-audit3-key_auth_usage-fips.patch,
  - audit4-kex_results-fips.patch)
- remove uneeded dependency on the OpenLDAP server (openldap2)
  in the helpers subpackage
* Fri Apr 11 2014 pcerny@suse.com
- update to 6.6p1
  Security:
  * sshd(8): when using environment passing with a sshd_config(5)
    AcceptEnv pattern with a wildcard. OpenSSH prior to 6.6 could
    be tricked into accepting any enviornment variable that
    contains the characters before the wildcard character.
  Features since 6.5p1:
  * ssh(1), sshd(8): removal of the J-PAKE authentication code,
    which was experimental, never enabled and has been
    unmaintained for some time.
  * ssh(1): skip 'exec' clauses other clauses predicates failed
    to match while processing Match blocks.
  * ssh(1): if hostname canonicalisation is enabled and results
    in the destination hostname being changed, then re-parse
    ssh_config(5) files using the new destination hostname. This
    gives 'Host' and 'Match' directives that use the expanded
    hostname a chance to be applied.
  Bugfixes:
  * ssh(1): avoid spurious "getsockname failed: Bad file
    descriptor" in ssh -W. bz#2200, debian#738692
  * sshd(8): allow the shutdown(2) syscall in seccomp-bpf and
    systrace sandbox modes, as it is reachable if the connection
    is terminated during the pre-auth phase.
  * ssh(1), sshd(8): fix unsigned overflow that in SSH protocol 1
    bignum parsing. Minimum key length checks render this bug
    unexploitable to compromise SSH 1 sessions.
  * sshd_config(5): clarify behaviour of a keyword that appears
    in multiple matching Match blocks. bz#2184
  * ssh(1): avoid unnecessary hostname lookups when
    canonicalisation is disabled. bz#2205
  * sshd(8): avoid sandbox violation crashes in GSSAPI code by
    caching the supported list of GSSAPI mechanism OIDs before
    entering the sandbox. bz#2107
  * ssh(1): fix possible crashes in SOCKS4 parsing caused by
    assumption that the SOCKS username is nul-terminated.
  * ssh(1): fix regression for UsePrivilegedPort=yes when
    BindAddress is not specified.
  * ssh(1), sshd(8): fix memory leak in ECDSA signature
    verification.
  * ssh(1): fix matching of 'Host' directives in ssh_config(5)
    files to be case-insensitive again (regression in 6.5).
- FIPS checks in sftp-server
* Mon Mar 31 2014 pcerny@suse.com
- FIPS checks during ssh client and daemon startup
  (-fips-checks.patch)
* Mon Mar 17 2014 pcerny@suse.com
- re-enabling the GSSAPI Key Exchange patch
* Fri Feb 28 2014 pcerny@suse.com
- re-enabling FIPS-enablement patch
- enable X11 forwarding when IPv6 is present but disabled on server
  (bnc#712683, FATE#315036)
* Tue Feb 18 2014 pcerny@suse.com
- re-enabling the seccomp sandbox
  (allowing use of getuid the syscall)
* Tue Feb 18 2014 pcerny@suse.com
- disabling seccomp sandboxing which doesn't work properly on SLE
* Wed Feb 12 2014 pcerny@suse.com
- Update to 6.5p1
  Features since 6.4p1:
  * ssh(1), sshd(8): support for key exchange using ECDH in
    Daniel Bernstein's Curve25519; default when both the client
    and server support it.
  * ssh(1), sshd(8): support for Ed25519 as a public key type fo
    rboth server and client.  Ed25519 is an EC signature offering
    better security than ECDSA and DSA and good performance.
  * Add a new private key format that uses a bcrypt KDF to better
    protect keys at rest. Used unconditionally for Ed25519 keys,
    on demand for other key types via the -o ssh-keygen(1)
    option.  Intended to become default in the near future.
    Details documented in PROTOCOL.key.
  * ssh(1), sshd(8): new transport cipher
    "chacha20-poly1305@openssh.com" combining Daniel Bernstein's
    ChaCha20 stream cipher and Poly1305 MAC to build an
    authenticated encryption mode. Details documented
    PROTOCOL.chacha20poly1305.
  * ssh(1), sshd(8): refuse RSA keys from old proprietary clients
    and servers that use the obsolete RSA+MD5 signature scheme.
    It will still be possible to connect with these
    clients/servers but only DSA keys will be accepted, and
    OpenSSH will refuse connection entirely in a future release.
  * ssh(1), sshd(8): refuse old proprietary clients and servers
    that use a weaker key exchange hash calculation.
  * ssh(1): increase the size of the Diffie-Hellman groups
    requested for each symmetric key size. New values from NIST
    Special Publication 800-57 with the upper limit specified by
    RFC4419.
  * ssh(1), ssh-agent(1): support pkcs#11 tokens that only
    provide X.509 certs instead of raw public keys (requested as
    bz#1908).
  * ssh(1): new ssh_config(5) "Match" keyword that allows
    conditional configuration to be applied by matching on
    hostname, user and result of arbitrary commands.
  * ssh(1): support for client-side hostname canonicalisation
    using a set of DNS suffixes and rules in ssh_config(5). This
    allows unqualified names to be canonicalised to
    fully-qualified domain names to eliminate ambiguity when
    looking up keys in known_hosts or checking host certificate
    names.
  * sftp-server(8): ability to whitelist and/or blacklist sftp
    protocol requests by name.
  * sftp-server(8): sftp "fsync@openssh.com" to support calling
    fsync(2) on an open file handle.
  * sshd(8): ssh_config(5) PermitTTY to disallow TTY allocation,
    mirroring the longstanding no-pty authorized_keys option.
  * ssh(1): ssh_config ProxyUseFDPass option that supports the
    use of ProxyCommands that establish a connection and then
    pass a connected file descriptor back to ssh(1). This allows
    the ProxyCommand to exit rather than staying around to
    transfer data.
  Bugfixes since 6.4p1:
  * ssh(1), sshd(8): fix potential stack exhaustion caused by
    nested certificates.
  * ssh(1): bz#1211: make BindAddress work with
    UsePrivilegedPort.
  * sftp(1): bz#2137: fix the progress meter for resumed
    transfer.
  * ssh-add(1): bz#2187: do not request smartcard PIN when
    removing keys from ssh-agent.
  * sshd(8): bz#2139: fix re-exec fallback when original sshd
    binary cannot be executed.
  * ssh-keygen(1): make relative-specified certificate expiry
    times relative to current time and not the validity start
    time.
  * sshd(8): bz#2161: fix AuthorizedKeysCommand inside a Match
    block.
  * sftp(1): bz#2129: symlinking a file would incorrectly
    canonicalise the target path.
  * ssh-agent(1): bz#2175: fix a use-after-free in the PKCS#11
    agent helper executable.
  * sshd(8): improve logging of sessions to include the user
    name, remote host and port, the session type (shell, command,
    etc.) and allocated TTY (if any).
  * sshd(8): bz#1297: tell the client (via a debug message) when
    their preferred listen address has been overridden by the
    server's GatewayPorts setting.
  * sshd(8): bz#2162: include report port in bad protocol banner
    message.
  * sftp(1): bz#2163: fix memory leak in error path in
    do_readdir().
  * sftp(1): bz#2171: don't leak file descriptor on error.
  * sshd(8): include the local address and port in "Connection
    from ..." message (only shown at loglevel>=verbose).
- systemd systems
  * create sysconfig file on systemd systems as well, yet do not
    require it at run-time (bnc#862600)
  * symlink rcsshd to /usr/bin/service
- rename "-forcepermissions" patch to "-sftp_force_permissions"
- disable key converter - ssh-keygen is able to do the same
* Tue Feb 11 2014 hare@suse.de
- Do not fail if sysconfig file isn't installed (bnc#862600)
* Wed Feb  5 2014 idonmez@suse.com
- Add openssh-6.2p1-forcepermissions.patch to implement a force
  permissions mode (fate#312774). The patch is based on
  http://marc.info/?l=openssh-unix-dev&m=128896838930893
* Fri Jan 24 2014 pcerny@suse.com
- Update to 6.4p1
  Features since 6.2p2:
  * ssh-agent(1) support in sshd(8); allows encrypted hostkeys, or
    hostkeys on smartcards.
  * ssh(1)/sshd(8): allow optional time-based rekeying via a
    second argument to the existing RekeyLimit option. RekeyLimit
    is now supported in sshd_config as well as on the client.
  * sshd(8): standardise logging of information during user
    authentication.
  * The presented key/cert and the remote username (if available)
    is now logged in the authentication success/failure message on
    the same log line as the local username, remote host/port and
    protocol in use.  Certificates contents and the key
    fingerprint of the signing CA are logged too.
  * ssh(1) ability to query what cryptographic algorithms are
    supported in the binary.
  * ssh(1): ProxyCommand=- for cases where stdin and stdout
    already point to the proxy.
  * ssh(1): allow IdentityFile=none
  * ssh(1)/sshd(8): -E option to append debugging logs to a
    specified file instead of stderr or syslog.
  * sftp(1): support resuming partial downloads with the "reget"
    command and on the sftp commandline or on the "get"
    commandline with the "-a" (append) option.
  * ssh(1): "IgnoreUnknown" configuration option to selectively
    suppress errors arising from unknown configuration directives.
  * sshd(8): support for submethods to be appended to required
    authentication methods listed via AuthenticationMethods.
  Bugfixes since 6.2p2:
  * sshd(8): fix refusal to accept certificate if a key of a
    different type to the CA key appeared in authorized_keys
    before the CA key.
  * ssh(1)/ssh-agent(1)/sshd(8): Use a monotonic time source for
    timers so that things like keepalives and rekeying will work
    properly over clock steps.
  * sftp(1): update progressmeter when data is acknowledged, not
    when it's sent. bz#2108
  * ssh(1)/ssh-keygen(1): improve error messages when the current
    user does not exist in /etc/passwd; bz#2125
  * ssh(1): reset the order in which public keys are tried after
    partial authentication success.
  * ssh-agent(1): clean up socket files after SIGINT when in debug
    mode; bz#2120
  * ssh(1) and others: avoid confusing error messages in the case
    of broken system resolver configurations; bz#2122
  * ssh(1): set TCP nodelay for connections started with -N;
    bz#2124
  * ssh(1): correct manual for permission requirements on
    ~/.ssh/config; bz#2078
  * ssh(1): fix ControlPersist timeout not triggering in cases
    where TCP connections have hung. bz#1917
  * ssh(1): properly deatch a ControlPersist master from its
    controlling terminal.
  * sftp(1): avoid crashes in libedit when it has been compiled
    with multi- byte character support. bz#1990
  * sshd(8): when running sshd -D, close stderr unless we have
    explicitly requested logging to stderr. bz#1976,
  * ssh(1): fix incomplete bzero; bz#2100
  * sshd(8): log and error and exit if ChrootDirectory is
    specified and running without root privileges.
  * Many improvements to the regression test suite. In particular
    log files are now saved from ssh and sshd after failures.
  * Fix a number of memory leaks. bz#1967 bz#2096 and others
  * sshd(8): fix public key authentication when a :style is
    appended to the requested username.
  * ssh(1): do not fatally exit when attempting to cleanup
    multiplexing- created channels that are incompletely opened.
    bz#2079
  * sshd(8): fix a memory corruption problem triggered during
    rekeying when an AES-GCM cipher is selected
  * Fix unaligned accesses in umac.c for strict-alignment
    architectures.  bz#2101
  * Fix broken incorrect commandline reporting errors. bz#1448
  * Only include SHA256 and ECC-based key exchange methods if
    libcrypto has the required support.
  * Fix crash in SOCKS5 dynamic forwarding code on
    strict-alignment architectures.
  - FIPS and GSSKEX patched disabled for now
* Fri Oct  4 2013 pcerny@suse.com
- fix server crashes when using AES-GCM
- removed superfluous build dependency on X
* Thu Sep 19 2013 pcerny@suse.com
- spec file and patch cleanup
  * key converter is now in the -key-converter.patch
  * openssh-nodaemon-nopid.patch is -no_fork-no_pid_file.patch
  * openssh-nocrazyabicheck.patch is
  - disable-openssl-abi-check.patch
  * removing obsolete -engines.diff patch
- patches from SLE11
  * use auditing infrastructure extending upstream hooks
    (-auditX-*.patch) instead of the single old patch
    (-audit.patch)
  * FIPS enablement (currently disabled)
    (-fingerprint_hash.patch, -fips.patch)
  * GSSAPI key exchange
    (bnc#784689, fate#313068, -gssapi_key_exchange.patch)
  * SysV init script update - 'stop' now terminates all sshd
    processes and closes all connections, 'soft-stop' only
    terminates the listener process (keeps active sessions intact)
    (fate#314243)
  * helper application for retrieving users' public keys from
    an LDAP server (bnc#683733, fate#302144, -ldap.patch)
  - subpackage openssh-akc-ldap
  * several bugfixes:
  - login invocation
    (bnc#833605, -login_options.patch)
  - disable locked accounts when using PAM
    (bnc#708678, fate#312033, -pam-check-locks.patch)
  - fix wtmp handling
    (bnc#18024, -lastlog.patch)
- init script is moved into documentation for openSUSE 12.3+
  (as it confused systemd)
* Tue Sep 10 2013 crrodriguez@opensuse.org
- fix the logic in openssh-nodaemon-nopid.patch which is broken
  and pid_file therefore still being created.
* Sat Aug  3 2013 crrodriguez@opensuse.org
- Update to version 6.2p2
  * ssh(1)/sshd(8): Added support for AES-GCM authenticated encryption
  * ssh(1)/sshd(8): Added support for encrypt-then-mac (EtM) MAC modes
  * ssh(1)/sshd(8): Added support for the UMAC-128 MAC
  * sshd(8): Added support for multiple required authentication
  * sshd(8)/ssh-keygen(1): Added support for Key Revocation Lists
  * ssh(1): When SSH protocol 2 only is selected (the default), ssh(1)
  now immediately sends its SSH protocol banner to the server without
  waiting to receive the server's banner, saving time when connecting.
  * dozens of other changes, see http://www.openssh.org/txt/release-6.2
* Mon Jul  1 2013 coolo@suse.com
- avoid the build cycle between curl, krb5, libssh2_org and openssh
  by using krb5-mini-devel
* Wed Jun 19 2013 speilicke@suse.com
- Recommend xauth, X11-forwarding won't work if it is not installed
* Sun Apr 14 2013 crrodriguez@opensuse.org
- sshd.service: Do not order after syslog.target, it is
  not required or recommended and that target does not even exist
  anymore.
* Tue Jan  8 2013 dmueller@suse.com
- use ssh-keygen(1) default keylengths in generating the host key
  instead of hardcoding it
* Tue Nov 13 2012 meissner@suse.com
- Updated to 6.1p1, a bugfix release
  Features:
  * sshd(8): This release turns on pre-auth sandboxing sshd by default for
  new installs, by setting UsePrivilegeSeparation=sandbox in sshd_config.
  * ssh-keygen(1): Add options to specify starting line number and number of
  lines to process when screening moduli candidates, allowing processing
  of different parts of a candidate moduli file in parallel
  * sshd(8): The Match directive now supports matching on the local (listen)
  address and port upon which the incoming connection was received via
  LocalAddress and LocalPort clauses.
  * sshd(8): Extend sshd_config Match directive to allow setting AcceptEnv
  and {Allow,Deny}{Users,Groups}
  * Add support for RFC6594 SSHFP DNS records for ECDSA key types. bz#1978
  * ssh-keygen(1): Allow conversion of RSA1 keys to public PEM and PKCS8
  * sshd(8): Allow the sshd_config PermitOpen directive to accept "none" as
  an argument to refuse all port-forwarding requests.
  * sshd(8): Support "none" as an argument for AuthorizedPrincipalsFile
  * ssh-keyscan(1): Look for ECDSA keys by default. bz#1971
  * sshd(8): Add "VersionAddendum" to sshd_config to allow server operators
  to append some arbitrary text to the server SSH protocol banner.
  Bugfixes:
  * ssh(1)/sshd(8): Don't spin in accept() in situations of file
  descriptor exhaustion. Instead back off for a while.
  * ssh(1)/sshd(8): Remove hmac-sha2-256-96 and hmac-sha2-512-96 MACs as
  they were removed from the specification. bz#2023,
  * sshd(8): Handle long comments in config files better. bz#2025
  * ssh(1): Delay setting tty_flag so RequestTTY options are correctly
  picked up. bz#1995
  * sshd(8): Fix handling of /etc/nologin incorrectly being applied to root
  on platforms that use login_cap.
  Portable OpenSSH:
  * sshd(8): Allow sshd pre-auth sandboxing to fall-back to the rlimit
  sandbox from the Linux SECCOMP filter sandbox when the latter is
  not available in the kernel.
  * ssh(1): Fix NULL dereference when built with LDNS and using DNSSEC to
  retrieve a CNAME SSHFP record.
  * Fix cross-compilation problems related to pkg-config. bz#1996
* Tue Nov 13 2012 kukuk@suse.de
- Fix groupadd arguments
- Add LSB tag to sshd init script
* Fri Oct 26 2012 coolo@suse.com
- explicit buildrequire groff, needed for man pages
* Tue Oct 16 2012 coolo@suse.com
- buildrequire systemd through pkgconfig to break cycle
* Wed Aug 15 2012 crrodriguez@opensuse.org
- When not daemonizing, such is used with systemd, no not
  create a PID file
* Mon Jun 18 2012 coolo@suse.com
- do not buildrequire xorg-x11, the askpass is an extra package
  and should build from a different package
* Tue May 29 2012 meissner@suse.com
- use correct download url and tarball format.
* Tue May 29 2012 crrodriguez@opensuse.org
- Update to version 6.0, large list of changes, seen
  http://www.openssh.org/txt/release-6.0 for detail.
* Thu May 10 2012 crrodriguez@opensuse.org
- By default openSSH checks at *runtime* if the openssl
  API version matches with the running library, that might
  be good if you are compiling SSH yourself but it is a totally
  insane way to check for binary/source compatibility in a distribution.
* Mon Feb 20 2012 meissner@suse.com
- include X11 app default dir
* Fri Dec 23 2011 brian@aljex.com
- Fix building for OS 11.0, 10.3, 10.2
  * Don't require selinux on OS 11.0 or lower
* Fri Dec 23 2011 brian@aljex.com
- Fix building for OS 11.2 and 11.1
- Cleanup remove remaining litteral /etc/init.d 's
* Wed Dec 21 2011 coolo@suse.com
- add autoconf as buildrequire to avoid implicit dependency
* Tue Nov 29 2011 crrodriguez@opensuse.org
- Add systemd startup units
* Sat Oct 29 2011 pcerny@suse.com
- finalising libexecdir change (bnc#726712)
* Wed Oct 19 2011 pcerny@suse.com
- Update to 5.9p1
  * sandboxing privsep child through rlimit
* Fri Sep 16 2011 jengelh@medozas.de
- Avoid overriding libexecdir with %%_lib (bnc#712025)
- Clean up the specfile by request of Minh Ngo, details entail:
  * remove norootforbuild comments, redundant %%clean section
  * run spec-beautifier over it
- Add PIEFLAGS to compilation of askpass; fails otherwise
* Mon Aug 29 2011 crrodriguez@opensuse.org
-  Update to verison 5.8p2
  * Fixed vuln in systems without dev/random, we arenot affected
  * Fixes problems building with selinux enabled
- Fix build with as-needed and no-add-needed
* Sat Aug 13 2011 crrodriguez@opensuse.org
- Enable libedit/autocompletion support in sftp
* Tue May 10 2011 meissner@novell.com
- Change default keysizes of rsa and dsa from 1024 to 2048
  to match ssh-keygen manpage recommendations.
* Fri Feb  4 2011 lchiquitto@novell.com
- Update to 5.8p1
  * Fix vulnerability in legacy certificate signing introduced in
  OpenSSH-5.6 and found by Mateusz Kocielski.
  * Fix compilation failure when enableing SELinux support.
  * Do not attempt to call SELinux functions when SELinux is
  disabled.
- Remove patch that is now upstream:
  * openssh-5.7p1-selinux.diff
* Thu Feb  3 2011 pcerny@novell.com
- specfile/patches cleanup
* Mon Jan 24 2011 lchiquitto@novell.com
- Update to 5.7p1
  * Implement Elliptic Curve Cryptography modes for key exchange (ECDH)
  and host/user keys (ECDSA) as specified by RFC5656.
  * sftp(1)/sftp-server(8): add a protocol extension to support a hard
  link operation.
  * scp(1): Add a new -3 option to scp: Copies between two remote hosts
  are transferred through the local host.
  * ssh(1): automatically order the hostkeys requested by the client
  based on which hostkeys are already recorded in known_hosts.
  * ssh(1)/sshd(8): add a new IPQoS option to specify arbitrary
  TOS/DSCP/QoS values instead of hardcoding lowdelay/throughput.
  * sftp(1): the sftp client is now significantly faster at performing
  directory listings, using OpenBSD glob(3) extensions to preserve
  the results of stat(3) operations performed in the course of its
  execution rather than performing expensive round trips to fetch
  them again afterwards.
  * ssh(1): "atomically" create the listening mux socket by binding it on
  a temporary name and then linking it into position after listen() has
  succeeded.
  * ssh(1)/sshd(8): add a KexAlgorithms knob to the client and server
  configuration to allow selection of which key exchange methods are
  used by ssh(1) and sshd(8) and their order of preference.
  * sftp(1)/scp(1): factor out bandwidth limiting code from scp(1) into
  a generic bandwidth limiter that can be attached using the atomicio
  callback mechanism and use it to add a bandwidth limit option to
  sftp(1).
  * Support building against openssl-1.0.0a.
  * Bug fixes.
- Remove patches that are now upstream:
  * openssh-5.6p1-tmpdir.diff
  * openssh-linux-new-oomkill.patch
- Add upstream patch to fix build with SELinux enabled.
* Wed Jan 12 2011 sbrabec@suse.cz
- Removed relics of no more implemented opensc support.
* Thu Nov 18 2010 lnussel@suse.de
- add pam_lastlog to show failed login attempts
- remove permissions handling, no special handling needed
* Tue Nov 16 2010 cristian.rodriguez@opensuse.org
- Use upstream oom_adj is deprecated patch
* Tue Nov  2 2010 coolo@novell.com
- remove the code trying to patch X11 paths - which was broken
  for a very long time and was useless anyway as the Makefiles
  do this correctly themselves
* Sun Oct 31 2010 jengelh@medozas.de
- Use %%_smp_mflags
* Thu Oct 14 2010 crrodriguez@opensuse.org
- Fix warning "oom_adj is deprecated use oom_score_adj instead"
* Mon Sep 13 2010 anicka@suse.cz
- actualize README.SuSE (bnc#638893)
* Tue Aug 24 2010 anicka@suse.cz
- update to 5.6p1
  * Added a ControlPersist option to ssh_config(5) that automatically
  starts a background ssh(1) multiplex master when connecting.
  * Hostbased authentication may now use certificate host keys.
  * ssh-keygen(1) now supports signing certificate using a CA key that
  has been stored in a PKCS#11 token.
  * ssh(1) will now log the hostname and address that we connected to at
  LogLevel=verbose after authentication is successful to mitigate
  "phishing" attacks by servers with trusted keys that accept
  authentication silently and automatically before presenting fake
  password/passphrase prompts.
  * Expand %%h to the hostname in ssh_config Hostname options.
  * Allow ssh-keygen(1) to import (-i) and export (-e) of PEM and PKCS#8
  keys in addition to RFC4716 (SSH.COM) encodings via a new -m option
  * sshd(8) will now queue debug messages for bad ownership or
  permissions on the user's keyfiles encountered during authentication
  and will send them after authentication has successfully completed.
  * ssh(1) connection multiplexing now supports remote forwarding with
  dynamic port allocation and can report the allocated port back to
  the user
  * sshd(8) now supports indirection in matching of principal names
  listed in certificates.
  * sshd(8) now has a new AuthorizedPrincipalsFile option to specify a
  file containing a list of names that may be accepted in place of the
  username when authorizing a certificate trusted via the
  sshd_config(5) TrustedCAKeys option.
  * Additional sshd_config(5) options are now valid inside Match blocks
  * Revised the format of certificate keys.
  * bugfixes
- removed -forward patch (SSH_MAX_FORWARDS_PER_DIRECTION not hard-coded
  any more), removed memory leak fix (fixed in upstream)
* Fri Aug 20 2010 anicka@suse.cz
- hint user how to remove offending keys (bnc#625552)
* Thu Jul 22 2010 anicka@suse.cz
- update to 5.5p1
* Tue Jul 20 2010 anicka@suse.cz
- update to 5.5p1
  * Allow ChrootDirectory to work in SELinux platforms.
  * bugfixes
* Wed Jun 30 2010 meissner@suse.de
- Disable visual hostkey support again, after discussion on
  its usefulness.
* Mon May 17 2010 cristian.rodriguez@opensuse.org
- Hardware crypto is supported and patched but never
  enabled, need to use --with-ssl-engine explicitely
* Fri May 14 2010 anicka@suse.cz
- fixed memory leak in sftp (bnc#604274)
* Fri Apr 23 2010 anicka@suse.cz
- honour /etc/nologin (bnc#530885)
* Thu Mar 25 2010 meissner@suse.de
- Enable VisualHostKey (ascii art of the hostkey fingerprint) and
  HashHostKeys (hardening measure to make them unusable for worms/malicious
  users for further host hopping).
* Tue Mar 23 2010 anicka@suse.cz
- update to 5.4p1
  * After a transition period of about 10 years, this release disables
  SSH protocol 1 by default. Clients and servers that need to use the
  legacy protocol must explicitly enable it in ssh_config / sshd_config
  or on the command-line.
  * Remove the libsectok/OpenSC-based smartcard code and add support for
  PKCS#11 tokens. This support is automatically enabled on all
  platforms that support dlopen(3) and was inspired by patches written
  by Alon Bar-Lev. Details in the ssh(1) and ssh-add(1) manpages.
  * Add support for certificate authentication of users and hosts using a
  new, minimal OpenSSH certificate format (not X.509). Certificates
  contain a public key, identity information and some validity
  constraints and are signed with a standard SSH public key using
  ssh-keygen(1). CA keys may be marked as trusted in authorized_keys
  or via a TrustedUserCAKeys option in sshd_config(5) (for user
  authentication), or in known_hosts (for host authentication).
  Documentation for certificate support may be found in ssh-keygen(1),
  sshd(8) and ssh(1) and a description of the protocol extensions in
  PROTOCOL.certkeys.
  * Added a 'netcat mode' to ssh(1): "ssh -W host:port ..." This connects
  stdio on the client to a single port forward on the server. This
  allows, for example, using ssh as a ProxyCommand to route connections
  via intermediate servers. bz#1618
  * Add the ability to revoke keys in sshd(8) and ssh(1). User keys may
  be revoked using a new sshd_config(5) option "RevokedKeys". Host keys
  are revoked through known_hosts (details in the sshd(8) man page).
  Revoked keys cannot be used for user or host authentication and will
  trigger a warning if used.
  * Rewrite the ssh(1) multiplexing support to support non-blocking
  operation of the mux master, improve the resilience of the master to
  malformed messages sent to it by the slave and add support for
  requesting port- forwardings via the multiplex protocol. The new
  stdio-to-local forward mode ("ssh -W host:port ...") is also
  supported. The revised multiplexing protocol is documented in the
  file PROTOCOL.mux in the source distribution.
  * Add a 'read-only' mode to sftp-server(8) that disables open in write
  mode and all other fs-modifying protocol methods. bz#430
  * Allow setting an explicit umask on the sftp-server(8) commandline to
  override whatever default the user has. bz#1229
  * Many improvements to the sftp(1) client, many of which were
  implemented by Carlos Silva through the Google Summer of Code
  program:
  - Support the "-h" (human-readable units) flag for ls
  - Implement tab-completion of commands, local and remote filenames
  - Support most of scp(1)'s commandline arguments in sftp(1), as a
    first step towards making sftp(1) a drop-in replacement for scp(1).
    Note that the rarely-used "-P sftp_server_path" option has been
    moved to "-D sftp_server_path" to make way for "-P port" to match
    scp(1).
  - Add recursive transfer support for get/put and on the commandline
  * New RSA keys will be generated with a public exponent of RSA_F4 ==
  (2**16)+1 == 65537 instead of the previous value 35.
  * Passphrase-protected SSH protocol 2 private keys are now protected
  with AES-128 instead of 3DES. This applied to newly-generated keys
  as well as keys that are reencrypted (e.g. by changing their
  passphrase).
- cleanup in patches
* Tue Mar  2 2010 coolo@novell.com
- do not use paths at all, but prereq packages
* Sat Feb 27 2010 aj@suse.de
- Use complete path for groupadd and useradd in pre section.
* Tue Feb 23 2010 anicka@suse.cz
- audit patch: add fix for bnc#545271
* Mon Feb 22 2010 anicka@suse.cz
- do not fix uid/gid anymore (bnc#536564)
* Tue Dec 15 2009 jengelh@medozas.de
- select large PIE for SPARC, it is required to avoid
  "relocation truncated to fit: R_SPARC_GOT13 against symbol xyz
  defined in COMMON section in sshd.o"
* Mon Sep 21 2009 anicka@suse.cz
- add new version of homechroot patch (added documentation, added
  check for nodev and nosuid)
- remove Provides and Obsoletes ssh
* Thu Aug 20 2009 anicka@suse.cz
- make sftp in chroot users life easier (ie. bnc#518238),
  many thanks jchadima@redhat.com for a patch
* Sun Jul 12 2009 coolo@novell.com
- readd $SSHD_BIN so that sshd starts at all
* Tue Jul  7 2009 llunak@novell.com  
- Added a hook for ksshaskpass
* Sun Jul  5 2009 dmueller@novell.com
- readd -f to startproc and remove -p instead to
  ensure that sshd is started even though old instances
  are still running (e.e. being logged in from remote)
* Fri Jun 19 2009 coolo@novell.com
- disable as-needed for this package as it fails to build with it
* Tue May 26 2009 anicka@suse.cz
- disable -f in startproc to calm the warning (bnc#506831)
* Thu Apr 23 2009 lnussel@suse.de
- do not enable sshd by default
* Mon Feb 23 2009 anicka@suse.cz
- update to 5.2p1
  * This release changes the default cipher order to prefer the AES CTR
  modes and the revised "arcfour256" mode to CBC mode ciphers that are
  susceptible to CPNI-957037 "Plaintext Recovery Attack Against SSH".
  * This release also adds countermeasures to mitigate CPNI-957037-style
  attacks against the SSH protocol's use of CBC-mode ciphers. Upon
  detection of an invalid packet length or Message Authentication
  Code, ssh/sshd will continue reading up to the maximum supported
  packet length rather than immediately terminating the connection.
  This eliminates most of the known differences in behaviour that
  leaked information about the plaintext of injected data which formed
  the basis of this attack. We believe that these attacks are rendered
  infeasible by these changes.
  * Added a -y option to ssh(1) to force logging to syslog rather than
  stderr, which is useful when running daemonised (ssh -f)
  * The sshd_config(5) ForceCommand directive now accepts commandline
  arguments for the internal-sftp server.
  * The ssh(1) ~C escape commandline now support runtime creation of
  dynamic (-D) port forwards.
  * Support the SOCKS4A protocol in ssh(1) dynamic (-D) forwards.
  (bz#1482)
  * Support remote port forwarding with a listen port of '0'. This
  informs the server that it should dynamically allocate a listen
  port and report it back to the client. (bz#1003)
  * sshd(8) now supports setting PermitEmptyPasswords and
  AllowAgentForwarding in Match blocks
  * Repair a ssh(1) crash introduced in openssh-5.1 when the client is
  sent a zero-length banner (bz#1496)
  * Due to interoperability problems with certain
  broken SSH implementations, the eow@openssh.com and
  no-more-sessions@openssh.com protocol extensions are now only sent
  to peers that identify themselves as OpenSSH.
  * Make ssh(1) send the correct channel number for
  SSH2_MSG_CHANNEL_SUCCESS and SSH2_MSG_CHANNEL_FAILURE messages to
  avoid triggering 'Non-public channel' error messages on sshd(8) in
  openssh-5.1.
  * Avoid printing 'Non-public channel' warnings in sshd(8), since the
  ssh(1) has sent incorrect channel numbers since ~2004 (this reverts
  a behaviour introduced in openssh-5.1).
  * Avoid double-free in ssh(1) ~C escape -L handler (bz#1539)
  * Correct fail-on-error behaviour in sftp(1) batchmode for remote
  stat operations. (bz#1541)
  * Disable nonfunctional ssh(1) ~C escape handler in multiplex slave
  connections. (bz#1543)
  * Avoid hang in ssh(1) when attempting to connect to a server that
  has MaxSessions=0 set.
  * Multiple fixes to sshd(8) configuration test (-T) mode
  * Several core and portable OpenSSH bugs fixed: 1380, 1412, 1418,
  1419, 1421, 1490, 1491, 1492, 1514, 1515, 1518, 1520, 1538, 1540
  * Many manual page improvements.
* Mon Dec  1 2008 anicka@suse.cz
- respect SSH_MAX_FORWARDS_PER_DIRECTION (bnc#448775)
* Mon Nov 10 2008 anicka@suse.cz
- fix printing banner (bnc#443380)
* Fri Oct 24 2008 anicka@suse.cz
- call pam functions in the right order (bnc#438292)
- mention default forwarding of locale settings in
  README.SuSE (bnc#434799)
* Tue Sep  9 2008 anicka@suse.cz
- remove pam_resmgr from sshd.pamd (bnc#422619)
* Sun Aug 24 2008 coolo@suse.de
- fix fillup macro usage
* Fri Aug 22 2008 prusnak@suse.cz
- enabled SELinux support [Fate#303662]
* Tue Jul 22 2008 anicka@suse.cz
- update to 5.1p1
  * sshd(8): Avoid X11 man-in-the-middle attack on HP/UX (and possibly
  other platforms) when X11UseLocalhost=no
  * Introduce experimental SSH Fingerprint ASCII Visualisation to ssh(1)
  and ssh-keygen(1). Visual fingerprinnt display is controlled by a new
  ssh_config(5) option "VisualHostKey".
  * sshd_config(5) now supports CIDR address/masklen matching in "Match
  address" blocks, with a fallback to classic wildcard matching.
  * sshd(8) now supports CIDR matching in ~/.ssh/authorized_keys
  from="..." restrictions, also with a fallback to classic wildcard
  matching.
  * Added an extended test mode (-T) to sshd(8) to request that it write
  its effective configuration to stdout and exit. Extended test mode
  also supports the specification of connection parameters (username,
  source address and hostname) to test the application of
  sshd_config(5) Match rules.
  * ssh(1) now prints the number of bytes transferred and the overall
  connection throughput for SSH protocol 2 sessions when in verbose
  mode (previously these statistics were displayed for protocol 1
  connections only).
  * sftp-server(8) now supports extension methods statvfs@openssh.com and
  fstatvfs@openssh.com that implement statvfs(2)-like operations.
  * sftp(1) now has a "df" command to the sftp client that uses the
  statvfs@openssh.com to produce a df(1)-like display of filesystem
  space and inode utilisation (requires statvfs@openssh.com support on
  the server)
  * Added a MaxSessions option to sshd_config(5) to allow control of the
  number of multiplexed sessions supported over a single TCP connection.
  This allows increasing the number of allowed sessions above the
  previous default of 10, disabling connection multiplexing
  (MaxSessions=1) or disallowing login/shell/subsystem sessions
  entirely (MaxSessions=0).
  * Added a no-more-sessions@openssh.com global request extension that is
  sent from ssh(1) to sshd(8) when the client knows that it will never
  request another session (i.e. when session multiplexing is disabled).
  This allows a server to disallow further session requests and
  terminate the session in cases where the client has been hijacked.
  * ssh-keygen(1) now supports the use of the -l option in combination
  with -F to search for a host in ~/.ssh/known_hosts and display its
  fingerprint.
  * ssh-keyscan(1) now defaults to "rsa" (protocol 2) keys, instead of
  "rsa1".
  * Added an AllowAgentForwarding option to sshd_config(8) to control
  whether authentication agent forwarding is permitted. Note that this
  is a loose control, as a client may install their own unofficial
  forwarder.
  * ssh(1) and sshd(8): avoid unnecessary malloc/copy/free when receiving
  network data, resulting in a ~10%% speedup
  * ssh(1) and sshd(8) will now try additional addresses when connecting
  to a port forward destination whose DNS name resolves to more than
  one address. The previous behaviour was to try the only first address
  and give up if that failed. (bz#383)
  * ssh(1) and sshd(8) now support signalling that channels are
  half-closed for writing, through a channel protocol extension
  notification "eow@openssh.com". This allows propagation of closed
  file descriptors, so that commands such as:
    "ssh -2 localhost od /bin/ls | true"
  do not send unnecessary data over the wire. (bz#85)
  * sshd(8): increased the default size of ssh protocol 1 ephemeral keys
  from 768 to 1024 bits.
  * When ssh(1) has been requested to fork after authentication
  ("ssh -f") with ExitOnForwardFailure enabled, delay the fork until
  after replies for any -R forwards have been seen. Allows for robust
  detection of -R forward failure when using -f. (bz#92)
  * "Match group" blocks in sshd_config(5) now support negation of
  groups. E.g. "Match group staff,!guests" (bz#1315)
  * sftp(1) and sftp-server(8) now allow chmod-like operations to set
  set[ug]id/sticky bits. (bz#1310)
  * The MaxAuthTries option is now permitted in sshd_config(5) match
  blocks.
  * Multiplexed ssh(1) sessions now support a subset of the ~ escapes
  that are available to a primary connection. (bz#1331)
  * ssh(1) connection multiplexing will now fall back to creating a new
  connection in most error cases. (bz#1439 bz#1329)
  * Added some basic interoperability tests against Twisted Conch.
  * Documented OpenSSH's extensions to and deviations from the published
  SSH protocols (the PROTOCOL file in the distribution)
  * Documented OpenSSH's ssh-agent protocol (PROTOCOL.agent).
  * bugfixes
- remove gssapi_krb5-fix patch
* Fri Apr 18 2008 werner@suse.de
- Handle pts slave lines like utemper
* Wed Apr  9 2008 anicka@suse.cz
- update to 5.0p1
  * CVE-2008-1483: Avoid possible hijacking of X11-forwarded
  connections by refusing to listen on a port unless all address
  families bind successfully.
- remove CVE-2008-1483 patch
* Wed Apr  2 2008 anicka@suse.cz
- update to 4.9p1
  * Disable execution of ~/.ssh/rc for sessions where a command has been
    forced by the sshd_config ForceCommand directive. Users who had
    write access to this file could use it to execute abritrary commands.
    This behaviour was documented, but was an unsafe default and an extra
    hassle for administrators.
  * Added chroot(2) support for sshd(8), controlled by a new option
    "ChrootDirectory". Please refer to sshd_config(5) for details, and
    please use this feature carefully. (bz#177 bz#1352)
  * Linked sftp-server(8) into sshd(8). The internal sftp server is
    used when the command "internal-sftp" is specified in a Subsystem
    or ForceCommand declaration. When used with ChrootDirectory, the
    internal sftp server requires no special configuration of files
    inside the chroot environment. Please refer to sshd_config(5) for
    more information.
  * Added a "no-user-rc" option for authorized_keys to disable execution
    of ~/.ssh/rc
  * Added a protocol extension method "posix-rename@openssh.com" for
    sftp-server(8) to perform POSIX atomic rename() operations.
    (bz#1400)
  * Removed the fixed limit of 100 file handles in sftp-server(8). The
    server will now dynamically allocate handles up to the number of
    available file descriptors. (bz#1397)
  * ssh(8) will now skip generation of SSH protocol 1 ephemeral server
    keys when in inetd mode and protocol 2 connections are negotiated.
    This speeds up protocol 2 connections to inetd-mode servers that
    also allow Protocol 1 (bz#440)
  * Accept the PermitRootLogin directive in a sshd_config(5) Match
    block. Allows for, e.g. permitting root only from the local
    network.
  * Reworked sftp(1) argument splitting and escaping to be more
    internally consistent (i.e. between sftp commands) and more
    consistent with sh(1). Please note that this will change the
    interpretation of some quoted strings, especially those with
    embedded backslash escape sequences. (bz#778)
  * Support "Banner=none" in sshd_config(5) to disable sending of a
    pre-login banner (e.g. in a Match block).
  * ssh(1) ProxyCommands are now executed with $SHELL rather than
    /bin/sh.
  * ssh(1)'s ConnectTimeout option is now applied to both the TCP
    connection and the SSH banner exchange (previously it just covered
    the TCP connection). This allows callers of ssh(1) to better detect
    and deal with stuck servers that accept a TCP connection but don't
    progress the protocol, and also makes ConnectTimeout useful for
    connections via a ProxyCommand.
  * Many new regression tests, including interop tests against PuTTY's
    plink.
  * Support BSM auditing on Mac OS X
  * bugfixes
- remove addrlist, pam_session_close, strict-aliasing-fix patches
  (not needed anymore)
* Tue Mar 25 2008 anicka@suse.cz
- fix CVE-2008-1483 (bnc#373527)
* Fri Jan  4 2008 anicka@suse.cz
- fix privileges of a firewall definition file [#351193]
* Fri Dec 14 2007 anicka@suse.cz
- add patch calling pam with root privileges [#334559]
- drop pwname-home patch [#104773]
* Fri Dec  7 2007 anicka@suse.cz
- fix race condition in xauth patch
* Wed Dec  5 2007 anicka@suse.cz
- update to 4.7p1
  * Add "-K" flag for ssh to set GSSAPIAuthentication=yes and
    GSSAPIDelegateCredentials=yes. This is symmetric with -k
  * make scp try to skip FIFOs rather than blocking when nothing is
    listening.
  * increase default channel windows
  * put the MAC list into a display
  * many bugfixes
* Mon Oct  8 2007 anicka@suse.cz
- block SIGALRM only during calling syslog() [#331032]
* Thu Sep 13 2007 nadvornik@suse.cz
- fixed checking of an untrusted cookie, CVE-2007-4752 [#308521]
* Tue Aug 28 2007 anicka@suse.cz
- fix blocksigalrm patch to set old signal mask after
  writing the log in every case [#304819]
* Tue Aug 21 2007 anicka@suse.cz
- avoid generating ssh keys when a non-standard location
  is configured [#281228]
* Wed Jul 25 2007 anicka@suse.cz
- fixed typo in sshd.fw [#293764]
* Mon Mar 19 2007 nadvornik@suse.cz
- fixed default for ChallengeResponseAuthentication [#255374]
* Mon Mar 12 2007 anicka@suse.cz
- update to 4.6p1
  * sshd now allows the enabling and disabling of authentication
    methods on a per user, group, host and network basis via the
    Match directive in sshd_config.
  * Allow multiple forwarding options to work when specified in a
    PermitOpen directive
  * Clear SIGALRM when restarting due to SIGHUP. Prevents stray
    signal from taking down sshd if a connection was pending at
    the time SIGHUP was received
  * hang on exit" when background processes are running at the
    time of exit on a ttyful/login session
  * some more bugfixes
* Mon Mar  5 2007 anicka@suse.cz
- fix path for firewall definition
* Thu Mar  1 2007 anicka@suse.cz
- add support for Linux audit (FATE #120269)
* Wed Feb 21 2007 anicka@suse.cz
- add firewall definition [#246921], FATE #300687,
  source: sshd.fw
* Sat Jan  6 2007 anicka@suse.cz
- disable SSHv1 protocol in default configuration [#231808]
* Tue Dec 12 2006 anicka@suse.cz
- update to 4.5p1
  * Use privsep_pw if we have it, but only require it if we
    absolutely need it.
  * Correctly check for bad signatures in the monitor, otherwise
    the monitor and the unpriv process can get out of sync.
  * Clear errno before calling the strtol functions.
  * exit instead of doing a blocking tcp send if we detect
    a client/server timeout, since the tcp sendqueue might
    be already full (of alive requests)
  * include signal.h, errno.h, sys/in.h
  * some more bugfixes
* Wed Nov 22 2006 anicka@suse.cz
- fixed README.SuSE [#223025]
* Thu Nov  9 2006 anicka@suse.cz
- backport security fixes from openssh 4.5 (#219115)
* Tue Nov  7 2006 ro@suse.de
- fix manpage permissions
* Tue Oct 31 2006 anicka@suse.cz
- fix gssapi_krb5-fix patch [#215615]
- fix xauth patch
* Tue Oct 10 2006 postadal@suse.cz
- fixed building openssh from src.rpm [#176528] (gssapi_krb5-fix.patch)
* Tue Oct  3 2006 postadal@suse.cz
- updated to version 4.4p1 [#208662]
  * fixed pre-authentication DoS, that would cause sshd(8) to spin
    until the login grace time expired
  * fixed unsafe signal hander, which was vulnerable to a race condition
    that could be exploited to perform a pre-authentication DoS
  * fixed a GSSAPI authentication abort that could be used to determine
    the validity of usernames on some platforms
  * implemented conditional configuration in sshd_config(5) using the
    "Match" directive
  * added support for Diffie-Hellman group exchange key agreement with a
    final hash of SHA256
  * added a "ForceCommand", "PermitOpen" directive to sshd_config(5)
  * added optional logging of transactions to sftp-server(8)
  * ssh(1) will now record port numbers for hosts stored in
    ~/.ssh/authorized_keys when a non-standard port has been requested
  * added an "ExitOnForwardFailure" option to cause ssh(1) to exit (with
    a non-zero exit code) when requested port forwardings could not be
    established
  * extended sshd_config(5) "SubSystem" declarations to allow the
    specification of command-line arguments
- removed obsoleted patches: autoconf-fix.patch, dos-fix.patch
- fixed gcc issues (gcc-fix.patch)
* Wed Sep 20 2006 postadal@suse.cz
- fixed DoS by CRC compensation attack detector [#206917] (dos-fix.patch)
- fixed client NULL deref on protocol error
- cosmetic fix in init script [#203826]
* Fri Sep  1 2006 kukuk@suse.de
- sshd.pamd: Add pam_loginuid, move pam_nologin to a better position
* Fri Aug 25 2006 postadal@suse.cz
- fixed path for xauth [#198676]
* Thu Aug  3 2006 postadal@suse.cz
- fixed build with X11R7
* Thu Jul 20 2006 postadal@suse.cz
- updated to version 4.3p2
  * experimental support for tunneling network packets via tun(4)
- removed obsoleted patches: pam-error.patch, CVE-2006-0225.patch,
  scp.patch, sigalarm.patch
* Mon Feb 13 2006 postadal@suse.cz
- upstream fixes
  - fixed "scp a b c", when c is not directory (scp.patch)
  - eliminate some code duplicated in privsep and non-privsep paths, and
    explicitly clear SIGALRM handler (sigalarm.patch)
* Fri Feb  3 2006 postadal@suse.cz
- fixed local arbitrary command execution vulnerability [#143435]
  (CVE-2006-0225.patch)
* Thu Feb  2 2006 postadal@suse.cz
- fixed xauth.diff for disabled UsePrivilegeSeparation mode [#145809]
- build on s390 without Smart card support (opensc) [#147383]
* Mon Jan 30 2006 postadal@suse.cz
- fixed patch xauth.diff [#145809]
- fixed comments [#142989]
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 16 2006 meissner@suse.de
- added -fstack-protector.
* Tue Jan  3 2006 postadal@suse.cz
- updated to version 4.2p1
- removed obsoleted patches: upstream_fixes.diff, gssapi-secfix.patch
* Tue Nov 15 2005 postadal@suse.cz
- do not delegate GSSAPI credentials to log in with a different method
  than GSSAPI [#128928] (CAN-2005-2798, gssapi-secfix.patch)
* Sun Oct 23 2005 postadal@suse.cz
- fixed PAM to send authentication failing mesaage to client [#130043]
  (pam-error.patch)
* Wed Sep 14 2005 postadal@suse.cz
- fixed uninitialized variable in patch xauth.diff [#98815]
* Thu Sep  8 2005 postadal@suse.cz
- don't strip
* Mon Sep  5 2005 postadal@suse.cz
- added patch xauth.diff prevent from polluting xauthority file [#98815]
* Mon Aug 22 2005 postadal@suse.cz
- fixed problem when multiple accounts have same UID [#104773]
  (pwname-home.diff)
- added fixes from upstream (upstream_fixes.diff)
* Thu Aug 18 2005 postadal@suse.cz
- added patch tmpdir.diff for using $TMPDIR by ssh-agent [#95731]
* Thu Aug  4 2005 uli@suse.de
- parallelize build
* Mon Aug  1 2005 postadal@suse.cz
- added patch resolving problems with hostname changes [#98627]
  (xauthlocalhostname.diff)
* Wed Jun 22 2005 kukuk@suse.de
- Compile/link with -fpie/-pie
* Wed Jun 15 2005 meissner@suse.de
- build x11-ask-pass with RPM_OPT_FLAGS.
* Fri Jun 10 2005 postadal@suse.cz
- updated to version 4.1p1
- removed obsoleted patches: restore_terminal, pam-returnfromsession,
  timing-attacks-fix, krb5ccname, gssapi-pam, logdenysource,
  sendenv-fix, documentation-fix
* Thu Mar 10 2005 postadal@suse.cz
- fixed SendEnv config parsing bug
- documented timeout on untrusted x11 forwarding sessions (openssh#849)
- mentioned ForwardX11Trusted in ssh.1 (openssh#987)
* Thu Mar  3 2005 postadal@suse.cz
- enabled accepting and sending locale environment variables in protocol 2
  [#65747, #50091]
* Thu Feb 24 2005 postadal@suse.cz
- added patches from cvs: gssapi-pam (openssh#918),
  krb5ccname (openssh#445), logdenysource (openssh#909)
* Thu Feb  3 2005 postadal@suse.cz
- fixed keyboard-interactive/pam/Kerberos leaks info about user existence
  [#48329] (openssh#971, CAN-2003-0190)
* Wed Jan 19 2005 postadal@suse.cz
- splited spec file to decreas number of build dependencies
- fixed restoring terminal setting after Ctrl+C during password prompt in scp/sftp [#43309]
- allowed users to see output from failing PAM session modules (openssh #890,
  pam-returnfromsession.patch)
* Mon Nov  8 2004 kukuk@suse.de
- Use common-* PAM config files for sshd PAM configuration
* Mon Oct 25 2004 postadal@suse.cz
- switched heimdal-* to kerberos-devel-packages in #needforbuild
* Fri Sep  3 2004 ro@suse.de
- fix lib64 issue
* Tue Aug 31 2004 postadal@suse.cz
- updated to version 3.9p1
- removed obsoleted patches: scp-fix.diff and window_change-fix.diff
* Thu Aug 26 2004 postadal@suse.cz
- added openssh-askpass-gnome subpackage
- added ssh-askpass script for choosing askpass depending on windowmanager
  (by Robert Love <rml@novell.com>)
- build with Smart card support (opensc) [#44289]
* Tue Aug 17 2004 postadal@suse.cz
- removed old implementation of "Update Messages" [#36059]
* Thu Aug 12 2004 postadal@suse.cz
- updated to version 3.8p1
- removed obsoleted patches: sftp-progress-fix and pam-fix4
* Mon Jun 28 2004 meissner@suse.de
- block sigalarm during syslog output or we might deadlock
  on recursively entering syslog(). (LTC#9523, SUSE#42354)
* Wed May 26 2004 postadal@suse.cz
- fixed commented default value for GSSAPI
* Thu May 20 2004 mludvig@suse.cz
- Load drivers for available hardware crypto accelerators.
* Fri Apr 30 2004 postadal@suse.cz
- updated README.kerberos (GSSAPICleanupCreds renamed to GSSAPICleanupCredentials)
* Mon Apr 19 2004 postadal@suse.cz
- updated README.SuSE (GSSAPICleanupCreds renamed to GSSAPICleanupCredentials)
  [#39010]
* Fri Mar 26 2004 postadal@suse.cz
- fixed sshd(8) and sshd_config(5) man pages (EAL3)
- fixed spelling errors in README.SuSE [#37086]
* Thu Mar 25 2004 postadal@suse.cz
- fixed change window request [#33177]
* Mon Mar 22 2004 postadal@suse.cz
- updated README.SuSE
- removed %%verify from /usr/bin/ssh in specfile
* Thu Mar 18 2004 postadal@suse.cz
- fixed previous fix of security bug in scp [#35443] (CAN-2004-0175)
  (was too restrictive)
- fixed permission of /usr/bin/ssh
* Mon Mar 15 2004 postadal@suse.cz
- fixed comments in sshd_config and ssh_config
* Mon Mar 15 2004 postadal@suse.cz
- enabled privilege separation mode (new version fixes a lot of problematic PAM
  calling [#30328])
- fixed security bug in scp [#35443] (CAN-2004-0175)
- reverted to old behaviour of ForwardingX11 [#35836]
  (set ForwardX11Trusted to 'yes' by default)
- updated README.SuSE
- fixed pam code (pam-fix4.diff, backported from openssh-SNAP-20040311)
* Fri Mar  5 2004 postadal@suse.cz
- updated README.SuSE (Remote x11 clients are now untrusted by default) [#35368]
- added gssapimitm patch (support for old GSSAPI)
* Mon Mar  1 2004 postadal@suse.cz
- updated to version 3.8p1
  * The "gssapi" support has been replaced with the "gssapi-with-mic"
    to fix possible MITM attacks. These two versions are not compatible.
- removed obsoleted patches: krb5.patch, dns-lookups.patch, pam-fix.diff,
  pam-end-fix.diff
- used process forking instead pthreads
  (developers fixed bugs in pam calling and they recommended to don't use threads)
* Tue Feb 24 2004 postadal@suse.cz
- fixed the problem with save_argv in sshd.c re-apeared again in version 3.7.1p2
  (it caused bad behaviour after receiving SIGHUP - used by reload of init script)
  [#34845]
* Wed Feb 18 2004 kukuk@suse.de
- Real strict-aliasing patch
* Wed Feb 18 2004 postadal@suse.cz
- fixed strict-aliasing patch [#34551]
* Fri Feb 13 2004 adrian@suse.de
- provide SLP registration file /etc/slp.reg.d/ssh.reg
* Tue Feb  3 2004 postadal@suse.cz
- used patch from pam-end-fix.diff [#33132]
- fixed instalation openssh without documentation [#33937]
- fixed auth-pam.c which breaks strict aliasing
* Mon Jan 19 2004 meissner@suse.de
- Added a ; to ssh-key-converter.c to fix gcc 3.4 build.
* Fri Jan 16 2004 kukuk@suse.de
- Add pam-devel to neededforbuild
* Thu Nov  6 2003 postadal@suse.cz
- added /usr/bin/slogin explicitly to %%file list [#32921]
* Sun Nov  2 2003 adrian@suse.de
- add %%run_permissions to fix build
* Tue Oct 14 2003 postadal@suse.cz
- reverted value UsePAM to "yes" and set PasswordAuthentication to "no"
  in file /etc/ssh/sshd_config (the version 3.7.1p2 disabled PAM support
  by default) [#31749]
* Tue Sep 23 2003 draht@suse.de
- New version 3.7.1p2; signature from 86FF9C48 Damien Miller
  verified for source tarball. Bugs fixed with this version:
  [#31637] (CAN-2003-0786, CAN-2003-0786). Briefly:
  1) SSH1 PAM challenge response auth ignored the result of the
    authentication (with privsep off)
  2) The PAM conversation function trashed the stack, by referring
    to the **resp parameter as an array of pointers rather than
    as a pointer to an array of struct pam_responses.
  At least security bug 1) is exploitable.
* Fri Sep 19 2003 postadal@suse.cz
- use pthreads instead process forking (it needs by pam modules)
- fixed bug in calling pam_setcred [#31025]
  (pam-fix.diff - string "FILE:" added to begin of KRB5CCNAME)
- updated README.SuSE
- reverted ChallengeResponseAuthentication option to default value yes
  (necessary for pam authentication) [#31432]
* Thu Sep 18 2003 postadal@suse.cz
- updated to version 3.7.1p1 (with security patches)
- removed obsoleted patches: chauthtok.patch, krb-include-fix.diff,
  gssapi-fix.diff, saveargv-fix.diff, gssapi-20030430.diff, racecondition-fix
- updated README.kerberos
* Tue Sep 16 2003 postadal@suse.cz
- fixed race condition in allocating memory [#31025] (CAN-2003-0693)
* Mon Sep 15 2003 postadal@suse.cz
- disabled privilege separation, which caused some problems [#30328]
  (updated README.SuSE)
* Thu Sep  4 2003 postadal@suse.cz
- fixed bug in x11-ssh-askpass dialog [#25846] (askpass-fix.diff is workaround for gcc bug)
* Fri Aug 29 2003 kukuk@suse.de
- Call useradd -r for system account [Bug #29611]
* Mon Aug 25 2003 postadal@suse.cz
- use new stop_on_removal/restart_on_upate macros
- fixed lib64 problem in /etc/ssh/sshd_config [#28766]
* Tue Aug 19 2003 mmj@suse.de
- Add sysconfig metadata [#28943]
* Thu Jul 31 2003 ro@suse.de
- add e2fsprogs-devel to neededforbuild
* Thu Jul 24 2003 postadal@suse.cz
- updated to version 3.6.1p2
- added the new version of patch for GSSAPI (gssapi-20030430.diff),
  the older one was removed (gssapi.patch)
- added README.kerberos to filelist
* Mon Jun  2 2003 mmj@suse.de
- Remove files we don't package
* Wed Apr  2 2003 postadal@suse.cz
- fixed bad behaviour after receiving SIGHUP (this bug caused not working reload of init script)
* Tue Mar 18 2003 postadal@suse.cz
- added $remote_fs to init.d script (needed if /usr is on remote fs [#25577])
* Thu Mar 13 2003 postadal@suse.cz
- fixed segfault while using GSSAPI for authentication when connecting to localhost (took care about error value of ssh_gssapi_import_name() in function ssh_gssapi_client_ctx())
* Mon Mar 10 2003 kukuk@suse.de
- Remove extra "/" from pid file path.
* Mon Mar  3 2003 postadal@suse.cz
- modified init.d script (now checking sshd.init.pid instead of port 22) [#24263]
* Mon Mar  3 2003 okir@suse.de
- added comment to /etc/pam.d/ssh on how to enable
  support for resmgr (#24363).
* Fri Feb 21 2003 postadal@suse.cz
- added ssh-copy-id shell script [#23745]
* Fri Feb 14 2003 postadal@suse.cz
- given back gssapi and dns-lookups patches
* Wed Jan 22 2003 postadal@suse.cz
- updated to version 3.5p1
- removed obsolete patches: owl-mm, forced-commands-only, krb
- added patch krb5 (for heimdal)
- temporarily removed gssapi patch and dns-lookups (needs rewriting)
- fix sysconfig metadata
* Thu Dec  5 2002 okir@suse.de
- avoid Kerberos DNS lookups in the default config (#20395)
- added README.kerberos
* Thu Sep 19 2002 postadal@suse.cz
- added info about changes in the new version of openssh
  to README.SuSE [#19757]
* Mon Sep  2 2002 okir@suse.de
- privsep directory now /var/lib/empty, which is provided by
  filesystem package (#17556)
* Wed Aug 28 2002 nashif@suse.de
- Added insserv & co to PreReq
* Mon Aug 26 2002 okir@suse.de
- applied patch that adds GSSAPI support in protocol version 2 (#18239)
* Thu Aug 22 2002 postadal@suse.cz
- added the patch to fix malfunction of PermitRootLogin seted to
  forced-commands-only [#17149]
* Fri Aug  9 2002 okir@suse.de
- syslog now reports kerberos auth method when logging in via
  kerberos (#17469)
* Tue Jul 23 2002 okir@suse.de
- enabled kerberos support
- added patch to support kerberos 5 authentication in privsep mode.
- added missing section 5 manpages
- added missing ssh-keysign to files list (new for privsep)
* Mon Jul 22 2002 okir@suse.de
- fixed handling of expired passwords in privsep mode
* Tue Jul  9 2002 mmj@suse.de
- Don't source rc.config
* Tue Jul  2 2002 draht@suse.de
- ssh-keygen must be told to explicitly create type rsa1 keys
  in the start script.
* Tue Jul  2 2002 ro@suse.de
- useradd/groupadd in preinstall to standardize
* Sat Jun 29 2002 ro@suse.de
- updated patch from solar: zero out bytes for no longer used pages
  in mmap-fallback solution
* Thu Jun 27 2002 ro@suse.de
- updated owl-fallback.diff from solar
* Thu Jun 27 2002 ro@suse.de
- update to 3.4p1
  o privilege separation support
  o overflow fix from ISS
- unsplit openssh-server and openssh-client
* Tue Jun 18 2002 mmj@suse.de
- Update to 3.2.3p1 which fixed following compared to 3.2.2p1
  o a defect in the BSD_AUTH access control handling for
  o login/tty problems on Solaris (bug #245)
  o build problems on Cygwin systems
- Split the package to openssh, openssh-server, openssh-client and
  openssh-askpass
* Sun May 19 2002 mmj@suse.de
- Updated to 3.2.2p which includes security and several bugfixes.
* Fri Mar 15 2002 ro@suse.de
- added "Obsoletes: ssh"
* Tue Mar  5 2002 draht@suse.de
- security fix for bug in channels.c (channelbug.dif)
* Fri Mar  1 2002 bk@suse.de
- fix ssh-agent example to use eval `ssh-agent -s` and a typo.
- add sentence on use of ssh-agent with startx
* Tue Feb 26 2002 bk@suse.de
- update README.SuSE to improve documentation on protocol version
* Wed Feb 13 2002 cihlar@suse.cz
- rewritten addrlist patch - "0.0.0.0" is removed from list
  after "::" is successful [#8951]
* Mon Feb 11 2002 cihlar@suse.cz
- added info about the change of the default protocol version
  to README.SuSE
* Thu Feb  7 2002 cihlar@suse.cz
- removed addrlist patch which fixed bug [#8951] as it breaks
  functionality on machines with kernel without IPv6 support,
  bug reopened, new solution will be find
- switched to default protocol version 2
- added ssh-keyconvert (thanks Olaf Kirch <okir@suse.de>)
- removed static linking against libcrypto, as crypt() was removed
  from it [#5333]
* Tue Jan 22 2002 kukuk@suse.de
- Add pam_nologin to account management (else it will not be
  called if user does not do password authentification)
* Tue Jan 15 2002 egmont@suselinux.hu
- removed colon from shutdown message
* Thu Jan 10 2002 cihlar@suse.cz
- use %%{_lib}
* Thu Dec 13 2001 ro@suse.de
- moved rc.config.d -> sysconfig
* Mon Dec 10 2001 cihlar@suse.cz
- removed START_SSHD
* Fri Dec  7 2001 cihlar@suse.cz
- update to version 3.0.2p1:
  * CheckMail option in sshd_config is deprecated
  * X11 cookies are now stored in $HOME
  * fixed a vulnerability in the UseLogin option
  * /etc/ssh_known_hosts2 and ~/.ssh/known_hosts2 are obsolete,
    /etc/ssh_known_hosts and ~/.ssh/known_hosts can be used
  * several minor fixes
- update x11-ssh-askpass to version 1.2.4.1:
  * fixed Imakefile.in
- fixed bug in adresses "::" and "0.0.0.0" [#8951]
* Fri Oct  5 2001 cihlar@suse.cz
- update to version 2.9.9p2
- removed obsolete clientloop and command patches
- uncommented "HostKey /etc/ssh/ssh_host_rsa_key" in sshd_config
- added German translation of e-mail to sysadmin
- init script fixed to work when more listening sshd runs
- added /bin/netstat to requires
* Mon Sep 24 2001 cihlar@suse.cz
- fixed security problem with sftp & bypassing
  keypair auth restrictions - patch based on CVS
- fixed status part of init script - it returned
  running even if there were only sshd of connections
  and no listening sshd [#11220]
- fixed stop part of init script - when there was no
  /var/run/sshd.pid, all sshd were killed
* Thu Sep  6 2001 nadvornik@suse.cz
- added patch for correct buffer flushing from CVS [bug #6450]
* Fri Jul 27 2001 cihlar@suse.cz
- update x11-ssh-askpass to version 1.2.2
* Thu Jul 26 2001 cihlar@suse.cz
- update to version 2.9p2
- removed obsolete "cookies" patch
* Mon Jun 11 2001 cihlar@suse.cz
- fixed to compile with new xmkmf
* Thu Jun  7 2001 cihlar@suse.cz
- fixed security bug when any file "cookies" could
  be removed by anybody
* Tue Jun  5 2001 bjacke@suse.de
- generate rsa host key in init script
* Tue Jun  5 2001 cihlar@suse.cz
- removed complete path from PAM modules
* Thu May  3 2001 cihlar@suse.cz
- update to version 2.9p1
- removed obsolete --with-openssl
- removed obsolete man patch
* Mon Apr 30 2001 cihlar@suse.cz
- enable PAM support
* Fri Apr 13 2001 ro@suse.de
- fixed specfile for extra README.SuSE
* Fri Apr 13 2001 cihlar@suse.cz
- fixed init script by new skeleton
* Thu Mar 22 2001 cihlar@suse.cz
- update to version 2.5.2p2
* Wed Mar 14 2001 cihlar@suse.cz
- fixed ssh man page
* Mon Mar 12 2001 cihlar@suse.cz
- update to version 2.5.1p2
- added xf86 to neededforbuild
* Fri Mar  9 2001 schwab@suse.de
- Fix missing crypt declaration.
* Fri Feb 23 2001 cihlar@suse.cz
- update to version 2.5.1p1
- update x11-ssh-askpass to version 1.2.0
* Tue Feb 20 2001 cihlar@suse.cz
- modified README.SuSE [#4365]
- fixed start script to agree with skeleton
- fixed start script so "stop" kills only sshd
  listening for connections
- compiled with --with-openssl
- "ListenAddress 0.0.0.0" in sshd_config commented out -
  listen on both ipv4 and ipv6
- fixed var/adm/notify/messages/openssh_update [#6406]
* Thu Jan 25 2001 smid@suse.cz
- startup script fixed [#5559]
* Tue Jan 16 2001 nadvornik@suse.cz
- libcrypto linked static [#5333]
* Thu Jan 11 2001 cihlar@suse.cz
- uncomment sftp-server part in sshd_config
- added /usr/X11R6/lib/X11/app-defaults/SshAskpass to %%files
* Thu Jan 11 2001 cihlar@suse.cz
- fixed %%files [#5230]
- fixed installation of x11-ssh-askpass to BuildRoot
- added man pages of x11-ssh-askpass
* Wed Jan 10 2001 smid@suse.cz
- notice about how to enable ipv6 added to mail
- for administrator [#5297]
* Wed Dec 13 2000 smid@suse.cz
- default ipv6 listennig disabled (problems with libc2.2) [#4588]
* Tue Dec  5 2000 smid@suse.cz
- notify message changed
* Mon Dec  4 2000 lmuelle@suse.de
- fixed provides/ conflicts to ssh
* Thu Nov 30 2000 smid@suse.cz
- path to ssh-askpass fixed
- stop in %%preun removed
- new init style
* Sun Nov 26 2000 schwab@suse.de
- Restore rcsshd link.
* Sun Nov 26 2000 kukuk@suse.de
- Add openssl-devel to neededforbuild
* Mon Nov 20 2000 smid@suse.cz
- New version 2.3.0
* Wed Sep  6 2000 smid@suse.cz
- remove --with-ipv4-default option
* Wed Jul  5 2000 garloff@suse.de
- ... and tell the sysadmin and user more about what they can do
  about it (schwab).
* Tue Jul  4 2000 garloff@suse.de
- Inform the user (admin) about the fact that the default behaviour
  with respect to X11-forwarding has been changed to be disabled.
* Wed Jun 28 2000 smid@suse.cz
- warning that generating DSA key can an take a long time.
  (bugzilla 3015)
- writing to wtmp and lastlog fixed (bugzilla 3024)
- reading config file (parameter Protocol) fixed
* Fri Jun 16 2000 garloff@suse.de
- Added generation of ssh_host_dsa_key
* Tue Jun 13 2000 nadvornik@suse.cz
- update to 2.1.1p1
* Thu Jun  8 2000 cihlar@suse.cz
- uncommented %%clean
* Fri May  5 2000 smid@suse.cz
- buildroot added
- upgrade to 1.2.3
* Tue Mar 21 2000 kukuk@suse.de
- Update to 1.2.2p1
* Mon Mar  6 2000 kukuk@suse.de
- Fix the diff.
* Sun Mar  5 2000 kukuk@suse.de
- Add a README.SuSE with a short description how to use ssh-add
* Tue Feb 29 2000 schwab@suse.de
- Update config.{guess,sub}.
* Fri Feb 25 2000 kukuk@suse.de
- Fix need for build, add group tag.
* Wed Feb  2 2000 kukuk@suse.de
- Change new defaults back to old one
* Sun Jan 30 2000 kukuk@suse.de
- Add x11-ssh-askpass to filelist
* Fri Jan 28 2000 kukuk@suse.de
- Update to OpenSSH 1.2.2
- Add x11-ssh-askpass-1.0
* Tue Jan 25 2000 kukuk@suse.de
- Add reload and status to /sbin/init.d/sshd [Bug 1747]
* Thu Jan 20 2000 kukuk@suse.de
- Update to 1.2.1pre27 with IPv6 support
* Fri Dec 31 1999 kukuk@suse.de
- Initial version
