%define pkg_base_name zsh

Summary: Zsh: The one shell to rule them all
Name: zsh
Version: 5.3.1
Release: 3%{?dist}
License: Zsh Development Group
Group: System Environment/Shells
Source: zsh-%{version}.tar.gz
Packager: TACC- mclay@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define _bindir    /bin

Provides: %{pkg_base_name} = %{version}-%{release}
Provides: %{name} = %{version}-%{release}
Provides: /bin/zsh

%description 
Zsh is a UNIX command interpreter (shell) which of the
standard shells most resembles the Korn shell (ksh); its compatibility
with the 1988 Korn shell has been gradually increasing. It includes
enhancements of many types, notably in the command-line editor,
options for customising its behaviour, filename globbing, features to
make C-shell (csh) users feel more at home and extra features drawn
from tcsh (another "custom" shell).


%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}

%setup -n %{pkg_base_name}-%{version}

%build

#dirlist=""
#for i in /etc/tacc/zsh /usr/lib/zsh /usr/share/zsh; do
#    dirlist="$i $dirlist"
#    mkdir -p $i $RPM_BUILD_ROOT/$i
#done

CC=gcc ./configure --prefix=/usr --mandir=/usr/share/man --bindir=/bin/     \
                   --enable-etcdir=/etc/tacc/zsh --infodir=/usr/share/info  \
                   --enable-cflags=-O2
make

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_bindir}/zsh-*

#mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_bindir}

##make check
#
#mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_bindir}
#
#
#for i in $dirlist ; do
#  mount -t tmpfs tmpfs $i
#done
#
#make install.man
#make install.fns
#make install.modules
#
#for i in $dirlist ; do
#  cp -r $i/ $RPM_BUILD_ROOT/$i/..
#  umount $i
#done

%files 
%defattr(-,root,install)

%{_bindir}/zsh
/usr/lib/zsh/%{version}
/usr/share/man/man1/zsh.1
/usr/share/man/man1/zshall.1
/usr/share/man/man1/zshbuiltins.1
/usr/share/man/man1/zshcalsys.1
/usr/share/man/man1/zshcompctl.1
/usr/share/man/man1/zshcompsys.1
/usr/share/man/man1/zshcompwid.1
/usr/share/man/man1/zshcontrib.1
/usr/share/man/man1/zshexpn.1
/usr/share/man/man1/zshmisc.1
/usr/share/man/man1/zshmodules.1
/usr/share/man/man1/zshoptions.1
/usr/share/man/man1/zshparam.1
/usr/share/man/man1/zshroadmap.1
/usr/share/man/man1/zshtcpsys.1
/usr/share/man/man1/zshzftpsys.1
/usr/share/man/man1/zshzle.1
/usr/share/zsh/%{version}

%post
if [ ! -f /etc/shells ]; then
        echo "%{_bindir}/zsh" >> /etc/shells
else
        grep -q '^%{_bindir}/zsh$' /etc/shells || \
        echo "%{_bindir}/zsh" >> /etc/shells
fi
%postun
if [ ! -x %{_bindir}/zsh ]; then
        grep -v '^%{_bindir}/zsh$'  /etc/shells > /etc/shells.rpm
        cat /etc/shells.rpm > /etc/shells && rm /etc/shells.rpm
fi

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}

