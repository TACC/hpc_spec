Summary: Zsh: The one shell to rule them all
Name: tacc-zsh
Version: 5.3.1
Release: 2
License: Zsh Development Group
Group: System Environment/Shells
Source: zsh-%{version}.tar.gz
Packager: TACC- cproctor@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

Obsoletes: zsh
Provides: /bin/zsh

Provides: zsh              = %{version}-%{release}
Provides: zsh(x86-64)      = %{version}-%{release}
Provides: tacc-zsh         = %{version}-%{release}
Provides: tacc-zsh(x86-64) = %{version}-%{release}


%define debug_package %{nil}
%include rpm-dir.inc

%define _bindir    /bin


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

%setup -n zsh-%{version}

%build

#dirlist=""
#for i in /etc/tacc/zsh /usr/lib/zsh /usr/share/zsh; do
#    dirlist="$i $dirlist"
#    mkdir -p $i $RPM_BUILD_ROOT/$i
#done

CC=gcc ./configure --prefix=/usr --mandir=/usr/share/man --bindir=/bin/     \
                   --enable-etcdir=/etc/tacc/zsh --infodir=/usr/share/info  \
		   --enable-cflags=-O2                                      \
                   --enable-site-fndir=/opt/apps/zsh/site-functions
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
/usr/lib/zsh
/usr/share/man/man1
/usr/share/zsh

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

