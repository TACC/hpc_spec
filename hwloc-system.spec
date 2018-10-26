#
# spec file for package hwloc
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


%global lname libhwloc5
%if ! 0%{?is_opensuse}
%define version_prefix 2.0.0.
%endif
%define mainversion 1.11.8
Name:           hwloc
Version:        %{?version_prefix}%{?mainversion}
Release:        lp150.1.11
Summary:        Portable Hardware Locality
License:        BSD-3-Clause
Group:          Productivity/Clustering/Computing
Url:            http://www.open-mpi.org/projects/hwloc/
#Source0:        %{name}-%{version}.tar.xz
Source0:        https://github.com/open-mpi/hwloc/archive/%{name}-%{mainversion}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  ncurses-devel
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  update-desktop-files
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)
Requires:       %{lname} = %{version}-%{release}
Requires:       perl-JSON
#Requires:       perl-base >= 5.18.2
Requires:       perl-base
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%ifnarch s390 s390x i586 aarch64 %{arm}
BuildRequires:  libnuma-devel
%endif

%description
The Portable Hardware Locality (hwloc) software package provides
an abstraction (across OS, versions, architectures, ...)
of the hierarchical topology of modern architectures, including
NUMA memory nodes, shared caches, processor sockets, processor cores
and processing units (logical processors or "threads"). It also gathers
various system attributes such as cache and memory information. It primarily
aims at helping applications with gathering information about modern
computing hardware so as to exploit it accordingly and efficiently.

hwloc may display the topology in multiple convenient formats.
It also offers a powerful programming interface (C API) to gather information
about the hardware, bind processes, and much more.

%package devel
Summary:        Headers and shared development libraries for hwloc
Group:          Development/Libraries/C and C++
Requires:       %{lname} = %{version}
Provides:       libhwloc-devel = %{version}
Obsoletes:      libhwloc-devel < %{version}
Obsoletes:      libhwloc-devel = 0.0.0

%description devel
This package contains the headers and shared object symbolic links
for the hwloc.

%package -n %{lname}
Summary:        Runtime libraries for hwloc
Group:          System/Libraries
Requires:       %{name}-data

%description -n %{lname}
This package contains the run time libraries for hwloc.

%package data
Summary:        Run time data for hwloc
Group:          Development/Libraries/C and C++
%if 0%{?sle_version} > 120300 || 0%{?is_opensuse}
BuildArch:      noarch
%endif

%description data
This package contains the run time data for the hwloc.

%package doc
Summary:        Documentation for hwloc
Group:          Documentation/Other
%if 0%{?sle_version} > 120300 || 0%{?is_opensuse}
BuildArch:      noarch
%endif

%description doc
This package contains the documentation for hwloc.

%prep
%setup -q -n %{name}-%{name}-%{mainversion}

%build
autoreconf -fvi

%configure \
    --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install
%suse_update_desktop_file -r lstopo System Monitor
# We don't ship .la files.
rm -rf %{buildroot}%{_libdir}/libhwloc.la

# documentation will be handled by % doc macro
rm -rf %{buildroot}%{_datadir}/doc/

# This binary is built only for intel architectures
%ifarch %{ix86} x86_64
mkdir -p %{buildroot}%{_libexecdir}/systemd/system
mv %{buildroot}%{_datadir}/hwloc/hwloc-dump-hwdata.service %{buildroot}%{_libexecdir}/systemd/system/hwloc-dump-hwdata.service
%else
rm %{buildroot}%{_datadir}/hwloc/hwloc-dump-hwdata.service
%endif

%fdupes -s %{buildroot}/%{_mandir}/man1
%fdupes -s %{buildroot}/%{_mandir}/man7

%check
#XXX: this is weird, but make check got broken by removing doxygen-doc/man above
#     the only one fix is to install documentation by hand, or to ignore check error
make %{?_smp_mflags} check || :

%post -n %{lname} -p /sbin/ldconfig
%postun -n %{lname} -p /sbin/ldconfig

%post
%desktop_database_post

%postun
%desktop_database_postun

%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING NEWS README VERSION
%{_mandir}/man1/hwloc*
%{_mandir}/man1/lstopo*
%{_bindir}/hwloc*
%{_bindir}/lstopo*
#%{_datadir}/applications/*.desktop
%ifarch %{ix86} x86_64
%attr(0755,root,root) %{_sbindir}/hwloc-dump-hwdata
%{_libexecdir}/systemd/system/hwloc-dump-hwdata.service
%endif

%files devel
%defattr(-, root, root, -)
%{_mandir}/man7/hwloc*
%{_includedir}/hwloc
%{_includedir}/hwloc.h
%{_libdir}/libhwloc.so
%{_libdir}/pkgconfig/hwloc.pc

%files -n %{lname}
%defattr(-, root, root, -)
%{_libdir}/libhwloc*so.*

%files data
%defattr(-, root, root, -)
%dir %{_datadir}/hwloc
%{_datadir}/hwloc/hwloc.dtd
%{_datadir}/hwloc/hwloc-valgrind.supp

%files doc
%defattr(-, root, root, -)
%doc ./doc/images/*.pdf

%changelog
* Tue Nov 21 2017 Thomas.Blume@suse.com
- update to latest released upstream version 1.11.8 (fate#324166)
  * Multiple Solaris improvements
  + Detect caches on Sparc.
  + Properly detect allowed/disallowed PUs and NUMA nodes with processor sets.
  + Add hwloc_get_last_cpu_location() support for the current thread.
  * Add support for CUDA compute capability 7.0 and fix support for 6.[12].
  * Tools improvements
  + Fix search for objects by physical index in command-line tools.
  + Add missing "cpubind:get_thisthread_last_cpu_location" in the output
    of hwloc-info --support.
  + Add --pid and --name to specify target processes in hwloc-ps.
  + Display thread names in lstopo and hwloc-ps on Linux.
  * Doc improvements
  + Add a FAQ entry about building on Windows.
  + Install missing sub-manpage for hwloc_obj_add_info() and
    hwloc_obj_get_info_by_name().
  * Fix hwloc-bind --membind for CPU-less NUMA nodes (again).
  Thanks to Gilles Gouaillardet for reporting the issue.
  * Fix a memory leak on IBM S/390 platforms running Linux.
  * Fix a memory leak when forcing the x86 backend first on amd64/topoext
  platforms running Linux.
  * Command-line tools now support "hbm" instead "numanode" for filtering
  only high-bandwidth memory nodes when selecting locations.
  + hwloc-bind also support --hbm and --no-hbm for filtering only or
    no HBM nodes.
  * Add --children and --descendants to hwloc-info for listing object
  children or object descendants of a specific type.
  * Add --no-index, --index, --no-attrs, --attrs to disable/enable display
  of index numbers or attributes in the graphical lstopo output.
  * Try to gather hwloc-dump-hwdata output from all possible locations
  in hwloc-gather-topology.
  * Updates to the documentation of locations in hwloc(7) and
  command-line tools manpages.
  * Make the Linux discovery about twice faster, especially on the CPU side,
  by trying to avoid sysfs file accesses as much as possible.
  * Add support for AMD Family 17h processors (Zen) SMT cores in the Linux
  and x86 backends.
  * Add the HWLOC_TOPOLOGY_FLAG_THISSYSTEM_ALLOWED_RESOURCES flag (and the
  HWLOC_THISSYSTEM_ALLOWED_RESOURCES environment variable) for reading the
  set of allowed resources from the local operating system even if the
  topology was loaded from XML or synthetic.
  * Fix hwloc_bitmap_set/clr_range() for infinite ranges that do not
  overlap currently defined ranges in the bitmap.
  * Don't reset the lstopo zoom scale when moving the X11 window.
  * lstopo now has --flags for manually setting topology flags.
  * hwloc_get_depth_type() returns HWLOC_TYPE_DEPTH_UNKNOWN for Misc objects.
* Tue Nov 21 2017 idonmez@suse.com
- Fix build on Leap where both sle_version is defined and
  is_opensuse is True.
* Mon Mar  6 2017 Thomas.Blume@suse.com
- make hwloc-dump-hwdata only available on x86, as it is only
  supported for Intel Knights Landing Xeon Phi platforms
- revert sub packages for SLE from no-arch to arch specific in order
  to keep backward compatibility
- fix typo in specfile
* Wed Feb  8 2017 jengelh@inai.de
- fix grammar errors
* Fri Jan 27 2017 Thomas.Blume@suse.com
- use correct upstream source version
* Tue Jan 24 2017 Thomas.Blume@suse.com
- use version_prefix in specfile and download_files service to get sources
* Mon Jan 23 2017 tchvatal@suse.com
- Set noarch on the subpackages that are arch independent
- Run configure with enabling verbose mode and disable needless knobs
- Set version in the package fully (not 1.11 but 1.11.5+git...)
- Rename files to name of the package, if it needs to be renamed the folder
  needs to keep the other name too
- Do not mess with provides/obsoletes about the hwloc-2.0 it won't work
  with libsolv anyway without user interaction
  * Bump the user version to 2.0.0.1.11.5+git... to allow 'fake' update
    for user in order to work with fate#321929c#5
* Tue Jan 17 2017 Thomas.Blume@suse.com
- switch  to version 1.11.5 since 2.0 is a development version with
  no .so-version set fate#321929 comment#5)
* Mon Aug 29 2016 Thomas.Blume@suse.com
- fix missing manpage bug (bsc#995407)
- remove dependency to selinux-policy, selinux is not essential
  for hwloc (bsc#976559 comment#4)
* Fri Apr 22 2016 Thomas.Blume@suse.com
- add dependency to selinux-policy (bsc#976559)
* Fri Mar 11 2016 thomas.blume@suse.com
- Update to 2.0 to support memory side cache (fate#319511)
* Sat Dec 26 2015 mpluskal@suse.com
- Update to 1.11.2
  * Improve support for Intel Knights Landing Xeon Phi on Linux:
    + Group local NUMA nodes of normal memory (DDR) and high-bandwidth memory
    (MCDRAM) together through "Cluster" groups so that the local MCDRAM is
    easy to find.
  - See "How do I find the local MCDRAM NUMA node on Intel Knights
    Landing Xeon Phi?" in the documentation.
  - For uniformity across all KNL configurations, always have a NUMA node
    object even if the host is UMA.
    + Fix the detection of the memory-side cache:
  - Add the hwloc-dump-hwdata superuser utility to dump SMBIOS
    information
    into /var/run/hwloc/ as root during boot, and load this dumped
    information from the hwloc library at runtime.
  - See "Why do I need hwloc-dump-hwdata for caches on Intel Knights
    Landing Xeon Phi?" in the documentation.
    Thanks to Grzegorz Andrejczuk for the patches and for the help.
  * The x86 and linux backends may now be combined for discovering CPUs
    through x86 CPUID and memory from the Linux kernel.
    This is useful for working around buggy CPU information reported by Linux
    (for instance the AMD Bulldozer/Piledriver bug below).
    Combination is enabled by passing HWLOC_COMPONENTS=x86 in the environment.
  * Fix L3 cache sharing on AMD Opteron 63xx (Piledriver) and 62xx (Bulldozer)
    in the x86 backend. Thanks to many users who helped.
  * Fix the overzealous L3 cache sharing fix added to the x86 backend in 1.11.1
    for AMD Opteron 61xx (Magny-Cours) processors.
  * The x86 backend may now add the info attribute Inclusive=0 or 1 to caches
    it discovers, or to caches discovered by other backends earlier.
    Thanks to Guillaume Beauchamp for the patch.
  * Fix the management on alloc_membind() allocation failures on AIX, HP-UX
    and OSF/Tru64.
  * Fix spurious failures to load with ENOMEM on AIX in case of Misc objects
    below PUs.
  * lstopo improvements in X11 and Windows graphical mode:
    + Add + - f 1 shortcuts to manually zoom-in, zoom-out, reset the scale,
    or fit the entire window.
    + Display all keyboard shortcuts in the console.
  * Debug messages may be disabled at runtime by passing
  * HWLOC_DEBUG_VERBOSE=0
    in the environment when --enable-debug was passed to configure.
  * Add a FAQ entry "What are these Group objects in my topology?".
* Mon Nov 16 2015 p.drouand@gmail.com
- Update to version 1.11.1
  * Hardwire the topology of Fujitsu K-computer, FX10, FX100 servers to
    workaround buggy Linux kernels.
  * Fix L3 cache information on AMD Opteron 61xx Magny-Cours processors
    in the x86 backend.
  * Detect block devices directly attached to PCI without a controller,
    for instance NVMe disks.
  * Add the PCISlot attribute to all PCI functions instead of only the
    first one.
  * Ignore PCI bridges that could fail assertions by reporting buggy
    secondary-subordinate bus numbers
  * Fix an overzealous assertion when inserting an intermediate Group object
    while Groups are totally ignored.
  * Fix a memory leak on Linux on AMD processors with dual-core compute units.
  * Fix a memory leak on failure to load a xml diff file.
  * Fix some segfaults when inputting an invalid synthetic description.
  * Fix a segfault when plugins fail to find core symbols.
  * Fix a segfault when displaying logical indexes in the graphical lstopo.
  * Fix lstopo linking with X11 libraries, for instance on Mac OS X.
  * hwloc-annotate, hwloc-diff and hwloc-patch do not drop unavailable
    resources from the output anymore and those may be annotated as well.
  * Command-line tools may now import XML from the standard input with -i -.xml
  * Add missing documentation for the hwloc-info --no-icaches option.
* Thu Mar  5 2015 mpluskal@suse.com
- Cleanup spec file with spec-cleaner
- Update to 1.10.1
  * Actually remove disallowed NUMA nodes from nodesets when the
    whole-system flag isn't enabled.
  * Fix the gathering of PCI domains. Thanks to James Custer for
    reporting the issue and providing a patch.
  * Fix the merging of identical parent and child in presence of
    Misc objects. Thanks to Dave Love for reporting the issue.
  * Fix some misordering of children when merging with
    ignore_keep_structure() in partially allowed topologies.
  * Fix an overzealous assertion in the debug code when running
    on a single-PU host with I/O. Thanks to Thomas Van Doren for
    reporting the issue.
  * Don't forget to setup NUMA node object nodesets in x86 backend
    (for BSDs) and OSF/Tru64 backend.
  * Fix cpuid-x86 build error with gcc -O3 on x86-32. Thanks to
    Thomas Van Doren for reporting the issue.
  * Fix support for future very large caches in the x86 backend.
  * Fix vendor/device names for SR-IOV PCI devices on Linux.
  * Fix an unlikely crash in case of buggy hierarchical distance matrix.
  * Fix PU os_index on some AIX releases. Thanks to Hendryk
    Bockelmann and Erik Schnetter for helping debugging.
  * Fix hwloc_bitmap_isincluded() in case of infinite sets.
  * Change hwloc-ls.desktop into a lstopo.desktop and only install
    it if lstopo is built with Cairo/X11 support. It cannot work
    with a non-graphical lstopo or hwloc-ls.
  * Add support for the renaming of Socket into Package in
    future releases.
  * Add support for the replacement of HWLOC_OBJ_NODE with
    HWLOC_OBJ_NUMANODE in future releases.
  * Clarify the documentation of distance matrices in hwloc.h and
    in the manpage of the hwloc-distances. Thanks to Dave Love for
    the suggestion.
  * Improve some error messages by displaying more information
    about the hwloc library in use.
  * Document how to deal with the ABI break when upgrading to
    the upcoming 2.0 See "How do I handle ABI breaks and API
    upgrades ?" in the FAQ.
* Tue Dec 30 2014 mardnh@gmx.de
- minor spec fixes (unbreak build for suse_version < Factory)
* Tue Dec 16 2014 alinm.elena@gmail.com
- Update to Version 1.10.0
  * v1.10.0 is the new feature release. There is no new major change
    in this release, just improvements everywhere.
    If you are buying new Intel Xeon E5 with 10 cores or more, this
    release is required for proper Socket/NUMA detection until the
    Linux kernel gets fixed.
  * API
    + Add hwloc_topology_export_synthetic() to export a topology to a
    synthetic string without using lstopo. See the Synthetic topologies
    section in the documentation.
    + Add hwloc_topology_set/get_userdata() to let the application save
    a private pointer in the topology whenever it needs a way to find
    its own object corresponding to a topology.
    + Add hwloc_get_numanode_obj_by_os_index() and document that this function
    as well as hwloc_get_pu_obj_by_os_index() are good at converting
    nodesets and cpusets into objects.
    + hwloc_distrib() does not ignore any objects anymore when there are
    too many of them. They get merged with others instead.
    Thanks to Tim Creech for reporting the issue.
  * Tools
    + hwloc-bind --get <command-line> now executes the command after displaying
    the binding instead of ignoring the command entirely.
    Thanks to John Donners for the suggestion.
    + Clarify that memory sizes shown in lstopo are local by default
    unless specified (total memory added in the root object).
  * Synthetic topologies
    + Synthetic topology descriptions may now specify attributes such as
    memory sizes and OS indexes. See the Synthetic topologies section
    in the documentation.
    + lstopo now exports in this fully-detailed format by default.
    The new option --export-synthetic-flags may be used to revert
    back the old format.
  * Documentation
    + Add the doc/examples/ subdirectory with several real-life examples,
    including the already existing hwloc-hello.C for basics.
    Thanks to Rob Aulwes for the suggestion.
    + Improve the documentation of CPU and memory binding in the API.
    + Add a FAQ entry about operating system errors, especially on AMD
    platforms with buggy cache information.
    + Add a FAQ entry about loading many topologies in a single program.
  * Misc
    + Work around buggy Linux kernels reporting 2 sockets instead
    1 socket with 2 NUMA nodes for each Xeon E5 v3 (Haswell) processor.
    + pciutils/libpci support is now removed since libpciaccess works
    well and there's also a Linux-specific PCI backend. For the record,
    pciutils was GPL and therefore disabled by default since v1.6.2.
    + Add --disable-cpuid configure flag to work around buggy processor
    simulators reporting invalid CPUID information.
    Thanks for Andrew Friedley for reporting the issue.
    + Fix a racy use of libltdl when manipulating multiple topologies in
    different threads.
    Thanks to Andra Hugo for reporting the issue and testing patches.
    + Fix some build failures in private/misc.h.
    Thanks to Pavan Balaji and Ralph Castain for the reports.
    + Fix failures to detect X11/Xutil.h on some Solaris platforms.
    Thanks to Siegmar Gross for reporting the failure.
    + The plugin ABI has changed, this release will not load plugins
    built against previous hwloc releases.
* Sun Aug 17 2014 mardnh@gmx.de
- removed patches (fixed upstream)
  * hwloc-1.7-manpage.patch
  * hwloc-1.7.patch
- Update to Version 1.9.0
  * API
    + Add hwloc_obj_type_sscanf() to extend hwloc_obj_type_of_string() with
    type-specific attributes such as Cache/Group depth and Cache type.
    hwloc_obj_type_of_string() is moved to hwloc/deprecated.h.
    + Add hwloc_linux_get_tid_last_cpu_location() for retrieving the
    last CPU where a Linux thread given by TID ran.
    + Add hwloc_distrib() to extend the old hwloc_distribute[v]() functions.
    hwloc_distribute[v]() is moved to hwloc/deprecated.h.
    + Don't mix total and local memory when displaying verbose object attributes
    with hwloc_obj_attr_snprintf() or in lstopo.
  * Backends
    + Add CPUVendor, CPUModelNumber and CPUFamilyNumber info attributes for
    x86, ia64 and Xeon Phi sockets on Linux, to extend the x86-specific
    support added in v1.8.1. Requested by Ralph Castain.
    + Add many CPU- and Platform-related info attributes on ARM and POWER
    platforms, in the Machine and Socket objects.
    + Add CUDA info attributes describing the number of multiprocessors and
    cores and the size of the global, shared and L2 cache memories in CUDA
    OS devices.
    + Add OpenCL info attributes describing the number of compute units and
    the global memory size in OpenCL OS devices.
    + The synthetic backend now accepts extended types such as L2Cache, L1i or
    Group3. lstopo also exports synthetic strings using these extended types.
  * Tools
    + lstopo
  - Do not overwrite output files by default anymore.
    Pass -f or --force to enforce it.
  - Display OpenCL, CUDA and Xeon Phi numbers of cores and memory sizes
    in the graphical output.
  - Fix export to stdout when specifying a Cairo-based output type
    with --of.
    + hwloc-ps
  - Add -e or --get-last-cpu-location to report where processes/threads
    run instead of where they are bound.
  - Report locations as likely-more-useful objects such as Cores or Sockets
    instead of Caches when possible.
    + hwloc-bind
  - Fix failure on Windows when not using --pid.
  - Add -e as a synonym to --get-last-cpu-location.
    + hwloc-distrib
  - Add --reverse to distribute using last objects first and singlify
    into last bits first. Thanks to Jirka Hladky for the suggestion.
    + hwloc-info
  - Report unified caches when looking for data or instruction cache
    ancestor objects.
  * Misc
    + Add experimental Visual Studio support under contrib/windows.
    Thanks to Eloi Gaudry for his help and for providing the first draft.
    + Fix some overzealous assertions and warnings about the ordering of
    objects on a level with respect to cpusets. The ordering is only
    guaranteed for complete cpusets (based on the first bit in sets).
    + Fix some memory leaks when importing xml diffs and when exporting a
    "too complex" entry.
  1.8.1:
  * Fix the cpuid code on Windows 64bits so that the x86 backend gets
    enabled as expected and can populate CPU information.
    Thanks to Robin Scher for reporting the problem.
  * Add CPUVendor/CPUModelNumber/CPUFamilyNumber attributes when running
    on x86 architecture. Thanks to Ralph Castain for the suggestion.
  * Work around buggy BIOS reporting duplicate NUMA nodes on Linux.
    Thanks to Jeff Becker for reporting the problem and testing the patch.
  * Add a name to the lstopo graphical window. Thanks to Michael Prokop
    for reporting the issue.
  1.8.0:
  * New components
    + Add the "linuxpci" component that always works on Linux even when
    libpciaccess and libpci aren't available (and even with a modified
    file-system root). By default the old "pci" component runs first
    because "linuxpci" lacks device names (obj->name is always NULL).
  * API
    + Add the topology difference API in hwloc/diff.h for manipulating
    many similar topologies.
    + Add hwloc_topology_dup() for duplicating an entire topology.
    + hwloc.h and hwloc/helper.h have been reorganized to clarify the
    documentation sections. The actual inline code has moved out of hwloc.h
    into the new hwloc/inlines.h.
    + Deprecated functions are now in hwloc/deprecated.h, and not in the
    official documentation anymore.
  * Tools
    + Add hwloc-diff and hwloc-patch tools together with the new diff API.
    + Add hwloc-compress-dir to (de)compress an entire directory of XML files
    using hwloc-diff and hwloc-patch.
    + Object colors in the graphical output of lstopo may be changed by adding
    a "lstopoStyle" info attribute. See CUSTOM COLORS in the lstopo(1) manpage
    for details. Thanks to Jirka Hladky for discussing the idea.
    + hwloc-gather-topology may now gather I/O-related files on Linux when
  - -io is given. Only the linuxpci component supports discovering I/O
    objects from these extended tarballs.
    + hwloc-annotate now supports --ri to remove/replace info attributes with
    a given name.
    + hwloc-info supports "root" and "all" special locations for dumping
    information about the root object.
    + lstopo now supports --append-legend to append custom lines of text
    to the legend in the graphical output. Thanks to Jirka Hladky for
    discussing the idea.
    + hwloc-calc and friends have a more robust parsing of locations given
    on the command-line and they report useful error messages about it.
    + Add --whole-system to hwloc-bind, hwloc-calc, hwloc-distances and
    hwloc-distrib, and add --restrict to hwloc-bind for uniformity among
    tools.
  * Misc
    + Calling hwloc_topology_load() or hwloc_topology_set_*() on an already
    loaded topology now returns an error (deprecated since release 1.6.1).
    + Fix the initialisation of cpusets and nodesets in Group objects added
    when inserting PCI hostbridges.
    + Never merge Group objects that were added explicitly by the user with
    hwloc_custom_insert_group_object_by_parent().
    + Add a sanity check during dynamic plugin loading to prevent some
    crashes when hwloc is dynamically loaded by another plugin mechanisms.
    + Add --with-hwloc-plugins-path to specify the install/load directories
    of plugins.
    + Add the MICSerialNumber info attribute to the root object when running
    hwloc inside a Xeon Phi to match the same attribute in the MIC OS device
    when running in the host.
  1.7.2:
  * Do not create invalid block OS devices on very old Linux kernel such
    as RHEL4 2.6.9.
  * Fix PCI subvendor/device IDs.
  * Fix the management of Misc objects inserted by parent.
    Thanks to Jirka Hladky for reporting the problem.
  * Add a Port<n>State into attribute to OpenFabrics OS devices.
  * Add a MICSerialNumber info attribute to Xeon PHI/MIC OS devices.
  * Improve verbose error messages when failing to load from XML.
  1.7.1:
  * Fix a failed assertion in the distance grouping code when loading a XML
    file that already contains some groups.
    Thanks to Laercio Lima Pilla for reporting the problem.
  * Remove unexpected Group objects when loading XML topologies with I/O
    objects and NUMA distances.
    Thanks to Elena Elkina for reporting the problem and testing patches.
  * Fix PCI link speed discovery when using libpciaccess.
  * Fix invalid libpciaccess virtual function device/vendor IDs when using
    SR-IOV PCI devices on Linux.
  * Fix GL component build with old NVCtrl releases.
    Thanks to Jirka Hladky for reporting the problem.
  * Fix embedding breakage caused by libltdl.
    Thanks to Pavan Balaji for reporting the problem.
  * Always use the system-wide libltdl instead of shipping one inside hwloc.
  * Document issues when enabling plugins while embedding hwloc in another
    project, in the documentation section Embedding hwloc in Other Software.
  * Add a FAQ entry "How to get useful topology information on NetBSD?"
    in the documentation.
  * Somes fixes in the renaming code for embedding.
  * Miscellaneous minor build fixes.
* Tue Nov 12 2013 meissner@suse.com
- fixed shared library rename
* Wed Oct 16 2013 boris@steki.net
- enable build on SLE and older (12.2) OS
* Fri Oct  4 2013 mvyskocil@suse.com
- Update to 1.7
  * New operating system backends
  * New I/O device discovery
  * New components
  1.6.2:
  * Use libpciaccess instead of pciutils/libpci by default for
    I/O discovery.
  1.6.1:
  * Fix some crash or buggy detection in the x86 backend when Linux
    cgroups/cpusets restrict the available CPUs.
  * Fix the pkg-config output with --libs --static.
    Thanks to Erik Schnetter for reporting one of the problems.
  * Fix the output of hwloc-calc -H --hierarchical when using logical
    indexes in the output.
  1.6.0:
  * Reorganize the backend infrastructure to support dynamic selection
    of components and dynamic loading of plugins.
  1.5.1:
  * Fix block OS device detection on Linux kernel 3.3 and later.
    Thanks to Guy Streeter for reporting the problem and testing the fix.
  * and many more changes, see NEWS files
- Added patches (taken from Fedora):
  * hwloc-1.7.patch
  * hwloc-1.7-manpage.patch
* Sat Oct 13 2012 d.pashov@gmail.com
- Set executable permissions to 2 scripts
* Fri Oct 12 2012 cfarrell@suse.com
- license update: BSD-3-Clause
  Use SPDX format (http://www.spdx.org/licenses)
* Fri Mar 30 2012 pascal.bleser@opensuse.org
- update to 1.4.1:
  * fix hwloc_alloc_membind
  * fix memory leaks in some get_membind() functions
  * fix helpers converting from Linux libnuma to hwloc (hwloc/linux-libnuma.h)
    in case of out-of-order NUMA node ids
  * fix some overzealous assertions in the distance grouping code
  * workaround BIOS reporting empty I/O locality in cuda and openfabrics
    helpers on Linux
  * install a valgrind suppressions file hwloc-valgrind.supp (see the FAQ)
  * fix memory binding documentation
- changes from 1.4.0:
  * add "custom" interface and "assembler" tools to build multi-node topology;
    see the Multi-node Topologies section in the documentation for details
  * add symmetric_subtree object attribute to ease assumptions when consulting
    regular symmetric topologies
  * add a CPUModel and CPUType info attribute to Socket objects on Linux and
    Solaris
  * add hwloc_get_obj_index_inside_cpuset() to retrieve the "logical" index of
    an object within a subtree of the topology
  * add more NVIDIA CUDA helpers in cuda.h and cudart.h to find hwloc objects
    corresponding to CUDA devices
  * add a group object above partial distance matrices to make sure the
    matrices are available in the final topology, except when this new object
    would contradict the existing hierarchy
  * grouping by distances now also works when loading from XML
  * fix some corner cases in object insertion, for instance when dealing with
    NUMA nodes without any CPU
  * implement hwloc_get_area_membind() on Linux
  * honor I/O topology flags when importing from XML
  * further improve XML-related error checking and reporting
  * hide synthetic topology error messages unless HWLOC_SYNTHETIC_VERBOSE=1
  * add synthetic exporting of symmetric topologies to lstopo
  * lstopo --horiz and --vert can now be applied to some specific object types
  * lstopo -v -p now displays distance matrices with physical indexes
  * add hwloc-distances utility to list distances
  * fix and/or document the behavior of most inline functions in hwloc/helper.h
    when the topology contains some I/O or Misc objects
  * backend documentation enhancements
  * fix dependencies in the embedded library
  * remove references to internal symbols in the tools
- changes from 1.3.2:
  * fix missing last bit in hwloc_linux_get_thread_cpubind()
  * fix PCI locality when Linux cgroups restrict the available CPUs
  * fix conversion from/to Linux libnuma when some NUMA nodes have no memory
  * remove references to internal symbols in the tools
  * further improve XML-related error checking and reporting
* Wed Dec 21 2011 pascal.bleser@opensuse.org
- update to 1.3.1:
  * silence some harmless pciutils warnings
- changes from 1.3.0:
  * add I/O devices and bridges to the topology using the pciutils library;
    only enabled after setting the relevant flag with
    hwloc_topology_set_flags() before hwloc_topology_load(). See the I/O
    Devices section in the documentation for details.
  * discovery improvements:
    + add associativity to the cache attributes
    + add support for s390/z11 "books" on Linux
    + add the HWLOC_GROUPING_ACCURACY environment variable to relax
    distance-based grouping constraints. See the Environment Variables
    section in the documentation for details about grouping behavior and
    configuration.
    + allow user-given distance matrices to remove or replace those discovered
    by the OS backend
  * XML improvements:
    + XML is now always supported: a minimalistic custom import/export code is
    used when libxml2 is not available. It is only guaranteed to read XML
    files generated by hwloc.
    + hwloc_topology_export_xml() and export_xmlbuffer() now return an integer
    + add hwloc_free_xmlbuffer() to free the buffer allocated by
    hwloc_topology_export_xmlbuffer()
    + hide XML topology error messages unless HWLOC_XML_VERBOSE=1
  * minor API updates:
    + add hwloc_obj_add_info to customize object info attributes
  * tools:
    + lstopo now displays I/O devices by default. Several options are added to
    configure the I/O discovery.
    + hwloc-calc and hwloc-bind now accept I/O devices as input
    + add --restrict option to hwloc-calc and hwloc-distribute
    + add --sep option to change the output field separator in hwloc-calc
    + add --whole-system option to hwloc-ps
- changes from 1.2.2:
  * fix XML import of very large page sizes or counts on 32bits platform
  * fix crash when administrator limitations such as Linux cgroup require to
    restrict distance matrices
  * fix the removal of objects such as AMD Magny-Cours dual-node sockets in
    case of administrator restrictions
  * improve error reporting and messages in case of wrong synthetic topology
    description
* Fri Aug 26 2011 pascal.bleser@opensuse.org
- update to 1.2.1:
  * improve support of AMD Bulldozer "Compute-Unit" modules by detecting
    logical processors with different core IDs on Linux
  * fix hwloc-ps crash when listing processes from another Linux cpuset
  * fix hwloc_get_last_cpu_location(THREAD) on Linux
* Wed Jun  1 2011 pascal.bleser@opensuse.org
- initial version (1.2)