#
# spec file for package bash
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
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


%bcond_with     import_function
%define base_name bash
Name:           tacc-%{base_name}
BuildRequires:  audit-devel
BuildRequires:  bison
%if %suse_version > 1020
BuildRequires:  autoconf
BuildRequires:  fdupes
%endif
%if %suse_version > 1220
BuildRequires:  makeinfo
%endif
BuildRequires:  ncurses-devel
BuildRequires:  patchutils
BuildRequires:  screen
BuildRequires:  sed
%define         bash_vers 4.3
%define         rl_vers   6.3
%define         extend    ""
%if %suse_version > 1020
Recommends:     bash-lang = %bash_vers
# The package bash-completion is a source of
# bugs which will hit at most this package
#Recommends:	bash-completion
Suggests:       command-not-found
Recommends:     bash-doc = %bash_vers
%endif
Version:        %{bash_vers}
Release:        294.42
Summary:        The GNU Bourne-Again Shell
License:        GPL-3.0+
Group:          System/Shells
Packager:       TACC - cproctor@tacc.utexas.edu
Url:            http://www.gnu.org/software/bash/bash.html

%include rpm-dir.inc

Obsoletes: bash 
Provides: /bin/sh
Provides: /bin/bash

Provides: bash              = %{version}-%{release}
Provides: config(bash)      = %{version}-%{release}
Provides: bash(x86-64)      = %{version}-%{release}
Provides: tacc-bash         = %{version}-%{release}
Provides: tacc-bash(x86-64) = %{version}-%{release}
                             
# Git:          http://git.savannah.gnu.org/cgit/bash.git
Source0:        ftp://ftp.gnu.org/gnu/bash/bash-%{bash_vers}.tar.gz
Source1:        ftp://ftp.gnu.org/gnu/readline/readline-%{rl_vers}.tar.gz
Source2:        bash-%{bash_vers}-patches.tar.bz2
Source3:        readline-%{rl_vers}-patches.tar.bz2
Source4:        run-tests
Source5:        dot.bashrc
Source6:        dot.profile
Source7:        bash-rpmlintrc
Source8:        baselibs.conf
# Remember unsafe method, compare with
# http://lists.gnu.org/archive/html/bug-bash/2011-03/msg00070.html
# http://lists.gnu.org/archive/html/bug-bash/2011-03/msg00071.html
# http://lists.gnu.org/archive/html/bug-bash/2011-03/msg00073.html
Source9:        bash-4.2-history-myown.dif.bz2
Patch0:         bash-%{bash_vers}.dif
Patch1:         bash-2.03-manual.patch
Patch2:         bash-4.0-security.patch
Patch3:         bash-4.3-2.4.4.patch
Patch4:         bash-3.0-evalexp.patch
Patch5:         bash-3.0-warn-locale.patch
Patch6:         bash-4.2-endpw.dif
Patch7:         bash-4.3-decl.patch
Patch8:         bash-4.0-async-bnc523667.dif
Patch9:         bash-4.3-include-unistd.dif
Patch10:        bash-3.2-printf.patch
Patch11:        bash-4.3-loadables.dif
Patch12:        bash-4.1-completion.dif
Patch13:        bash-4.2-nscdunmap.dif
Patch14:        bash-4.3-sigrestart.patch
# PATCH-FIX-UPSTREAM bnc#382214 -- disabled due bnc#806628 by -DBNC382214=0
Patch15:        bash-3.2-longjmp.dif
Patch16:        bash-4.0-setlocale.dif
Patch17:        bash-4.3-headers.dif
# PATCH-EXTEND-SUSE bnc#828877 -- xterm resizing does not pass to all sub clients
Patch18:        bash-4.3-winch.dif
Patch20:        readline-%{rl_vers}.dif
Patch21:        readline-6.3-input.dif
Patch22:        readline-6.1-wrap.patch
Patch23:        readline-5.2-conf.patch
Patch24:        readline-6.2-metamode.patch
Patch25:        readline-6.2-endpw.dif
Patch27:        readline-6.2-xmalloc.dif
Patch30:        readline-6.3-destdir.patch
Patch31:        readline-6.3-rltrace.patch
Patch40:        bash-4.1-bash.bashrc.dif
Patch46:        man2html-no-timestamp.patch
Patch47:        bash-4.3-perl522.patch
# PATCH-FIX-SUSE
Patch48:        bash-4.3-extra-import-func.patch
# PATCH-EXTEND-SUSE Allow root to clean file system if filled up
Patch49:        bash-4.3-pathtemp.patch
BuildRoot:      %{_tmppath}/%{base_name}-%{version}-build


# TACC WCP 2018-10-02 change paths from /etc to /etc/tacc
Patch300:       bash43_config.patch


%global         _sysconfdir /etc
%global         _incdir     %{_includedir}
%global         _ldldir     /%{_lib}/bash
%global         _minsh      0
%{expand:       %%global rl_major %(echo %{rl_vers} | sed -r 's/.[0-9]+//g')}

%description
Bash is an sh-compatible command interpreter that executes commands
read from standard input or from a file.  Bash incorporates useful
features from the Korn and C shells (ksh and csh).  Bash is intended to
be a conformant implementation of the IEEE Posix Shell and Tools
specification (IEEE Working Group 1003.2).

%package doc
Summary:        Documentation how to Use the GNU Bourne-Again Shell
Group:          Documentation/Man
Provides:       bash:%{_infodir}/bash.info.gz
PreReq:         %install_info_prereq
Version:        %{bash_vers}
Release:        293.42
%if %suse_version > 1120
BuildArch:      noarch
%endif

%description doc
This package contains the documentation for using the bourne shell
interpreter Bash.

%if %{defined lang_package}
%lang_package(bash)
%else

%package lang
Summary:        Languages for package bash
Group:          System/Localization
Provides:       bash-lang = %{bash_vers}
Requires:       bash = %{bash_vers}

%description lang
Provides translations to the package bash
%endif

%if 0%suse_version >= 1020
%package devel
Summary:        Include Files mandatory for Development of bash loadable builtins
Group:          Development/Languages/C and C++
Version:        %{bash_vers}
Release:        293.42

%description devel
This package contains the C header files for writing loadable new
builtins for the interpreter Bash. Use -I /usr/include/bash/<version>
on the compilers command line.
%endif

%package loadables
Summary:        Loadable bash builtins
Group:          System/Shells
Version:        %{bash_vers}
Release:        293.42

%description loadables
This package contains the examples for the ready-to-dynamic-load
builtins found in the source tar ball of the bash:

basename      Return non-directory portion of pathname.

cut	      cut(1) replacement.

dirname       Return directory portion of pathname.

finfo	      Print file info.

getconf       POSIX.2 getconf utility.

head	      Copy first part of files.

id	      POSIX.2 user identity.

ln	      Make links.

logname       Print login name of current user.

mkdir	      Make directories.

pathchk       Check pathnames for validity and portability.

print	      Loadable ksh-93 style print builtin.

printenv      Minimal builtin clone of BSD printenv(1).

push	      Anyone remember TOPS-20?

realpath      Canonicalize pathnames, resolving symlinks.

rmdir	      Remove directory.

sleep	      sleep for fractions of a second.

strftime      Loadable builtin interface to strftime(3).

sync	      Sync the disks by forcing pending filesystem writes to
complete.

tee	      Duplicate standard input.

tty	      Return terminal name.

uname	      Print system information.

unlink	      Remove a directory entry.

whoami	      Print out username of current user.


%package -n libreadline6
Summary:        The Readline Library
Group:          System/Libraries
Provides:       bash:/%{_lib}/libreadline.so.%{rl_major}
Version:        %{rl_vers}
Release:        293.42
%if 0%suse_version > 1020
Recommends:     readline-doc = %{version}
%endif
# bug437293
%ifarch ppc64
Obsoletes:      readline-64bit
%endif
#
Provides:       readline =  %{rl_vers}
Obsoletes:      readline <= 6.2

%description -n libreadline6
The readline library is used by the Bourne Again Shell (bash, the
standard command interpreter) for easy editing of command lines.  This
includes history and search functionality.

%package -n readline-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/C and C++
Provides:       bash:%{_libdir}/libreadline.a
Version:        %{rl_vers}
Release:        293.42
Requires:       libreadline6 = %{rl_vers}
Requires:       ncurses-devel
%if 0%suse_version > 1020
Recommends:     readline-doc = %{rl_vers}
%endif
# bug437293
%ifarch ppc64
Obsoletes:      readline-devel-64bit
%endif
#

%description -n readline-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package -n readline-doc
Summary:        Documentation how to Use and Program with the Readline Library
Group:          System/Libraries
Provides:       readline:%{_infodir}/readline.info.gz
PreReq:         %install_info_prereq
Version:        %{rl_vers}
Release:        293.42
%if 0%suse_version > 1120
BuildArch:      noarch
%endif

%description -n readline-doc
This package contains the documentation for using the readline library
as well as programming with the interface of the readline library.

%prep
%setup -q -n bash-%{bash_vers}%{extend} -b1 -b2 -b3
typeset -i level
for patch in ../bash-%{bash_vers}-patches/*; do
    test -e $patch || break
    let level=0 || true
    file=$(lsdiff --files=1 $patch)
    if test ! -e $file ; then
	file=${file#*/}
	let level++ || true
    fi
    test -e $file || exit 1
    sed -ri '/^\*\*\* \.\./{ s@\.\./bash-%{bash_vers}[^/]*/@@ }' $patch
    echo Patch $patch
    patch -s -p$level < $patch
done
%patch1  -p0 -b .manual
%patch2  -p0 -b .security
%patch3  -p0 -b .2.4.4
%patch4  -p0 -b .evalexp
%patch5  -p0 -b .warnlc
#%patch6  -p0 -b .endpw
%patch7  -p0 -b .decl
%patch8  -p0 -b .async
%patch9  -p0 -b .unistd
%patch10 -p0 -b .printf
%patch11 -p0 -b .plugins
%patch12 -p0 -b .completion
%patch13 -p0 -b .nscdunmap
%patch14 -p0 -b .sigrestart
%patch15 -p0 -b .longjmp
%patch16 -p0 -b .setlocale
%patch17 -p0 -b .headers
%patch18 -p0 -b .winch
%patch21 -p0 -b .zerotty
%patch22 -p0 -b .wrap
%patch23 -p0 -b .conf
%patch24 -p0 -b .metamode
#%patch25 -p0 -b .endpw
%patch31 -p0 -b .tmp
%patch40 -p0 -b .bashrc
%patch46 -p0 -b .notimestamp
%patch47 -p0 -b .perl522
%if %{with import_function}
%patch48
%endif
%patch49
%patch0  -p0 -b .0

%patch300 -p1

pushd ../readline-%{rl_vers}%{extend}
for patch in ../readline-%{rl_vers}-patches/*; do
    test -e $patch || break
    let level=0 || true
    file=$(lsdiff --files=1 $patch)
    if test ! -e $file ; then
	file=${file#*/}
	let level++ || true
    fi
    sed -ri '/^\*\*\* \.\./{ s@\.\./readline-%{rl_vers}[^/]*/@@ }' $patch
    echo Patch $patch
    patch -s -p$level < $patch
done
%patch21 -p2 -b .zerotty
%patch22 -p2 -b .wrap
%patch23 -p2 -b .conf
%patch24 -p2 -b .metamode
#%patch25 -p2 -b .endpw
%patch31 -p2 -b .tmp
%patch27 -p0 -b .xm
%patch30 -p0 -b .destdir
%patch20 -p0 -b .0

%build
  LANG=POSIX
  LC_ALL=$LANG
  unset LC_CTYPE
  SCREENDIR=$(mktemp -d ${PWD}/screen.XXXXXX) || exit 1
  SCREENRC=${SCREENDIR}/bash
  export SCREENRC SCREENDIR
  exec 0< /dev/null
  SCREENLOG=${SCREENDIR}/log
  cat > $SCREENRC<<-EOF
	deflogin off
	logfile $SCREENLOG
	logfile flush 1
	logtstamp off
	log on
	setsid on
	scrollback 0
	silence on
	utf8 on
	EOF
  CPU=$(uname -m 2> /dev/null)
  HOSTTYPE=${CPU}
  MACHTYPE=${CPU}-suse-linux
  export LANG LC_ALL HOSTTYPE MACHTYPE
pushd ../readline-%{rl_vers}%{extend}
%if 0%suse_version >= 1020
  autoconf
%endif
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
	  if ${CC:-gcc} -Werror ${flag/#-Wno-/-W} -S -o /dev/null -xc /dev/null > /dev/null 2>&1 ; then
	      eval $var=\${$var:+\$$var\ }$flag
	  fi
	  if ${CXX:-g++} -Werror ${flag/#-Wno-/-W} -S -o /dev/null -xc++ /dev/null > /dev/null 2>&1 ; then
	      eval $var=\${$var:+\$$var\ }$flag
	  fi
      esac
      set +o noclobber
  }
  LARGEFILE="$(getconf LFS_CFLAGS)"
  (cat > dyn.map)<<-'EOF'
	{
	    *;
	    !rl_*stream;
	};
	EOF
  (cat > rl.map)<<-'EOF'
	READLINE_6.3 {
	    rl_change_environment;
	    rl_clear_history;
	    rl_executing_key;
	    rl_executing_keyseq;
	    rl_filename_stat_hook;
	    rl_history_substr_search_backward;
	    rl_history_substr_search_forward;
	    rl_input_available_hook;
	    rl_print_last_kbd_macro;
	    rl_signal_event_hook;
	};
	EOF
  CFLAGS="$RPM_OPT_FLAGS $LARGEFILE -D_GNU_SOURCE -DRECYCLES_PIDS -Wall -g"
  LDFLAGS=""
  #
  # Never ever put -DMUST_UNBLOCK_CHLD herein as this breaks bash
  #
  cflags -Wuninitialized         CFLAGS
  cflags -Wextra                 CFLAGS
  cflags -Wno-unprototyped-calls CFLAGS
  cflags -Wno-switch-enum        CFLAGS
  cflags -Wno-unused-variable    CFLAGS
  cflags -Wno-unused-parameter   CFLAGS
  cflags -Wno-parentheses        CFLAGS
  cflags -ftree-loop-linear      CFLAGS
  cflags -pipe                   CFLAGS
  cflags -DBNC382214=0           CFLAGS
  cflags -DIMPORT_FUNCTIONS_DEF=0 CFLAGS
  cflags -Wl,--as-needed         LDFLAGS
  cflags -Wl,-O2                 LDFLAGS
  cflags -Wl,-rpath,%{_ldldir}/%{bash_vers}   LDFLAGS
  cflags -Wl,--version-script=${PWD}/rl.map   LDFLAGS
  cflags -Wl,--dynamic-list=${PWD}/dyn.map    LDFLAGS
  CC=gcc
  CC_FOR_BUILD="$CC"
  CFLAGS_FOR_BUILD="$CFLAGS"
  LDFLAGS_FOR_BUILD="$LDFLAGS"
  export CC_FOR_BUILD CFLAGS_FOR_BUILD LDFLAGS_FOR_BUILD CFLAGS LDFLAGS CC
  ./configure --build=%{_target_cpu}-suse-linux	\
	--disable-static		\
	--prefix=%{_prefix}		\
	--with-curses			\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--docdir=%{_defaultdocdir}/readline	\
	--libdir=%{_libdir}
  make
  make documentation
  ln -sf shlib/libreadline.so.%{rl_vers} libreadline.so
  ln -sf shlib/libreadline.so.%{rl_vers} libreadline.so.%{rl_major}
  ln -sf shlib/libhistory.so.%{rl_vers} libhistory.so
  ln -sf shlib/libhistory.so.%{rl_vers} libhistory.so.%{rl_major}
  LDFLAGS=${LDFLAGS/-Wl,--version-script=*rl.map/}
  LDFLAGS=${LDFLAGS/-Wl,--dynamic-list=*dyn.map/}
  LDFLAGS_FOR_BUILD="$LDFLAGS"
popd
  # /proc is required for correct configuration
  test -d /dev/fd || { echo "/proc is not mounted!" >&2; exit 1; }
  ln -sf ../readline-%{rl_vers} readline
  LD_LIBRARY_PATH=$PWD/../readline-%{rl_vers}
  export LD_LIBRARY_PATH
  CC="gcc -I$PWD -L$PWD/../readline-%{rl_vers}"
%if %_minsh
  cflags -Os CFLAGS
# cflags -U_FORTIFY_SOURCE CFLAGS
# cflags -funswitch-loops CFLAGS
# cflags -ftree-loop-im CFLAGS
# cflags -ftree-loop-ivcanon CFLAGS
# cflags -fprefetch-loop-arrays CFLAGS
# cflags -fno-stack-protector CFLAGS
# cflags -fno-unwind-tables CFLAGS
# cflags -fno-asynchronous-unwind-tables CFLAGS
%endif
  CC_FOR_BUILD="$CC"
  CFLAGS_FOR_BUILD="$CFLAGS"
  export CC_FOR_BUILD CFLAGS_FOR_BUILD CFLAGS LDFLAGS CC
%if 0%suse_version > 1020
  autoconf
%endif
  #
  # We have a malloc with our glibc
  #
  SYSMALLOC="
	--without-gnu-malloc
	--without-bash-malloc
  "
  #
  # System readline library (comment out it not to be used)
  #
  READLINE="
	--with-installed-readline
  "
  bash support/mkconffiles -v
%if %_minsh
  ./configure --build=%{_target_cpu}-suse-linux	\
	--prefix=%{_prefix}		\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--libdir=%{_libdir}		\
	--with-curses			\
	--with-afs			\
	$SYSMALLOC			\
	--enable-minimal-config		\
	--enable-arith-for-command	\
	--enable-array-variables	\
	--enable-brace-expansion	\
	--enable-casemod-attributes	\
	--enable-casemod-expansion	\
	--enable-command-timing		\
	--enable-cond-command		\
	--enable-cond-regexp		\
	--enable-coprocesses		\
	--enable-directory-stack	\
	--enable-dparen-arithmetic	\
	--enable-extended-glob		\
	--enable-job-control		\
	--enable-net-redirections	\
	--enable-process-substitution	\
	--disable-strict-posix-default	\
	--enable-separate-helpfiles=%{_datadir}/bash/helpfiles \
	$READLINE
  make Program=sh sh
  make distclean
%endif
  ./configure --build=%{_target_cpu}-suse-linux	\
	--prefix=%{_prefix}		\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--libdir=%{_libdir}		\
	--docdir=%{_defaultdocdir}/bash	\
	--with-curses			\
	--with-afs			\
	$SYSMALLOC			\
	--enable-job-control		\
	--enable-alias			\
	--enable-readline		\
	--enable-history		\
	--enable-bang-history		\
	--enable-directory-stack	\
	--enable-process-substitution	\
	--enable-prompt-string-decoding	\
	--enable-select			\
	--enable-help-builtin		\
	--enable-array-variables	\
	--enable-brace-expansion	\
	--enable-command-timing		\
	--enable-disabled-builtins	\
	--disable-strict-posix-default	\
	--enable-separate-helpfiles=%{_datadir}/bash/helpfiles \
	$READLINE
  make %{?do_profiling:CFLAGS="$CFLAGS %cflags_profile_generate"} \
	all printenv recho zecho xcase
  TMPDIR=$(mktemp -d /tmp/bash.XXXXXXXXXX) || exit 1
  > $SCREENLOG
  tail -q -s 0.5 -f $SCREENLOG & pid=$!
  env -i HOME=$PWD TERM=$TERM LD_LIBRARY_PATH=$LD_LIBRARY_PATH TMPDIR=$TMPDIR \
	SCREENRC=$SCREENRC SCREENDIR=$SCREENDIR \
	screen -L -D -m make TESTSCRIPT=%{SOURCE4} check
  kill -TERM $pid
  make %{?do_profiling:CFLAGS="$CFLAGS %cflags_profile_feedback" clean} all
  make -C examples/loadables/
  make documentation

%install
pushd ../readline-%{rl_vers}%{extend}
  make install htmldir=%{_defaultdocdir}/readline \
	       installdir=%{_defaultdocdir}/readline/examples DESTDIR=%{buildroot}
  make install-shared libdir=/%{_lib} linkagedir=%{_libdir} DESTDIR=%{buildroot}
  rm -rf %{buildroot}%{_defaultdocdir}/bash
  mkdir -p %{buildroot}%{_defaultdocdir}/bash
  chmod 0755 %{buildroot}/%{_lib}/libhistory.so.%{rl_vers}
  chmod 0755 %{buildroot}/%{_lib}/libreadline.so.%{rl_vers}
  rm -vf %{buildroot}/%{_lib}/libhistory.so.%{rl_vers}*old
  rm -vf %{buildroot}/%{_lib}/libreadline.so.%{rl_vers}*old
  rm -vf %{buildroot}/%{_lib}/libhistory.so
  rm -vf %{buildroot}/%{_lib}/libreadline.so
  ln -sf /%{_lib}/libhistory.so.%{rl_vers}  %{buildroot}/%{_libdir}/libhistory.so
  ln -sf /%{_lib}/libreadline.so.%{rl_vers} %{buildroot}/%{_libdir}/libreadline.so
popd
  make install DESTDIR=%{buildroot}
  make -C examples/loadables/ install-plugins DESTDIR=%{buildroot} libdir=/%{_lib}
  make -C examples/loadables/ install-headers DESTDIR=%{buildroot}
  mkdir -p %{buildroot}/bin
  mv %{buildroot}%{_bindir}/bash %{buildroot}/bin/
%if %_minsh
  install sh  %{buildroot}/bin/sh
  ln -sf ../../bin/sh   %{buildroot}%{_bindir}/sh
%else
  ln -sf bash %{buildroot}/bin/sh
  ln -sf ../../bin/bash %{buildroot}%{_bindir}/sh
%endif
  ln -sf ../../bin/bash %{buildroot}%{_bindir}/rbash
  install -m 644 COMPAT NEWS    %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 COPYING        %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/FAQ        %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/INTRO      %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/*.html     %{buildroot}%{_defaultdocdir}/bash/
  install -m 644 doc/builtins.1 %{buildroot}%{_mandir}/man1/bashbuiltins.1
  install -m 644 doc/rbash.1    %{buildroot}%{_mandir}/man1/rbash.1
  gzip -9f %{buildroot}%{_infodir}/*.inf*[^z] || true
  mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
  sed 's/^|//' > %{buildroot}%{_defaultdocdir}/bash/BUGS <<\EOF
Known problems
--------------
|
This version of bash/readline supports multi byte handling
that is e.g. wide character support for UTF-8.  This causes
problems in geting the current cursor position within the
readline runtime library:
|
bash-%{bash_vers}> LANG=ja_JP
bash-%{bash_vers}> echo -n "Hello"
bash-%{bash_vers}>
|
In other words the prompt overwrites the output of the
echo comand.  The boolean variable byte-oriented
set in %{_sysconfdir}/inputrc or $HOME/.inputrc avoids this
but disables multi byte handling.
EOF
  # remove unpackaged files
  rm -fv %{buildroot}%{_libdir}/libhistory.so.*
  rm -fv %{buildroot}%{_libdir}/libreadline.so.*
  rm -fv %{buildroot}%{_infodir}/rluserman.info.gz
  rm -fv %{buildroot}%{_mandir}/man3/history.3*
  rm -fv %{buildroot}%{_defaultdocdir}/readline/INSTALL
  mkdir -p %{buildroot}%{_sysconfdir}/skel
  install -m 644 %{S:5}    %{buildroot}%{_sysconfdir}/skel/.bashrc
  install -m 644 %{S:6}    %{buildroot}%{_sysconfdir}/skel/.profile
  touch -t 199605181720.50 %{buildroot}%{_sysconfdir}/skel/.bash_history
  chmod 600                %{buildroot}%{_sysconfdir}/skel/.bash_history
  %find_lang bash
%if %suse_version > 1020
  %fdupes -s %{buildroot}%{_datadir}/bash/helpfiles
%endif

%post doc
%install_info --info-dir=%{_infodir} %{_infodir}/bash.info.gz

%preun doc
%install_info_delete --info-dir=%{_infodir} %{_infodir}/bash.info.gz

%post -n libreadline6 -p /sbin/ldconfig

%postun -n libreadline6 -p /sbin/ldconfig

%post -n readline-doc
%install_info --info-dir=%{_infodir} %{_infodir}/history.info.gz
%install_info --info-dir=%{_infodir} %{_infodir}/readline.info.gz

%preun -n readline-doc
%install_info_delete --info-dir=%{_infodir} %{_infodir}/history.info.gz
%install_info_delete --info-dir=%{_infodir} %{_infodir}/readline.info.gz

%clean
LD_LIBRARY_PATH=%{buildroot}/%{_lib} \
ldd -u -r %{buildroot}/bin/bash || true
ldd -u -r %{buildroot}/%{_lib}/libreadline.so.* || true
%{?buildroot: %{__rm} -rf %{buildroot}}

%files
%defattr(-,root,root)
%config %attr(600,root,root) %{_sysconfdir}/skel/.bash_history
%config %attr(644,root,root) %{_sysconfdir}/skel/.bashrc
%config %attr(644,root,root) %{_sysconfdir}/skel/.profile
/bin/bash
/bin/sh
%dir %{_sysconfdir}/bash_completion.d
%{_bindir}/bashbug
%{_bindir}/rbash
%{_bindir}/sh
%dir %{_datadir}/bash
%dir %{_datadir}/bash/helpfiles
%{_datadir}/bash/helpfiles/*

%files lang -f bash.lang
%defattr(-,root,root)

%files doc
%defattr(-,root,root)
%doc %{_infodir}/bash.info.gz
%doc %{_mandir}/man1/bash.1.gz
%doc %{_mandir}/man1/bashbuiltins.1.gz
%doc %{_mandir}/man1/bashbug.1.gz
%doc %{_mandir}/man1/rbash.1.gz
%doc %{_defaultdocdir}/bash/

%if 0%suse_version >= 1020
%files devel
%defattr(-,root,root)
%dir /%{_includedir}/bash/
%dir /%{_includedir}/bash/%{bash_vers}/
%dir /%{_includedir}/bash/%{bash_vers}/builtins/
/%{_incdir}/bash/%{bash_vers}/*.h
/%{_incdir}/bash/%{bash_vers}/builtins/*.h
%endif

%files loadables
%defattr(-,root,root)
%dir %{_ldldir}/
%dir %{_ldldir}/%{bash_vers}/
%{_ldldir}/%{bash_vers}/*

%files -n libreadline6
%defattr(-,root,root)
/%{_lib}/libhistory.so.%{rl_major}
/%{_lib}/libhistory.so.%{rl_vers}
/%{_lib}/libreadline.so.%{rl_major}
/%{_lib}/libreadline.so.%{rl_vers}

%files -n readline-devel
%defattr(-,root,root)
%{_incdir}/readline/
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%doc %{_mandir}/man3/readline.3.gz

%files -n readline-doc
%defattr(-,root,root)
%doc %{_infodir}/history.info.gz
%doc %{_infodir}/readline.info.gz
%doc %{_defaultdocdir}/readline/

%changelog
* Mon Oct 19 2015 werner@suse.de
- Define the USE_MKTEMP and USE_MKSTEMP cpp macros as the
  implementation is already there.
- Add patch bash-4.3-pathtemp.patch to allow root to clear the
  file systems.  Otherwise the completion does not work if /tmp
  if full (ENOSPC for here documents)
* Fri Oct 16 2015 werner@suse.de
- Remove --hash-size options as there is no any change in the final
  binary nor library anymore
* Mon Aug 31 2015 werner@suse.de
- Add upstream patch bash43-039
  Using the output of `declare -p' when run in a function can result in variables
  that are invisible to `declare -p'.  This problem occurs when an assignment
  builtin such as `declare' receives a quoted compound array assignment as one of
  its arguments.
- Add upstream patch bash43-040
  There is a memory leak that occurs when bash expands an array reference on
  the rhs of an assignment statement.
- Add upstream patch bash43-041
  There are several out-of-bounds read errors that occur when completing command
  lines where assignment statements appear before the command name.  The first
  two appear only when programmable completion is enabled; the last one only
  happens when listing possible completions.
- Add upstream patch bash43-042
  There is a problem when parsing command substitutions containing `case'
  commands within pipelines that causes the parser to not correctly identify
  the end of the command substitution.
* Wed Jul  1 2015 coolo@suse.com
- add bash-4.3-perl522.patch to fix texi2html for perl 5.22
  (defined(@array) has been deprecated since at least 2012)
* Thu May 28 2015 werner@suse.de
- Add upstream patch bash43-034
  If neither the -f nor -v options is supplied to unset, and a name argument is
  found to be a function and unset, subsequent name arguments are not treated as
  variables before attempting to unset a function by that name.
- Add upstream patch bash43-035
  A locale with a long name can trigger a buffer overflow and core dump.  This
  applies on systems that do not have locale_charset in libc, are not using
  GNU libiconv, and are not using the libintl that ships with bash in lib/intl.
- Add upstream patch bash43-036
  When evaluating and setting integer variables, and the assignment fails to
  create a variable (for example, when performing an operation on an array
  variable with an invalid subscript), bash attempts to dereference a null
  pointer, causing a segmentation violation.
- Add upstream patch bash43-037
  If an associative array uses `@' or `*' as a subscript, `declare -p' produces
  output that cannot be reused as input.
- Add upstream patch bash43-038
  There are a number of instances where `time' is not recognized as a reserved
  word when the shell grammar says it should be.
* Mon May 18 2015 meissner@suse.com
- move info deletion to %%preun sections
* Wed Mar  4 2015 jdelvare@suse.de
- bash-4.3-loadables.dif: One more warning fixed, in
  examples/loadables/logname.c.
- bash-4.3-loadables.dif: Reverted one warning fix, which was
  introducing another warning and possibly a bug.
* Wed Mar  4 2015 jdelvare@suse.de
- bash-4.3-loadables.dif: Split changes to shell.h to a separate
  patch "bash-4.3-include-unistd.dif", as the loadables build just
  fine without these changes.
- bash-4.3-loadables.dif: Drop all header file inclusion fixups,
  upstream fixed the problem differently 5 years ago.
* Wed Feb 18 2015 werner@suse.de
- Do not restart all signal handlers for bash 4.3 as this breaks
  trap handler in subshells waotiug for a process
* Fri Jan 16 2015 werner@suse.de
- Remove -DMUST_UNBLOCK_CHLD(=1) as this breaks waitchild(2) on linux
* Fri Jan  9 2015 werner@suse.de
- Add upstream patch bash43-031
  The new nameref assignment functionality introduced in bash-4.3 did not perform
  enough validation on the variable value and would create variables with
  invalid names.
- Add upstream patch bash43-032
  When bash is running in Posix mode, it allows signals -- including SIGCHLD --
  to interrupt the `wait' builtin, as Posix requires.  However, the interrupt
  causes bash to not run a SIGCHLD trap for all exited children.  This patch
  fixes the issue and restores the documented behavior in Posix mode.
- Add upstream patch bash43-033
  Bash does not clean up the terminal state in all cases where bash or
  readline  modifies it and bash is subsequently terminated by a fatal signal.
  This happens when the `read' builtin modifies the terminal settings, both
  when readline is active and when it is not.  It occurs most often when a script
  installs a trap that exits on a signal without re-sending the signal to itself.
* Wed Dec  3 2014 jdelvare@suse.de
- Fix the sed command that fixes up the patch headers. It was
  printing a duplicate header line, which suprisingly did not
  confuse patch, but could in the future.
- Fix all patches that had the duplicate header line issue.
* Tue Nov  4 2014 werner@suse.de
- Use tail command to follow run-tests instead of a simpe cat command
* Fri Oct 24 2014 werner@suse.de
- Really remove obsolete patches
* Fri Oct 24 2014 brian@aljex.com
- Skip autoconf on OS 10.2 or older
* Wed Oct 22 2014 werner@suse.de
- Avoid fdupes on SLES-10
* Wed Oct 22 2014 werner@suse.de
- Bump bash version to 4.3
* Tue Oct 21 2014 brian@aljex.com
- Allow building on targets from SL 10.1 to current since it's free
* Mon Oct  6 2014 werner@suse.de
- Add upstream patches
  bash43-030 which fixes CVE-2014-6278
  bash43-029 which fixes CVE-2014-6277
  bash43-028 which fixes CVE-2014-7186/CVE-2014-7187
* Tue Sep 30 2014 werner@suse.de
- Add patch bash-4.2-extra-import-func.patch which is based on the
  BSD patch of Christos.  As further enhancements the option
  import-functions is mentioned in the manual page and a shopt
  switch is added to enable and disable import-functions on the fly
- Rename bash-4.2-extra-import-func.patch to bash-4.3-extra-import-func.patch
* Mon Sep 29 2014 werner@suse.de
- Add upstream patches
  bash43-027 which fixed bsc#898604
  bash43-026 which fixes CVE-2014-7169 and bsc#898346
  bash43-025 which replaces bash-4.3-CVE-2014-6271.patch and
  fixes bnc#896776
- Remove patch bash-4.3-CVE-2014-6271.patch due patch bash43-027
- Add patch bash-4.2-CVE-2014-7187.patch for bsc#898603, CVE-2014-7186,
  CVE-2014-7187: bad handling of HERE documents and for loop issue
* Fri Sep 26 2014 werner@suse.de
- Use a version linker script for libreadline 6.3 as there are new
  symbols in this 6.3 version like the rl_executing_keyseq and those
  are used by the new bash 4.3
* Thu Sep 18 2014 werner@suse.de
- Add bash-4.3-CVE-2014-6271.patch
  to fix CVE-2014-6271, the unexpected code execution with
  environment variables (bnc#896776)
* Tue Aug 19 2014 werner@suse.de
- Update to bash 4.3 with patch level 24
  * The -t timeout option to `read' does not work when the -e option is used
  * When PS2 contains a command substitution, here-documents entered in an
    interactive shell can sometimes cause a segmentation fault.
  * When the readline `revert-all-at-newline' option is set, pressing newline
    when the current line is one retrieved from history results in a double free
    and a segmentation fault.
  * Using nested pipelines within loops with the `lastpipe' option set can result
    in a segmentation fault.
  * Bash does not correctly parse process substitution constructs that contain
    unbalanced parentheses as part of the contained command.
  * Indirect variable references do not work correctly if the reference
    variable expands to an array reference using a subscript other than 0
* Sun Jun 29 2014 schwab@linux-m68k.org
- Don't use outdated C standard
* Tue May 20 2014 werner@suse.de
- Update to bash 4.3 with patch level 18
  * When a SIGCHLD trap runs a command containing a shell builtin while
    a script is running `wait' to wait for all running children to complete,
    the SIGCHLD trap will not be run once for each child that terminates.
  * Using reverse-i-search when horizontal scrolling is enabled doe
    not redisplay the entire line containing the successful search results.
  * Under certain circumstances, $@ is expanded incorrectly in contexts where
    word splitting is not performed.
  * When completing directory names, the directory name is dequoted twice.
    This causes problems for directories with single and double quotes in
    their names.
  * An extended glob pattern containing a slash (`/') causes the globbing code
    to misinterpret it as a directory separator.
  * The code that creates local variables should not clear the `invisible'
    attribute when returning an existing local variable.  Let the code that
    actually assigns a value clear it.
  * When assigning an array variable using the compound assignment syntax,
    but using `declare' with the rhs of the compound assignment quoted, the
    shell did not mark the variable as visible after successfully performing
    the assignment.
- Update to readline library 6.3 with patch level 6
  * Using reverse-i-search when horizontal scrolling is enabled does
    not redisplay the entire line containing the successful search results.
- Remove readline-horizontal-redisplay.patch as now upstream
- Rename readline-6.2.dif to readline-6.3.dif and bash-4.2.dif to bash-4.3.dif
* Wed Apr 30 2014 werner@suse.de
- Add readline-horizontal-redisplay.patch from upstream as a temporary
  fix for failing incremental search in horizontal-scroll-mode
* Thu Apr 17 2014 werner@suse.de
- Make patch command work on older products
* Thu Apr 17 2014 werner@suse.de
- Update to bash 4.3 with patch level 11
  * The `helptopic' completion action now maps to all the help topics, not just
    the shell builtins.
  * The `help' builtin no longer does prefix substring matching first, so
    `help read' does not match `readonly', but will do it if exact string
    matching fails.
  * The shell can be compiled to not display a message about processes that
    terminate due to SIGTERM.
  * Non-interactive shells now react to the setting of checkwinsize and set
    LINES and COLUMNS after a foreground job exits.
  * There is a new shell option, `globasciiranges', which, when set to on,
    forces globbing range comparisons to use character ordering as if they
    were run in the C locale.
  * There is a new shell option, `direxpand', which makes filename completion
    expand variables in directory names in the way bash-4.1 did.
  * In Posix mode, the `command' builtin does not change whether or not a
    builtin it shadows is treated as an assignment builtin.
  * The `return' and `exit' builtins accept negative exit status arguments.
  * The word completion code checks whether or not a filename containing a
    shell variable expands to a directory name and appends `/' to the word
    as appropriate.  The same code expands shell variables in command names
    when performing command completion.
  * In Posix mode, it is now an error to attempt to define a shell function
    with the same name as a Posix special builtin.
  * When compiled for strict Posix conformance, history expansion is disabled
    by default.
  * The history expansion character (!) does not cause history expansion when
    followed by the closing quote in a double-quoted string.
  * `complete' and its siblings compgen/compopt now takes a new `-o noquote'
    option to inhibit quoting of the completions.
  * Setting HISTSIZE to a value less than zero causes the history list to be
    unlimited (setting it 0 zero disables the history list).
  * Setting HISTFILESIZE to a value less than zero causes the history file size
    to be unlimited (setting it to 0 causes the history file to be truncated
    to zero size).
  * The `read' builtin now skips NUL bytes in the input.
  * There is a new `bind -X' option to print all key sequences bound to Unix
    commands.
  * When in Posix mode, `read' is interruptible by a trapped signal.  After
    running the trap handler, read returns 128+signal and throws away any
    partially-read input.
  * The command completion code skips whitespace and assignment statements
    before looking for the command name word to be completed.
  * The build process has a new mechanism for constructing separate help files
    that better reflects the current set of compilation options.
  * The -nt and -ot options to test now work with files with nanosecond
    timestamp resolution.
  * The shell saves the command history in any shell for which history is
    enabled and HISTFILE is set, not just interactive shells.
  * The shell has `nameref' variables and new -n(/+n) options to declare and
    unset to use them, and a `test -R' option to test for them.
  * The shell now allows assigning, referencing, and unsetting elements of
    indexed arrays using negative subscripts (a[-1]=2, echo ${a[-1]}) which
    count back from the last element of the array.
  * The {x}<word redirection feature now allows words like {array[ind]} and
    can use variables with special meanings to the shell (e.g., BASH_XTRACEFD).
  * There is a new CHILD_MAX special shell variable; its value controls the
    number of exited child statues the shell remembers.
  * There is a new configuration option (--enable-direxpand-default) that
    causes the `direxpand' shell option to be enabled by default.
  * Bash does not do anything special to ensure that the file descriptor
    assigned to X in {x}<foo remains open after the block containing it
    completes.
  * The `wait' builtin has a new `-n' option to wait for the next child to
    change status.
  * The `printf' %%(...)T format specifier now uses the current time if no
    argument is supplied.
  * There is a new variable, BASH_COMPAT, that controls the current shell
    compatibility level.
  * The `popd' builtin now treats additional arguments as errors.
  * The brace expansion code now treats a failed sequence expansion as a
    simple string and will continue to expand brace terms in the remainder
    of the word.
  * Shells started to run process substitutions now run any trap set on EXIT.
  * The fc builtin now interprets -0 as the current command line.
  * Completing directory names containing shell variables now adds a trailing
    slash if the expanded result is a directory.
  * `cd' has a new `-@' option to browse a file's extended attributes on
    systems that support O_XATTR.
  * The test/[/[[ `-v variable' binary operator now understands array
    references.
- Update to readline library 6.3 with patch level 5
  * Readline is now more responsive to SIGHUP and other fatal signals when
    reading input from the terminal or performing word completion but no
    longer attempts to run any not-allowable functions from a signal handler
    context.
  * There are new bindable commands to search the history for the string of
    characters between the beginning of the line and the point
    (history-substring-search-forward, history-substring-search-backward)
  * Readline allows quoted strings as the values of variables when setting
    them with `set'.  As a side effect, trailing spaces and tabs are ignored
    when setting a string variable's value.
  * The history library creates a backup of the history file when writing it
    and restores the backup on a write error.
  * New application-settable variable: rl_filename_stat_hook: a function called
    with a filename before using it in a call to stat(2).  Bash uses it to
    expand shell variables so things like $HOME/Downloads have a slash
    appended.
  * New bindable function `print-last-kbd-macro', prints the most-recently-
    defined keyboard macro in a reusable format.
  * New user-settable variable `colored-stats', enables use of colored text
    to denote file types when displaying possible completions (colored analog
    of visible-stats).
  * New user-settable variable `keyseq-timout', acts as an inter-character
    timeout when reading input or incremental search strings.
  * New application-callable function: rl_clear_history. Clears the history list
    and frees all readline-associated private data.
  * New user-settable variable, show-mode-in-prompt, adds a characters to the
    beginning of the prompt indicating the current editing mode.
  * New application-settable variable: rl_input_available_hook; function to be
    called when readline detects there is data available on its input file
    descriptor.
  * Readline calls an application-set event hook (rl_event_hook) after it gets
    a signal while reading input (read returns -1/EINTR but readline does not
    handle the signal immediately) to allow the application to handle or
    otherwise note it.
  * If the user-settable variable `history-size' is set to a value less than
    0, the history list size is unlimited.
  * New application-settable variable: rl_signal_event_hook; function that is
    called when readline is reading terminal input and read(2) is interrupted
    by a signal.  Currently not called for SIGHUP or SIGTERM.
  * rl_change_environment: new application-settable variable that controls
    whether or not Readline modifies the environment (currently readline
    modifies only LINES and COLUMNS).
- Removed patches
  audit-rl-patch and audit-patch which are now upstream
  readline-6.2-msgdynamic.patch which is upstream
  bash-4.2-nsec.dif which is upstream
  config-guess-sub-update.patch which is upstream
- Modify patches
  bash-4.2-2.4.4.patch becomes bash-4.3-2.4.4.patch
  bash-3.0-decl.patch becomes bash-4.3-decl.patch
  bash-4.0-loadables.dif becomes bash-4.3-loadables.dif
  bash-4.2-sigrestart.patch becomes bash-4.3-sigrestart.patch
  bash-4.0-headers.dif becomes bash-4.3-headers.dif
  bash-4.2-winch.dif becomes bash-4.3-winch.dif
  readline-4.3-input.dif becomes readline-6.3-input.dif
  readline-6.2-destdir.patch becomes readline-6.3-destdir.patch
  readline-6.2-rltrace.patch becomes readline-6.3-rltrace.patch
* Tue Apr 15 2014 werner@suse.de
- Add bash upstream patch 47 to fix a problem where the function
  that shortens pathnames for $PS1 according to the value of
  $PROMPT_DIRTRIM uses memcpy on potentially-overlapping regions
  of memory, when it should use memmove.  The result is garbled
  pathnames in prompt strings.
- Remove bash-4.2-prompt-dirtrim.patch as this was the original
  report of above.
* Tue Apr  1 2014 werner@suse.de
- Add bash upstream patch 46 to fix a problem introduced by patch
  32 a problem with "$@" and arrays expanding empty positional
  parameters or array elements when using substring expansion,
  pattern substitution, or case modfication.  The empty parameters
  or array elements are removed instead of expanding to empty
  strings ("").
- Add readline upstream patch 5: The readline shared library
  helper script needs to be updated for Mac OS X 10.9
* Tue Mar 18 2014 werner@suse.de
- CVE-2014-2524: bash,readline: temporary file misuse in _rl_tropen (bnc#868822)
  Even if used only by developers to debug readline library do not
  open temporary files from public location without O_EXCL
* Fri Jan 31 2014 werner@suse.de
- Add upstream patch bash-4.2-prompt-dirtrim.patch
  bash patch tar ball to solve some some cases strange output
  displayed in the prompt if PROMPT_DIRTRIM i sset.
* Fri Jul 12 2013 werner@suse.de
- Reintroduce patch bash-4.2-winch.dif to solve bnc#828877
  accordingly to my test and upstream (search on bug-bash@gnu.org
  for message-id <51DFEB10.8080302@case.edu>)
* Mon Jul  8 2013 werner@suse.de
- Add bash-4.2-strcpy.patch from upstream mailing list to patch
  collection tar ball to avoid when using \w in the prompt and
  changing the directory outside of HOME the a strcpy work on
  overlapping memory areas.
* Tue Jun  4 2013 coolo@suse.com
- add a conflict between readline5 and readline6-32bit
* Tue May 28 2013 werner@suse.de
- Do not restart the sighandler after a trap is reset (bnc#820149)
* Thu Mar 21 2013 werner@suse.de
- Add patch from upstream mailing list to speed up array handling
- Add patch from upstream mailing list to avoid fdleaks
- Use lsdiff to determine the depth of the leading slashes in a
  patch file
* Fri Mar 15 2013 werner@suse.de
- Disable workaround for bnc#382214 due bnc#806628, let's see when
  the old bug will be up again.
- Update bash 4.2 to patch level 45
  * When SIGCHLD is trapped, and a SIGCHLD trap handler runs when
    a pending `read -t' invocation times out and generates SIGALRM,
    bash can crash with a segmentation fault.
  * When converting a multibyte string to a wide character string
    as part of pattern matching, bash does not handle the end of
    the string correctly, causing the search for the NUL to go
    beyond the end of the string and reference random memory.
    Depending on the contents of that memory, bash can produce
    errors or crash.
  * The <&n- and >&n- redirections, which move one file descriptor
    to another, leave the file descriptor closed when applied to
    builtins or compound commands.
- Use screen to provide a controlling terminal for running the
  test suite
* Tue Feb 12 2013 schwab@suse.de
- config-guess-sub-update.patch:
  Update config.guess/sub for aarch64
- Fix check for negated warning switch
* Wed Jan  9 2013 werner@suse.de
- Avoid autoconf on older products
- Apply audit patch variant to readline as well as we use a shared
  libreadline
- Avoid bash-devel on older products as older GNU make do not have
  a realpath builtin
* Tue Jan  8 2013 werner@suse.de
- Do not trigger the export of COLUMNS or LINES due enforced
  checkwinsize (bnc#793536)
* Tue Jan  8 2013 werner@suse.de
- Update bash 4.2 to patch level 42
  * Missing I/O errors if output redirection applied to builtin
    commands when the file descriptor was closed
  * Process substitution incorrectly inherited a flag that
    inhibited using the temporary environment for variable lookups
    if it was providing the filename to a redirection.
  * Compilation failed after specifying the `minimal config' option
* Mon Nov  5 2012 werner@suse.de
- Update bash 4.2 to patch level 39
  * Official fix for the last crash fix
  * Avoid variable expansion in arithmetic expressions when
    evaluation is being suppressed
* Wed Oct 17 2012 werner@suse.de
- Do not mix xmalloc/xfree of libreadline and bash by making the
  libreadline version weak symbols instead of private symbols
* Fri Aug 24 2012 werner@suse.de
- Add patch from upstream mailing list to avoids crash
* Fri Jul 20 2012 werner@suse.de
- Update bash 4.2 to patch level 37
  * Attempting to redo (using `.') the vi editing mode `cc', `dd',
    or `yy' commands leads to an infinite loop.
* Thu Jul 19 2012 werner@suse.de
- Do not mask internal _rl symbols as internal as there are many
  tools out there which uses them (gdb as an example)
* Wed Jul 18 2012 werner@suse.de
- libreadlib: try to avoid to bind references of the symbols
  rl_instream and rl_outstream
- libreadlib: make private symbols really private
* Wed Jul 18 2012 werner@suse.de
- Increase buffer for libreadline messsages if required
- Include stdio.h in libreadline header files to get the declaration
  of FILES correct.
* Mon Jul  9 2012 werner@suse.de
- Update bash 4.2 to patch level 36
  * Patch 25: When used in a shell function,
    `declare -g -a array=(compound assignment)' creates a local
    variable instead of a global one.
  * Patch 26: The `lastpipe' option does not behave correctly on
    machines where the open file limit is less than 256.
  * Patch 27: When the `extglob' shell option is enabled, pattern
    substitution does not work correctly in the presence of
    multibyte characters.
  * Patch 28: When using a word expansion for which the right hand
    side is evaluated, certain expansions of quoted null strings
    include spurious ^? characters.
  * Patch 29: Bash-4.2 tries to leave completed directory names as
    the user typed them, without expanding them to a full pathname.
    One effect of this is that shell variables used in pathnames
    being completed (e.g., $HOME) are left unchanged, but the `$'
    is quoted by readline because it is a special character to the shell.
  * Patch 30: When attempting to glob strings in a multibyte locale,
    and those strings contain invalid multibyte characters that cause
    mbsnrtowcs to return 0, the globbing code loops infinitely.
  * Patch 31: A change between bash-4.1 and bash-4.2 to prevent the
    readline input hook from being called too frequently had the side
    effect of causing delays when reading pasted input on systems such
    as Mac OS X.  This patch fixes those delays while retaining the
    bash-4.2 behavior.
  * Patch 32: Bash-4.2 has problems with DEL characters in the
    expanded value of variables used in the same quoted string as
    variables that expand to nothing.
  * Patch 33: Bash uses a static buffer when expanding the /dev/fd
    prefix for the test and conditional commands, among other uses,
    when it should use a dynamic buffer to avoid buffer overflow.
  * Patch 34: In bash-4.2, the history code would inappropriately add
    a semicolon to multi-line compound array assignments when adding
    them to the history.
  * Patch 35: When given a number of lines to read, `mapfile -n lines'
    reads one too many.
  * Patch 36: Bash-4.2 produces incorrect word splitting results when
    expanding double-quoted $@ in the same string as and adjacent to
    other variable expansions.  The $@ should be split, the other
    expansions should not.
- Add patch to avoid double free or corruption due expanding number
  sequence with huge numbers. Patch will go upstream (bnc#763591)
* Tue Jun 26 2012 cfarrell@suse.com
- license update: GPL-3.0+
  Upstream declares the bash license to be GPL-3.0+ - not GPL-2.0+
* Mon Jun 11 2012 werner@suse.de
- Enable auditing patch by simply applying it
* Wed May 23 2012 meissner@suse.com
- added auditing patch from
  http://git.savannah.gnu.org/cgit/bash.git/plain/CWRU/audit-patch
* Thu Apr  5 2012 werner@suse.de
- Remove not required patch (was a fix for bnc#141394) which now
  cause a wrong behaviour if applied (bnc#755453)
* Tue Mar 13 2012 werner@suse.de
- Update bash 4.2 to patch level 24
* Fri Mar  9 2012 werner@suse.de
- Avoid endless loop in user completion caused by endpw patches
* Tue Mar  6 2012 werner@suse.de
- Add small patch for be able to use nanoseconds in comparision
  of time stamps of files (bnc#750640)
* Tue Mar  6 2012 werner@suse.de
- Reenable patch for bnc#725657 with latest change from latest
  git repository of the patch.
* Tue Dec 20 2011 coolo@suse.com
- add autoconf as buildrequire to avoid implicit dependency
* Mon Dec 19 2011 coolo@suse.de
- remove suse_update_config calls - obsolete
* Fri Nov 25 2011 werner@suse.de
- Make build check quiet
* Fri Nov 25 2011 werner@suse.de
- Update bash 4.2 to patch level 20
- Update readline 6.2 to patch level 2
* Mon Nov 21 2011 werner@suse.de
- Disable endpwent() in rl_username_completion_function() as this
  cause a deadlock in a futex of the glibc (bnc#731556)
* Fri Nov 18 2011 werner@suse.de
- Enforce bind references to global function symbols to the
  definition within libreadline
* Wed Nov 16 2011 werner@suse.de
- Use libtinfo if available otherwise libncurses, this avoids
  linkage against libncursesw of libreadline (required due
  bnc #729226)
* Fri Nov 11 2011 werner@suse.de
- Avoid memory mapped /var/run/nscd/passwd at shutdown by simply
  unmapping this only used area if parent is systemd or SysVinit
* Fri Nov 11 2011 werner@suse.de
- Always close get(pw|gr)func with endpw() respectivly with endgr()
  to avoid memory mapped passwd/groups of cache files from nscd
* Wed Nov  2 2011 werner@suse.de
- Disable last patch as it seems a bit broken (bnc#725657)
* Tue Oct 25 2011 werner@suse.de
- Add direxpand patch from upstream (bnc#725657)
* Fri Oct  7 2011 werner@suse.de
- Add patch from upstream mailing list to avoid memory leak by
  reassigning associative array variable
* Mon Sep 19 2011 coolo@suse.com
- remove autoreqprov and author lists
* Tue Jun 21 2011 werner@suse.de
- Add fix from upstream mailing list to avoid crash
* Fri Jun 17 2011 coolo@novell.com
- use original source URLs
* Thu Jun 16 2011 werner@suse.de
- Fix the fix for bug bnc#681286 to be able to avoid both a not
  expanding glob as well as the infinit loop in multi byte locale
* Thu May 12 2011 werner@suse.de
- Update bash 4.2 to patch level 10
- Add patch from upstream to avoid loosing quoted-nulls
- Add modified patch to avod endless loop in UTF-8 locale
* Tue Mar 22 2011 werner@suse.de
- Remove patch to avod endless loop in UTF-8 locale as it breaks
  glob expanding (bnc#681286)
* Tue Mar 15 2011 werner@suse.de
- Update bash 4.2 to patch level 8
- Add Ctr-C patch from upstream
- Add fix for endless loop in UTF-8 locale
* Wed Mar  9 2011 werner@suse.de
- Avoid siglongjmp, compare with
  http://lists.gnu.org/archive/html/bug-bash/2011-03/msg00070.html
  use temprary solution from Chet
* Tue Mar  8 2011 werner@suse.de
- Much better solution for saving history for system with sigsetjmp
* Tue Mar  8 2011 werner@suse.de
- Reintroduce history saving at SIGHUP
* Mon Mar  7 2011 werner@suse.de
- Update bash 4.2 to patch level 7
* Thu Feb 17 2011 coolo@novell.com
- having a bash man page is recommended (bnc#672528)
* Mon Feb 14 2011 werner@suse.de
- Update to bash 4.2 -- changelog see entry for bash 4.2 rc1
* Mon Jan 17 2011 werner@suse.de
- Update to bash 4.2 rc1
  * `exec -a foo' now sets $0 to `foo' in an executable shell script
    without a leading #!.
  * Subshells begun to execute command substitutions or run shell functions or
    builtins in subshells do not reset trap strings until a new trap is
    specified.  This allows $(trap) to display the caller's traps and the
    trap strings to persist until a new trap is set.
  * `trap -p' will now show signals ignored at shell startup, though their
    disposition still cannot be modified.
  * $'...', echo, and printf understand \uXXXX and \UXXXXXXXX escape sequences.
  * declare/typeset has a new `-g' option, which creates variables in the
    global scope even when run in a shell function.
  * test/[/[[ have a new -v variable unary operator, which returns success if
    `variable' has been set.
  * Posix parsing changes to allow `! time command' and multiple consecutive
    instances of `!' (which toggle) and `time' (which have no cumulative
    effect).
  * Posix change to allow `time' as a command by itself to print the elapsed
    user, system, and real times for the shell and its children.
  * $((...)) is always parsed as an arithmetic expansion first, instead of as
    a potential nested command substitution, as Posix requires.
  * A new FUNCNEST variable to allow the user to control the maximum shell
    function nesting (recursive execution) level.
  * The mapfile builtin now supplies a third argument to the callback command:
    the line about to be assigned to the supplied array index.
  * The printf builtin has a new %%(fmt)T specifier, which allows time values
    to use strftime-like formatting.
  * There is a new `compat41' shell option.
  * The cd builtin has a new Posix-mandated `-e' option.
  * Negative subscripts to indexed arrays, previously errors, now are treated
    as offsets from the maximum assigned index + 1.
  * Negative length specifications in the ${var:offset:length} expansion,
    previously errors, are now treated as offsets from the end of the variable.
  * Parsing change to allow `time -p --'.
  * Posix-mode parsing change to not recognize `time' as a keyword if the
    following token begins with a `-'.  This means no more Posix-mode
    `time -p'.  Posix interpretation 267.
  * There is a new `lastpipe' shell option that runs the last command of a
    pipeline in the current shell context.  The lastpipe option has no
    effect if job control is enabled.
  * History expansion no longer expands the `$!' variable expansion.
  * Posix mode shells no longer exit if a variable assignment error occurs
    with an assignment preceding a command that is not a special builtin.
  * History expansion no longer expands the `$!' variable expansion.
  * Posix mode shells no longer exit if a variable assignment error occurs
    with an assignment preceding a command that is not a special builtin.
  * Non-interactive mode shells exit if -u is enabled and an attempt is made
    to use an unset variable with the %% or # expansions, the `//', `^', or
    `,' expansions, or the parameter length expansion.
  * Posix-mode shells use the argument passed to `.' as-is if a $PATH search
    fails, effectively searching the current directory.  Posix-2008 change.
- Update to readline 6.2 rc1
  * The history library does not try to write the history filename in the
    current directory if $HOME is unset.  This closes a potential security
    problem if the application does not specify a history filename.
  * New bindable variable `completion-display-width' to set the number of
    columns used when displaying completions.
  * New bindable variable `completion-case-map' to cause case-insensitive
    completion to treat `-' and `_' as identical.
  * There are new bindable vi-mode command names to avoid readline's case-
    insensitive matching not allowing them to be bound separately.
  * New bindable variable `menu-complete-display-prefix' causes the menu
    completion code to display the common prefix of the possible completions
    before cycling through the list, instead of after.
* Mon Oct 18 2010 jslaby@suse.de
- fix czech message
* Thu Oct 14 2010 werner@suse.de
- Update bash 4.1 to patch level 9
  * When declaring an associative array and implicitly assigning a
    value to element "0", bash does not correctly allocate memory,
    leading to a segmentation violation when that element or the
    array itself is unset.
  * An arriving SIGCHLD will interrupt `slow' system calls such as
    write(2) to or read(2) from a terminal.  This results in an
    error message and truncated input or output.
* Fri Sep  3 2010 cristian.rodriguez@opensuse.org
- builtin "man2html"generates html manual with a timestamp
  that causes the package to be published over and over again.
* Mon Aug 16 2010 werner@suse.de
- A modified version of the pipe patch which should handle
  the PIPESTATUS array
* Fri Aug 13 2010 werner@suse.de
- Disable the pipe patch from Thu Jun 24 10:40:09 CEST 2010
  as this resets the PIPESTATUS array to the status of the
  forground process only
* Thu Jul 29 2010 werner@suse.de
- Add fix from mailing list to avoid crash
* Mon Jul 19 2010 werner@suse.de
- Comment out recommendation of bash-completion, as I'd like
  no to see the bugs of bash-completion in my bugzilla
* Sat Jul 17 2010 cristian.rodriguez@opensuse.org
- Do not package static libraries
- Fix Recommends/Suggests
* Thu Jun 24 2010 werner@suse.de
- Add fix from upstream: restore the parser state over changing
  readline editing mode otherwise e.g. set alias before the
  change are lost.
* Thu Jun 24 2010 werner@suse.de
- Avoid running the last member of a pipe command sequence to run
  in its own subshell, this makes know lines like the simple
  echo 1 2 | read a b; echo $a $b
  work as expected by the users
* Tue May 25 2010 werner@suse.de
- Update bash 4.1 to patch level 7
  * Bash did not correctly print/reproduce here documents attached
    to commands inside compound commands such as for and while.
  * A typo caused bash to not honor a precision specification in a
    printf format.
* Mon Apr 12 2010 werner@suse.de
- Add fix for memory double free in array handling
* Tue Apr  6 2010 werner@suse.de
- Update bash 4.1 to patch level 5 (related to bnc#522351)
  * If command completion is attempted on a word with a quoted globbing
    character (e.g., `*' or `?'), bash can reference a NULL pointer and
    dump core.
  * When running in Posix mode and executing a shell function without local
    variables, bash will not propagate a variable in a special builtin's temporary
    environment to have global scope.
  * When the `read' builtin times out after the timeout specified with -t is
    exceeded, it does not reset the flags that tell signal handlers to process
    signals immediately instead of deferring their handling.  This can result
    in unsafe functions being called from signal handlers, which can cause bash
    to hang or dump core.
* Tue Mar  9 2010 werner@suse.de
- Add patch from bash-bug list to avoid crahs on some strange
  TAB completions
* Mon Mar  1 2010 ro@suse.de
- fix warning no return statement in function returning non-void
  to fix build (in bashline.c)
* Wed Feb 24 2010 werner@suse.de
- Avoid hang due malloc()/free() within signal handler (bnc#522351)
* Thu Feb 18 2010 werner@suse.de
- Add patch to reflect the usage of /etc/bash.bashrc (bnc#577221)
* Mon Feb 15 2010 werner@suse.de
- Update bash 4.1 to patch level 2
  * Here-documents within $(...) command substitutions may once more be
    delimited by the closing right paren, instead of requiring a newline.
  * Bash's file status checks (executable, readable, etc.) now take file
    system ACLs into account on file systems that support them.
  * Bash now passes environment variables with names that are not valid
    shell variable names through into the environment passed to child
    processes.
  * The `execute-unix-command' readline function now attempts to clear and
    reuse the current line rather than move to a new one after the command
    executes.
  * `printf -v' can now assign values to array indices.
  * New `complete -E' and `compopt -E' options that work on the "empty"
    completion: completion attempted on an empty command line.
  * New complete/compgen/compopt -D option to define a `default' completion:
    a completion to be invoked on command for which no completion has been
    defined.  If this function returns 124, programmable completion is
    attempted again, allowing a user to dynamically build a set of completions
    as completion is attempted by having the default completion function
    install individual completion functions each time it is invoked.
  * When displaying associative arrays, subscripts are now quoted.
  * Changes to dabbrev-expand to make it more `emacs-like': no space appended
    after matches, completions are not sorted, and most recent history entries
    are presented first.
  * The [[ and (( commands are now subject to the setting of `set -e' and the
    ERR trap.
  * The source/. builtin now removes NUL bytes from the file before attempting
    to parse commands.
  * There is a new configuration option (in config-top.h) that forces bash to
    forward all history entries to syslog.
  * A new variable $BASHOPTS to export shell options settable using `shopt' to
    child processes.
  * There is a new confgure option that forces the extglob option to be
    enabled by default.
  * New variable $BASH_XTRACEFD; when set to an integer bash will write xtrace
    output to that file descriptor.
  * If the optional left-hand-side of a redirection is of the form {var}, the
    shell assigns the file descriptor used to $var or uses $var as the file
    descriptor to move or close, depending on the redirection operator.
  * The < and > operators to the [[ conditional command now do string
    comparison according to the current locale if the compatibility level
    is greater than 40.
  * Programmable completion now uses the completion for `b' instead of `a'
    when completion is attempted on a line like: a $(b c.
  * Force extglob on temporarily when parsing the pattern argument to
    the == and != operators to the [[ command, for compatibility.
  * Changed the behavior of interrupting the wait builtin when a SIGCHLD is
    received and a trap on SIGCHLD is set to be Posix-mode only.
  * The read builtin has a new `-N nchars' option, which reads exactly NCHARS
    characters, ignoring delimiters like newline.
  * The mapfile/readarray builtin no longer stores the commands it invokes via
    callbacks in the history list.
  * There is a new `compat40' shopt option.
- Update readline 6.1 to patch level 1
  * New bindable function: menu-complete-backward.
  * In the vi insertion keymap, C-n is now bound to menu-complete by default,
    and C-p to menu-complete-backward.
  * When in vi command mode, repeatedly hitting ESC now does nothing, even
    when ESC introduces a bound key sequence.  This is closer to how
    historical vi behaves.
  * New bindable function: skip-csi-sequence.  Can be used as a default to
    consume key sequences generated by keys like Home and End without having
    to bind all keys.
  * New application-settable function: rl_filename_rewrite_hook.  Can be used
    to rewite or modify filenames read from the file system before they are
    compared to the word to be completed.
  * New bindable variable: skip-completed-text, active when completing in the
    middle of a word.  If enabled, it means that characters in the completion
    that match characters in the remainder of the word are "skipped" rather
    than inserted into the line.
  * The pre-readline-6.0 version of menu completion is available as
    "old-menu-complete" for users who do not like the readline-6.0 version.
  * New bindable variable: echo-control-characters.  If enabled, and the
    tty ECHOCTL bit is set, controls the echoing of characters corresponding
    to keyboard-generated signals.
  * New bindable variable: enable-meta-key.  Controls whether or not readline
    sends the smm/rmm sequences if the terminal indicates it has a meta key
    that enables eight-bit characters.
* Wed Dec 16 2009 jengelh@medozas.de
- package documentation as noarch
* Sat Dec 12 2009 jengelh@medozas.de
- add baselibs.conf as a source
* Fri Dec  4 2009 werner@suse.de
- Fix bug in bash-4.0-security.patch (bnc#559877)
* Thu Oct 29 2009 werner@suse.de
- Update to newest patch level 35
  * bash incorrectly interprets wildcarded path components between
    a **/ and the last /
  * bash incorrectly treated single and double quotes as
    delimiters rather than introducing quoted strings when
    splitting the line into words for programmable completion
    functions
* Wed Sep 30 2009 werner@suse.de
- Make _rl_enable_meta configurable by the users (bnc#541379)
* Wed Sep  9 2009 werner@suse.de
- Do not change tty owner group twice by child and parent (bnc#523667)
* Wed Sep  9 2009 werner@suse.de
- Update to newest patch level 33
  * Includes one of our own patches
* Wed Aug 26 2009 coolo@novell.com
- rediff patches to avoid fuzz
* Tue Jul 28 2009 werner@suse.de
- Update to newest patch level 28
* Thu Jul  2 2009 werner@suse.de
- Add fix from bash maintainer for closing memory leak in read
  builtin (bnc#510288)
* Tue Jun  9 2009 werner@suse.de
- Branch off some sub packages:
  * bash-lang to include localization
  * bash-loadables for installing the loadable runtime builtins
  * bash-devel to install headers for developing loadable builtins
* Wed Jun  3 2009 werner@suse.de
- Enforce the usage of euidaccess(3) instead of stat(2) for testing
  permissions for a file (bnc#509105)
* Mon May 25 2009 werner@suse.de
- Update to newest patch level 24:
  * include last few patches
- Add patches from mailing list for globstar expansion
* Mon May 11 2009 werne@suse.de
- Increase size of hash table for runtime linker a lot
* Mon Apr 27 2009 werne@suse.de
- Add patches from mailing list:
  * fix problem with invisible characters in prompt
  * make dir*/** work
* Tue Apr 21 2009 werne@suse.de
- Do not crash on forbidden subdirectories with globstar extension
* Wed Apr 15 2009 werne@suse.de
- Add fix to be able to clear to eol in readline library
* Tue Apr 14 2009 werne@suse.de
- Add fix for timing issue in readline SIGWINCH handling
* Wed Apr  8 2009 werne@suse.de
- Add patches from bug-bash@gnu.org to avoid eg. segmentation fault
* Mon Mar 16 2009 werner@suse.de
- Add patches from bug-bash@gnu.org to avoid eg. segmentation fault
* Thu Mar 12 2009 werner@suse.de
- Add patch from bug-bash@gnu.org to enable |& not only for
  builtins and shell functions but for all commands.
* Tue Mar 10 2009 werner@suse.de
- Switch to official patches, now we are on patch level 10
* Wed Mar  4 2009 werner@suse.de
- Use patches from bug-bash@gnu.org to make it work
* Wed Mar  4 2009 werner@suse.de
- Patch for bnc#481817 does not work in any case
* Wed Mar  4 2009 werner@suse.de
- My last patch for bnc#470548 send to bug-bash@gnu.org was not
  fully applied and this had caused a memory corruption on tab
  completion.
- Enable the parser to find closing parenthesis at the end of
  an argument of a command even if backslash is used (bnc#481817)
- Correct link of shared libraries of devel readline package
* Fri Feb 27 2009 werner@suse.de
- Update bash 4.0 to patch level 0
- Update readline 6.0 to patch level 0
* Wed Feb 18 2009 werner@suse.de
- Add readline patch 13
* Fri Jan 30 2009 werner@suse.de
- Restore state if shell function for completion is interrupted (bnc#470548)
* Tue Jan 13 2009 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Fri Dec 19 2008 werner@suse.de
- Enable large file support (bnc#460560)
* Tue Dec  9 2008 schwab@suse.de
- Add bash patches 40-48.
* Tue Nov 25 2008 werner@suse.de
- Parse the return value of setlocale(LC_ALL) (bnc#447846)
* Thu Oct 16 2008 werner@suse.de
- Let's avoid not needed library dependencies (bnc#439051)
* Mon Sep  1 2008 prusnak@suse.cz
- bash should suggest command-not-found, not scout
* Thu Jul 24 2008 werner@suse.de
- Add command-not-found.patch for scout support (fate#303730)
* Tue Jun 17 2008 werner@suse.de
- Avoid underline the full paragraph in the man page (bnc#400767)
* Sat May 17 2008 coolo@suse.de
- fix rename of xxbit packages
* Tue May  6 2008 schwab@suse.de
- Add bash patches 34-39.
* Mon Apr 28 2008 matz@suse.de
- Fix last patch.
* Thu Apr 24 2008 werner@suse.de
- Add workaround for bnc#382214
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Wed Apr  2 2008 werner@suse.de
- Allow to (re)send signals within trap handlers (bnc#345441)
- Clear exit status if not sourcing system profile (bnc#372061)
* Thu Feb 28 2008 dmueller@suse.de
- remove invalid filerequires, the libreadline5 dependency is enough
* Mon Jan 28 2008 schwab@suse.de
- Add bash patches 26-33.
* Tue Jan  8 2008 werner@suse.de
- Restart the signal handler for SIGCHLD if not already done
  within the signal handler its self (may help for bug #345441)
* Mon Jan  7 2008 schwab@suse.de
- Fix memory leak in read builtin.
* Fri Dec  7 2007 werner@suse.de
- Add skel files .bashrc, bash_history, and .profile from aaa_skel
* Tue Dec  4 2007 werner@suse.de
- Extend fix for off-by-one error in libreadline (bug #274120)
- Enable ssh detection in the bash (bug #345570)
* Thu Sep 20 2007 werner@suse.de
- Remove error triggering path requirement (bug #326751)
* Sun Aug 26 2007 schwab@suse.de
- Add bash patches 18-25.
* Sat Aug 11 2007 schwab@suse.de
- Add bash patches 10-17.
* Fri Aug  3 2007 dmueller@suse.de
- fix devel requires
* Fri Aug  3 2007 schwab@suse.de
- Fix dependencies.
* Tue Jul 31 2007 werner@suse.de
- Branch off bash-doc and readline-doc (bug #260209)
- Rename readline to libreadline5 (bug #260209)
* Thu Apr 19 2007 schwab@suse.de
- Fix bug in readline redisplay.
* Thu Mar 29 2007 dmueller@suse.de
- add ncurses-devel requires to readline-devel
* Mon Mar 26 2007 rguenther@suse.de
- Add bison and ncurses-devel BuildRequires.
* Tue Mar  6 2007 rguenther@suse.de
- Fix order of changelog entries.  Remove duplicate entry.
* Wed Feb 28 2007 werner@suse.de
- Don't access buffer but resulting pointer for array element names
  to avoid the not initialized area of the buffer.  This also fixes
  an inherent wrong calculation of the string length of the array
  element names (bug #248717)
* Thu Dec 14 2006 werner@suse.de
- Update to bash 3.2 patch level 9
* Wed Dec  6 2006 schwab@suse.de
- Remove obsolete patches.
* Fri Nov 17 2006 werner@suse.de
- Remove /usr/bin/bash (#206000)
* Tue Nov 14 2006 werner@suse.de
- Update to bash 3.2 patch level 5
* Wed Sep 27 2006 werner@suse.de
- Use PIE to make a shared bash binary
- Make the bash modules build for testing
* Fri Sep 22 2006 werner@suse.de
- Remove rpath option for libraries use linker defaults instead
* Fri Sep 22 2006 werner@suse.de
- Add symbolic link for POSIX bourne shell to /usr/bin/ (#206000)
* Thu Sep 14 2006 werner@suse.de
- Add environment variable DEFAULT_BELL_STYLE to control the
  bell style of the readline library without using intputrc.
* Mon Aug  7 2006 werner@suse.de
- Let readline-devel requires libncurses.so (bug #188673)
* Thu Jul 27 2006 werner@suse.de
- Let printf builtin handle stdout errors correctly (bug #190349)
* Wed May 31 2006 werner@suse.de
- Fix crash in IFS multi byte handling (bug #180317)
* Tue May 23 2006 werner@suse.de
- Make the test suite run even on ppc emulated on ppc64
* Mon May 15 2006 werner@suse.de
- Update bash 3.1 to patch level 17
  * Allow array subscripts to be sourounded by double quotes
- Run test suite with nearly all scripts
* Mon Apr  3 2006 werner@suse.de
- Update bash 3.1 to patch level 16
  * Bash will dump core when attempting to perform globbing in
    directories with very large numbers of files
  * Solve problem with the extended globbing code prevented dots
    from matching filenames when used in some matching patterns
* Mon Mar 27 2006 werner@suse.de
- Use access(2) with temporary switched euid/ruid and egid/rgid
  instead of stat(2) to determine the access permissions of a
  file, this works even on RO mounted NFS file systems (#160513)
* Wed Mar 22 2006 werner@suse.de
- Be sure that ~/.inputrc is read even if INPUTRC is set to
  system wide /etc/inputrc (bug #160003)
- Make prefix-meta work even with new readline syntax but
  disable it by default (since bug #suse21096)
* Mon Mar 20 2006 werner@suse.de
- Update to bash 3.1 to patch level 14 and readline 5.1 to level 4
  * Do not terminate words prematurely if parentheses are involved
  * Readline sometimes reference freed memory
  * Fix double displayed prompt when using non-incremental searches
* Sun Mar 12 2006 schwab@suse.de
- Update bash31-010 patch, better fix for #151000.
* Thu Mar  2 2006 werner@suse.de
- Update bash 3.1 to patch level 11 and readline 5.1 to level 2
  * Includes fix for line-wrapping errors
  * Replacement for bug fix of bug #146075 with better
    reallocation and compaction of the job array list.
  * Do not let SIGINT from terminal reach background processes
  * Do not let asynchronous background jobs set the terminal
    process group incorrectly.
  * Replacement for bug fix of bug #151000
  * Do not strip quoting inside double-quoted command substitutions
* Wed Mar  1 2006 werner@suse.de
- Re-enable escaping newline within quotes in commands (#151000)
* Mon Jan 30 2006 werner@suse.de
- Do initialize the fresh members of the job array (bug #146075)
* Mon Jan 30 2006 schwab@suse.de
- Barf if /proc is missing.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 10 2006 werner@suse.de
- Update to newest patch level 5:
  + corrects several omissions in the bash documentation
  + local array variable declared at function scope shadowing
    a global variable should create a separate instance
  + When tilde expansion fails, do not skip rest of an expansion
- Expand dollar quotes even for the single quote case (bug #141394)
* Thu Dec 22 2005 werner@suse.de
- Switch to first patchlevel for the bash and the readline library.
  This should fix problems happen with local/eval/let builtins.
* Mon Dec 19 2005 werner@suse.de
- Remove dangling sym links
* Tue Dec 13 2005 schwab@suse.de
- Fix segfault in readline callback interface.
* Mon Dec 12 2005 schwab@suse.de
- Fix return of random data.
- Set CFLAGS_FOR_BUILD.
* Fri Dec  9 2005 werner@suse.de
- Update to bash version 3.1 and readline library version 5.1
* Thu Sep 29 2005 werner@suse.de
- More cookie for the compiler
* Mon Sep 19 2005 werner@suse.de
- Give the compiler its cookie
* Tue Apr 19 2005 postadal@suse.cz
- fixed crashing on read -e command and line wrapping (in readline code)
  (bug #76709)
* Fri Jan 28 2005 werner@suse.de
- Add workaround for NFS bug which does not check permissions
  on open of a file but close (bug #20244)
* Thu Nov 25 2004 werner@suse.de
- Remove local array patch because not needed anymore
- Fix a crash on internal arrays if unset during execution of
  functions and files (bug #48511)
* Sun Nov 21 2004 schwab@suse.de
- Add patches from <ftp://ftp.cwru.edu/pub/bash/bash-3.0-patches/> and
  <ftp://ftp.cwru.edu/pub/bash/readline-5.0-patches/>.
* Fri Nov 19 2004 werner@suse.de
- Fix the evalexp fix (bug #48253)
* Mon Oct 25 2004 werner@suse.de
- Be sure that the FN macro nroff macro is available in all
  sub manual pages (bug #47560)
* Tue Oct 12 2004 werner@suse.de
- Re-activate first part of prompt fix because it does not harm
  (bug #36919)
* Tue Oct 12 2004 ro@suse.de
- no macros in Version lines
* Mon Oct 11 2004 werner@suse.de
- Disable prompt patch for now because not needed and other
  problmes caused by this fix (bug #36919)
- Clear out last_made_pid on success (bug #42232)
* Thu Sep 30 2004 werner@suse.de
- Clear out prompt line of isearch for invisible chars (bug #36919)
* Wed Sep 29 2004 werner@suse.de
- Fix prompt problem with invisible characters (bug #36919)
* Fri Sep 17 2004 werner@suse.de
- Fix line wraping for newlines in prompt (bug #45519)
* Wed Sep 15 2004 schwab@suse.de
- Fix missing return value.
* Sat Sep 11 2004 kukuk@suse.de
- Disable use of WCONTINUED as long as bash does not check if
  it is supported.
* Mon Sep  6 2004 werner@suse.de
- Fix prefix strip for last added patch
* Fri Sep  3 2004 werner@suse.de
- Add warning about broken glibc locale before we get the SIGSEGV
  (bug #44658)
* Sun Aug  1 2004 schwab@suse.de
- Fix rl_maybe_save_line.
- Track LC_TIME.
* Fri Jul 30 2004 werner@suse.de
- Put version to bash 3.0 and readline 5.0
* Mon Jun  7 2004 werner@suse.de
- Add missed declaration of oldval for previous bugfix
* Fri Jun  4 2004 werner@suse.de
- Fix local array variable handling (bug #41649)
* Wed Jun  2 2004 werner@suse.de
- Fix evaluation none local return stack curruption (bug #41488)
* Wed Apr  7 2004 werner@suse.de
- In case of quotes position counter has to be advanced (#38599)
* Thu Apr  1 2004 werner@suse.de
- Add directoy check to distinguish none unique and unique
  executables  (bug #37329)
* Mon Mar 29 2004 werner@suse.de
- Make the directory patch working as it should (bug #37329)
* Thu Mar 25 2004 werner@suse.de
- Move forward to official bug fixes to catch UTF-8 bug #31451
  and bug #36919
* Thu Feb 12 2004 werner@suse.de
- Fix cut&paste error of fix for bug #34427
* Wed Feb 11 2004 werner@suse.de
- Fix SIGSEGV in using UTF-8 and pattern matching (bug #34427)
- Fix LC_NUMERIC handling of builtin printf (bug #34428)
* Mon Feb  2 2004 werner@suse.de
- Fix the fix and also bug #34242
* Thu Jan 29 2004 werner@suse.de
- Fix performance problem for pattern matching in UTF-8 locale
  (port back patch from Mitsuru Chinen <mchinen@yamato.ibm.com>)
* Tue Jan 13 2004 kukuk@suse.de
- Fix last changes
* Sat Jan 10 2004 adrian@suse.de
- add %%run_ldconfig
* Mon Jul 28 2003 werner@suse.de
- Add /etc/bash_completion.d directory
* Thu Jun 26 2003 kukuk@suse.de
- Fix specfile for lib64
* Wed Jun  4 2003 jh@suse.de
- Enable profile feedback
* Fri May 23 2003 ro@suse.de
- remove unpackaged files
* Thu May 22 2003 mfabian@suse.de
- improvement for bash-2.05b-locale.patch and
  bash-2.05b-readline-init.patch: this fixes the problem that
  the line editor in bash is not correctly initialized in the first
  bash after login via ssh or on the linux console. This is
  especially obvious in UTF-8 locales when editing non-ASCII
  characters on the command line. See also:
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=74701
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=74925
  The following bug remains fixed:
  http://bugzilla.suse.de/show_bug.cgi?id=16999
- bash-2.05b-complete.patch: (by Miloslav Trmac <mitr@volny.cz>)
  achieve correct alignment of file names containing non-ASCII
  characters when typing "ls " and pressing Tab twice to show
  the completions. See also:
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=90201
* Mon Mar 17 2003 werner@suse.de
- Do not execute command line if tty is closed (bug #25445)
* Thu Feb 13 2003 schwab@suse.de
- Fix prompt decoding with -noediting.
* Tue Feb 11 2003 kukuk@suse.de
- To avoid loop in PreRequires, don't install info pages. The info
  package contains a dir file which contains the bash entries
  already.
* Fri Feb  7 2003 ro@suse.de
- fixed specfile
* Fri Feb  7 2003 ro@suse.de
- added install_info macros
* Mon Jan 27 2003 schwab@suse.de
- Fix bugs #21096 and #21392 properly: don't recurse on
  do-lowercase-version for fallback entry.
* Tue Jan 21 2003 werner@suse.de
- Allow rbash as login shell (`-' problem, bug #22917)
* Wed Dec 18 2002 schwab@suse.de
- Use BuildRoot.
* Thu Dec 12 2002 mfabian@suse.de
- add bash-2.05b-display-mbspeed.patch received from
  Jiro SEKIBA <jir@yamato.ibm.com> to improve display speed in
  multibyte locales.
* Sat Nov  9 2002 ro@suse.de
- add bison to neededforbuild for now
  (till we're sure about bison again)
* Thu Oct 31 2002 werner@suse.de
- For bug #21096 and #21392: implement an oom protection.
* Mon Oct 21 2002 werner@suse.de
- More for bug#21096: Make prefix-meta work even if mapped onto
  longer escape sequences.
* Fri Oct 18 2002 werner@suse.de
- Fix bug#21096: sequences like `ESC ... CHARACTER' with CHARACTER
  mapped on functions will not cause an endless recursion anymore.
* Wed Sep 25 2002 ro@suse.de
- removed more bogus provides
* Wed Sep 11 2002 werner@suse.de
- Correct Provides (package should not provides its self)
* Fri Aug 30 2002 werner@suse.de
- Add version dependend require on readline (bug #18652)
* Fri Aug 30 2002 werner@suse.de
- Fix annoying display bug in wide character support (bug #18449)
* Wed Aug 28 2002 werner@suse.de
- Add comment about multi byte handling and echo builtin (#18449)
* Wed Aug 21 2002 mls@suse.de
- fix $RANDOM randomness in subshells
* Fri Aug  9 2002 kukuk@suse.de
- readline-devel should require readline
* Mon Jul 29 2002 werner@suse.de
- Expansion of `~user/<dir>' is like `/<dir>'
* Sat Jul 27 2002 kukuk@suse.de
- Remove not used tetex from neededforbuild
- Fix building of man2html (bash.html still broken)
* Fri Jul 19 2002 werner@suse.de
- Check value of LANG before LC_ALL will be unset for getting the
  _current_ default value of LC_ALL with setlocale(3) (bug #16999)
* Fri Jul 19 2002 werner@suse.de
- Fix NULL pointer handled by memset (readline:mbutil.c)
* Thu Jul 18 2002 werner@suse.de
- Update to new version bash 2.05b/readline 4.3
* Wed May 22 2002 schwab@suse.de
- Fix vi-change-char.
- Fix missing declaration.
* Wed Apr 17 2002 schwab@suse.de
- Fix last change.
* Thu Apr 11 2002 sf@suse.de
- using %%{_libdir} to put the shlibs into the correct directories
  (lib / lib64)
* Tue Mar 26 2002 werner@suse.de
- Fix possible endless loop if terminal will be disconneted during
  complete answer (bug report from bastian@kde.org, for more see
  http://bugs.kde.org/db/37/37999.html)
* Tue Mar 19 2002 ro@suse.de
- removed tetex from neededforbuild, it's not used here
* Wed Mar  6 2002 werner@suse.de
- Use improved bug fix for line wrapping problem, now line wrapping
  work for char and wide char environments
- Fix readline version number
* Wed Feb 27 2002 mfabian@suse.de
- add readline-4.2-i18n-0.3-display.patch from
  Jiro SEKIBA <jir@yamato.ibm.com> to fix a line wrapping
  problem.
* Mon Jan 21 2002 werner@suse.de
- Fix bug #12834: Update to bash-2.05-i18n-0.5.patch.gz and
  bash-2.05-readline-i18n-0.3.patch.gz
* Thu Oct 18 2001 werner@suse.de
- Allways include /etc/inputrc if INPUTRC isn't system file
* Mon Oct  8 2001 werner@suse.de
- Fix readline i18n patch: enable configure of multi byte handling,
  fix warnings and bug in histexpand.c
* Fri Oct  5 2001 werner@suse.de
- Add two patches for I18N support of bash and readline library
* Tue Sep  4 2001 werner@suse.de
- Add patch to avoid trouble with C++ header definitions
* Fri Aug  3 2001 werner@suse.de
- Fix fc crash (bug #9620)
* Mon Jul  2 2001 olh@suse.de
- dont apply bash-2.05-s390x-unwind.patch on ppc and sparc
* Wed Jun 13 2001 bk@suse.de
- fix 64-bit bigendian bug for s390x
* Wed Jun  6 2001 werner@suse.de
- Re-order configure.in to avoid trouble with new autoconf
* Tue May  8 2001 mfabian@suse.de
- bzip2 sources
* Sat May  5 2001 schwab@suse.de
- Fix process substitution when stdin is closed.
* Wed May  2 2001 werner@suse.de
- Make patch for 2.4.4 work within spec
* Wed May  2 2001 werner@suse.de
- Remove buggy patch in job control, add a workaround
* Mon Apr 30 2001 werner@suse.de
- Add patch to get job control into right order on a pipe
* Thu Apr 12 2001 werner@suse.de
- Provide cpp macro OLD_READLINE for backwards compatibility
  at compile time with old readline interface
* Wed Apr 11 2001 ro@suse.de
- added split-alias as provides (again)
* Wed Apr 11 2001 werner@suse.de
- Update to bash 2.05 and readline 4.2
- Port of our patches
* Thu Feb 22 2001 werner@suse.de
- Split package into bash/readline/readline-devel
- Depend libreadline on libncurses
* Thu Sep 14 2000 werner@suse.de
- Add some bug fixes
- Add missed ssh fix for none interactive shell
* Wed Jun  7 2000 werner@suse.de
- Fix some patches
- Add export patch for bash 2.04
- Fix `soname' of readline and history libraries
- Fix linkage of major readline and history libraries
* Mon Jun  5 2000 schwab@suse.de
- Fix unwind_protect_pointer on 64-bit systems.
* Wed May 31 2000 schwab@suse.de
- Comment out declaration of savestring in <readline.h> that conflicts
  with other people's declaration (eg. gdb).
* Mon May 29 2000 aj@suse.de
- Upgrade to bash 2.04 and readline 4.1.
* Sun May 21 2000 kukuk@suse.de
- Use docdir
* Sat Apr  1 2000 bk@suse.de
- remove obviosly unneeded link /usr/lib/libreadline.so on s390
* Tue Mar 14 2000 werner@suse.de
- Add locale patch to enable LC_NUMERIC handling
* Thu Feb 24 2000 werner@suse.de
- Use $VENDOR for several linux architectures
- Set check_window_size (shopt checkwinsize) to true, this will
  correct screen size even if it changes during a job.
* Tue Feb 15 2000 schwab@suse.de
- Update config.{guess,sub} to latest version.
- Fix spec file to create doc directory before installing into it.
* Fri Jan 28 2000 werner@suse.de
- Add mailstat patch (handles mail directories)
- Fix configuration (system is %%arch-suse-linux)
- Fix segfault (job handling)
- Fix manual (add rbash manual, add some missed options)
- Install rbash (symlink to bash)
- Fix readline (End, Del)
- Fix temporary file handling (do not write without check)
- Use system random interface not builtin
- Remove some compiler warnings
- Set --enable-disabled-builtins (useful)
- Install shared readline and history in /lib (bash needs that)
- Enable shared readline (version 4.0) and history library
- Try to use shared readline and history for bash (TEST)
* Fri Dec  3 1999 kasal@suse.de
- added command to make and install doc/bashref.html
* Fri Nov 26 1999 kukuk@suse.de
- Fix spec file
* Thu Nov 25 1999 kukuk@suse.de
- Merge Makefile.Linux with spec file, use RPM_OPT_FLAGS
- Remove --disable-dparen-arithmetic
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Tue Aug 24 1999 uli@suse.de
- fixed for PPC
* Mon Jul 19 1999 florian@suse.de
- update to bash 2.03, readline 4.0
* Wed Jan 13 1999 @suse.de
- disabled `Broken pipe' messages
* Sun Dec 13 1998 bs@suse.de
- removed notify message - bash 2.0 is standard for a long time now.
* Mon Dec  7 1998 florian@suse.de
- remove SSH_CLIENT-kludge as this cannot detect all correct cases
  where .bashrc should be loaded
- delete email-changes in bashbug script
- update readline to version 2.2.1
* Thu Nov 12 1998 bs@suse.de
- minor fix for new rpm
* Thu Oct  1 1998 ro@suse.de
- update to 2.02.1 / reintegrated werner's tmp-fix for bashbug
* Thu Jul 23 1998 werner@suse.de
- use mktemp
* Thu Jul 16 1998 werner@suse.de
- fix bashbug temp file handling
* Wed Jun 17 1998 ro@suse.de
- changed general.h: !defined (gid_t)
* Mon Oct 27 1997 florian@suse.de
- do not include old compatible-only safestring() in libreadline.a
* Thu Oct  9 1997 florian@suse.de
- update to version 2.01.1
- add several bugfixes
- fix missing things in spec-file
* Thu Aug 14 1997 florian@suse.de
- add several bug-fixes from gnu.bash.bug and fix memory management
  of LC_ALL
* Sat Jul  5 1997 florian@suse.de
- add another bugfix from gnu.utils.bugs
* Mon Jun 23 1997 florian@suse.de
- create the history file with 0600 perms
- add minor bugfix to check for new email
* Thu Jun  5 1997 florian@suse.de
- bash: check for NULL-pointer before calling "savestring()"
- add bashref.info and newer FAQ
* Tue Apr 22 1997 bs@suse.de
- added FAQ and bashref.html to /usr/doc/packages/bash
* Sun Apr 13 1997 florian@suse.de
- update to bash 2.0 with lots of patches from gnu.utils.bugs
  Mon Sep  2 02:48:35 MET DST 1996
  new version with security patches
* Thu Jan  2 1997 florian@suse.de
  security fix included (0xff was command separator)
  This document details the changes between this version, bash-4.1-rc,
  and the previous version, bash-4.1-beta.
