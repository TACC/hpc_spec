#
# spec file for package perl-JSON
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


Name:           perl-JSON
Version:        2.97001
Release:        lp150.1.3
%define cpan_name JSON
Summary:        JSON (JavaScript Object Notation) encoder/decoder
License:        Artistic-1.0 or GPL-1.0+
Group:          Development/Libraries/Perl
Url:            http://search.cpan.org/dist/JSON/
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/%{cpan_name}-%{version}.tar.gz
Source1:        cpanspec.yml
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  perl
BuildRequires:  perl-macros
Recommends:     perl(JSON::XS) >= 2.34
%{perl_requires}

%description
This module is a thin wrapper for JSON::XS-compatible modules with a few
additional features. All the backend modules convert a Perl data structure
to a JSON text as of RFC4627 (which we know is obsolete but we still stick
to; see below for an option to support part of RFC7159) and vice versa.
This module uses JSON::XS by default, and when JSON::XS is not available,
this module falls back on JSON::PP, which is in the Perl core since 5.14.
If JSON::PP is not available either, this module then falls back on
JSON::backportPP (which is actually JSON::PP in a different .pm file)
bundled in the same distribution as this module. You can also explicitly
specify to use Cpanel::JSON::XS, a fork of JSON::XS by Reini Urban.

All these backend modules have slight incompatibilities between them,
including extra features that other modules don't support, but as long as
you use only common features (most important ones are described below),
migration from backend to backend should be reasonably easy. For details,
see each backend module you use.

%prep
%setup -q -n %{cpan_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%check
%{__make} test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%defattr(-,root,root,755)
%doc Changes README

%changelog
* Fri Dec 22 2017 coolo@suse.com
- updated to 2.97001
  see /usr/share/doc/packages/perl-JSON/Changes
  2.97001 2017-12-21
  - updated backportPP with JSON::PP 2.97001
* Tue Nov 21 2017 coolo@suse.com
- updated to 2.97000
  see /usr/share/doc/packages/perl-JSON/Changes
  2.97000 2017-11-21
  - updated backportPP with JSON::PP 2.97000
  - use 5 digit minor version number for a while to avoid
    confusion
  - fixed is_bool to use blessed() instead of ref()
* Mon Nov 20 2017 coolo@suse.com
- updated to 2.96
  see /usr/share/doc/packages/perl-JSON/Changes
  2.96 2017-11-20
  - fixed packaging issue
  - updated backportPP with JSON::PP 2.96
  - not to use newer Test::More features (RT-122421; ilmari++)
  2.95 2017-11-20
  - updated backportPP with JSON::PP 2.95
* Tue May 30 2017 coolo@suse.com
- updated to 2.94
  see /usr/share/doc/packages/perl-JSON/Changes
  2.94 2017-05-29
  - fixed VERSION issue caused by VERSION methods added to abstract
    backend packages (RT-121892; ppisar++)
  - fixed a test for perl 5.6
* Fri May 19 2017 coolo@suse.com
- updated to 2.93
  see /usr/share/doc/packages/perl-JSON/Changes
  2.93 2017-05-19
  - add VERSION methods to (abstract) backend packages
  - explained backward incompatibility about backend method
  - updated VERSIONs of backportPP modules
* Tue May 16 2017 coolo@suse.com
- updated to 2.92
  see /usr/share/doc/packages/perl-JSON/Changes
* Mon Feb 10 2014 lchiquitto@suse.com
- removed unused patch:
  * fix_provides.diff
* Tue Nov 26 2013 coolo@suse.com
- updated to 2.90
  CAUTION!!!
  INCOMPATIBLE CHANGE
  JSON.pm had patched JSON::XS::Boolean and JSON::PP::Boolean internally
  on loading time for making these modules inherit JSON::Boolean.
  But since JSON::XS v3.0 it use Types::Serialiser as boolean class.
  Then now JSON.pm breaks boolean classe overload features and
  - support_by_pp if JSON::XS v3.0 or later is installed.
  JSON::true and JSON::false returned JSON::Boolean objects.
  For workaround, they return JSON::PP::Boolean objects in this version.
    isa_ok(JSON::true, 'JSON::PP::Boolean');
  And it discards a feature:
    ok(JSON::true eq 'true');
  In other word, JSON::PP::Boolean overload numeric only.
    ok( JSON::true == 1 );
* Mon Jun 10 2013 coolo@suse.com
- updated to 2.59
  - PUREPERL_ONLY support was not supported...
    and finally remove all PP options from Makefile.PL.
  - recommend JSON::XS instead of conditionally requiring it
    patched by miyagaw
    ( for example, $ cpanm --with-recommends JSON)
  - Hide more packages from PAUSE (and other stuff)
    patched by miyagawa
  - support PUREPERL_ONLY install option. (rt#84876)
    (PERL_ONLY and NO_XS are not yet removed)
  - stop installing JSON::XS automatically on Perl 5.18
  - t/x17_strage_overload.t didn't work correctly.
  - fixed t/x17_strage_overload.t (rt#84451 by Ricardo Signes)
  - update JSON::BackportPP version
  - fixed t/19_incr.t on perl >= 5.17.10 (wyant, rt#84154)
    pathced by mbeijen and modified with demerphq's patch
  - Fixed some spelling (by briandfoy)
  - fixed sppeling (by Perlover)
  - enhanced documents (Thanks to Justin Hunter and Olof Johansson)
  - changed backend module loading for overloaded object behavior
    (reported by tokuhirom)
- remove upstreamed fix_provides.diff
* Fri Nov 18 2011 coolo@suse.com
- update to 2.53
  - made Makefile.PL skipping a installing XS question
    when set $ENV{PERL_ONLY} or $ENV{NO_XS} (rt#66820)
  - fixed to_json (pointed and patched by mmcleric in rt#68359)
  - backport JSON::PP 2.27200
  * fixed incr_parse docodeing string more correctly (rt#68032 by LCONS)
* Tue Apr  5 2011 coolo@novell.com
- fix provides - JSON::PP is really another module
* Tue Mar  8 2011 pascal.bleser@opensuse.org
- update to 2.51:
  * import JSON::PP 2.27105 as BackportPP
  * JSON::PP is split away JSON distributino for perl 5.14
  * JSON::backportPP is included in instead
* Wed Dec  1 2010 coolo@novell.com
- switch to perl_requires macro
* Tue Sep 28 2010 pascal.bleser@opensuse.org
- update to 2.26:
  * JSON::PP: cleaned up code and enhanced sort option efficiency in encode
- changes from 2.25:
  * JSON: JSON::Backend::XS::Supportable always executed a needless process
    with JSON::XS backend; this made encode/decode a bit slower
- changes from 2.24:
  * JSON::PP:
    + tweaked code.
    + optimized code in hash object encoding
- changes from 2.23:
  * JSON::PP
    + modified tied object handling in encode; it made encoding speed faster
    (RT#61604)
    + modified t/e10_bignum.t for avoiding a warning in using Math::BigInt dev
    version
* Mon Sep  6 2010 chris@computersalat.de
- update to 2.22
  * added JSON::XS installing feature in Makefile.PL
    with cpan or cpanm (some points suggested by gfx)
  * check that to_json and from_json are not called as methods (CHORNY)
  * modified for -Duse64bitall -Duselongdouble compiled perl.
    11_pc_expo.t too. (these are patched by H.Merijn Brand)
- recreated by cpanspec 1.78
- noarch pkg
- remove blanks from changes file
* Wed Aug 25 2010 pascal.bleser@opensuse.org
- completely rewritten spec file
- updated to 2.22:
  * check that to_json and from_json are not called as methods
- changes from 2.21:
  * enhanced 'HOW DO I DECODE A DATA FROM OUTER AND ENCODE TO OUTER'
  * renamed eg/bench_pp_xs.pl to eg/bench_decode.pl
  * added eg/bench_encode.pl
- changes from 2.20:
  * added eg/bench_pp_xs.pl for benchmark sample
  * updated 'INCREMENTAL PARSING' section
  * decode_prefix() didn't count a consumed text length properly
  * enhanced XS compatibilty in the case of decoding a white space garbaged
    text
- changes from 2.19:
  * fixed typo (rt#53535 by Angel Abad)
  * added a recommendation refering to (en|de)code_json to pod
  * added 'HOW DO I DECODE A DATA FROM OUTER AND ENCODE TO OUTER'
- changs from 2.18:
  * updated document (compatible with JSON::XS 2.29)
  * fixed encode an overloaded 'eq' object bug
  * enhanced an error message compatible to JSON::XS
* Wed Jan 13 2010 jw@novell.com
- updated to 2.17
  * fixed a problem caused by JSON::XS backend and support_by_pp option
  (rt#52842,  rt#52847 by ikegami)
  [JSON::PP]
  * made compatible with JSON::XS 2.27
  * patched decode for incr_parse (rt#52820 by ikegami)
  * relaxed option caused an infinite loop in some condition.
* Sat Jul 25 2009 chris@computersalat.de
- spec mods
  * removed ^----------
  * removed ^#---------
* Sat Jun 20 2009 chris@computersalat.de
- update to 2.15
- added perl-macros
  o autogen filelist with perl_gen_filelist
- spec mods
  o added header
  o fixed deps
