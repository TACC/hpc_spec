%define	_bindir	/bin

Summary: An enhanced version of csh, the C shell.
Name: tcsh
Version: 6.18.01
Release: 2
License: distributable
Group: System Environment/Shells
Source: ftp://ftp.astron.com/pub/tcsh/tcsh-%{version}.tar.gz
Patch1: tcsh-6.18.01-bufsize.patch
Patch2: tcsh-6.18.01-pathnames.patch
Prereq: fileutils, grep
URL: http://www.tcsh.org/
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

%prep
%setup -n tcsh-%{version}
%patch1 -p0
%patch2 -p0

nroff -me eight-bit.me > eight-bit.txt
#autoreconf

%build
%configure --without-hesiod
make all
%{__perl} tcsh.man2html tcsh.man
make -C nls catalogs

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 tcsh ${RPM_BUILD_ROOT}%{_bindir}/tcsh
install -m 644 tcsh.man ${RPM_BUILD_ROOT}%{_mandir}/man1/tcsh.1
ln -sf tcsh ${RPM_BUILD_ROOT}%{_bindir}/csh
ln -sf tcsh.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/csh.1

while read lang language ; do
	dest=${RPM_BUILD_ROOT}%{_datadir}/locale/$lang/LC_MESSAGES
	if test -f tcsh.$language.cat ; then
		mkdir -p $dest
		install -m644 tcsh.$language.cat $dest/tcsh
		echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/tcsh"
	fi
done > tcsh.lang << _EOF
de german
el greek
en C
es spanish
et et
fi finnish
fr french
it italian
ja ja
pl pl
ru russian
uk ukrainian
_EOF

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}

%post
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/tcsh" >> /etc/shells
	echo "%{_bindir}/csh"  >> /etc/shells
else
	grep -q '^%{_bindir}/tcsh$' /etc/shells || \
	echo "%{_bindir}/tcsh" >> /etc/shells
	grep -q '^%{_bindir}/csh$'  /etc/shells || \
	echo "%{_bindir}/csh"  >> /etc/shells
fi

%postun
if [ ! -x %{_bindir}/tcsh ]; then
	grep -v '^%{_bindir}/tcsh$'  /etc/shells | \
	grep -v '^%{_bindir}/csh$' > /etc/shells.rpm
	cat /etc/shells.rpm > /etc/shells && rm /etc/shells.rpm
fi

%files -f tcsh.lang
%defattr(-,root,root)
%doc FAQ Fixes NewThings complete.tcsh eight-bit.txt tcsh.html
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/*/*

