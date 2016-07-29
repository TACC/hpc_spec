#
# Antonio Gomez
# 2015-02-02
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#

Summary: PAPI/Perfctr Library - Local TACC Build

# Give the package a base name
%define pkg_base_name papi
%define MODULE_VAR    PAPI

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 4
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1
License:   LGPL
Group:     Development/Tools
URL:       http://icl.cs.utk.edu/papi/
Packager:  TACC - agomez@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This package provides the perfctr hardware counter and PAPI
library support.  It must be built against a kernel with the
appropriate perfctr patches.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
This package provides the perfctr hardware counter and PAPI
library support.  It must be built against a kernel with the
appropriate perfctr patches.


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

%setup -n %{pkg_base_name}-%{pkg_version}


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

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

  
  cd src
  export ARCH=x86_64
  ./configure --prefix=%{INSTALL_DIR} --with-perf_events
  make
  make DESTDIR=$RPM_BUILD_ROOT install

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
The %{MODULE_VAR} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_INC for
the location of the %{name} distribution, libraries,
and include files, respectively.

To use the %{MODULE_VAR} library, compile the source code with the option:
-I\$TACC_%{MODULE_VAR}_INC
add the following options to the link step:
-Wl,-rpath,\$TACC_%{MODULE_VAR}_LIB -L\$TACC_%{MODULE_VAR}_LIB -lpapi

The -Wl,-rpath,\$TACC_%{MODULE_VAR}_LIB option is not required, however,
if it is used, then this module will not have to be loaded
to run the program during future login sessions.

Version %{pkg_version}
]]

--help(help_msg)
help(help_msg)

whatis("PAPI: Performance Application Programming Interface")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: library, performance measurement")
whatis("Keywords: Profiling, Library, Performance Measurement")
whatis("Description: Interface to monitor performance counter hardware for quantifying application behavior")
whatis("URL: http://icl.cs.utk.edu/papi/")


%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local papi_dir           = "%{INSTALL_DIR}"

family("papi")
prepend_path(    "PATH",                pathJoin(papi_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(pai_dir, "lib"))
prepend_path(    "MANPATH",             pathJoin(papi_dir, "share/man"))
setenv( "TACC_%{MODULE_VAR}_DIR",                papi_dir)
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(papi_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(papi_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(papi_dir, "include"))
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
