#
# Mumps spec file by piggy-backing on petsc
# Victor Eijkhout 2016
#
# Inspired by Bar.spec; W. Cyrus Proctor Antonio Gomez 2015-08-25
#
# Important Build-Time Environment Variables (see name-defines.inc)
#    -> Do Not Build/Rebuild Package RPM
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

Summary: Mumps spec file by piggy-backing on PETSc

# Give the package a base name
%define pkg_base_name mumps
%define MODULE_VAR    MUMPS

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 0
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define petscversion 3.7

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

Release:  2
License:  BSD-like; see src/docs/website/documentation/copyright.html
Group:    Development/Numerial-Libraries
Vendor:   ENS-Lyon
URL:      http://graal.ens-lyon.fr/MUMPS/
Packager: TACC - eijkhout@tacc.utexas.edu
# no Source

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The MUMPS package RPM
Group: Development/Numerical-libraries
%description package
Mumps is a direct solver for distributed sparse linear system.

%package %{MODULEFILE}
Summary: The MUMPS modulefile RPM
Group: Lmod/Numerical-libraries
%description modulefile
Mumps is a direct solver for distributed sparse linear system.

%description
Mumps is a direct solver for distributed sparse linear system.

#---------------------------------------
%prep
#---------------------------------------

# #------------------------
# %if %{?BUILD_PACKAGE}
# #------------------------
#   # Delete the package installation directory.
#   rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ### %setup -n %{pkg_base_name}-%{pkg_version}

# #-----------------------
# %endif # BUILD_PACKAGE |
# #-----------------------

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

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

export dynamic="debug cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug "

# #------------------------
# %if %{?BUILD_PACKAGE}
# #------------------------

#   mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
#   #######################################
#   ##### Create TACC Canary Files ########
#   #######################################
#   touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
#   #######################################
#   ########### Do Not Remove #############
#   #######################################

#   #========================================
#   # Insert Build/Install Instructions Here
#   #========================================
  

# #-----------------------  
# %endif # BUILD_PACKAGE |
# #-----------------------


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
## same loop but for module files
##
for ext in \
  "" \
  ${dynamic} \
  ; do

if [ -z "${ext}" ] ; then
  export modulefilename=%{version}
  export architecture=sandybridge
  module load petsc/%{petscversion}
else
  export modulefilename=%{version}-${ext}
  export architecture=sandybridge-${ext}
  module load petsc/%{petscversion}-${ext}
fi

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.
]] )

whatis("Name: mumps")
whatis("Version: %{pkg_version}")

-- Create environment variables.
local mumps_dir           = "${TACC_PETSC_DIR}"
local mumps_arch          = "${PETSC_ARCH}"
local mumps_inc           = pathJoin(mumps_dir,mumps_arch,"include")
local mumps_lib           = pathJoin(mumps_dir,mumps_arch,"lib")

family("mumps")
prepend_path("LD_LIBRARY_PATH", mumps_lib)
setenv("TACC_MUMPS_INC",        mumps_inc )
setenv("TACC_MUMPS_LIB",        mumps_lib)
EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "${modulefilename}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua
  %endif

done
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


# #------------------------
# %if %{?BUILD_PACKAGE}
# %files package
# #------------------------

#   %defattr(-,root,install,)
#   # RPM package contains files within these directories
#   %{INSTALL_DIR}

# #-----------------------
# %endif # BUILD_PACKAGE |
# #-----------------------
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
* Thu Jun 01 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: update to petsc 3.7
* Wed Feb 03 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: first release
