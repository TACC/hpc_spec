# Si Liu
# 2021-09-30

Summary: CDO spec file 

# Give the package a base name
%define pkg_base_name cdo
%define MODULE_VAR    CDO

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 9
%define micro_version 10

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc

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

Release:   1%{?dist}
License: BSD Open Source License
Group:   Data/Climate
Packager: TACC - siliu@tacc.utexas.edu
Source: %{pkg_base_name}-%{version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: CDO
Group: Data/Climate

%description package
CDO is a collection of command line Operators to manipulate and analyse Climate and NWP model Data.
Supported data formats are GRIB 1/2, netCDF 3/4, SERVICE, EXTRA and IEG. There are more than 600 operators available.

%package %{MODULEFILE}
Summary: CDO
Group: Data/Climate

%description modulefile
Module RPM for CDO

%description
CDO is a collection of command line Operators to manipulate and analyse Climate and NWP model Data.
Supported data formats are GRIB 1/2, netCDF 3/4, SERVICE, EXTRA and IEG. There are more than 600 operators available.

#---------------------------------------
%prep
#---------------------------------------


echo %{INSTALL_DIR}

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
%include compiler-defines.inc

module load  intel/19.1.1 impi/19.0.9 TACC
module load hdf5

%include compiler-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

  INSTALL_DIR=%{INSTALL_DIR}

  # Removed from config:
  # --enable-sharedlibs=gcc  --enable-shared


   export CFLAGS="-O3 -mavx2 "
   export FFLAGS="-O3 -assume buffered_io -mavx2 "
   export CXXFLAGS="-O3 -mavx2 "
   export LDFLAGS="-O3 -mavx2 "

  ./configure --prefix=$INSTALL_DIR   \
  --with-hdf5=${TACC_HDF5_DIR} --with-netcdf=${TACC_NETCDF_DIR}

  make -j 16

  make DESTDIR=$RPM_BUILD_ROOT install

  cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}

#---------------------- -
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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[

Version: 1.9.10
]]
)

whatis("Name: CDO")
whatis("Version: 1.9.10")
whatis("Category: Library, DATA, Climate")
whatis("Description: a collection of command line Operators to manipulate and analyse Climate and NWP model Data.")
whatis("URL: https://code.mpimet.mpg.de/projects/cdo")

prepend_path("PATH",    "%{INSTALL_DIR}/bin")

setenv("TACC_%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")

EOF


cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile
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
