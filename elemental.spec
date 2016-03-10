#
# Adapted from Bar.spec by Victor Eijkhout 2016/02/15
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

Summary: Elemental rpm build script

# Give the package a base name
# !!! Jack releases the tarballs as "Elemental-0.85.tgz". I rename this to "elemental-0.85.tgz" !!!
%define pkg_base_name elemental
%define MODULE_VAR    ELEMENTAL

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 20160229

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1
License: Jack Poulson
Vendor: http://libelemental.org/
Group: libFlame
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Elemental rpm building
Group: HPC/libraries
%description package
ELEMENTAL is a package of distributed dense linear algebra routines.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
ELEMENTAL is a package of distributed dense linear algebra routines.

%description
ELEMENTAL is a package of distributed dense linear algebra routines.
Details.....

#---------------------------------------
%prep
#---------------------------------------

# just for compatibility with stampede spec file
%define elemental_install_dir %{INSTALL_DIR}

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
%include compiler-load.inc
%include mpi-load.inc

export modulefilename=%{pkg_version}

# Insert necessary module commands
module load cmake
export BLAS_LAPACK_LOAD=--with-blas-lapack-dir=${MKLROOT}

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

export ELEMENTAL_RELEASES="PureDebug PureRelease HybridDebug HybridRelease"

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
  
export ELEMENTAL_DIR=`pwd`

mkdir -p %{elemental_install_dir}
mount -t tmpfs tmpfs %{elemental_install_dir} 

#for ext in PureRelease ; do
for ext in ${ELEMENTAL_RELEASES} ; do

  ( mkdir -p build/${ext} ; \
      cd build/${ext} ; \
      cmake -D CMAKE_BUILD_TYPE=${ext} \
      	    -D CMAKE_INSTALL_PREFIX=%{elemental_install_dir}/${ext} \
	    -D MATH_LIBS="-mkl" \
	    ../.. ; \
      make -j 2 VERBOSE=1 2>&1 | tee make.log ; \
      make install ; \
      rm -rf bin/tests \
  )

done

cp -r %{elemental_install_dir}/* $RPM_BUILD_ROOT/%{elemental_install_dir}/
umount tmpfs

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
  
# same loop as for the software
for ext in ${ELEMENTAL_RELEASES} ; do

export moduleversion=%{version}-${ext}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${moduleversion}.lua << EOF
help( [[
The ELEMENTAL modulefile defines the following environment variables:
TACC_ELEMENTAL_DIR, TACC_ELEMENTAL_LIB, and TACC_ELEMENTAL_INC
for the location of the ELEMENTAL %{version} distribution, 
libraries, and include files, respectively.

Version: ${moduleversion}
]] )

whatis( "Name: Elemental" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${moduleversion}" )
whatis( "Category: library, mathematics" )
whatis( "Keywords: Linear Algebra, Library, Mathematics, Parallel" )
whatis( "URL: http://libelemental.org/" )
whatis( "Description: Library for distributed dense linear algebra" )

local             elemental_dir =        "%{elemental_install_dir}/${ext}"

prepend_path("PATH", pathJoin(elemental_dir,"bin") )

setenv(          "TACC_ELEMENTAL_DIR",        elemental_dir )
setenv(          "TACC_ELEMENTAL_LIB",        pathJoin(elemental_dir,"lib") )
setenv(          "TACC_ELEMENTAL_INC",        pathJoin(elemental_dir,"include") )
setenv(          "TACC_ELEMENTAL_VARIANT",    "${ext}" )
setenv(          "TACC_ELEMENTAL_VERSION",    "%{version}" )

EOF
#Also TACC_ELEMENTAL_LINK for the full content of a link line"
#setenv(          "TACC_ELEMENTAL_LINK",       "-L\$elemental_dir/build/${ext} -lelemental -L\$elemental_dir/build/${ext}/contrib/pmrrr -lpmrrr -llapack-addons -L/opt/apps/intel/11.1/mkl/lib/em64t -lmkl_intel_ilp64 -lmkl_sequential -lmkl_core -lguide -lpthread -L/opt/apps/intel/11.1/lib/intel64/ -lifcore" )

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${moduleversion} << EOF
#%Module1.0##################################################
##
## version file for elemental
##
 
set     ModulesVersion      "${moduleversion}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${moduleversion}.lua

done

cp -r examples %{elemental_install_dir}

##
## end of configure install section
##

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
# %post %{MODULEFILE}
# export MODULEFILE_POST=1
# %include post-defines.inc
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
#
* Tue Jan 26 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial install
