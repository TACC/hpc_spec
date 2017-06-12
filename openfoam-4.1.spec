#
# Si Liu
# 2017-05-16
#

# Give the package a base name
%define pkg_base_name openfoam
%define MODULE_VAR    OPENFOAM

# Create some macros (spec file variables)
%define major_version 4
%define minor_version 1
%define pkg_version %{major_version}.%{minor_version}


Summary: Open Field Operation And Manipulation(OpenFOAM)
Release: 1%{?dist}
License: General Public Licence (GPL).
Vendor: OpenFOAM Foundation
Group: Utility/CFD
Source: %{name}-%{version}.tar.gz
Packager:  TACC - siliu@tacc.utexas.edu

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
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

%define INSTALL_DIR /home1/apps/OpenFOAM/

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%define APPS /home1/apps/
%define MODULES modulefiles

%package %{PACKAGE}
Summary: The package RPM
Group: OpenFOAM
%description package
OpenFOAM® is the leading free, open source software for computational fluid dynamics (CFD), owned by the OpenFOAM Foundation and distributed exclusively under the General Public Licence (GPL). 

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile

%description



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

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
##  mount -t tmpfs tmpfs %{INSTALL_DIR}
  
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
  
# Write out the modulefile associated with the application

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[

The OpenFOAM (Open Field Operation and Manipulation) CFD Toolbox is a free, open source CFD software package.
This module is for OpenFOAM 4.1 compiled with Intel 17.0.4 and impi 17.0.3.

This OpenFOAM module defines a lot of environment variables from OpenFOAM bashrc file.
User may also source the following basrc file when necessary
/home1/apps/OpenFOAM/OpenFOAM-4.1/etc/bashrc

We suggest users set their own WM_PROJECT_USER_DIR and FOAM_RUN environment for their own OpenFOAM runs.
Typical settings could be:
export WM_PROJECT_USER_DIR=$WORK/OpenFOAM/personal-4.1
export FOAM_RUN=$WORK/OpenFOAM/personal-4.1/run

OpenFOAM user guide can be reached at
https://cfd.direct/openfoam/user-guide

For extra OpenFOAM support, please contact
https://cfd.direct/contact/

Version 4.1
]]
)

whatis("Name: OpenFOAM")
whatis("Version: 4.1")
whatis("Category: CFD")
whatis("Keywords: CFD, Tools")
whatis("URL: https://openfoam.org/")
whatis("Description: OpenFOAM 4.1")

setenv("FOAM_APP","/home1/apps/OpenFOAM/OpenFOAM-4.1/applications")
setenv("FOAM_APPBIN","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/bin")
setenv("FOAM_ETC","/home1/apps/OpenFOAM/OpenFOAM-4.1/etc");
setenv("FOAM_EXT_LIBBIN","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64IccDPInt32/lib")
setenv("FOAM_INST_DIR","/home1/apps/OpenFOAM")
setenv("FOAM_JOB_DIR","/home1/apps/OpenFOAM/jobControl")
setenv("FOAM_LIBBIN","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64IccDPInt32/lib")
setenv("FOAM_MPI","impi")
setenv("FOAM_SETTINGS","")
setenv("FOAM_SIGFPE","")
setenv("FOAM_SITE_APPBIN","/home1/apps/OpenFOAM/site/4.1/platforms/linux64IccDPInt32Opt/bin")
setenv("FOAM_SITE_LIBBIN","/home1/apps/OpenFOAM/site/4.1/platforms/linux64IccDPInt32Opt/lib")
setenv("FOAM_SOLVERS","/home1/apps/OpenFOAM/OpenFOAM-4.1/applications/solvers")
setenv("FOAM_SRC","/home1/apps/OpenFOAM/OpenFOAM-4.1/src")
setenv("FOAM_TUTORIALS","/home1/apps/OpenFOAM/OpenFOAM-4.1/tutorials")
setenv("FOAM_UTILITIES","/home1/apps/OpenFOAM/OpenFOAM-4.1/applications/utilities")

setenv("FOAMY_HEX_MESH","yes")

-- The following lines have been manually modified by Si Liu on May 20, 2017
prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64Icc/boost_1_63_0/lib")
prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64Icc/CGAL-4.8/lib")

prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/lib/impi")
prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64IccDPInt32/lib/impi")

prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/lib")

prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/site/4.1/platforms/linux64IccDPInt32Opt/lib")
prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/lib")
prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64IccDPInt32/lib")
prepend_path("LD_LIBRARY_PATH","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/lib/dummy")

setenv("MPI_ARCH_PATH","/opt/intel/impi/2017.3.196/")
setenv("MPI_BUFFER_SIZE","20000000")

-- The following lines have been manually modified by Si Liu on May 21, 2017,
prepend_path("PATH","/home1/apps/OpenFOAM/site/4.1/platforms/linux64IccDPInt32Opt/bin")
prepend_path("PATH","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/bin")
prepend_path("PATH","/home1/apps/OpenFOAM/OpenFOAM-4.1/bin:/home1/apps/OpenFOAM/OpenFOAM-4.1/wmake")

setenv("CGAL_ARCH_PATH","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64Icc/CGAL-4.8")
setenv("BOOST_ARCH_PATH","/home1/apps/OpenFOAM/ThirdParty-4.1/platforms/linux64Icc/boost_1_63_0")

-- Extra WM environment variables
setenv("WM_ARCH","linux64")
setenv("WM_ARCH_OPTION","64")
setenv("WM_CC","mpicc")
setenv("WM_CFLAGS","-O3 -xCORE-AVX2 -axMIC-AVX512 -fPIC")
setenv("WM_COMPILER","Icc")
setenv("WM_COMPILER_LIB_ARCH","64")
setenv("WM_COMPILE_OPTION","Opt")
setenv("WM_COMPILER_TYPE","system")
setenv("WM_CXX","mpicxx")
setenv("WM_CXXFLAGS","-O3 -xCORE-AVX2 -axMIC-AVX512 -fPIC -std=c++0x")
setenv("WM_DIR","/home1/apps/OpenFOAM/OpenFOAM-4.1/wmake")
setenv("WM_LABEL_OPTION","Int32")
setenv("WM_LABEL_SIZE","32")

setenv("WM_LDFLAGS","-xCORE-AVX2 -axMIC-AVX512 -O3")
setenv("WM_LINK_LANGUAGE","c++")
setenv("WM_MPLIB","IMPI")
setenv("WM_OPTIONS","linux64IccDPInt32Opt")
setenv("WM_OSTYPE","POSIX")
setenv("WM_PRECISION_OPTION","DP")
setenv("WM_PROJECT","OpenFOAM")
setenv("WM_PROJECT_DIR","/home1/apps/OpenFOAM/OpenFOAM-4.1")
setenv("WM_PROJECT_INST_DIR","/home1/apps/OpenFOAM")
setenv("WM_PROJECT_VERSION","4.1")
setenv("WM_THIRD_PARTY_DIR","/home1/apps/OpenFOAM/ThirdParty-4.1")

-- The following lines have been manually modified by Si Liu on July 28, 2014.
setenv("TACC_OPENFOAM_DIR","/home1/apps/OpenFOAM/OpenFOAM-4.1")
setenv("TACC_OPENFOAM_LIB","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/lib")
setenv("TACC_OPENFOAM_BIN","/home1/apps/OpenFOAM/OpenFOAM-4.1/platforms/linux64IccDPInt32Opt/bin")



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

