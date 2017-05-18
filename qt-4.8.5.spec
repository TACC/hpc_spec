#
# Spec file for qt 4.8.5
#

Summary:  Qt 4.8.5 local binary install
Name:     qt
Version:  4.8.5
Release:  1
License:  freely distributable
Vendor:   qt.nokia.com
Group:    Visualization
Source:   qt-everywhere-opensource-src-4.8.5.tar.gz
Packager:  gda@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define __spec_install_post /usr/lib/rpm/brp-compress
%define __spec_install_post /usr/lib/rpm/brp-strip
%define debug_package %{nil}

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/qt/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/qt

%include rpm-dir.inc

%package -n %{name}-%{comp_fam_ver}
Summary: qt 4.8.5 local binary install
Group: Visualization

%description
%description -n %{name}-%{comp_fam_ver}
Qt is a cross-platform application and UI framework.

%prep
%setup -q -n  qt-everywhere-opensource-src-4.8.5

%build

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

echo 'o
yes
' | ./configure -no-webkit --prefix=%{INSTALL_DIR} 
make -j 8


%install


# make DESTDIR=$RPM_BUILD_ROOT install
make install
mkdir -p $RPM_BUILD_ROOT/%{APPS}/%{name}
cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}
umount %{INSTALL_DIR}

## Module for %{name}-%{version}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#####################################################################
##
## Qt visual widget library
##
proc ModulesHelp { } {
        puts stderr "\tQt visual widget library\n"
        puts stderr "\tThis module loads Qt library variables.\n"
        puts stderr "\t{ The command directory is added to PATH.             } \n"
	puts stderr "\t{ The include directory is added to INCLUDE.          } \n"
        puts stderr "\t{ The lib     directory is added to LD_LIBRARY_PATH.  } \n"
        puts stderr "\n\tVersion %{version}\n"

}

module-whatis   "Qt visual widget library"
module-whatis   "Version: %{version}"
module-whatis   "Category: library, graphics"
module-whatis   "Description: a visual widget library for UI construction"
module-whatis   "URL: http://qt.nokia.com/"

# load only one version of qt at a time
conflict qt

prepend-path    PATH            %{INSTALL_DIR}/bin
prepend-path    LD_LIBRARY_PATH %{INSTALL_DIR}/lib
prepend-path    PKG_CONFIG_PATH %{INSTALL_DIR}/lib/pkgconfig

setenv TACC_QT_DIR  %{INSTALL_DIR}
setenv TACC_QT_INC  %{INSTALL_DIR}/include
setenv TACC_QT_LIB  %{INSTALL_DIR}/lib
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################################
##
## version file for qt %{version}
##

set     ModulesVersion     "%version"
EOF 

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}
