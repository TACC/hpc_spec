#
# Adapted from Bar.spec by Victor Eijkhout 2015/11/30
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

Summary: Libmesh rpm build script

# Give the package a base name
%define pkg_base_name libmesh
%define MODULE_VAR    LIBMESH

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

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
License:   GPL
Group:     Development/Tools
URL:       http://libmesh.github.io/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Libmesh rpm building
Group: HPC/libraries
%description package
Portable Extendible Toolkit for Scientific Computations

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
The longer-winded description of the package that will 
end in up inside the rpm and is queryable if installed via:
rpm -qi <rpm-name>


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_full_version}

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
module load boost cmake python trilinos

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
  
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

# VLE here is where we start copying from the old spec file
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

export SOFTDIR=`pwd` # here is where we deposit the log files
export LIBMESH_INSTALLATION=%{INSTALL_DIR}

# and here is where we do the configure and compile
rm -rf /tmp/libmesh-build
mkdir -p /tmp/libmesh-build
pushd /tmp/libmesh-build

export VERSION=%{version}
export LIBMESH_DIR=%{_topdir}/BUILD//libmesh-${VERSION}

## VLE remove this when Cyrus adds them to 
%if "%{comp_fam}" != "intel"
  export MKLROOT=/opt/apps/intel/16/compilers_and_libraries_2016.0.109/linux/mkl
%endif
export TACC_MKL_DIR=${MKLROOT}
export TACC_MKL_LIB=${MKLROOT}/lib/intel64
export TACC_MKL_INC=${MKLROOT}/include

export GCC_VERSION=4.9.3
export CPP_PATHS="-I/opt/apps/gcc/${GCC_VERSION}/include/c++/${GCC_VERSION} -I/opt/apps/gcc/${GCC_VERSION}/include/c++/${GCC_VERSION}/x86_64-unknown-linux-gnu "
# leads to: /opt/apps/gcc/4.9.3/include/c++/4.9.3/ext/atomicity.h(49): error: identifier "__ATOMIC_ACQ_REL" is undefined

####
#### Configure
####

${LIBMESH_DIR}/configure --prefix=${LIBMESH_INSTALLATION} \
  --with-trilinos=${TACC_TRILINOS_DIR} \
  --with-boost=${TACC_BOOST_DIR} \
  2>&1 | tee ${SOFTDIR}/configure.log

####
#### Compile
####

make 2>&1 | tee ${SOFTDIR}/make.log

####
#### Install permanently
####

make install

popd

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The libmesh module defines the following environment variables:
TACC_LIBMESH_DIR, TACC_LIBMESH_BIN, and
TACC_LIBMESH_LIB for the location
of the Libmesh distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Libmesh" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/libmesh/libmesh-as/" )
whatis( "Description: Numerical library for sparse linear algebra" )

local             libmesh_arch =    "${architecture}"
local             libmesh_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(libmesh_dir,libmesh_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(libmesh_dir,libmesh_arch,"lib") )

setenv("LIBMESH_ARCH",            libmesh_arch)
setenv("LIBMESH_DIR",             libmesh_dir)
setenv("TACC_LIBMESH_DIR",        libmesh_dir)
setenv("TACC_LIBMESH_BIN",        pathJoin(libmesh_dir,libmesh_arch,"bin") )
setenv("TACC_LIBMESH_LIB",        pathJoin(libmesh_dir,libmesh_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Libmesh %version
##

set     ModulesVersion      "${modulefilename}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua

##
## end of configure install section
##

module unload python
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

#tacctmpfs -u %{INSTALL_DIR}
umount tmpfs

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
#
* Thu Aug 04 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
