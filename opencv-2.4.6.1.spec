#
# Spec file for OpenCV 2.4.6.1
#

Summary:   OpenCV 2.4.6.1 local binary install
Name:      opencv
Version:   2.4.6.1
Release:   1
License:   freely distributable
Vendor:    www.opencv.org
Group:     Visualization
Source:    opencv-2.4.6.1.tar
Packager:  walling@tacc.utexas.edu, ada@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

# compiler-defines is loading 15.0.2 which isn't available,so I commented it out for now
%define is_intel15 1
%include compiler-defines.inc
#%define comp_fam intel
#%define comp_fam_ver intel15
#%define comp_fam_name Intel
#%define is_intel 1

%define RPM_PACKAGE_NAME %{name}-%{comp_fam_ver}-%{version}-%{release}

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary: OpenCV image library
Group: Visualization

%description
%description -n %{name}-%{comp_fam_ver}
OpenCV is an image processing library.

%prep
%setup -q -n opencv-2.4.6.1

%build

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
tacctmpfs -mount %{INSTALL_DIR}

pwd
mkdir -p build
cd build



#/opt/apps/cmake/2.8.9/bin/cmake \
/bin/cmake \
        -D CMAKE_INSTALL_PREFIX=%{INSTALL_DIR} \
        ..

	make -j 8 install

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

# umount %{INSTALL_DIR}
tacctmpfs -umount %{INSTALL_DIR}

%include compiler-load.inc

## Module for %{name}-%{version}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#####################################################################
##
## OpenCV 2.4.6.1 parallel interactive visualization system
##
proc ModulesHelp { } {
        puts stderr "\tOpenCV 2.4.6.1 parallel interactive visualization system\n"
        puts stderr "\tThe OpenCV module defines the following OpenCV environment variables:\n"
        puts stderr "\t{ TACC_OPENCV_DIR,TACC_OPENCV_LIB, TACC_OPENCV_INC             } \n"
        puts stderr "\t{ for the location of the OpenCV distribution, libraries and include files respectively } \n"
        puts stderr "\n\tVersion %{version}\n"

}

module-whatis   "OpenCV imaging library"
module-whatis   "Version: %{version}"
module-whatis   "Category: application, library, graphics"
module-whatis   "Description: an imaging library"
module-whatis   "URL: http://www.opencv.org"

# load only one version of qt at a time
conflict opencv

#prereq qt/4.8.4

prepend-path    PATH            %{INSTALL_DIR}/bin
prepend-path    LD_LIBRARY_PATH %{INSTALL_DIR}/lib/
prepend-path    INCLUDE %{INSTALL_DIR}/include/opencv

setenv TACC_OPENCV_DIR  %{INSTALL_DIR}
setenv TACC_OPENCV_INC  %{INSTALL_DIR}/include/opencv
setenv TACC_OPENCV_LIB  %{INSTALL_DIR}/lib
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

%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}
