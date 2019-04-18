# HYPRE specfile
# Victor Eijkhout 2017
# the version 3.10 corresponds to the petsc version
# that this inherits from
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
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: Hypre, piggybacking on the PETSc install

# Give the package a base name
%define pkg_base_name hypre
%define MODULE_VAR    HYPRE

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 14
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}
%define petscversion 3.10
###%define NO_PACKAGE 0

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
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

Release:   3%{?dist}
License:   LGPL
Group:     Development/Numerical-Libraries
URL:       llnl.gov
Packager:  TACC - eijkhout@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Hypre local binary install
Group: System Environment/Base
%description modulefile
This is the long description for the modulefile RPM...

%description
Hypre is a solver library for distributed sparse linear system.

#---------------------------------------
%prep
#---------------------------------------

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

%include compiler-load.inc
%include mpi-load.inc

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

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
## configure install loop
##
export dynamic="debug cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug "

for ext in \
  "" hyprefei \
  ${dynamic} \
  ; do

echo "module file for ${ext}"

module unload petsc
if [ -z "${ext}" ] ; then
#  export architecture=knightslanding
  module load petsc/%{petscversion}
  export architecture=${PETSC_ARCH}
else
#  export architecture=knightslanding-${ext}
  module load petsc/%{petscversion}-${ext}
fi
export architecture=${PETSC_ARCH}


##
## modulefile part of the configure install loop
##
if [ -z "${ext}" ] ; then
  export modulefilename=%{version}
else
  export modulefilename=%{version}-${ext}
fi

echo 
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The Hypre module defines the following environment variables:
TACC_HYPRE_INC and TACC_HYPRE_LIB for the location
of the Hypre include files and libraries.

Version %{version}
]] )

whatis( "Name: Hypre" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://llnl.gov/hypre/" )
whatis( "Description: Numerical library for sparse solvers" )

local             hypre_arch =    "${architecture}"
local             hypre_dir  =     "${TACC_PETSC_DIR}"
local             hypre_inc  = pathJoin(hypre_dir,hypre_arch,"include")
local             hypre_lib  = pathJoin(hypre_dir,hypre_arch,"lib")

prepend_path("LD_LIBRARY_PATH", hypre_lib)

setenv("TACC_HYPRE_DIR",        hypre_dir )
setenv("TACC_HYPRE_INC",        hypre_inc )
setenv("TACC_HYPRE_LIB",        hypre_lib)
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Hypre %version
##

set     ModulesVersion      "${modulefilename}"
EOF

# Check the syntax of the generated lua modulefile only if a visible module
%if %{?VISIBLE}
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua
%endif

##
## end of module file loop
##
done

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


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
* Mon Mar 11 2019 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: move to petsc 3.10, add hyprefei, remove bin directory
* Thu Dec 21 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: petsc architecture fix
* Tue May 30 2017 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release with 3.10
