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
%define pkg_base_name paraview
%define MODULE_VAR    PARAVIEW

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

Release:   1%{?dist}
License:   GPL
Group:     Software/Library
URL:       http://www.paraview.org/
Packager:  TACC - gda@tacc.utexas.edu (pnav on Hikari)
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%define paraview_version %{version}


%package %{PACKAGE}
Summary: The package RPM
Group: Software/Library
%description package
ParaView is an open-source, multi-platform data analysis and visualization application. ParaView users can quickly build visualizations to analyze their data using qualitative and quantitative techniques. The data exploration can be done interactively in 3D or programmatically using ParaView’s batch processing capabilities.

ParaView was developed to analyze extremely large datasets using distributed memory computing resources. It can be run on supercomputers to analyze datasets of petascale size as well as on laptops for smaller data, has become an integral tool in many national laboratories, universities and industry, and has won several awards related to high performance computation.

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

#%setup -n %{pkg_base_name}-%{pkg_version}

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
%define package_version %{major_version}.%{minor_version}.%{micro_version} 
  rm -rf %{_sourcedir}/ParaView-v%{package_version}

  cd %{_sourcedir}
  wget -O ParaView-v%{package_version}.tar.gz "https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v%{major_version}.%{minor_version}&type=binary&os=Sources&downloadFile=ParaView-v%{package_version}.tar.gz"

  tar xf ParaView-v%{package_version}.tar.gz
  rm -f ParaView-v%{package_version}.tar.gz

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
#%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  export QA_SKIP_BUILD_ROOT=1

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
  
  # Copy everything from tarball over to the installation directory
  # cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  export WORK_DIR=`pwd`
  export WORK_INSTALL_DIR=$RPM_BUILD_ROOT/%{INSTALL_DIR}
  #export CFLAGS='%{TACC_OPT}'

  mkdir -p $WORK_INSTALL_DIR/bin

  module load cmake
  module load intel/16.0.1 
  module load impi
  module load qt5
  module load swr 
  #module load python
  module load ospray/1.4.3
  module load boost
  
    cd $WORK_DIR
    rm -rf %{pkg_base_name}
    mkdir %{pkg_base_name}
    cd %{pkg_base_name}
    CC=icc CXX=icpc cmake %{_sourcedir}/ParaView-v%{package_version} -DCMAKE_C_FLAGS="-Doff64_t=__off64_t" \
	-DModule_VisItLib=ON \
 	-DModule_vtkIOVisItBridge=ON \
 	-DPARAVIEW_USE_VISITBRIDGE=ON \
	-DBoost_DIR=$TACC_BOOST_DIR \
        -DBoost_INCLUDE_DIR:PATH=$TACC_BOOST_INC \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_INSTALL_PREFIX=$WORK/paraview-%{major_version}.%{minor_version}/pv \
	-DCMAKE_BUILD_TYPE=Release \
	-DPARAVIEW_QT_VERSION=5 \
	-DQt5_DIR=$TACC_QT5_LIB/cmake/Qt5 \
	-DPARAVIEW_USE_MPI=ON \
	-DPARAVIEW_ENABLE_PYTHON=ON \
	-DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON \
	-DPARAVIEW_USE_OSPRAY=ON \
	-Dospray_DIR=$TACC_OSPRAY_LIB/cmake/ospray-1.4.3 \
	-Dembree_DIR=$TACC_OSPRAY_LIB/cmake/embree-2.16.5 \
	-DVTK_OPENGL_HAS_OSMESA=OFF \
	-DVTK_USE_OFFSCREEN=OFF \
 	-DOSPRAY_INSTALL_DIR=$TACC_OSPRAY_LIB/cmake/ospray-1.4.3 \
	-DOSPRAY_BUILD_DIR=$TACC_OSPRAY_LIB/cmake/ospray-1.4.3 \
        -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python2 \
        -DPYTHON_INCLUDE_DIR:PATH=/usr/include/python2.7 \
        -DPYTHON_LIBRARY:FILEPATH=/usr/lib64/libpython2.7.so

    make 
    make install

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
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.
]]

--help(help_msg)
help(help_msg)

whatis("Name: ParaView")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local paraview_dir           = "%{INSTALL_DIR}"

family("paraview")
prepend_path(    "PATH",                pathJoin(paraview_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(paraview_dir, "lib"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(paraview_dir, "lib64"))
prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/ospray%{pkg_version}/modulefiles")

setenv( "TACC_%{MODULE_VAR}_DIR",                "%{INSTALL_DIR}")
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(paraview_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(paraview_dir, "lib64"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(paraview_dir, "bin"))

setenv( "embree_DIR",	"%{INSTALL_DIR}")
setenv( "ospray_DIR",	"%{INSTALL_DIR}")
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

