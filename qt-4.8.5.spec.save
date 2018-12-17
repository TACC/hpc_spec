#
# Adapted from Bar.spec by Greg Abram 2016/01/14
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary:  Qt 4.8.5 local binary install

# Give the package a base name
%define pkg_base_name qt
%define MODULE_VAR    QT

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 8
%define micro_version 5

%define pkg_version %{major_version}.%{minor_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

%define is_intel16 1

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################


Release:  1
License:  freely distributable
Vendor:   qt.nokia.com
Group:    Visualization
Source:   qt-everywhere-opensource-src-%{pkg_full_version}.tar.gz
Packager:  gda@tacc.utexas.edu
Patch0:   qt-4.8.5-patch-1.txt

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%include rpm-dir.inc

%package %{PACKAGE}
Summary: qt 4.8.5 local binary install
Group: Visualization
%description package
Qt is a cross-platform application and UI framework.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Qt is a cross-platform application and UI framework.

%description
Qt

%prep

%if %{?BUILD_PACKAGE}

rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n qt-everywhere-opensource-src-%{pkg_full_version}
%patch0 -p1

%endif # BUILD_PACKAGE 

%if %{?BUILD_MODULEFILE}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif # BUILD_MODULEFILE 

%build


%install

# Setup modules
%include system-load.inc

module purge
%include compiler-load.inc

# Insert further module commands
module load cmake

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

%if %{?BUILD_PACKAGE}

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

echo 'o
yes
' | ./configure -platform linux-icc --prefix=%{INSTALL_DIR} 
make -j 8

make install

mkdir -p $RPM_BUILD_ROOT/%{APPS}/%{name}
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}
umount %{INSTALL_DIR}

%endif # BUILD_PACKAGE 

%if %{?BUILD_MODULEFILE}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary

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

%endif # BUILD_MODULEFILE

%if %{?BUILD_PACKAGE}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%endif # BUILD_PACKAGE
