Summary: This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker.
Group:   Utilities
Name:       tacc-rabbitmq-c
Version:    0.7.1
Release:    1 
License:    MIT
Packager:   TACC - rtevans@tacc.utexas.edu
Source:     rabbitmq-c-%{version}.tar.gz

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc

%define INSTALL_DIR /opt/apps/rabbitmq-c/%{version}
%define PACKAGE_NAME %{name}-%{version}

%package -n %{PACKAGE_NAME}
Summary: This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker.
Group:   Utilities

%description
%description -n %{PACKAGE_NAME}
This is a C-language AMQP client library for use with v2.0+ of the RabbitMQ broker.

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n rabbitmq-c-%{version}

%build

%install
rm -rf build
mkdir -p build
cd build
ls
ml cmake
cmake -DCMAKE_C_FLAGS="-fPIC" -DCMAKE_INSTALL_PREFIX:PATH=$RPM_BUILD_ROOT/%{INSTALL_DIR} .. 
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

