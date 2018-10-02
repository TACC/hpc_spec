#
# Adapted from Bar.spec by Victor Eijkhout 2015/11/30
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

Summary: Swig rpm build script

# Give the package a base name
%define pkg_base_name swig
%define MODULE_VAR    SWIG

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 0
%define micro_version 12

%define pkg_version %{major_version}.%{minor_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  

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

Release:   2
License:   BSD
Group:     Development/Tools
URL:       http://www.mcs.anl.gov/swig/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Swig rpm building
Group: System Environment/Base
%description package
Portable Extendible Toolkit for Scientific Computations

%package %{MODULEFILE}
Summary: The modulefile RPM
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

%setup -n %{pkg_base_name}-%{pkg_full_version}

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

export modulefilename=%{pkg_full_version}
# Insert necessary module commands
module load boost

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

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
  
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

# VLE here is where we start copying from the old spec file
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 

./configure --help | grep boost
./configure --prefix=%{INSTALL_DIR} --with-boost=${TACC_BOOST_DIR} \
 && make \
 && make install
#make DESTDIR=$RPM_BUILD_ROOT install

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/

umount tmpfs

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

# Write out the modulefile associated with the application
echo "writing modulefile as: $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua"
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
SWIG: tool to connect different programming languages.

Version %{pkg_full_version}
]] )

whatis( "Name: Swig" )
whatis( "Version: %{version}" )
whatis( "Category: Development/Tools" )
whatis( "URL: http://www.swig.org/" )
whatis( "Description: a software development tool for connecting different languages" )

local             swig_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(swig_dir,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(swig_dir,"lib") )

setenv("TACC_SWIG_DIR",        swig_dir)
setenv("TACC_SWIG_BIN",        pathJoin(swig_dir,"bin") )
setenv("TACC_SWIG_LIB",        pathJoin(swig_dir,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Swig %version
##

set     ModulesVersion      "${modulefilename}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua

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
* Mon Jul 30 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: upgrade to 3.0.12
* Thu Jan 14 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: first release
