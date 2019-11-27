# $Id$

Summary: XALT
Name: xalt
Version: 2.7.19
Release: 1
License: LGPLv2
Group: System Environment/Base
Source0:  xalt-%{version}.tar.bz2
Packager: mclay@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME xalt
%define APPS /opt/apps
%define MODULES modulefiles

%define PKG_BASE      %{APPS}/%{name}
%define INSTALL_DIR   %{APPS}/%{PNAME}/%{version}
%define GENERIC_IDIR  %{PKG_BASE}/%{name}
%define MODULE_DIR    %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR    TACC_XALT

%description
A method to collect system usage data.

%prep

%setup -n %{PNAME}-%{version}

%build
%install


if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/xsede/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi


myhost=$(hostname -f)
myhost=${myhost%.tacc.utexas.edu}
HOST=$myhost
first=${myhost%%.*}
SYSHOST=${myhost#*.}

TRANSMISSION=syslog
SYSHOST_CONF=nth_name:2
ETC_DIR=/tmp/moduleData
if [[ $SYSHOST = "ls5" ]]; then
  TRANSMISSION=file
  CONF_OPTS="--with-xaltFilePrefix=/scratch/projects/XALT"
  SYSHOST_CONF=hardcode:ls5
  ETC_DIR=/home1/moduleData
fi

if [[ $SYSHOST = "frontera" ]]; then
  CONF_OPTS="--with-trackGPU=yes"
fi

CXX=/usr/bin/g++ CC=/usr/bin/gcc ./configure CXX=/usr/bin/g++ CC=/usr/bin/gcc --prefix=%{APPS} --with-syshostConfig=$SYSHOST_CONF \
   --with-config=Config/TACC_config.py --with-transmission=$TRANSMISSION --with-MySQL=no                                          \
   --with-etcDir=$ETC_DIR $CONF_OPTS

make CXX=/usr/bin/g++ CC=/usr/bin/gcc DESTDIR=$RPM_BUILD_ROOT install Inst_TACC
rm -f $RPM_BUILD_ROOT/%{INSTALL_DIR}/sbin/xalt_db.conf
rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/../%{name}

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The xalt module collects system usage data.

Version %{version}
]]
)

whatis("Name: XALT")
whatis("Version: %{version}")
whatis("Category: tools")
whatis("Keywords: System, TOOLS")
whatis("URL: http://xalt.sf.net")
whatis("Description: Collects system usage data")

prepend_path{"PATH",                      "%{GENERIC_IDIR}/bin", priority = 100}
prepend_path("COMPILER_PATH",             "%{GENERIC_IDIR}/bin")
prepend_path("LD_PRELOAD",                "%{GENERIC_IDIR}/lib64/libxalt_init.so")
setenv (     "%{MODULE_VAR}_DIR",         "%{GENERIC_IDIR}/")
setenv (     "%{MODULE_VAR}_BIN",         "%{GENERIC_IDIR}/bin")
setenv (     "XALT_EXECUTABLE_TRACKING",  "yes")
setenv (     "XALT_SCALAR_SAMPLING",      "yes")
EOF

#--------------
#  Version file. 
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

cd %{PKG_BASE}

if [ -d %{name} ]; then
  rm -f %{name}
fi
ln -s %{version} %{name}

%postun

cd %{PKG_BASE}

if [ -h %{name} ]; then
  lv=`readlink %{name}`
  if [ ! -d $lv ]; then
    rm %{name}
  fi
fi

%clean
rm -rf $RPM_BUILD_ROOT
