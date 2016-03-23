Summary: This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker.
Group:      Utilities
Name:       tacc-rabbitmq-c
Version:    0.8.0
Release:    1 
License:    MIT
Packager:   TACC - rtevans@tacc.utexas.edu
Source:     rabbitmq-c-%{version}.tar.gz

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc

%define INSTALL_DIR /usr
%define PACKAGE_NAME %{name}

%package -n %{PACKAGE_NAME}-%{version}
Summary: This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker.
Group:   Utilities

%description
%description -n %{PACKAGE_NAME}-%{version}
This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker.

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n rabbitmq-c

%build

%install
%include system-load.inc
module load cmake
cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR} .
make install

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{PACKAGE_NAME}
%defattr(-,root,install)
%{INSTALL_DIR}/lib64
%{INSTALL_DIR}/include

%post -n %{PACKAGE_NAME}
%clean
rm -rf $RPM_BUILD_ROOT

