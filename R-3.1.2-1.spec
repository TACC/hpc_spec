#
# R-2.15.1.spec, v2.15.1, 2012-08-22 11:59:00 vaughn@tacc.utexas.edu
#
# See http://www.r-project.org/

Summary:    R is a free software environment for statistical computing and graphics.
Name:       R
Version:    3.1.2 
Release:    1 
License:    GPLv2
Vendor:     R Foundation for Statistical Computing
Group:      Applications/Statistics
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - walling@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%include rpm-dir.inc

%define APPS    /opt/apps
%define MODULES modulefiles

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}
R provides a wide variety of statistical (linear and nonlinear 
modelling, classical statistical tests, time-series analysis, 
classification, clustering, ...) and graphical techniques, and 
is highly extensible. 

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/R-2.15.2
%setup 

# Set environment
module purge
module load TACC
module load boost

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
# Use mount temp trick
# mkdir -p             %{INSTALL_DIR}
# mount -t tmpfs tmpfs %{INSTALL_DIR}

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

 module purge
 module load TACC
 export TACC_MKL_LIB=/opt/apps/intel/13/composer_xe_2013.1.117/mkl/lib/intel64
 
# DO NOT preppend $RPM_BUILD_ROOT in prefix
#./configure --enable-R-shlib --prefix=%{INSTALL_DIR} --with-x --with-tcltk --with-tcl-config=/usr/lib64/tclConfig.sh --with-tk-config=/usr/lib64/tkConfig.sh TCLTK_LIB="-L/usr/lib64 -Wl,-rpath,/usr/lib64 -ltcl8.5 -ltk8.5" TCLTK_CPPFLAGS="-I/usr/include" --with-blas="-Wl,-rpath,$TACC_MKL_LIB -L$TACC_MKL_LIB -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread -lm" --with-lapack --with-system-zlib=/usr/lib64/libz.a

./configure --enable-R-shlib --prefix=%{INSTALL_DIR} --with-x="no" 
 

make 

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

 mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
 make DESTDIR=$RPM_BUILD_ROOT install

#  Kluge, the make install, installs in /tmp/carlos
# cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
# umount                                   %{INSTALL_DIR}


# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0####################################################################
##
## R
##
proc ModulesHelp { } {
	puts stderr "\tThe module %{name} defines the following environmental variables:"
        puts stderr "\t%TACC_R_DIR, %TACC_R_BIN, %TACC_R_LIB for the location of the %{name}"
        puts stderr "\tdistribution, its binaries, and its libraries. It also adds the "
        puts stderr "\tdirectory locations to the %PATH and the %LD_LIBRARY_PATH.\n"
	puts stderr "\tVersion %{version}\n"
}

module-whatis "R"
module-whatis "Version: %{version}"
module-whatis "Category: applications, statistics, graphics"
module-whatis "Keywords: Applications, Statistics, Graphics, Scripting Language"
module-whatis "Description: statistics package"
module-whatis "URL: http://www.r-project.org/"

# Tcl script only
set version %{version}

# Export environmental variables
setenv TACC_R_DIR %{INSTALL_DIR}
setenv TACC_R_BIN %{INSTALL_DIR}/bin
setenv TACC_R_LIB %{INSTALL_DIR}/lib64/

# Prepend the scalasca directories to the adequate PATH variables
prepend-path PATH %{INSTALL_DIR}/bin
prepend-path LD_LIBRARY_PATH %{INSTALL_DIR}/lib64

# This is only necessary if there will be submodules built on 
# this package. Not the case with R (for the time being).
# prepend-path MODULEPATH %{MODULE_DIR}
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for R version %{version}
##
set ModulesVersion "%version"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}
#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}

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
