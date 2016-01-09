#
# Antonio Gomez
# 2016-01-07
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#

Summary: GRVY is a toolkit for HPC Application Development 

# Give the package a base name
%define pkg_base_name grvy
%define MODULE_VAR    GRVY

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 32
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc
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

Release:   2
License:   GPL
Group:     Development/Tools
Packager:  TACC - agomez@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: GRVY is a toolkit for HPC Application Development
Group: Development/Tools
%description package
GRVY is a toolkit for HPC Application Development

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
The GRVY Toolkit is a library used to house various support functions
often required for application development of high-performance,
scientific applications. The library is written in C++, but provides
an API for development in C and Fortran.


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
%include mpi-load.inc

module load boost
module load hdf5
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
  #CC=mpicc CXX=mpicc ./configure LDFLAGS=-Wl,-rpath,$TACC_BOOST_LIB --prefix=%{INSTALL_DIR} --with-boost=$TACC_BOOST_DIR --with-hdf5=$TACC_HDF5_DIR --enable-mpi
  ./configure LDFLAGS=-Wl,-rpath,$TACC_BOOST_LIB --prefix=%{INSTALL_DIR} --with-boost=$TACC_BOOST_DIR --with-hdf5=$TACC_HDF5_DIR
  make -j 4
  make DESTDIR=$RPM_BUILD_ROOT install
  
  # Copy everything from tarball over to the installation directory
#  cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

To use %{MODULE_VAR}, compile the source code with the option:

\t-I\$TACC_%{MODULE_VAR}_INC 

and add the following options to the link step:
\t-L\$TACC_%{MODULE_VAR}_LIB -lgrvy

Version: %{pkg_version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: grvy")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local grvy_dir           = "%{INSTALL_DIR}"

family("grvy")
prepend_path(    "PATH",                pathJoin(grvy_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(grvy_dir, "lib64"))
prepend_path(    "PKG_CONFIG_PATH",     pathJoin(grvy_dir, "lib/pkgconfig"))

setenv( "GRVY_DIR",                     grvy_dir)
setenv( "TACC_%{MODULE_VAR}_DIR",       grvy_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(grvy_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(grvy_dir, "lib64"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(grvy_dir, "bin"))
EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
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

