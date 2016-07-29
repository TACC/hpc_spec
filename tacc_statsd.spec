Summary: TACC system statistics collector
Name: tacc_statsd
Version: 2.3.1
Release: 1
License: GPL
Vendor: Texas Advanced Computing Center
Group: System Environment/Base
Packager: TACC - rtevans@tacc.utexas.edu
Source: tacc_stats-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%include rpm-dir.inc

%define _bindir /opt/%{name}
%define _sysconfdir /etc

%description
This package provides the tacc_stats daemon, along with an /etc/init.d
script to provide control.

%prep
%setup -n tacc_stats-%{version}

%build
./configure --bindir=%{_bindir} --sysconfdir=%{_sysconfdir} --disable-infiniband --enable-rabbitmq LDFLAGS="-L/home1/02561/rtevans/rabbitmq-c/librabbitmq -lrt" CPPFLAGS=-I/home1/02561/rtevans/rabbitmq-c/librabbitmq
make

%install
rm -rf %{buildroot}
cd src
install -m 0755 -d %{buildroot}/%{_bindir}
install -m 0755 -d %{buildroot}/%{_sysconfdir}
install -m 0755 -d %{buildroot}/%{_sysconfdir}/init.d
install -m 6755 tacc_stats %{buildroot}/%{_bindir}/tacc_stats
install -m 0511 tacc_stats.conf %{buildroot}/%{_sysconfdir}/tacc_stats.conf
install -m 0755 taccstats %{buildroot}/%{_sysconfdir}/init.d/taccstats

%post
chkconfig --add taccstats
sed -i -e 's/localhost/tacc-stats02.tacc.utexas.edu/' \
    -e 's/default/ls5/' %{_sysconfdir}/tacc_stats.conf
/sbin/service taccstats restart

%preun
if [ $1 == 0 ]; then
/sbin/service taccstats stop || :
chkconfig --del taccstats || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_bindir}/
%attr(6755,root,root) %{_bindir}/tacc_stats
%attr(0744,root,root) %{_sysconfdir}/tacc_stats.conf
%attr(0744,root,root) %{_sysconfdir}/init.d/taccstats

