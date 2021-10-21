#
# Spec file for ANTLR
# needed for NCO
#
# Victor Eijkhout, 2021

# Give the package a base name
%define pkg_base_name antlr
%define MODULE_VAR    ANTLR

# note : NCO needs exactly this version, even though a much newer exists.
%define major_version 2
%define minor_version 7
%define micro_version 7

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc                  
%include compiler-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Summary: NetCDF operators
Release: 2%{?dist}
License: GPL 3
Source: antlr-%{version}.tar.gz
URL:  http://antlr.sourceforge.net/
Packager: TACC - cazes@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0
%undefine __brp_mangle_shebangs

%package %{PACKAGE}
Summary: for NetCDF operators
Group: applications/io

%package %{MODULEFILE}
Summary: Modules for Antlr

%description 
Stuff for NCO
%description package
Stuff for NCO
%description modulefile
Stuff for NCO

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf ${RPM_BUILD_ROOT}/%{INSTALL_DIR}

# The first call to setup untars the first source.
%setup -n %{pkg_base_name}-%{pkg_version}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
module purge
# Load Compiler
%include compiler-load.inc

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

mkdir -p %{INSTALL_DIR}
rm -rf   %{INSTALL_DIR}/*
mount -t tmpfs tmpfs %{INSTALL_DIR}

cp -r * %{INSTALL_DIR}
pushd   %{INSTALL_DIR}

export ANTLR_PATH=%INSTALL_DIR

./configure \
-v \
--prefix=${ANTLR_PATH} \
--enable-shared \
--with-pic \
--enable-netcdf-4 
make 
make install 


# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

popd 
umount %{INSTALL_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  

#Module for antlr
rm -rf  $RPM_BUILD_ROOT/%MODULE_DIR
mkdir -p $RPM_BUILD_ROOT/%MODULE_DIR
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--  modulefile for ANTLR

local help_message = [[
The %{name} module file defines the following environment variables:
TACC_ANTLR_DIR, TACC_ANTLR_BIN, TACC_ANTLR_LIB, and 
TACC_ANTLR_INC for the location of the ANTLR distribution, binaries,
libraries, and include files, respectively.

To use the ANTLR library, compile the source code with the option:
	-I\${TACC_ANTLR_INC 

and add the following options to the link step: 
	-L\${TACC_ANTLR_LIB -lantlr

Version %{version}

]]

help(help_message,"\n")

whatis("Version: 2.7.7")
whatis("Category: utility, runtime support")
whatis("Description: Programs for manipulating and analyzing NetCDF files")
whatis("URL: http://antlr.sourceforge.net")

setenv("TACC_ANTLR_DIR","%{INSTALL_DIR}")
setenv("TACC_ANTLR_BIN","%{INSTALL_DIR}/bin")
setenv("TACC_ANTLR_INC","%{INSTALL_DIR}/include")
setenv("TACC_ANTLR_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_ANTLR_MAN","%{INSTALL_DIR}/share/man")
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
##
## version file for antlr
##
 
set     ModulesVersion      "%{version}"
EOF

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

%defattr(-,root,root)
%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

%post


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 15 2021 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: first release

