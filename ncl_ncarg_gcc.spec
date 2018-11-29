#
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
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

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name ncl_ncarg
%define MODULE_VAR    ncl_ncarg
#gcc binary
%define SOURCE_NAME   ncl_ncarg-6.3.0.Linux_RHEL6.4_x86_64_nodap_gcc472

# Create some macros (spec file variables)
%define major_version 6
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
##NOPE!! don't need to tell it use the system gcc!!!
##%include compiler-defines.inc
#%include mpi-defines.inc
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

#Name: ncl_ncarg
Release:   2
License: http://www.ncl.ucar.edu/Download/NCL_binary_license.shtml
Group:     applications/io
Source:    %{SOURCE_NAME}.tar.gz
URL: http://www.ncl.ucar.edu/Download/
Distribution: RedHat Linux 6.4 x86_64 nodap gcc 4.7.2 
Vendor: Computational & Information Systems Laboratory, National Center for Atmospheric Research

Source1: pixman-0.34.0.tar.gz
Source2: cairo-1.14.8.tar.xz

Packager:  TACC - cazes@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: NCAR Languange and NCAR Graphics
Group: applications/io
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: NCAR Languange and NCAR Graphics
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description 
NCAR Command Language (NCL) is an interpreted language designed for
scientific data analysis and visualization
Includes NCAR Graphics functionality
Supports netcdf3/4, GRIB1/2, HDF-SDS, HDF4-EOS, binary, shapefiles, and 
ascii
* a library containing over two dozen Fortran/C utilities for drawing contours, 
  maps, vectors, streamlines, weather maps, surfaces, histograms, X/Y plots, annotations, and more
* an ANSI/ISO standard version of GKS, with both C and FORTRAN callable entries
* a math library containing a collection of C and Fortran interpolators and approximators
  for one-dimensional, two-dimensional, and three-dimensional data
* applications for displaying, editing, and manipulating graphical output
* map databases
* hundreds of FORTRAN and C examples
* demo programs
* compilation scripts

http://www.ncl.ucar.edu/index.shtml



#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
# system version
%define INSTALL_DIR %{APPS}/%{pkg_base_name}/%{version}
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# %setup expects it to untar into a directory called %{name}-%{version};
# otherwise you have to pass it the -n switch, which renames the
# directory. The important %setup switches are:
# -n <name>    (name of build directory)
# -c           (creates top-level build directory)
# -D           (don't delete top-level build directory)
# -T           (don't unpack Source0)
# -a <n>       (unpack Source number n, after cd'ing to build directory)
# -a <n>       (unpack Source number n, before cd'ing to build directory)
# -q           (unpack silently)

# This binary package unpacks to '.' by default.  We'll unpack to
# a subdirectory that we'll also create using the -c option
%setup -c -n %{name}-%{version}

#This untars pixman-0.34.0
%setup -T -D -a 1
#This untars libcairo-1.14.8
%setup -T -D -a 2

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  %define MODULE_DIR  %{APPS}/%{MODULES}/%{pkg_base_name}
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

###Nope don't need it using system gcc
### Load Compiler
##%include compiler-load.inc
### Load MPI Library
###%include mpi-load.inc
  export CC=gcc
  export CXX=g++
  export FC=gfortran
  export F77=gfortran
  export FC=gfortran

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"

#Build pixman
cd pixman-0.34.0
export PIXMAN_DIR=%{INSTALL_DIR}/pixman_0.34.0
./configure --prefix=$PIXMAN_DIR
make 
make install
cd ../

#Build libcairo
cd cairo-1.14.8
export pixman_LIBS=" -L${PIXMAN_DIR}/lib -lpixman-1 "
export pixman_CFLAGS=" -I${PIXMAN_DIR}/include/pixman-1 "
export CFLAGS=" -I${PIXMAN_DIR}/include/pixman-1 "
export CAIRO_DIR=%{INSTALL_DIR}/cairo_1.14.8
./configure --prefix=$CAIRO_DIR
make 
make install
cd ../

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
  
  #Copy bin/libs/docs over
  cp -r bin $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r include $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r $PIXMAN_DIR $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r $CAIRO_DIR $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
--ncl_ncarg

local help_message = [[
The ncarg_ncl module file defines the following environment variables:
NCARG_ROOT, TACC_NCARG_ROOT, TACC_NCARG_BIN, TACC_NCARG_LIB, and 
TACC_NCARG_INC for the location of the NCARG distribution, binaries,
libraries, and include files, respectively.

To use the NCARG library, compile the source code with the option:

	-I$TACC_NCARG_INC 

and add the following options to the link step: 

	-L$TACC_NCARG_LIB -lncarg

(or another of the available libraries that is appropriate to your application) 

Version 6.1.2

]]

help(help_message,"\n")

whatis("ncarg: NCAR Graphics utilities")
whatis("Version: %{version}")
whatis("Category: utility, runtime support")
whatis("Keywords: Graphics, Utility")
whatis("Description: A library of graphics utilites from the Natl. Center for Atmospheric Research." )
whatis("URL: http://ngwww.ucar.edu/")


prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("MANPATH","%{INSTALL_DIR}/man")
prepend_path("LIBRARY_PATH","%{INSTALL_DIR}/cairo_1.14.8/lib")

setenv("NCARG_ROOT","%{INSTALL_DIR}")
setenv("TACC_NCARG_ROOT","%{INSTALL_DIR}")
setenv("TACC_NCARG_INC","%{INSTALL_DIR}/include")
setenv("TACC_NCARG_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_NCARG_BIN","%{INSTALL_DIR}/bin")

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
#%post %{PACKAGE}
#export PACKAGE_POST=1
#%include post-defines.inc
#%post %{MODULEFILE}
#export MODULEFILE_POST=1
#%include post-defines.inc
#%preun %{PACKAGE}
#export PACKAGE_PREUN=1
#%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

