#
# spec file for package tcsh
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

%define         base_name tcsh

Name:           tacc-%{base_name}
BuildRequires:  ncurses-devel
Url:            http://www.tcsh.org/
Requires:       gawk
Requires:       textutils
%if %suse_version > 1020
Recommends:     tcsh-lang = 6.18.00
%endif
Version:        6.18.01
Release:        8.3.1
Summary:        The C SHell
License:        BSD-3-Clause
Group:          System/Shells



Obsoletes: tcsh 
Provides: /bin/csh
Provides: /bin/tcsh

Provides: tcsh              = %{version}-%{release}
Provides: config(tcsh)      = %{version}-%{release}
Provides: tcsh(x86-64)      = %{version}-%{release}
Provides: tacc-tcsh         = %{version}-%{release}
Provides: config(tacc-tcsh) = %{version}-%{release}
Provides: tacc-tcsh(x86-64) = %{version}-%{release}



Source:         ftp.astron.com:/pub/tcsh/tcsh-6.18.01.tar.gz
Source2:        bindkey.tcsh
Source3:        complete.tcsh
Patch:          tcsh-6.18.00.dif
Patch1:         tcsh-6.15.00-pipe.dif
Patch2:         tcsh-6.16.00-norm-cmd.dif
Patch3:         tcsh-6.15.00-blanks.dif
Patch4:         tcsh-6.17.03-colorls.dif
Patch5:         tcsh-6.17.06-dspmbyte.dif
Patch6:         tcsh-6.17.10-catalogs.dif
Patch7:         tcsh-6.18.01-blk_buf.patch
Patch8:         tcsh-6.18.01-metakey.patch
# PATCH-FIX-SUSE add history file locking (bsc#901076)
Patch9:         tcsh-6.18.00-history-file-locking.patch
Patch10:        tcsh-6.18.01-history-merge.dif
# PATCH-FIX-UPSTREAM add history file locking (bsc#901076)
Patch11:        tcsh-closem.patch
Patch100:       tcsh-6.18.01-tacc.patch
BuildRoot:      %{_tmppath}/%{base_name}-%{version}-build

%include rpm-dir.inc

%description
Tcsh is an enhanced, but completely compatible, version of the Berkeley
UNIX C shell, csh(1). It is a command language interpreter usable as an
interactive login shell and a shell script command processor. It
includes a command-line editor, programmable word completion, spelling
correction, a history mechanism, job control, and a C-like syntax.



Authors:
--------
    Christos Zoulas <christos@deshaw.com>
    Scott Krotz <krotz@mot.com>

%package -n %{name}-lang
Summary:        Languages for package tcsh
Group:          System/Localization
Provides:       tcsh-lang = %{version}
Requires:       tcsh = %{version}

%description -n %{name}-lang
Provides translations to the package tcsh

%prep
%setup -n %{base_name}-%{version}
%patch1 -p0 -b .pipe
%patch2 -p0 -b .normcmd
### disabled for know, should work on os11.1 without
### %patch3 -p0 -b .blanks
%patch4 -p0 -b .colorls
%patch5 -p0 -b .dspmbyte
%patch6 -p0 -b .catalogs
%patch7 -p0 -b .blk_buf
%patch8 -p0 -b .metakey
%patch9 -p1 -b .histlock
%patch10 -p0 -b .histmerg
%patch11 -p0 -b .sockets
%patch      -b .0
%patch100 -p0

%build
    cflags ()
    {
	local flag=$1; shift
	local var=$1; shift
	test -n "${flag}" -a -n "${var}" || return
	case "${!var}" in
	*${flag}*) return
	esac
	set -o noclobber
	case "$flag" in
	-Wl,*)
	    if echo 'int main () { return 0; }' | \
	       ${CC:-gcc} -Werror $flag -o /dev/null -xc - > /dev/null 2>&1 ; then
		eval $var=\${$var:+\$$var\ }$flag
	    fi
	    ;;
	*)
	    if ${CC:-gcc} -Werror $flag -S -o /dev/null -xc /dev/null > /dev/null 2>&1 ; then
		eval $var=\${$var:+\$$var\ }$flag
	    fi
	    if ${CXX:-g++} -Werror $flag -S -o /dev/null -xc++ /dev/null > /dev/null 2>&1 ; then
		eval $var=\${$var:+\$$var\ }$flag
	    fi
	esac
	set +o noclobber
    }
    CC=gcc
    CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -DBUFSIZE=8192 -pipe"
    cflags -ftree-loop-linear      CFLAGS
    cflags -Wl,-O2                 LDFLAGS
    cflags -Wl,--as-needed         LDFLAGS
    cflags -Wl,--hash-size=16699   LDFLAGS
    export CC CFLAGS LDFLAGS
%ifarch %ix86
    CPU=i586
%else
    CPU=${RPM_ARCH}
%endif
    ./configure --build=${CPU}-suse-linux \
	--prefix=/usr			\
	--bindir=/bin			\
	--sysconfdir=/etc		\
	--localstatedir=/var		\
	--sharedstatedir=%_datadir	\
	--infodir=%_infodir		\
	--mandir=%_mandir		\
	--libexecdir=/usr/%{_lib}/tcsh	\
	--disable-rpath			\
	--with-gnu-ld
    make
#
# requires a working terminal on stdin
#   make check

%install
    rm -rf $RPM_BUILD_ROOT
    for nls in nls/*.cat ; do
	msg=$nls
	nls=${nls##*/}
	nls=${nls%%.*}
	case "${nls}" in
	fi*)	nls=fi		;;
	fr*)	nls=fr		;;
	ge*)	nls=de		;;
	gr*)	nls=el		;;
	it*)	nls=it		;;
	ru*)	nls=ru_RU	;;
	sp*)	nls=es		;;
	uk*)	nls=uk_UA	;;
	C)	continue	;;
	esac
	dir=$RPM_BUILD_ROOT/usr/share/locale/${nls}/LC_MESSAGES
	test ! -e ${dir}/tcsh || continue
	mkdir -p -m 0755 $dir
	install -m 0444 ${msg} ${dir}/tcsh
    done
    make DESTDIR=$RPM_BUILD_ROOT GENCAT='/usr/bin/gencat --new' install
    make DESTDIR=$RPM_BUILD_ROOT GENCAT='/usr/bin/gencat --new' install.man
    mkdir -p $RPM_BUILD_ROOT%{_docdir}/tcsh
    install -m 0644 FAQ       $RPM_BUILD_ROOT%{_docdir}/tcsh/FAQ.tcsh
    install -m 0644 Copyright $RPM_BUILD_ROOT%{_docdir}/tcsh/Copyright
    mkdir -p $RPM_BUILD_ROOT/etc/profile.d/
    mkdir -p $RPM_BUILD_ROOT/usr/bin
    install -m 644 $RPM_SOURCE_DIR/bindkey.tcsh  $RPM_BUILD_ROOT/etc/profile.d/
    install -m 644 $RPM_SOURCE_DIR/complete.tcsh $RPM_BUILD_ROOT/etc/profile.d/
    rm -f  $RPM_BUILD_ROOT/bin/csh
    rm -f  $RPM_BUILD_ROOT/usr/bin/csh
    rm -f  $RPM_BUILD_ROOT/usr/bin/tcsh
    rm -f  $RPM_BUILD_ROOT%{_mandir}/man1/csh.*
    rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/C
    ln -sf tcsh           $RPM_BUILD_ROOT/bin/csh
    ln -sf tcsh.1.gz      $RPM_BUILD_ROOT%{_mandir}/man1/csh.1.gz
    ln -sf ../../bin/tcsh $RPM_BUILD_ROOT/usr/bin/csh
    ln -sf ../../bin/tcsh $RPM_BUILD_ROOT/usr/bin/tcsh

%clean
    rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{_docdir}/tcsh
/bin/csh
/bin/tcsh
%config /etc/profile.d/bindkey.tcsh
%config /etc/profile.d/complete.tcsh
/usr/bin/csh
/usr/bin/tcsh
%doc %{_docdir}/tcsh/Copyright
%doc %{_docdir}/tcsh/FAQ.tcsh
%doc %{_mandir}/man1/csh.1.gz
%doc %{_mandir}/man1/tcsh.1.gz

%files -n %{name}-lang
%defattr(-,root,root)
%{_datadir}/locale/*/LC_MESSAGES/tcsh*

%changelog
* Fri Jun 16 2017 werner@suse.de
- Add patch tcsh-closem.patch to fix a long standing misbehaviour
  of upstram tcsh whic his that it close sockets which do not
  belong to it (bsc#1028864)
* Tue Jan 13 2015 werner@suse.de
- Add patch tcsh-6.18.00-history-file-locking.patch for bsc#901076
  Cluster switch does not started completely packages on other node
- Modified patch  tcsh-6.18.01-history-merge.dif to fit with former
* Tue Oct 15 2013 werner@suse.de
- Add patch tcsh-6.18.01-history-merge.dif which is a backport of
  the patch from Stanislav Tokos (bnc#844752)
* Tue Aug  6 2013 werner@suse.de
- Update to tcsh bug fix version V6.18.01
- Remove patch tcsh-6.18.01.patch as not required anymore
- Add patch tcsh-6.18.01-metakey.patch to make meta key work
* Thu May 10 2012 werner@suse.de
- Fix tcsh segfaults in bb_cleanup() (bnc#761353)
* Fri Feb 24 2012 werner@suse.de
- Update tcsh to patch level 6.18.01 - 20120214
  * fix interruptible wait again
  * ignore bogus compiler overflow message
  * cleanup ifdefs in utmp code, and provide default array entries
  * Ignore #machine entries in host.defs
  * Detect missing ) in gethost.c (Corinna Vinschen)
* Mon Jan 16 2012 werner@suse.de
- Update to tcsh final version V6.18.00
  * remove unused variables.
  * Make gethost use definitions for x __x__ and __x automatically.
  * More utmp fixes
* Tue Jan 10 2012 werner@suse.de
- Update to tcsh minor version V6.17.10
  * Add more FreeBSD/NetBSD machines
  * Add portability wrapper for gencat
  * Fix warning for write in SYSMALLOC systems.
  * revert gencat handling to pre-cygwin fixes (without the env settings)
  * remove stray endutent()
  * Remove - from gencat
  * Provide support for malloc_usable_size() so that linux works again
  without SYSMALLOC
  * Add support for FreeBSD's utmpx.
  * Fix debian bug #645238: tcsh segfaults when prompt includes %%j and
  there are more than 10 jobs.
  * PR/155: Default $anyerror to set for backward compatibility
  * PR/149: Don't print -1 in %%j (Vojtech Vitek)
  * handle -- on chdir commands as the end of options processing so that
  they can process a directory like -x without resorting to ./-x
  (Andrew Stevenson)
  * Handle write(2) returning ENOENT from SoFS, thanks ++HAL (Robert Byrnes)
  * PR/38: Null check for jobs (Kurt Miller)
  * Fix spelling correction correcting ./foo -> ../foo2 (jean-luc leger)
  * PR/120: string0 in filetest does not have enough space.
* Fri Nov 18 2011 werner@suse.de
- Increase size of hash table for runtime linker a lot
* Thu Nov 17 2011 werner@suse.de
- Split off tcsh-lang as its own package
- Make language catalogs work that is use tcsh instead of tcsh.cat
  as this is the system default
* Wed Nov 16 2011 werner@suse.de
- Update to tcsh minor version V6.17.06
  * PR/110: Add $anyerror to select behavior. Default to the new one.
  * Don't try to spell commands that are correct (Rouben Rostamian)
    [./tcsh -f; set path=($path 2); mkdir foo2; cd foo2; touch foo;
    chmod +x foo; set correct=cmd; ./foo -> ../foo]
  * Don't push the syntax struct on the cleanup stack, because on foo;bar
    if foo fails, we will free bar prematurely (Ben Miller)
  * Avoid infinite loop while trying to print the pid of a dying process
    to a closed file (Bob Arendt)
  * Handle completion of ${ variables (Anthony Mallet)
  * Add --disable-nls-catalogs (Corinna Vinschen)
  * convert message catalogs to UTF-8 (Werner Fink)
  * check that the NLS path works before setting $NLSPATH.
  * use SYSMALLOC for GLIBC (Werner Fink)
  * use mallinfo for SYSMALLOC (Corinna Vinschen)
  * Use mkstemp() if there for here docs (Werner Fink)
  * Fix handling of errors and exit values in builtins (Werner Fink)
  * Better pty name detection (Werner Fink)
  * Enable NLS catalogs on Cygwin (Corinna Vinschen)
  * NLSPATH handling fixes (Corinna Vinschen)
  * Avoid infrequent exit when tcsh cd's into a non-existent directory
    https://bugzilla.novell.com/show_bug.cgi?id=293395 (Werner Fink)
  * Don't try to spell check full path binaries that are correct because
    they can cause hangs when other nfs partitions are hung. (Werner Fink)
  * Avoid nested interrupts when exiting causing history writing to fail
    https://bugzilla.novell.com/show_bug.cgi?id=331627 (Werner Fink)
  * Instead of giving an error or ignoring lines with missing eol at eof,
    process them.
  * Avoid leaking fd's in mail check (Werner Fink)
  * Recognize i686 (Corinna Vinschen)
  * Avoid double slashes in cdpath (Corinna Vinschen)
  * PR/102: Complain on input files with missing trailing \n
  * PR/104: If atime == mtime we don't have new mail.
  * PR/113: Don't allow illegal variable names to be set.
  * PR/112: don't set $REMOTEHOST on the local machine.
  * Add AUTOSET_KANJI which works around the Shift-JIS encoding that
    translates unshifted 7 bit ASCII (Werner Fink)
  * Handle mb{r,}towc() returning 0 by setting the return value to NUL
    (Jean-Luc Leger)
  * PR/109: make wait interruptible (Vojtech Vitek)
  * resource limit fixes: signed vs. unsigned, megabyte issue, doc issues
    (Robert Byrnes)
  * Don't echo history while history -L or history -M
  * Check for EOS before ** from Greg Dionne
  * Don't fork in backeval from Bryan Mason
  * Better globstar support from Greg Dionne
  * Error out when processing the last incomplete line instead of silently
    ignoring it (Anders Kaseorg)
  * Fix SEGV from echo ``
  * Better fixes for histchars and promptchars (nargs)
* Wed Nov 16 2011 werner@suse.de
- Use libtinfo if available otherwise libncurses (required due
  bnc #729226)
* Mon Feb 28 2011 werner@suse.de
- Add key support for screen terminal emluator
* Mon Feb  7 2011 werner@suse.de
- Renew some patches to make it build
* Tue Dec 14 2010 werner@suse.de
- Update to tcsh minor version V6.17.02
  * PR/79: nargs: Better handling for promptchars.
  * PR/97: Add parseoctal to retain compatibility with previous versions (Jim
    Zajkowski)
  * PR/84: Performance fixes for large history merges (add
    hashtable (Ted Anderson)
  * Don't kill "hup" background jobs when a child of the shell exits.
    From Debian.
  * Ignore \r\n in the command line options for OS's that don't strip
    these from #!; from Debian
  * Callers of rt_mbtowc don't grok -2 as a return. Return -1 for now.
    (Corinna Vinschen)
  * set autoexpand; set histchars="";\n<tab> crash. From Debian
  * unset verbose while we are reading the history file to avoid echoing
    to the terminal. (Jeffrey Bastian)
  * globstar addition, Enhance addition, euid, euser, gid variables
    (Greg Dionne)
  * Make 'e' in vi mode work like 'b' - use wordchars (Alistair Crooks)
  * Make tcsh work on systems where sizeof(wchar_t) == 2 (Corinna Vinschen)
  * Change internal expression calculations to long long so that we can
    deal with > 32 bit time, inodes, uids, file sizes etc.
  * Don't print 'Exit X' when printexitvalue is set in `` expressions
    (Jeff Bastian)
  * Add more LS_COLORS vars (M.H. Anderson)
  * Manual page fixes (Alan R. S. Bueno)
  * Remove history in loops bug from the documentation (Holger Weiss)
  * Add autorehash (Holger Weiss)
  * Add history.at (Ted Anderson)
  * Better NLSPATH handling (Norm Jacobs)
  * Fix hostname building from utmp (Cyrus Rahman)
  * Handle pending signals before flush so that the the history file does
    not get truncated.  (Ted Anderson)
  * Fix AsciiOnly setting that broke 8 bit input. (Juergen Keil)
  * remember to closedir in mailchk (from Werner Fink, reported by
    David Binderman)
- Add workaround for Shift-JIS endcoding that translates unshifted
  7 bit ASCII (bnc#655306)
* Fri Jun 11 2010 werner@suse.de
- Avoid crash due own malloc due buggy nss implementation of glibc
* Wed Mar 17 2010 werner@suse.de
- Add Forms Data Format (.fdf) for acroread and co (bnc#573202)
* Mon Mar  8 2010 ro@suse.de
- fix tcsh-6.16.00-history.dif to apply
* Mon Feb 15 2010 werner@suse.de
- Increase BUFSIZE to 8kB resulting in INBUFSIZE of 16kB (fate#308882)
* Mon Feb 15 2010 werner@suse.de
- Update to tcsh version V6.17.00
  * Fix dataroot autoconf issue.
  * Fix directory stuff for unit tests.
  * Fix small bug in history in loops.
  * Provide newer config.{guess,sub}
  * Fix gcc 4 warnings.
  * Fix memory trashing bug introduced in 10.
  * add missing sigemptyset in goodbye()
  * restore behavior where a[n-] never prints an error.
  * always save the whole command, not just the first 80 chars of it.
  * fix short2str/short2qstr length adjustment in wide chars
  (Vitezslav Crhonek)
  * set histfile=/tmp/history.temp; set savehist=(100 merge);
  alias precmd history -S. After that justpr is not restored
  and commands don't execute. (Andriy Gapon)
  * Fix "as" $ modifier from corrupting memory.
  set t=demfonsftraftionf; echo $t:as/f//
  * Make $%% work with environment variable (Ron Johnston)
  * Add autoexpand=onlyhistory (Don Estabrook, m66)
  * Add history in loops (Laurence Darby, m48)
  * Add missing colorls "rs" variable (Shlomi Fish, m70)
  * Fix pts detection issue (Ruslan Ermilov)
* Mon Dec  7 2009 meissner@suse.de
- fixed patch fuzz in a minimalistic way.
* Wed Dec  2 2009 werner@suse.de
- Remove left over in old patch to re-enable message on suppended
  jobs at exit/logout
* Fri Aug 14 2009 werner@suse.de
- After mailbox counting close directory (bnc#530779)
* Tue Jun 23 2009 werner@suse.de
- Add four unknown colorls variables (rs, ca, hl, and cl) used
  by dircolors but not by the tcsh ls-F builtin (bnc#494406)
* Tue Mar 31 2009 werner@suse.de
- Also enable patch for bnc#472866
* Wed Mar 25 2009 werner@suse.de
- Update to tcsh version V6.16.00
- Add patch to avoid endless loop due incorrect tty process group
  (bnc#472866)
* Wed Jan 21 2009 werner@suse.de
- Reenable Alt-BackSpace for delete word in XTerm in UTF-8 mode
* Wed Nov 26 2008 werner@suse.de
- For commands with full execution path bypass correction algorithm
  if the command is found (bnc#444992)
* Wed Nov  5 2008 werner@suse.de
- Disable patch for bnc#437295 as it cause trouble (bnc#441654)
  and the gcc of openSuSE 11.1 seems to be safe
* Tue Oct 21 2008 werner@suse.de
- Command line expansion: Allow not only "compress" for co<TAB>
  but any other command starting with "co" (bnc#437295)
* Wed Oct  8 2008 werner@suse.de
- Make code of last change unambiguous
* Mon Oct  6 2008 werner@suse.de
- Avoid blanks at the beginning of command lists (bnc#431661)
* Fri Jun 13 2008 werner@suse.de
- Add complete rule for local executables ./*
* Thu Dec 20 2007 werner@suse.de
- Oops ... also apply the patch for bug ##331627 (bug #349577)
* Mon Oct 15 2007 werner@suse.de
- Improve bug fix (bug #331627)
* Fri Oct 12 2007 werner@suse.de
- Fix save history bug: do not jump out from handler for pending
  signals like for SIGHUP, just run the handler up to its end and
  ignore any error happen to be interrupted (bug #331627)
* Tue Aug 28 2007 werner@suse.de
- Correct boolean expression for normalize-command (bug #304903)
* Mon Jul 23 2007 werner@suse.de
- Add workaround to avoid run onto already cleaned stack pointer
  after an error (bug #293395)
* Thu Jul 19 2007 werner@suse.de
- Small correction in bindkey.tcsh: for urxvt, mlterm, and konsole
* Mon Jul 16 2007 werner@suse.de
- Update to tcsh version V6.15.00
  * fix extension eating windows code
  * fix loop in %%R history expansion
  * sched +X source file disables interrupts (Mike Sullivan)
  * One off copying macro buffers
  * Avoid infinite loops in :ga modifiers when the LHS is a
    substring of the RHS.
- Update bindkey.tcsh to fit current xterm and others (bug #262330)
* Thu Mar 29 2007 rguenther@suse.de
- Add ncurses-devel BuildRequires.
* Mon Feb 26 2007 werner@suse.de
- Expand local ./files for manual pages even for tcsh (#248865)
* Wed Aug 16 2006 aj@suse.de
- Remove unneeded BuildRequires.
* Wed Jun 21 2006 werner@suse.de
- Do not overwrite memory by not initialized Char array (#186669)
* Wed Apr 26 2006 werner@suse.de
- Fix typo in compelete macro for the command man
* Tue Apr 25 2006 werner@suse.de
- Add new LS_COLORS variables to avoid error message (bug #168601)
* Mon Apr 10 2006 werner@suse.de
- Tcsh completion: expand also for sections of posix manual pages
  and include section 0 into search scheme (bug #160782)
* Thu Mar 23 2006 werner@suse.de
- Source the users ~/.cshrc and ~/.login in the traditional order,
  nevertheless the system wide /etc/csh.cshrc and /etc/csh.login
  will be sourced in the natual order (bug #160278)
* Mon Feb  6 2006 werner@suse.de
- Make $< operator work even when fed by pipe (bug #147724)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Oct 25 2005 werner@suse.de
- Switch order of sourcing csh.login csh.cshrc, now csh.login
  comes first to provide all exported environment variables.
* Thu Aug 18 2005 werner@suse.de
- Update to tcsh 6.14.00, the wide character version (bug #104108).
* Mon May 23 2005 werner@suse.de
- Make mh handling more smarter
* Fri Apr  1 2005 werner@suse.de
- Gcc4 does not allow function prototype declaration within other
  function prototype declaration even if the internals are static.
* Fri Oct  8 2004 werner@suse.de
- Make fcntl call with O_LARGEFILE portable (bug #46977)
* Thu May 27 2004 ro@suse.de
- fix sigpause call (force use of sysv flavour)
* Fri Apr  2 2004 mls@suse.de
- fix utf-8 expansion, ls-F, prompt handling
* Mon Mar 29 2004 mls@suse.de
- fix utf-8 handling (really fixes #29983, #35486)
* Tue Mar 16 2004 werner@suse.de
- Do not forget the patch for bug #29983 even if not used
- Accept chinese in dspmbyte and map this on euc
* Wed Mar 10 2004 werner@suse.de
- Disable multibyte ix due problems on long lines (bug #35486)
- Simplify mv/cp complete
* Thu Mar  4 2004 werner@suse.de
- Fix mv/cp complete bug (#35339)
* Fri Feb 20 2004 werner@suse.de
- Add simple workaround for multibyte command lines (bug #29983)
* Wed Jan 28 2004 werner@suse.de
- Fix bug #34126: add runtime detection as fallback
* Sat Jan 10 2004 adrian@suse.de
- add %%defattr
* Fri Sep 19 2003 werner@suse.de
- Fix the fix for bug #29956: use a ringbuffer to avoid trouble
  with recursive calls of UTF-8 convertes messges (bug #31335)
* Thu Sep  4 2003 werner@suse.de
- Corruption of cursor position is currently not fixable.
  fix some other bugs.
* Wed Sep  3 2003 mfabian@suse.de
- Bugzilla #29956: convert all message catalogs to UTF-8 and
  convert the strings returned by catgets from UTF-8 into the
  encoding of the current locale.
- move Ukrainian message catalog into uk_UA subdirectory
  instead of ru_UA.koi8u.
* Fri Jul 18 2003 werner@suse.de
- Fix multi byte initialization (bug #27793)
- Enable multi byte unset on LANG change
- Fix signess/unsigness mixtures
* Fri May 23 2003 coolo@suse.de
- use BuildRoot
* Wed May 14 2003 werner@suse.de
- Move pointer adress handling from int to intptr_t
* Thu Apr 17 2003 werner@suse.de
- Fix multibyte initialization
* Mon Feb 17 2003 werner@suse.de
- Fix bug #23681: don't reset full command line if an error occurs
* Mon Nov 11 2002 ro@suse.de
- use x-devel-packages in neededforbuild
* Tue Sep 17 2002 ro@suse.de
- removed bogus self-provides
* Wed Aug  7 2002 werner@suse.de
- Fix bindkey.tcsh for xterm and add some more keys (bug #15002)
* Tue Jul 30 2002 werner@suse.de
- Update to 6.12.00
- Fix codesets of message cats
* Fri Jul 19 2002 mls@suse.de
- fix bindkey.tcsh to make it work with an unset $TERM variable
* Wed Mar 20 2002 werner@suse.de
- Fix bug # 15143: Unreadable /etc/printcap due paranoid SysAdmins
  should not stop tcsh.
* Wed Dec 12 2001 werner@suse.de
- Revisit some complete expansion (mainly for mv, cp, make, and
  man), sed error scanners should work for all languages.
* Thu Sep  6 2001 werner@suse.de
- Update to 6.11.00 due
  * correct large file support
  * Avoid core-dumping on very long $HOME variable
  * Don't call qsort(3) with 0 items
  * Fix redrawing in the recognize case
  * MAXHOSTNAMELEN needs to be 256 (instead of 255)
  * Big5 multibyte support
  * Fix rmstar not to corrupt memory on off
* Wed May 16 2001 werner@suse.de
- Force large file support
* Wed May  9 2001 cstein@suse.de
- Corrected German spellings in nls/german/set6
* Wed Mar  7 2001 werner@suse.de
- We use xmkmf therefore we need a full X environment at build
* Fri Feb  9 2001 werner@suse.de
- Don't use the authors (endless looping) security temp file
  change but the mkstemp() function.
* Fri Feb  2 2001 mfabian@suse.de
- update to version 6.10.00
  (because the new version has  support for display and editing of
  multibyte characters)
- add patch to enable multibyte character editing
- patch to glob.c removed (included upstream)
- patch to sh.dir.c removed (included upstream)
- patch to tw.color.c removed (incuded upstream)
- last hunk of patch to tw.h removed (included upstream)
- bzip2 sources
* Fri Dec 15 2000 werner@suse.de
- Add missed hash for a comment.
* Wed Nov 22 2000 werner@suse.de
- Make /etc/profile.d/bindkey.tcsh knowing about TERM kvt and gnome
* Fri Nov 17 2000 kukuk@suse.de
- fix neededforbuild: textutil -> textutils
* Thu Nov  2 2000 werner@suse.de
- Use mkstemp for opening tmp files for `<<' redirects
  - Use TMPDIR variable for location of tmp files
  - Set group tag in spec
* Wed May 24 2000 uli@suse.de
- moved docs to %%{_docdir}
* Wed Jan 26 2000 werner@suse.de
- New version 6.09.00
  - /usr/man -> /usr/share/man
  - Fix usage of catopen (MCLoadBySet isn't that what is used
  internally within glibc, set it to MCLoadBySet)
  - Avoid crahs due coloured ls-F
  - Correct setpath NLS message
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Mon Jun 28 1999 werner@suse.de
- Source key binding and completion code from
  /etc/csh.cshrc out into /etc/profile.d/bindkey.tcsh and
  /etc/profile.d/complete.tcsh
  - No newgrp builtin because its equivalent to exec newgrp
* Tue Jun 15 1999 ro@suse.de
- create localedirs before make install
* Fri Jun 11 1999 werner@suse.de
- New version
  Fri Mar 12 14:21:46 MET 1999
  - Fix SIGSEGV caused different sizes of FILSIZ and BUFSIZE
  - New version
  - Restore missed MAXNAMLEN
  - Make it alpha compile
* Thu Dec  3 1998 werner@suse.de
- Fix SIGSEGV with SYSMALOC
  * alloc n+1 not n chunks
  * set freed pointer to (ptr_t)NULL
* Wed Sep 16 1998 werner@suse.de
- Stupid error fixed
* Tue Sep 15 1998 werner@suse.de
- Security fix
  - Avoid I/O trouble, use POSIX
* Wed Oct 22 1997 werner@suse.de
- Updatet FAQ.tcsh
  - Better installation: remove old files before linking
* Thu Jan  2 1997 bs@suse.de
  added FAQ.tcsh
* Thu Jan  2 1997 werner@suse.de
- Neue Version 6.07.02 mit einigen Fixes
