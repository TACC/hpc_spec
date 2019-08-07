# Give the package a base name
%define pkg_base_name ncview
%define MODULE_VAR    NCVIEW

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 1
%define micro_version 7

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

#
# Spec file for Ncview
#
Summary:   Ncview is a library for generating platform-independent data files
Release:   1%{?dist}
License:   GPL
Group:     applications/io
Source:    ncview-%{version}.tar.gz
URL:       http://meteora.ucsd.edu/~pierce/ncview_home_page.html
Distribution: RedHat Linux
Vendor:    Unidata Program Center, UCAR
Packager:  TACC - eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Ncview is a program for viewing NetCDF files
Group: applications/io

%package %{MODULEFILE}
Summary: Ncview is a program for viewing NetCDF files
Group: applications/io

%description
%description %{PACKAGE}
Ncview is a GUI viewer for NetCDF (network Common Data Form) files
%description %{MODULEFILE}
Ncview is a GUI viewer for NetCDF (network Common Data Form) files

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
module purge
# Load Compiler
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

module load hdf5 netcdf udunits

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
#
# Use mount temp trick
#
mkdir -p             %{INSTALL_DIR}
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
  
#
# config/make:
#

./configure  --prefix=%{INSTALL_DIR}  \
    -with-udunits2_incdir=${TACC_UDUNITS_INC} \
    -with-udunits2_libdir=${TACC_UDUNITS_LIB}
make -j 3
make install
# VLE this was before mount tmpfs: make DESTDIR=$RPM_BUILD_ROOT install
# make test

cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

umount %{INSTALL_DIR}

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

rm -rf   $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--ncview

local help_message = [[
The %{name} module file defines the following environment variables:
TACC_NCVIEW_DIR, TACC_NCVIEW_BIN,
for the location of the NCVIEW distribution and binaries, respectively.

Version %{version}

]]

help(help_message,"\n")


whatis("Ncview: NetCDF data viewer")
whatis("Version: %{version}")
whatis("Category: visualization, application")
whatis("Keywords: I/O")
whatis("Description: Visualization program for NetCDF files")
whatis("URL: http://meteora.ucsd.edu/~pierce/ncview_home_page.html")

-- Prerequisites
depends_on("hdf5","netcdf","udunits")

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH",           "%{INSTALL_DIR}/bin")

--Env variables 
setenv("TACC_NCVIEW_DIR", "%{INSTALL_DIR}")
setenv("TACC_NCVIEW_BIN", "%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Ncview
##
 
set     ModulesVersion      "%{version}"
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
%files %{PACKAGE}
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE} 
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

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jul 15 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: Initial build.
