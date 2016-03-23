#
# gnuplot.spec
# 2016-02-29
# Antia Lamas-Linares (alamas@tacc.utexas.edu)


%define major_version 5
%define minor_version 0
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

Summary:  Gnuplot
Name:     gnuplot
Version:  %{pkg_version}
Release:  4
License:  http://www.gnuplot.info/faq/faq.html
Group:    Development/Tools
Source:   %{name}-%{version}.tar.gz
Packager: TACC - alamas@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%package -n tacc-%{name}
Summary:  Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms.
Group:    Development/Tools

%description
%description -n tacc-%{name}
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms.
#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/scalasca-1.1
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
# Use mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}

# Start with a clean environment
%include system-load.inc
#if [ -f "$BASH_ENV" ]; then
#  . $BASH_ENV
##  . /etc/tacc/tacc_functions
#  module purge
#  clearMT
#  export MODULEPATH=/opt/apps/tools/modulefiles:/opt/apps/modulefiles
#fi

module purge
module load TACC

# Build remora
#sed -i 's/pip/#pip/g' ./install.sh
#REMORA_INSTALL_PREFIX=%{INSTALL_DIR} ./install.sh

#module load python
#pip install blockdiag --target=%{INSTALL_DIR}/python

# Build gnuplot
  wget http://sourceforge.net/projects/gnuplot/files/gnuplot/%{pkg_version}/gnuplot-%{pkg_version}.tar.gz/download

  tar xvf gnuplot-%{pkg_version}.tar.gz
  cd gnuplot-%{pkg_version}
  ./configure --prefix=${INSTALL_DIR}
  make
  make install
  #make DESTDIR=$RPM_BUILD_ROOT install


%install
mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount                                   %{INSTALL_DIR}


# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_msg=[[
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries and tools respectively.
]]


whatis("Name: Gnuplot")
whatis("Version: 5.0.1")
whatis("Category: Development/Tools ")
whatis("Keywords: Tools, Graphics")
whatis("Description: Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms.")
whatis("URL: http://www.gnuplot.info")

help(help_msg,"\n")

-- Create environment variables.
local gnuplot_dir           = "%{INSTALL_DIR}"

family("gnuplot")
prepend_path(    "PATH",                pathJoin(gnuplot_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(gnuplot_dir, "libexec"))
setenv( "TACC_GNUPLOT_DIR",       gnuplot_dir)
setenv( "TACC_GNUPLOT_LIB",       pathJoin(gnuplot_dir, "libexec"))
setenv( "GNUPLOT_BIN",       pathJoin(gnuplot_dir, "bin"))

EOF

# Version File
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF


## %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n tacc-%{name}
# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the source files from /tmp/BUILD
rm -rf /tmp/BUILD/%{name}-%{version}

# Remove the installation files now that the RPM has been generated
rm -rf /var/tmp/%{name}-%{version}-buildroot

rm -rf $RPM_BUILD_ROOT
