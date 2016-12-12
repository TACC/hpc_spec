Summary: Libxml2 install

# Give the package a base name
%define pkg_base_name libxml2
%define MODULE_VAR    LIBXML2

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 7
%define micro_version 8
%define versionpatch 2.7.8

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
#%include mpi-defines.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release: 1%{?dist}
License: http://www.libxml2.net/libxml2_license.html
Vendor: Jean-loup Gailly and Mark Adler, http://www.libxml2.net/
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{major_version}.%{minor_version}.%{micro_version}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Libxml2 local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Libxml2 local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
XML support
%description %{MODULEFILE}
XML support

%prep

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n libxml2-%{versionpatch}

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
%include compiler-defines.inc
## %include mpi-defines.inc
module purge
%include compiler-load.inc
## %include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

# make the rpm install dir
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# but we are actually making in a tmpfs
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 
  
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
  
export CC=icc
export CXX=icpc
export CFLAGS="-xMIC-AVX512"
export CXXFLAGS="-xMIC-AVX512"
./configure \
    --prefix=%{INSTALL_DIR} \
    --host=x86_64-klom-linux --without-python \
    && \
  make all && \
  make install


# since we made this in a tmpfs, we copy straight to the rpm install dir
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

umount tmpfs
  
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
  
##
## modulefile part of the configure install loop
##
#%include name-defines-noreloc.inc
echo "using module filename: %{MODULE_FILENAME}"
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} <<EOF
help( [[
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.
]] )

whatis( "Name: Libxml2" )
whatis( "Version: %{pkg_version}%{dbg}")
whatis( "Category: library, comporession" )
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

whatis( "Description: Compression library" )

local             libxml2_arch =    "${architecture}"
local             libxml2_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(libxml2_dir,libxml2_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(libxml2_dir,libxml2_arch,"lib") )

setenv("LIBXML2_ARCH",            libxml2_arch)
setenv("LIBXML2_DIR",             libxml2_dir)
setenv("TACC_LIBXML2_DIR",        libxml2_dir)
setenv("TACC_LIBXML2_BIN",        pathJoin(libxml2_dir,libxml2_arch,"bin") )
setenv("TACC_LIBXML2_LIB",        pathJoin(libxml2_dir,libxml2_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << EOF
#%Module1.0#################################################
##
## version file for Libxml2 %version
##

set     ModulesVersion      "${modulefilename}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

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

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Oct 24 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
