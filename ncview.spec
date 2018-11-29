#
# Spec file for Ncview
#
Summary:   Ncview is a library for generating platform-independent data files

# Give the package a base name
%define pkg_base_name ncview
%define MODULE_VAR    NCVIEW

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 1
%define micro_version 7

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

##
## Settings
##
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

Release: 1%{?dist}
License:   GPL
Group:     applications/io
Source:    ncview-%{pkg_version}.tar.gz
URL:       http://meteora.ucsd.edu/~pierce/ncview_home_page.html
Distribution: RedHat Linux
Vendor:    Unidata Program Center, UCAR
Packager:  TACC - eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools

%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
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

# Insert further module commands

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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
  
  # Copy everything from tarball over to the installation directory
  cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
#
# config/make:
#

module list
module spider hdf5/1.8.16
module load hdf5 netcdf udunits
./configure  --prefix=%{INSTALL_DIR}  \
    -with-udunits2_incdir=${TACC_UDUNITS_INC} \
    -with-udunits2_libdir=${TACC_UDUNITS_LIB}
make -j 3
make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--ncview
EOF

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

echo "make!"
  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  #######################################
  ########### Do Not Remove #############
  #######################################
  
echo "touch!"
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
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
prereq("hdf5","netcdf","udunits")

local ncdir = "%{INSTALL_DIR}"

-- Prepend paths
prepend_path("LD_LIBRARY_PATH",pathJoin(ncdir,"lib") )
prepend_path("PATH",           pathJoin(ncdir,"bin") )

-- Env variables 
setenv("TACC_NCVIEW_DIR", ncdir )
setenv("TACC_NCVIEW_BIN", pathJoin(ncdir,"bin") )

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Ncview
##
 
set     ModulesVersion      "%{version}"
EOF

echo "what's in the module dir"
ls $RPM_BUILD_ROOT/%{MODULE_DIR}

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
#    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
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
* Fri Nov 02 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: Initial build.

