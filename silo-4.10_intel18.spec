# Si Liu
# 2018-07-13

Summary: SILO spec file 

# Give the package a base name
%define pkg_base_name silo
%define MODULE_VAR    SILO

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 10
%define micro_version 2

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

Release:   3%{?dist}
License: BSD Open Source License
Group:   Data/Visualization
Packager: TACC - siliu@tacc.utexas.edu
Source: %{pkg_base_name}-%{version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: Silo
Group: Data/Visualization

%description package
Silo is a library for reading and writing a wide variety of scientific data to binary, disk files. 
The files Silo produces and the data within them can be easily shared and exchanged 
between wholly independently developed applications running on disparate computing platforms. 
Consequently, Silo facilitates the development of general purpose tools for processing scientific data. 

%package %{MODULEFILE}
Summary: Silo
Group: Data/Visualization 

%description modulefile
Module RPM for Silo

%description
Silo is a library for reading and writing a wide variety of scientific data to binary, disk files. 
The files Silo produces and the data within them can be easily shared and exchanged 
between wholly independently developed applications running on disparate computing platforms. 
Consequently, Silo facilitates the development of general purpose tools for processing scientific data.

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
module purge

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

  ./configure --prefix=$INSTALL_DIR   \
  --enable-static --enable-shared \
  --with-hdf5=/opt/apps/intel18/hdf5/1.10.4/x86_64/include,/opt/apps/intel18/hdf5/1.10.4/x86_64//lib

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
Silo is a library for reading and writing a wide variety of scientific data to binary, disk files.
The files Silo produces and the data within them can be easily shared and exchanged
between wholly independently developed applications running on disparate computing platforms.
Consequently, Silo facilitates the development of general purpose tools for processing scientific data.

Version: 4.10.2
]]
)

whatis("Name:SILO scientific database library")
whatis("Version: 4.10.2")
whatis("Category: Library, Visualization")
whatis("Description: a scalable mesh and field I/O library and scientific database")
whatis("URL: https://wci.llnl.gov/codes/silo/")

prepend_path("PATH",    "%{INSTALL_DIR}/bin")
prepend_path("INCLUDE", "%{INSTALL_DIR}/include")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")

setenv("TACC_%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_%{MODULE_VAR}_INC","%{INSTALL_DIR}/include")
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
