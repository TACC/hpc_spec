#
# W. Cyrus Proctor
# 2015-11-07
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
%define pkg_base_name basemap
%define MODULE_VAR    BASEMAP

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0
%define micro_version 7

%define geos_major_version 3
%define geos_minor_version 6
%define geos_micro_version 1

%define python_version 2.7.13

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define geos_pkg_version %{geos_major_version}.%{geos_minor_version}.%{geos_micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
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
License:   BSD
Group:     System/Utils
URL:       http://www.cmake.org
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
The matplotlib basemap toolkit is a library for plotting 2D data on maps in
Python. It is similar in functionality to the matlab mapping toolbox, the IDL
mapping facilities, GrADS, or the Generic Mapping Tools. PyNGL and CDAT are
other libraries that provide similar capabilities in Python.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
The matplotlib basemap toolkit is a library for plotting 2D data on maps in
Python. It is similar in functionality to the matlab mapping toolbox, the IDL
mapping facilities, GrADS, or the Generic Mapping Tools. PyNGL and CDAT are
other libraries that provide similar capabilities in Python.

%description
The matplotlib basemap toolkit is a library for plotting 2D data on maps in
Python. It is similar in functionality to the matlab mapping toolbox, the IDL
mapping facilities, GrADS, or the Generic Mapping Tools. PyNGL and CDAT are
other libraries that provide similar capabilities in Python.


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

#%setup -n %{pkg_base_name}-%{pkg_version}


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
%include compiler-load.inc
module load python

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  mount -t tmpfs tmpfs %{INSTALL_DIR}
  
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
 
export ncores=68
export geos=`pwd`/geos
export geos_install=%{INSTALL_DIR}
export GEOS_DIR=${geos_install}

export geos_major=%{geos_major_version}
export geos_minor=%{geos_minor_version}
export geos_patch=%{geos_micro_version}
export geos_version=${geos_major}.${geos_minor}.${geos_patch}


export CC=icc
export CXX=icpc
export CFLAGS="-xCORE-AVX2 -axMIC-AVX512,CORE-AVX512"
export CXXFLAGS="-xCORE-AVX2 -axMIC-AVX512,CORE-AVX512"
export LDFLAGS="-xCORE-AVX2 -axMIC-AVX512,CORE-AVX512"

mkdir -p ${geos}
cd ${geos}

printf "\n\n************************************************************\n"
printf "geos\n"
printf "************************************************************\n\n"

wget http://download.osgeo.org/geos/geos-${geos_version}.tar.bz2
tar xvfj geos-${geos_version}.tar.bz2

cd geos-${geos_version}
${geos}/geos-${geos_version}/configure \
--prefix=${geos_install}               \
--enable-python

make -j ${ncores}
make -j ${ncores} install
 
if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/

########################
########################
########################

export basemap=`pwd`/basemap
export basemap_install=%{INSTALL_DIR}

export basemap_major=%{major_version}
export basemap_minor=%{minor_version}
export basemap_patch=%{micro_version}
export basemap_version=${basemap_major}.${basemap_minor}.${basemap_patch}


export CC=icc
export CXX=icpc
export CFLAGS="-shared -lpthread -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512"
export CXXFLAGS="-shared -lpthread -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512"
export LDFLAGS="-xCORE-AVX2 -axMIC-AVX512,CORE-AVX512"

mkdir -p ${basemap}
cd ${basemap}

printf "\n\n************************************************************\n"
printf "basemap\n"
printf "************************************************************\n\n"

wget http://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-${basemap_version}/basemap-${basemap_version}.tar.gz
tar xvfz basemap-${basemap_version}.tar.gz

cd basemap-${basemap_version}
python setup.py install --prefix=${basemap_install}


 
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
The matplotlib basemap toolkit is a library for plotting 2D data on maps in
Python. It is similar in functionality to the matlab mapping toolbox, the IDL
mapping facilities, GrADS, or the Generic Mapping Tools. PyNGL and CDAT are
other libraries that provide similar capabilities in Python.

This module defines the environmental variables TACC_%{MODULE_VAR}_LIB
and TACC_%{MODULE_VAR}_DIR for the location of the main GEOS directory
and the libraries.

The location of the library files for GEOS and basemap are added to your
LD_LIBRARY_PATH while basemap is also added to your PYTHONPATH.


Version %{version}
]]

prereq("python","%{python_version}")

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: Python Package")
whatis("Keywords: Cartography")
whatis("Description: Plot 2D data on maps in Python")
whatis("URL: https://matplotlib.org/basemap/users/intro.html")

-- Export environmental variables
local basemap_dir="%{INSTALL_DIR}"
local geos_lib=pathJoin(basemap_dir,"lib")
setenv("TACC_%{MODULE_VAR}_DIR",basemap_dir)
setenv("TACC_GEOS_LIB",geos_lib)

-- Prepend the basemap directories to the adequate PATH variables
prepend_path("LD_LIBRARY_PATH", geos_lib)
prepend_path("LD_LIBRARY_PATH", pathJoin(basemap_dir,"lib"))
prepend_path("PYTHONPATH",      pathJoin(basemap_dir,"lib/python2.7/site-packages"))

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
ln -s %{INSTALL_DIR}/lib/python2.7/site-packages/mpl_toolkits/basemap /opt/apps/intel17/python/%{python_version}/lib/python2.7/site-packages/mpl_toolkits/basemap
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
unlink /opt/apps/intel17/python/%{python_version}/lib/python2.7/site-packages/mpl_toolkits/basemap
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

