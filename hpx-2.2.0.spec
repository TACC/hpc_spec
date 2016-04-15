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

Summary: Hpx rpm build script

# Give the package a base name
%define pkg_base_name hpx
%define MODULE_VAR    HPX

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}
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

Release:   2
License:   GPL
Group:     Development/Tools
URL:       https://hpx.crest.iu.edu/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Hpx rpm building
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
module load boost cmake python swig
# python

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

export INSTALL_LOCATION=%{INSTALL_DIR}
rm -rf CMakeCache.txt CMakeFiles
echo "cmaking in" `pwd`

export VERSION=%{version}
export HPX_LOCATION=%{_topdir}/BUILD/

export GCC_VERSION=4.9.3
export CPP_PATHS="-I/opt/apps/gcc/${GCC_VERSION}/include/c++/${GCC_VERSION} -I/opt/apps/gcc/${GCC_VERSION}/include/c++/${GCC_VERSION}/x86_64-unknown-linux-gnu "
# leads to: /opt/apps/gcc/4.9.3/include/c++/4.9.3/ext/atomicity.h(49): error: identifier "__ATOMIC_ACQ_REL" is undefined

cp -r hpx-apps %{INSTALL_DIR}

cd hpx
./configure --prefix=%{INSTALL_DIR} \
    CC=mpicc CXX=mpicxx --enable-mpi CFLAGS="-O3 -g" CXXFLAGS="-O3 -g" \
    --enable-photon PHOTON_CARGS="--enable-ugni --disable-libfabric" --enable-hugetlbfs \
    --enable-rebalancing --enable-hpx++ \
    TESTS_CMD=ibrun
export noopt="\
--hpx-parcel-compression \
    "
make

####
#### Testing
####

####
#### Install permanently
####

make install

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

# Write out the modulefile associated with the application
# The hpx module defines the following environment variables:
# TACC_HPX_DIR, TACC_HPX_BIN, and
# TACC_HPX_LIB for the location
# of the Hpx distribution, documentation, binaries,
# and libraries.

# Version %{version}
# ]] )
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
local help_msg=[[ 
This module sets the environment variables
TACC_HPX_DIR, TACC_HPX_BIN, TACC_HPX_INC, TACC_HPX_LIB.

HPX examples can be found in TACC_HPX_DIR/hpx_apps.
To build an example do first
  ./configure CC=mpicc CXX=mpicxx CFLAGS="-O3" CXXFLAGS="-O3"
in the example directory.
 ]]
help( help_msg )

whatis( "Name: Hpx" )
whatis( "Version: %{version}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://hpx.crest.iu.edu/" )
whatis( "Description: Parallel programming system" )

local             hpx_dir =     "%{INSTALL_DIR}"

prepend_path("PATH",            pathJoin(hpx_dir,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(hpx_dir,"lib64") )
prepend_path("LD_LIBRARY_PATH", pathJoin(hpx_dir,"lib") )
prepend_path("PKG_CONFIG_PATH", pathJoin(hpx_dir,"lib","pkgconfig") )

setenv("TACC_HPX_DIR",        hpx_dir)
setenv("TACC_HPX_BIN",        pathJoin(hpx_dir,"bin") )
setenv("TACC_HPX_INC",        pathJoin(hpx_dir,"include") )
setenv("TACC_HPX_LIB",        pathJoin(hpx_dir,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Hpx %version
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
* Mon Mar 28 2016 eijkhout <eijkhout@tacc.utexas.edu>
* Wed Mar 02 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
