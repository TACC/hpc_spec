#
# Spec file for SWIG:
# interface generator utility 
# which is always too old for trilinos
#
# Victor Eijkhout, 2017
# based on:
#
# Bar.spec, 
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
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

Summary:    Set of tools for manipulating geographic and Cartesian data sets

# Give the package a base name
%define pkg_base_name swig
%define MODULE_VAR    SWIG

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 0
%define micro_version 12

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc
#%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   3%{?dist}
License:   GNU
Group:     Development/Tools
Vendor:     SOEST - hawaii
Group:      Libraries/maps
Source:	    swig-%{version}.tar.gz
URL:	    http://swig.soest.hawaii.edu/ 
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: SWIG install
Group: System Environment/Base
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: SWIG install
Group: System Environment/Base
%description modulefile
This is the long description for the modulefile RPM...

%description
SWIG is a software development tool that connects programs written in C and C++
with a variety of high-level programming languages. SWIG is primarily used with
common scripting languages such as Perl, Python, Tcl/Tk, and Ruby, however the
list of supported languages also includes non-scripting languages such as Java,
OCAML and C#. Also several interpreted and compiled Scheme implementations
(Guile, MzScheme, Chicken) are supported. SWIG is most commonly used to create
high-level interpreted or compiled programming environments, user interfaces,
and as a tool for testing and prototyping C/C++ software. SWIG can also export
its parse tree in the form of XML and Lisp s-expressions. 


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
# Load Compiler
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}

./configure --prefix=%{INSTALL_DIR} \
 && make \
 && make install

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

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
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
Simplified Wrapper and Interface Generator
This module loads swig.
The command directory is added to PATH.
The include directory is added to INCLUDE.
The lib     directory is added to LD_LIBRARY_PATH.

Version %{version}
]] )

whatis( "Simplified Wrapper and Interface Generator" )
whatis( "Version: %{version}" )
whatis( "Category: Development/Tools" )
whatis( "Description: SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages." )
whatis( "URL: http://www.swig.org" )

local swig_dir = "%{INSTALL_DIR}"

prepend_path( "PATH", pathJoin( swig_dir,"bin" ) )
setenv("TACC_SWIG_DIR", swig_dir )
setenv("TACC_SWIG_BIN", pathJoin(swig_dir,"bin" ) )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for %{name} version %{version}
##
set ModulesVersion "%version"
EOF

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
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

########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jun 15 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: proper path in modulefiles
* Thu Jun 01 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: lua modulefiles
* Fri Feb 24 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
