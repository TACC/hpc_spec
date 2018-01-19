%define version v5.1.0

Summary   : chroot, mount --bind, and binfmt_misc without privilege/setup
Version   : %{version}
Release   : 1
License   : GPL2+
Group     : Applications/System
Source    : proot-%{version}.tar.gz
Buildroot : %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Prefix    : /usr
Name      : proot

BuildRequires: libtalloc-devel

%if 0%{?suse_version} >= 1210 || 0%{?fedora_version} >= 15
BuildRequires: glibc-static
%endif

%if !0%{?suse_version} != 0
BuildRequires: which
%endif
%include rpm-dir.inc
%description
PRoot is a user-space implementation of chroot, mount --bind,
and binfmt_misc.  This means that users don't need any privileges
or setup to do things like using an arbitrary directory as the new
root filesystem, making files accessible somewhere else in the
filesystem hierarchy, or executing programs built for another CPU
architecture transparently through QEMU user-mode.  Also, developers
can use PRoot as a generic Linux process instrumentation engine thanks
to its extension mechanism, see CARE for an example.  Technically
PRoot relies on ptrace, an unprivileged system-call available in
every Linux kernel.

%prep
%setup -n proot-%{version}

%build
make -C src

%install
make -C src install PREFIX=%{buildroot}/%{prefix}
install -D doc/proot/man.1 %{buildroot}/%{_mandir}/man1/proot.1

%check
env LD_SHOW_AUXV=1 true
cat /proc/cpuinfo
./src/proot -V
./src/proot -v 1 true
make -C tests

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{prefix}/bin/proot
%doc %{_mandir}/man1/proot.1*
%doc COPYING
%doc doc/*

%changelog
* Tue Jan 27 2015 Cédric VINCENT <cedric.vincent@st.com>
Release v5.1.0
==============

New features
------------

+ Processes under PRoot now appear with their real names, that is,
  they are not renamed "ld-linux.so" or "prooted-..." anymore:

  before:

      $ proot-v4.0.3 ps
        PID TTY          TIME CMD
       7885 pts/11   00:00:00 bash
       8131 pts/11   00:00:00 proot-v4.0.3
       8132 pts/11   00:00:00 ld-2.17.so

      $ proot-v5.0.0 ps
        PID TTY          TIME CMD
       7885 pts/11   00:00:00 bash
       7916 pts/11   00:00:00 proot-v5.0.0
       7917 pts/11   00:00:00 prooted-7916-Jb

  now:

      $ proot-v5.1.0 ps
        PID TTY          TIME CMD
       7885 pts/11   00:00:00 bash
       8585 pts/11   00:00:00 proot-v5.1.0
       8586 pts/11   00:00:00 ps

Fixes
-----

+ It is now possible to use GDB against multi-threaded programs under
  PRoot x86_64 and x86.

+ It is possible to execute x86_64 programs from x86 programs again.

+ It is possible to use x86 ptrace-based programs (strace, gdb, ...)
  under PRoot x86_64 again.

+ The loader is now built with the "build-id" linker option explicitly
  disabled.  This special section might interfere with loaded
  programs.

+ The loader can now load relocatable objects that have a predefined
  base address.

Acknowledgements
----------------

Thanks to Erwan Gouriou, Sébastien Gandon, Christian milkylainen,
Henrik Wallin, and Frank Teo for their bug reports and tests.

Thanks to Jérôme Audu, Yann Droneaud, and Christophe Monat for their
precious help.


Release v5.0.0
==============

Highlight
---------

PRoot used to rely on the ELF loader embedded in the ELF interpreter
from the GNU libc.  Sadly this latter suffers from many issues:

+ programs that use constructors or destructors might crash: a typical
  example is C++ programs.

+ programs that rely on the "rpath" mechanism and that are invoked
  through a symlink might not start: a typical example is the JVM on
  Debian.

+ programs that read processes command-line migth be confused because
  initial argv[0] is replaced: typical examples are ps and top.

Moreover not all ELF interpreters provide this feature.  For instance,
ELF interpreters shipped with Bionic (Android) and some versions of
the uClibC can't be used as ELF loaders.  As a consequence it was not
possible to proot into a rootfs that uses such C library.

Now PRoot has its own loader, that means all the limitations above
doesn't exist anymore.

Fixes
-----

+ Most bugs related to shebang support -- ie. "#!" at the beginning of
  a program -- were fixed.

Command-line interface changes
------------------------------

+ PRoot now starts a login shell when no command is specified; this
  makes the shell read profile files from the guest rootfs, as
  expected by some guest programs.  To get the old behavior, launch
  "/bin/sh" explicitly:

      proot -r whatever /bin/sh

+ The -R option now binds "/run" and "/var/run/dbus/system_bus_socket"
  too.  This is useful for guest programs that need to communicate
  with host services.


Release v4.0.3
==============

+ Heap emulation is disabled when a "suspicious" call to brk(2) is
  actually legit, as it might be the case when launching the very
  first program.

+ The "-0" and "-S" options ("root" identity emulation) now fake
  success of mknodat(2), as it was the case for mknod(2) previously.
  This missing feature was revealed by the AArch64 port.

+ The "-k" option (kernel compatibility emulation) now works on
  Linux/AArch64.

Thanks to Rémi Duraffort for the bug reports and for his LAVA testing
platform!


Release v4.0.2
==============

+ Fix how the very first program is launched by PRoot.  Previously,
  argv[0] was not preserved when the very first program was launched
  through a symbolic link.  This old behavior used to bug programs
  like Busybox and python-exec.  Thanks to "hhm", Ivailo "fluxer"
  Monev, and Joakim Tjernlund for the bug reports.

+ Fix renameat(2) sysexit support.  There was a bug in PRoot that was
  exposed by the Aarch64 (a.k.a arm64) port only but that might affect
  other architectures.

+ Fix build for AArch64.  Thanks to Rémi Duraffort for the patches and
  for the Debian/arm64 testing platform.

+ Fix support for "long" socket paths.  These can only be 108 bytes
  long; this limit might be easily reached with PRoot since the path
  to the rootfs is always prepended.  The solution was to
  automatically bind this long path to a shorter path.  This bug was
  exposed by LibreOffice and Yocto's pseudo.  Thanks to Christophe
  Guillon for the bug report.


Release v4.0.1
==============

+ Fix a couple of portability issues in the testsuite.  Thanks to Rémi
  Duraffort for all the tests he made on his instance of Linaro LAVA.

+ Set $PWD to the value specified by the -w option, otherwise Bash pwd
  builtin might be confused under some specific circumstances.  Thanks
  to Jérémy Bobbio for the bug report.

+ Fix support for accessat and fchmodat syscalls: they have only three
  parameters, not four.  This bug was exposed by Gentoo's sandbox:

      proot -S gentoo-amd64-hardened+nomultilib-rootfs emerge util-linux


Release v4.0.0
==============

Highlights
----------

+ It is now possible to use GDB, Strace, or any other program based on
  "ptrace" under PRoot.  This was not the case previously because it
  is not possible to stack ptracers on Linux, so an emulation layer
  was developed in order to bypass this limitation.  This has required
  a lot of changes in PRoot, hence the major number version bumping.
  It was mostly tested on x86_64, and partially tested on x86 and ARM.
  This ptrace emulation support is still experimental, and there are a
  couple of known issues, but feel free to report unexpected behaviors
  if you need a fix.

+ A new command-line option is available: "-S".  It is similar to the
  "-R" option expect it enables the "-0" option and binds only a
  minimal set of paths that are known to not be updated by package
  installations, to avoid unexpected changes on host files.  This
  option is useful to safely create and install packages into the
  guest rootfs.  For example:

      $ proot -S ubuntu-14.04-rootfs/ apt-get install samba

  or:

      $ proot -S ubuntu-14.04-rootfs/
      # apt-get install samba

  If "-0 -R" is used instead of "-S", the same command fails since it
  tries to update "/etc/group", which is bound to the host system and
  is not writable (assuming PRoot is ran without privileges):

      $ proot -0 -R ubuntu-14.04-rootfs/
      # apt-get install samba
      [...]
      Adding group `sambashare' (GID 105) ...
      Permission denied

+ The fake_id0 extension can now fake any user and group identifiers.
  That means, when "-0" is specified, PRoot-ed processes can change
  their real, effective and saved identifiers, with respect to the
  rules described in setuid, setfsuid, setreuid, setresuid, and
  setfsuid manuals.  Also, the new command-line option "-i" was added
  to change explicitly the identifiers to the specified values.  This
  option will be used by CARE to re-execute with the same initial
  identifiers, but it could also be useful to threaten your teammates
  ;).  Note that the "-0" option is actually the same as "-i 0:0".

+ The old command-line interface is not supported anymore.  That means
  it is now impossible to specify the path to the guest rootfs without
  using -r or -R.  Also, -Q and -B options are definitively gone,
  instead the -R option must be specified, respectively with and
  without -q.  See PRoot v3.1 release notes for details.

Fixes
-----

+ getcwd(2) and chdir(2) now return the correct error code when,
  respectively, the current directory does not exist anymore and the
  target directory doesn't have the "search" permission.

+ Named file descriptors (ie. links in /proc/<pid>/fd/*) are not
  dereferenced anymore since they may point to special objects like
  pipes, sockets, inodes, ...  Such objects do not exist on the
  file-system name-space, so dereferencing them used to cause
  unexpected errors.

+ Extensions now see every component of canonicalized paths.  An
  optimization in the canonicalization loop used to skip the first
  part of a path if it was known to be already canonicalized, sadly
  this short-cut may confuse some extensions, like -0.

+ Temporary files and directories created by PRoot for its own purpose
  are now automatically deleted when PRoot exits.


Miscellaneous
-------------

+ PRoot does not rely on GCC C extensions anymore, like nested
  functions.  That means its stack does not have to be executable
  (this is required for hardened Linux systems), and it can now be
  compiled with Clang.

+ The ASLR (Address Space Layout Randomization) is not disabled
  anymore, and the heap is now emulated on all architectures.


Internal changes
----------------

This section is dedicated to developers.

+ PRoot now remembers the parent of all tracees, it is similar to a
  traced process tree.  This was required for the ptrace emulation
  support, but this could be useful to some extensions.

+ It is now possible to restart a tracee with any ptrace restart mode:
  single-step, single-block, ...

+ Functions {peek,poke}_mem were replaced with functions
  {peek,poke}_{,u}int{8,16,32,64}.  These new functions performs type
  conversion and fetch only the necessary amount of data in target
  tracee's memory to avoid invalid accesses.

+ There is a new interface to handle ELF auxiliary vectors.  See
  ptrace emulation, kompat and fake_id0 extensions for usage examples.

+ There is a new interface to create temporary files and directories
  that are automatically deleted on exit.  See CARE extension, glue
  and auxv support for usage examples.

+ When built with GCC function instrumentation support, PRoot prints
  the currently called function on standard error stream (stderr).

Thanks
------

Thanks go to Stephen McCamant, Oren Tirosh, Jérôme Audu, and Carlos
Hernan Prada Rojas for their bug reports and tests; and to Rémi
Duraffort for his contributions.


Release v3.2.2
==============

+ Remove a useless memory layout constraint on x86_64 that bugs some
  programs like java and or qemu.

+ It is now possible to launch the initial program from a relative
  path without specifying the "./" prefix, for example:

    $ proot path/to/program

+ Don't discard fcntl(F_DUPFD_CLOEXEC) systematically when the kompat
  extension is enabled (-k option).

+ Don't use syscalls that require Linux >= 2.6.16 anymore.


Release v3.2.1
==============

+ Make ptrace/seccomp even more portable on Ubuntu.

Thanks to Maxence Dalmais for the bug report and tests.


Release v3.2
============

This release was mostly driven by the requirements of "CARE", a new
project based on PRoot that will be released publicly soon on
https://proot-me.github.io.  For information, "CARE" is the short for
"Comprehensive Archiver for Reproducible Execution".

Highlights
----------

+ Many bugs exposed by a couple of static code analyzers (Coverity,
  Clang, ...) and some test-suites (Linux Test Project, libuv, ...)
  are now fixed.

+ The "kompat" extension ("-k" option) can now emulate most of the
  kernel features that would be required by the guest system but that
  are not available on the host kernel.  For example, it can now make
  programs from Ubuntu 13.04 64-bit run on RedHat 5 64-bit without any
  further tweaks:

     rh5-64$ proot -k 3.8 -R ubuntu-13.04-64bit/ ...

+ On ARM and x86_64, the heap segment is now emulated with a regular
  memory mapping to ensure this former always exists.  This was
  required because some kernels might put a non-fixed memory mapping
  right after the regular heap when using some GNU ELF interpreters
  (ld.so) as loaders.  Without the heap segment emulation, some
  programs like Bash would crash because the heap can't grow anymore:

      bash: xmalloc: locale.c:73: cannot allocate 2 bytes (0 bytes allocated)

Miscellaneous
-------------

+ When using the "-R" option, the path to the guest rootfs is now
  bound into the guest rootfs itself.  This is required to run
  programs that search for their DSOs in /proc/self/maps, like VLC for
  instance.

+ When using the "-v" option with a level greater than 2, syscalls are
  now printed as strings instead of numbers, à la strace:

    $ proot -v 3 true
    [...]
    proot info: pid 29847: sysenter start: mmap(0x0, 0x2d141, 0x1, 0x2, 0x3, 0x0) [...]
    [...]

+ The article about the migration from ScratchBox2 is now publicly
  available:

    https://github.com/cedric-vincent/PRoot/blob/v3.2/doc/articles/howto_migrate_from_scratchbox2.txt

Internal changes
----------------

+ Tools based on PRoot (CARE, DepsTracker, ATOS, ...) can now easily
  replace the original command-line interface with their own
  command-line interface.

+ It is now possible to chain forged syscalls to a regular syscall.
  Search for "register_chained_syscall" in the sources for details.

+ A couple of new helpers are now visible from the extensions.

Thanks
------

+ Bug reports and tests: Corbin Champion, Maxence Dalmais, and Nicolas
  Cornu.

+ Static code analysis: Antoine Moynault and Christophe Guillon.

+ Patches: Rémi Duraffort.

+ Unexpected hint: Christophe Monat :)


Release v3.1
============

Command-line interface changes
------------------------------

+ The initial command is not search in "." anymore, unless the "./"
  prefix is specified or unless "." is in $PATH, as expected.

+ The "-B" and "-Q" options are obsoleted by the new "-R" option.
  This latter is equivalent to "-B -r", as there was actually no point
  at using the "-B" option without "-r".

+ A warning is now emitted when the rootfs is specified à la
  chroot(1), that is, without using "-r" or "-R".

The old command-line interface is not documented anymore, but it will
be still supported for a couple of releases.  Although, users are
strongly encouraged to switch to the new one:

        ======================   =================
        old CLI                  new CLI
        ======================   =================
        proot rootfs             proot -r rootfs
        proot -B rootfs          proot -R rootfs
        proot -B -r rootfs       proot -R rootfs
        proot -Q qemu rootfs     proot -R rootfs -q qemu
        proot -Q qemu -r rootfs  proot -R rootfs -q qemu
        =======================  =======================

Extensions
----------

+ The "kompat" extension ("-k" option) has been greatly enhanced.  For
  example, it can now make programs from Ubuntu 13.04 32-bit run on
  RedHat 5 64-bit:

     rh5-64$ proot -k 3.8 -R ubuntu-13.04-32bit/ ...

+ The "fake id0" extension ("-0" option) handles more syscalls:
  mknod(2), capset(2), setxattr(2), setresuid(2), setresgid(2),
  getresuid(2), and getresgid(2).

Miscellaneous
-------------

+ PRoot is now compiled with large file-system support (LFS), this
  make it works with 64-bit file-systems (eg. CIFS) on 32-bit
  platforms.

+ The special symbolic link "/proc/self/root" now points to the guest
  rootfs, that is, to the path specified by "-r" or "-R".  Just like
  with chroot(2), this symlink may be broken as the referenced host
  path likely does not exist in the guest rootfs.  Although, this
  symlink is typically used to know if a process is under a chroot-ed
  environment.

+ Under QEMU, LD_LIBRARY_PATH is not clobbered anymore when a guest
  program is launched by a host program.

+ When seccomp-filter is enabled, this release is about 8% faster than
  the previous one.

+ A couple of bugs reported by Scan Coverity are fixed.

Thanks
------

Special thanks to Stephan Hadamik, Jérôme Audu, and Rémi Duraffort for
their valuable help.


Release v3.0.2
==============

+ Fix the search of the initial command: when the initial command is a
  symbolic link, PRoot has to dereference it in guest namespace, not
  in the host one.

+ Return error code EACCESS instead of EISDIR when trying to execute a
  directory.  Some programs, such as "env", behave differently with
  respect to this error code.  For example:

      ### setup
      $ mkdir -p /tmp/foo/python
      $ export PATH=/tmp/foo:$PATH

      ### before (PRoot v2.3 ... v3.0.1)
      before$ proot env python
      env: python: Is a directory

      ### now (PRoot v3.0.2 ...)
      $ proot env python
      Python 2.7.5 (default, May 29 2013, 02:28:51)
      [GCC 4.8.0] on linux2
      Type "help", "copyright", "credits" or "license" for more information.
      >>>


Release v3.0.1
==============

Fix support for bindings where the guest path is explicitly not
dereferenced.  Be careful, the syntax has changed:

        before$ proot -b /bin/bash:!/bin/sh

        now$ proot -b /bin/bash:/bin/sh!


Release v3.0
============

New features
------------

+ PRoot can now use the kernel feature named "seccomp-filter", a.k.a
  "seccomp mode 2", to improve its own performance significantly.  For
  examples on my workstation, the tables below show the time overhead
  induced by PRoot compared to a native execution:

  - when generating the Perl 5.16.1 package:

    ===============  ===========  ==========
    command          seccomp off  seccomp on
    ===============  ===========  ==========
    ./configure.gnu          75%         25%
    make -j4                 70%         45%
    make -j4 check           25%          9%
    ===============  ===========  ==========

  - when generating the Coreutils 8.19 package:

    ===============  ===========  ==========
    command          seccomp off  seccomp on
    ===============  ===========  ==========
    ./configure              80%         33%
    make -j4                 75%         33%
    make -j4 check           80%          8%
    ===============  ===========  ==========

+ It is now possible to explicitly not dereference the guest location
  of a binding by specifying ``!`` as the first character.  For
  instance::

      proot -b /bin/bash:!/bin/sh

  will not overlay ``/bin/dash`` when this latter is pointed to by
  ``/bin/sh`` (it's typically the case on Ubuntu and Debian).

Fix
---

+ The initial command is not search in $PATH anymore when it starts
  with ``/`` or ``./``, and it doesn't exist.  For instance::

      $ rm test
      $ proot ./test
      proot warning: './test not found (root = /, cwd = /usr/local/cedric/git/proot)
      proot error: see `proot --help` or `man proot`.

Thanks
------

Many thanks to Will Drewry and Indan Zupancic, who made possible to
accelerate PTRACE_SYSCALL with seccomp-filter.  Also, thanks to Paul
Moore for his valuable set of seccomp tools.

Notes
-----

+ Unlike what I said, this release is not shipped with a ptrace
  emulator.  It's planned for the next one, though.

+ Seccomp-filter was first introduced in Linux 3.5 a year ago, it was
  also officially back-ported to Ubuntu 12.04 (Linux 3.2).  To know if
  PRoot is actually using this accelerator on your system, check the
  verbose output.  For instance::

    $ proot -v 1 true
    ...
    proot info: ptrace acceleration (seccomp mode 2) enabled
    ...

  But first, be sure it was built with this support::

    $ proot -V
    ...
    built-in accelerators: process_vm = yes, seccomp_filter = yes
    ...


Release v2.4.1
==============

Fixes
-----

+ Fix all warnings reported by GCC-4.8 "-Wall -Wextra" and Coverity
  Prevent 4.5.

+ Fix Unix sockets path translation for some x86_64 systems.

+ Make the "kompat" extension (-k option) work again.

+ Fix spurious "can't delete /tmp/proot-$PID-XXXXX" messages.



Release v2.4
============

New architectures
-----------------

+ PRoot now works natively on Linux ARM64 systems (a.k.a AArch64).
  Note that PRoot/AArch64 doesn't support 32-bit binaries yet.

+ PRoot/x86_64 now supports x32 binaries/rootfs.

Fixes
-----

+ Paths from Unix domain sockets are now translated.  For example, it
  wasn't possible previously to use "tmux" in the guest rootfs if
  another instance were running in the host rootfs.

+ When a host path is bound to a nonexistent guest path, PRoot tries
  to create this latter in the guest rootfs, for some technical
  reasons.  Previously, this "dummy" guest path was created with RWX
  permissions but this might cause troubles when re-using the rootfs
  for other purpose.  Now, this "dummy" guest path is created with
  minimal permissions, and it is also possible to avoid its creation
  by defining the PROOT_DONT_POLLUTE_ROOTFS environment variable.

Command-line interface changes
------------------------------

+ The directory "/run" is removed from the list of recommended
  bindings (-B option) because this creates to much conflicts with
  programs that write in the "/run/var" directory.

+ The -0 option now makes user's files appear as if they were actually
  owned by root, and it also fakes the success of any mode changes
  (chmod* syscalls).  This is typically useful to create packages
  where the files belong to the root user (it's almost always the
  case).

Internal changes
----------------

+ PRoot should be even more portable now.  For instance, there's no
  need to worry about syscallee-saved registers anymore.

Thanks
------

This release was made possible thanks to, in no special order: Yvan
Roux, Jerôme Audu, Heehooman, Yann Droneaud, and James Le Cuirot.  See
"git log" for details.


Release v2.3.1
==============

New feature
-----------

+ The "fake id0" feature was improved by Rémi Duraffort in order to
  support privileged write operations in read-only files/directories.
  Some package managers (Fedora, Debian, ...) relies on this special
  behavior::

      # ls -ld /usr/lib
      dr-xr-xr-x 22 root root 40960 Jan  2 11:19 /usr/lib/
      # install -v something.so /usr/lib/
      removed ‘/usr/lib/something.so‘
      ‘something.so‘ -> ‘/usr/lib/something.so‘

Fixes
-----

+ Fix bindings to a guest path that contains a symbolic link.  For
  example when the given guest path ``/var/run/dbus`` is a symbolic
  link to ``/run/dbus``.

+ Fix a memory corruption when accessing files in "/proc/self/"

Special thanks to Rémi Duraffort for the improved "fake id0" feature
and for the bug reports.


Release v2.3
============

This release is intended more specifically to developers and advanced
users, it was mostly driven by the requirements of an internal
STMicroelectronics project named "Auto-Tuning Optimization Service".

New features
------------

+ There's now an extension mechanism in PRoot that allows developers
  to add their own features and/or to use PRoot as a Linux process
  instrumentation engine.  The two following old features were moved
  to this new extension interface: "-k *string*" and "-0"
  (respectively: set the kernel release and compatibility level to
  *string*"; and force some syscalls to behave as if executed by
  "root").

+ It is now possible to execute PRoot under PRoot, well somewhat.
  Actually the initial instance of PRoot detects that it is being
  called again and recomputes the configuration for the new process
  tree.  This feature is still experimental and was way harder to
  implement than expected, however it was worth the effort since it
  enforced the consistency in PRoot.  Just one example among many, in
  PRoot the "chroot" feature is now really equivalent to the
  "mount/bind" one, that is, ``chroot path/to/rootfs`` is similar to
  ``mount --bind path/to/rootfs /``.

+ The "current working directory" (chdir(2), getcwd(2), ...) is now
  fully emulated by PRoot.  Sadly a minor regression was introduced:
  even if the current working directory has been removed, getcwd(2)
  returns a "correct" value.  This should be fixed in the next
  release.

Command-line interface changes
------------------------------

+ The message "proot info: started/exited" isn't printed by default
  anymore since it might introduce noise when PRoot is used inside a
  test-suite that compares outputs.  This message was initially added
  to know whether the guest program has exited immediately.

+ The "-u" and "-W" options have disappeared.  The former wasn't
  really useful and the latter was definitely useless since the
  default "current working directory" is "." since v2.1, that means
  the three examples below are equivalent ("-W" was just an alias to
  "-b . -w .")::

      proot -b . [...]
      proot -b . -w . [...]
      proot -W [...]

Fixes
-----

+ The option ``-w .`` is now really equivalent to ``-w $PWD``.

+ A bug almost impossible to describe here has been fixed, it appeared
  only when specifying relative bindings, for instance: ``-b .``.

Internal changes
----------------

+ PRoot now relies on Talloc: a hierarchical, reference counted memory
  pool system with destructors.  It is the core memory allocator used
  in Samba: http://talloc.samba.org.  This is definitely a worthwhile
  dependency for the sake of development scalability and
  debuggability.  For example, PRoot now has an explicit garbage
  collector (c.f. ``tracee->ctx``), and the full dynamic memory
  hierarchy can be printed by sending the USR1 signal to PRoot::

      native-shell$ proot --mount=$HOME --mount=/proc --rootfs=./slackware-14/
      prooted-shell$ kill -s USR1 $(grep Tracer /proc/self/status | cut -f 2)

      Tracee           0x6150c0  768 bytes  0 ref'    (pid = 22495)
          talloc_new: ./tracee/tracee.c:97 0x615420  0 bytes  0 ref'
          $exe             0x61bef0  10 bytes  0 ref'     ("/bin/bash")
          @cmdline         0x61bf60  16 bytes  0 ref'     ("/bin/sh", )
              /bin/sh          0x61bfd0  8 bytes  0 ref'
          $glue            0x61bae0  24 bytes  0 ref'     ("/tmp/proot-22494-UfGAPh")
          FileSystemNameSpace 0x615480  32 bytes  0 ref'
              $cwd             0x61b880  13 bytes  0 ref'     ("/home/cedric")
              Bindings         0x61b970  16 bytes  0 ref'     (host)
                  Binding          0x615570  8280 bytes  1 ref'   (/home/cedric:/home/cedric)
                  Binding          0x6176a0  8280 bytes  1 ref'   (/proc:/proc)
                  Binding          0x6197d0  8280 bytes  1 ref'   (/usr/local/proot/slackware-14:/)
              Bindings         0x61b900  16 bytes  0 ref'     (guest)
                  Binding          -> 0x6176a0
                  Binding          -> 0x615570
                  Binding          -> 0x6197d0


Release v2.2
============

+ This release brings some critical fixes so an upgrade is highly
  recommended, especially on x86_64 and Ubuntu.

+ PRoot is now a lot faster: the speed-up can be up to 50% depending
  on the kind of application.

+ PRoot can now mount/bind files anywhere in the guest rootfs, even if
  the mount point has no parent directory (and/or can't be created).
  With previous versions of PRoot, that would created kinda black hole
  in the filesystem hierarchy that might bug some programs like "cpio"
  or "rpm".

  For example, with the previous version of PRoot::

       $ proot -b /etc/motd:/black/holes/and/revelations
       proot warning: can't create the guest path (binding) ...
       proot info: started

       $ find /black
       find: `/black: No such file or directory

       $ cat /black/holes/and/revelations
       Time has come to make things right -- Matthew Bellamy

  And now::

       $ proot -b /etc/motd:/black/holes/and/revelations
       proot info: started

       $ find /black
       /black
       /black/holes
       /black/holes/and
       /black/holes/and/revelations

       $ cat /black/holes/and/revelations
       Time has come to make things right -- Matthew Bellamy

+ "/run" was added to the list of recommended bindings (-B/-Q).

+ SH4 and ARM architectures are now officially supported.

Thanks
------

Huge thanks to Rémi DURAFFORT for all the tests, bug reports, fixes,
and for hosting http://proot.me.

Thanks to Thomas P. HIGDON for the advanced investigation on a really
tricky bug (red zone corruption).


Release v2.1
============

New features
------------

+ PRoot can now emulate some of the syscalls that are available in the
  kernel release specified by -k but that are missing in the host
  kernel.  This allows the execution of guest programs expecting a
  kernel newer than the actual one, if you encountered the famous
  "FATAL: kernel too old" or "qemu: Unsupported syscall" messages.

+ The current working directory isn't changed anymore if it is still
  accessible in the guest environment (binding).

Fixes
-----

+ Added support for architectures with no misalignment support (SH4).

+ Fix support for: link(2), linkat(2), symlink(2), and symlinkat(2).


Release v2.0.1
==============

+ Fix a compatibility issue with QEMU v1.1

+ Fix the initialization of bindings that point to "/proc/self".

These problems were reported by Alkino:

    https://github.com/cedric-vincent/PRoot/issues/3


Release v2.0
============

New features
------------

+ There's now a specific support to handle special symlinks in /proc.
  As of now, only the following ones are correctly handled:

      * /proc/self, it was already supported previously but now this
        is done consistently (i.e. not a hack);

      * /proc/<PID>/exe, for any <PID> monitored by PRoot; and

      * /proc/<PID>/fd/<FD>.

+ The list of supported syscalls was updated, as of Linux 3.4.1.

Command-line interface changes
------------------------------

+ The path to the guest rootfs can now be specified by the new
  -r/--rootfs option.  This permits the use of shell aliases, for
  example:

      $ alias armedslack='proot -Q qemu-arm -r /path/to/armedslack'
      $ armedslack -v 1 -b ~/arm_cpuinfo:/proc/cpuinfo

  That wasn't possible previously because the path to the guest rootfs
  had to be the last option.

+ The -v/--verbose option now takes a parameter, and a negative
  integer makes PRoot quiet except on fatal errors.

+ The -h/--help option now prints a detailed message.

+ The -V/--version and -h/--help options now exit with success.

Fix
---

+ Return correct errno if a non-final path component isn't a directory
  nor a symlink.

+ Fix the insertion of an item in the list of host/guest bindings.


Internal changes
----------------

This section is dedicated to PRoot developers.

+ File-system information is now inherited from a traced process to
  its children.  This permits the emulation of symlinks in /proc/self:
  cmdline, exe, cwd, root, ...

+ The execution of QEMU is now fully confined to the virtual rootfs
  namespace: it now relies on the "mixed-execution" feature, just like
  a regular host program.


Release v1.9
============

Fixes
-----

+ Be as transparent as possible with respect to SIGSTOP and SIGTRAP
  signals.  For instance, the Open POSIX Test Suite now reports the
  same level of success whether it is run under PRoot or not (it
  depends on the kernel version though).

+ Ignore terminating signals and kill all tracees on abnormal
  termination signals (^\, segmentation fault, divide by zero, ...).
  This ensures no tracee will stay alive without being monitored
  anymore.

+ Force utsname.machine to "i686" -- instead of "i386" -- for 32-bit
  programs running on x86_64 systems.  This improves the compatibility
  with package managers that deduce the current architecture from
  `uname -m`.

+ Fix x86_64 support for linkat() and fchownat().

+ Fix mixed-execution support, LD_LIBRARY_PATH was defined twice for
  host programs.


Release v1.8.4
==============

New feature
-----------

+ The -0 option now fakes success on ``chroot("/")``.  This feature is
  required by some guest package managers, like ``pacman`` -- the Arch
  Linux Package Manager.

Fix
---

+ Nested bindings are now correctly supported.  For example with these
  bindings -- nested from the host point-of-view::

      host$ proot -b /:/host-rootfs -b /tmp ...
      guest$ ln -s /tmp/bar /tmp/foo
      # ... points to "/tmp/bar" instead of "/host-rootfs/tmp/bar"

  and with these bindings -- nested from the guest point-of-view::

      host$ proot -b /bin -b /usr/bin/find:/bin/find ...
      guest$ /bin/find
      # ... works instead of "no such file or directory"

Internal changes
----------------

This section is dedicated to PRoot developers.

+ Functions to compare two pathes (equal, prefix, not comparable, ...)
  are now available, at last.

+ The "ignore ELF interpreter" option can be (dis|en)able with the
  ``PROOT_IGNORE_ELF_INTERPRETER`` environment variable and/or with
  the ``config.ignore_elf_interpreter`` internal variable.


Release v1.8.3
==============

New features
------------

+ The -0 option now fakes success on ownership changes.  This improves
  the compatibility with package managers that abort if ``chown(2)``
  fails.  Note that this is quite limited compared to ``fakeroot``.

+ Force utsname.machine to "i386" for 32-bit programs running on
  x86_64 systems.  This improves the compatibility with package
  managers that deduce the current architecture from `uname -m`.

Fixes
-----

+ Fix a regression regarding the concatenation of the ``..`` with a
  path ending with ``.``.  For intance you can now do ``ls foo`` where
  ``foo`` is a symbolic link to ``/bar/.``.

+ Don't return an error if the specified size for ``getcwd(2)`` and
  ``readlink(2)`` is greater than PATH_MAX.  Technically the result
  may likely be shorter than this limit.


Release v1.8.2
==============

+ This is the first public release of PRoot, it's time to increase its
  maturity artificially ...  Actually it's an homage to Blink 182 ;)

+ User manual finally published.

+ PRoot can now *mix* the execution of host programs and the execution
  of guest programs emulated by QEMU.  This is useful to use programs
  that aren't available initially in the guest environment and to
  speed up build-time by using cross-compilation tools or any CPU
  independent program, like interpreters.

+ Absolute symlinks from bound directories that point to any bound
  directory are kept consistent: for example, given the host symlink
  ``/bin/sh -> /bin/bash``, and given the command-line option ``-b
  /bin:/foo``, the symlink will appeared as ``/foo/sh -> /foo/bash``.

+ Three command-line options are gone:

  * ``-p`` (don't block the ptrace syscall) wasn't really useful.

  * ``-e`` (don't use the ELF interpreter) isn't required anymore.

  * ``-a`` (disable the ASLR mechanism) is now the default.

+ Don't complain anymore when parent directories of a *recommended
  binding* (as enabled by ``-B``, ``-M`` and ``-Q`` options) can't be
  created.

+ Support job control under ptrace as introduced in Linux 3.0+.

+ ``LD_`` environment variables are now passed to the QEMUlated
  program, not to QEMU itself.  It means ``ldd`` works (there's a bug
  in QEMU/ARM though).

+ Many fixes and improved compatibility thanks to the Open Build
  Service instantiated at http://build.opensuse.com

+ Note: v0.7.1 was an experimental release.


Release v0.7.0
==============

+ Search the guest program in $PATH relatively to the guest rootfs,
  for instance you can now just write::

      proot /path/to/guest/rootfs/  perl

  instead of::

      proot /path/to/guest/rootfs/  /usr/bin/perl

+ The command-line interface was re-written from scratch, the only
  incompatible change is that QEMU options are now separated by
  spaces::

     proot -Q "qemu-arm -g 1234" ...

  instead of::

     proot -Q qemu-arm,-g,1234 ...

+ New option "-0": force syscalls "get*id" to report identity 0, aka
  "root".

+ Many fixes, code refactoring, new testing framework, ...

Special thanks to Claire ROBINE for her contribution.


Release v0.6.2
==============

+ Change the default command from $SHELL to "/bin/sh".  The previous
  behaviour led to an unexpected error -- from user's point-of-view --
  when $SHELL didn't exit in the new root file-system.

+ Fix *partially* support for readlink(2) when mirror pathes are in
  use.  Prior this patch, any symbolic link -- that points to an
  absolute path which prefix is equal to the host-side of any mirror
  path -- was bugged.  For instance, the command "proot -m /bin:/host
  $ROOTFS /usr/bin/readlink /usr/bin/ps" returned "/host" instead of
  "/bin/ps".

+ Add the option "-V" to print the version then exit.

+ Be more explicit when a wrong command-line argument is used.

+ Remove the SIGSEGV help message: it was too confusing to the user.

+ Use a new shining build-system (again :D).

Special thanks go to those contributors: Yves JANIN, Remi Duraffort
and Christophe GUILLON.


Release v0.6.1
==============

+ Add `/tmp` to the list of mirrored paths when using -M.

+ Fix the ELF interpreter extraction.

+ Rewrite the build system.


Release v0.6
============

New features
------------

+ Added support for "asymmetric" path mirrors.

    The command-line option for mirrors was extended to support the
    syntax "-m <p1>:<p2>" where <p1> is the location of the mirror
    within the alternate rootfs and <p2> is the path to the real
    directory/file.  For instance you can now mirror the whole host
    rootfs in the directory "/hostfs" within the alternate rootfs that
    way::

        proot -m /:/hostfs ...

+ Added an option to disable ASLR (Address Space Layout
  Randomization).

    RHEL4 and Ubuntu 10.04 use an ASLR mechanism that creates
    conflicts between the layout of QEMU and the layout of the target
    program.  This new option is automatically set when QEMU is used.

+ Added "/etc/resolv.conf" and $HOME to the list of mirrored paths
  when using the option -M or -Q.

Fixes
-----

+ Fixed the detranslation of getcwd(2) and readlink(2).

+ Improved the build compatibility on old/broken distro.

+ Added support for pthread cancellation when QEMU is used.

+ Set QEMU's fake argv[0] to the program actually launched, not to the
  initial script name.

+ Create the path up to the mirror location to cheat "walking"
  programs.
