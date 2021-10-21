#
# Spec file for Udunits
#
Summary:   Udunits is a utility for netcdf

# Give the package a base name
%define pkg_base_name udunits
%define MODULE_VAR    UDUNITS

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2
%define micro_version 26

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
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

Release:   1%{?dist}
License:   GPL
Group:     applications/io
Source:    udunits-%{version}.tar.gz
URL:       http://www.unidata.ucar.edu/downloads/udunits/index.jsp
Distribution: RedHat Linux
Vendor:    Unidata Program Center, UCAR
Packager:  TACC - cazes@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: Udunits is utility for NetCDF
Group: applications/io

%package %{MODULEFILE}
Summary: Udunits is utility for NetCDF
Group: applications/io

%description
%description %{PACKAGE}
Udunits

%description %{MODULEFILE}
Udunits

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
module load hdf5
module load netcdf

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
./configure --prefix=%{INSTALL_DIR}
make -j 4
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

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--udunits

local help_message = [[
The %{name} module file defines the following environment variables:
TACC_UDUNITS_DIR, TACC_UDUNITS_BIN, TACC_UDUNITS_LIB, and 
TACC_UDUNITS_INC forthe location of the UDUNITS distribution, binaries,
libraries, and include files, respectively.

UDUNITS 4.1.1 uses the hdf5 libraries to support the UDUNITS 4 file format 
in addition to the classic UDUNITS file format. 

To use the UDUNITS library, compile the source code with the option:

	-I${TACC_UDUNITS_INC} 

and add the following options to the link step: 

	-L${TACC_UDUNITS_LIB} -ludunits -L${TACC_HDF5_LIB} -lhdf5_hl -lhdf5 -lz -lm

Version %{version}

]]

help(help_message,"\n")


whatis("Udunits: Network Common Data Form")
whatis("Version: %{version}")
whatis("Category: library, runtime support")
whatis("Keywords: I/O, Library")
whatis("Description: I/O library which stores and retrieves data in self-describing, machine-independent datasets." )
whatis("URL: http://www.unidata.ucar.edu/software/udunits/")

-- Prerequisites
depends_on("hdf5")

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH",           "%{INSTALL_DIR}/bin")
prepend_path("MANPATH",        "%{INSTALL_DIR}/share/man")
prepend_path("PKG_CONFIG_PATH","%{INSTALL_DIR}/lib/pkgconfig")

--Env variables 
setenv("TACC_UDUNITS_DIR", "%{INSTALL_DIR}")
setenv("TACC_UDUNITS_INC", "%{INSTALL_DIR}/include")
setenv("TACC_UDUNITS_LIB", "%{INSTALL_DIR}/lib")
setenv("TACC_UDUNITS_BIN", "%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Udunits
##
 
set     ModulesVersion      "%{version}"
EOF

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

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

#---------------------------------------
%changelog
#---------------------------------------
* Mon Jul 29 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial install
