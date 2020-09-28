# Works only with PGI . No need to make package file.
#
# Amit Ruhela
# 2020-10-08 Add name-defines-noreloc.inc
# 2020-10-08 Need to investigate relocation -- use /opt/apps for now
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
# NO_PACKAGE=1 ./build_rpm.sh --pgi=20 ompi-3.1.5.spec
# cd ../RPMS/x86_64
# rpm -qilp tacc-ompi-modulefile-3.1.5-1.el7.x86_64.rpm
# rpm -hiv --nodeps --relocate /tmpmod=/opt/apps tacc-ompi-modulefile-3.1.5-1.el7.x86_64.rpm
# rpm -e tacc-pgi-package-20.7.0-1.el7.x86_64.rpm tacc-ompi-modulefile-3.1.5-1.el7.x86_64.rpm


Summary: A Nice little non-relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name ompi
%define MODULE_VAR    OMPI

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 1
%define micro_version 5

%define year 2020
#%define pgversion %{major_version}.%{minor_version}
%define underscore_version %{major_version}_%{minor_version}

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
#%define pgi_ver pgi%{pgversion}
%define pgi_ver pgi/20.7.0/Linux_x86_64/20.7

%global __os_install_post %{nil}

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc

#%define MODULE_PREFIX /opt/apps

%define lib_dir Linux_x86_64/%{major_version}.%{minor_version}


########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   Community
Group:     Development/Tools
URL:       https://www.pgroup.com/products/community.htm
Packager:  TACC - aruhela@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

#--------------------------------------- '
%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the package RPM...
This is Open MPI package supplied with NIVIDIA HPC SDK.

#--------------------------------------- '
%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the modulefile RPM...
This is Open MPI package supplied with NIVIDIA HPC SDK.

#--------------------------------------- '
%description
This is Open MPI package supplied with NIVIDIA HPC SDK.

#--------------------------------------- '
%prep
#---------------------------------------
echo "RPM_BUILD_ROOT=$RPM_BUILD_ROOT"
echo "comp_fam_ver=%{comp_fam_ver}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

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

# Insert necessary module commands
module purge

echo "Building the modulefile?: %{BUILD_MODULEFILE}"
#echo "pgi_install = %{pgi_install}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

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
local help_message = [[

This module loads Open MPI Compiler variables.
The command directory is added to PATH.
The library directory is added to LD_LIBRARY_PATH.
The include directory is added to INCLUDE.
The man     directory is added to MANPATH.

Also Defined:
TACC_%{MODULE_VAR}_DIR   = %{MODULE_VAR} base             directory
TACC_%{MODULE_VAR}_BIN   = %{MODULE_VAR} binary           directory
TACC_%{MODULE_VAR}_LIB   = %{MODULE_VAR} library          directory
TACC_%{MODULE_VAR}_INC   = %{MODULE_VAR} include          directory

The PGI module also defines the following environment variables:
TACC_OMPI_DIR, TACC_OMPI_LIB, TACC_OMPI_INC and
TACC_OMPI_BIN for the location of the Open MPI distribution,
libraries, include files, and tools respectively.

Version %{pkg_version}
]]

help(help_message,"\n")

whatis("Name: Open MPI Compilers")
whatis("Version: %{pkg_version}")
whatis("Category: compiler")
whatis("Keywords: System, compiler")
whatis("URL: https://www.open-mpi.org/")

-- Create environment variables
local ompidir = "/opt/apps/%{pgi_ver}/comm_libs/openmpi/openmpi-%{major_version}.%{minor_version}.%{micro_version}"

prepend_path( "PATH"                     , pathJoin(ompidir,"bin"                 ))
prepend_path( "LD_LIBRARY_PATH"          , pathJoin(ompidir,"lib"                 ))
prepend_path( "MANPATH"                  , pathJoin(ompidir,"man"                 ))
prepend_path( "CPATH"                    , pathJoin(ompidir,"include"             ))
prepend_path( "MODULEPATH"               , "/opt/apps/%{comp_fam_ver}/ompi%{underscore_version}/modulefiles" )

setenv(       "OMPI"                     , ompidir  )
setenv(       "TACC_%{MODULE_VAR}_DIR"   , ompidir                     )
setenv(       "TACC_%{MODULE_VAR}_BIN"   , pathJoin(ompidir,"bin"       ))
setenv(       "TACC_%{MODULE_VAR}_LIB"   , pathJoin(ompidir,"lib"       ))
setenv(       "TACC_%{MODULE_VAR}_INC"   , pathJoin(ompidir,"include"   ))

prereq("pgi/20.7.0")
family("MPI")
EOF


cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile
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
%{echo: "PKG_BASE = %{PKG_BASE}" }

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


