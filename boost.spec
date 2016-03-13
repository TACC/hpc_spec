Prefix:    /opt/apps
Summary:   Boost spec file 
Name:      boost
%define    major_version 1
%define    minor_version 59
%define    micro_version 0
%define    pkg_version %{major_version}.%{minor_version}.%{micro_version}
Version:   %{pkg_version}
Release:   1
Group:     Utility
License:   GPL
URL:       http://www.boost.org
Source0:   boost_%{major_version}_%{minor_version}_%{micro_version}.tar.gz
Source1:   icu4c-56_1-src.tgz
Packager:  TACC - agomez@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS           /opt/apps
%define PKG_BASE       /opt/apps/%{name}
%define INSTALL_DIR    %{PKG_BASE}/%{version}
%define GENERIC_IDIR   %{PKG_BASE}/lmod
%define MODULES        modulefiles
%define MODULE_DIR     %{APPS}/%{MODULES}/lmod
%define MODULE_DIR_ST  %{APPS}/%{MODULES}/settarg
%define ZSH_SITE_FUNC  /usr/share/zsh/site-functions

%description
Boost emphasizes libraries that work well with the C++ Standard
Library. Boost libraries are intended to be widely useful, and usable
across a broad spectrum of applications. The Boost license encourages
both commercial and non-commercial use.

Boost aims to establish "existing practice" and provide reference
implementations so that Boost libraries are suitable for eventual
standardization. Ten Boost libraries are already included in the C++
Standards Committee's Library Technical Report (TR1) as a step toward
becoming part of a future C++ Standard. More Boost libraries are
proposed for the upcoming TR2.


%prep


%setup

%build


%install

%include system-load.inc
%include compiler-defines.inc
module purge
%include compiler-load.inc


ICU_MODE=Linux
%if "%{comp_fam}" == "intel"
      export CONFIGURE_FLAGS=--with-toolset=intel-linux
      ICU_MODE=Linux/ICC
%endif

%if "%{comp_fam}" == "gcc"
      export CONFIGURE_FLAGS=--with-toolset=gcc
%endif

WD=`pwd`

cd icu/source
./runConfigureICU  $ICU_MODE --prefix=%{INSTALL_DIR}
make -j 10
make install
rm -f ~/user-config.jam

cd $WD
cd boost_1_59_0
EXTRA="-sICU_PATH=%{INSTALL_DIR}"
CONFIGURE_FLAGS="$CONFIGURE_FLAGS --with-libraries=all --without-libraries=mpi"

./bootstrap.sh --prefix=%{INSTALL_DIR} ${CONFIGURE_FLAGS}
./b2 -j 10 --prefix=%{INSTALL_DIR} $EXTRA install

mkdir -p              $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..


rm -f ~/tools/build/v2/user-config.jam

if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}



#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}



cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
The boost module file defines the following environment variables:"
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_INC for"
the location of the boost distribution."

To load the mpi boost      do "module load boost-mpi"
To load the rest of boost  do "module load boost"

It is save to load both.

Version %{version}"
]])

whatis("Name: boost")
whatis("Version: %{version}")
whatis("Category: %{group}")
whatis("Keywords: System, Library, C++")
whatis("URL: http://www.boost.org")
whatis("Description: Boost provides free peer-reviewed portable C++ source libraries %{BOOST_TYPE}.")


setenv("TACC_%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_%{MODULE_VAR}_INC","%{INSTALL_DIR}/include")

-- Add boost to the LD_LIBRARY_PATH
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{MODULE_VAR}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
# Check the syntax of the generated lua modulefile
%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}



%files
%defattr(-,root,root,)
%{INSTALL_DIR}
%{MODULE_DIR}


%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
