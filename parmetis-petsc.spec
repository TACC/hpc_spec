# PARMETIS specfile based on the petsc installation
# Victor Eijkhout 2019-2020
#

Summary: Parmetis, piggybacking on the PETSc install

# Give the package a base name
%define pkg_base_name parmetis_petsc
%define MODULE_VAR    PARMETISPETSC

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 0
%define micro_version 3

%define pkg_version %{major_version}.%{minor_version}
%define petscversion 3.12

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc-home1.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   BSD-like
Group:     Development/Numerical-Libraries
URL:       http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overview
Packager:  TACC - eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: Parmetis local binary install
Group: System Environment/Base
%description modulefile
This is the long description for the modulefile RPM...

%description
Parmetis package of graph partitioners

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
export dynamic="debug complex complexdebug "

for ext in \
  "" \
  ${dynamic} \
  ; do

echo "module file for ${ext}"

module unload petsc
if [ -z "${ext}" ] ; then
  export architecture=clx
  module load petsc/%{petscversion}
else
  export architecture=clx-${ext}
  module load petsc/%{petscversion}-${ext}
fi


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
The Parmetis module defines the following environment variables:
TACC_PARMETIS_INC and TACC_PARMETIS_LIB for the location
of the Parmetis include files and libraries.

Version %{version}
]] )

whatis( "Name: Parmetis" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://graal.ens-lyon.fr/PARMETIS/" )
whatis( "Description: Numerical library for sparse solvers" )

local             parmetis_arch =    "${architecture}"
local             parmetis_dir  =     "${TACC_PETSC_DIR}"
local             parmetis_inc  = pathJoin(parmetis_dir,parmetis_arch,"include")
local             parmetis_lib  = pathJoin(parmetis_dir,parmetis_arch,"lib")

prepend_path("LD_LIBRARY_PATH", parmetis_lib)

setenv("TACC_PARMETIS_INC",        parmetis_inc )
setenv("TACC_PARMETIS_LIB",        parmetis_lib)

conflict("pmetis")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Parmetis %version
##

set     ModulesVersion      "${modulefilename}"
EOF

## %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua 

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
* Sat Apr 25 2020 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
