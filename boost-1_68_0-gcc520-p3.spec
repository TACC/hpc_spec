#
# Si Liu 
# 2018-08-10
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
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: Boost spec file (www.boost.org)

# Give the package a base name
%define pkg_base_name boost-p3
%define MODULE_VAR    BOOST-P3

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 68
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

%define mpi_fam none

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
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
Group:     Utility
URL:       http://www.boost.org
Packager:  TACC - siliu@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Boost RPM
Group: Development/System Environment
%description package
Boost provides free peer-reviewed portable C++ source libraries.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Module RPM for Boost

%description

Boost emphasizes libraries that work well with the C++ Standard
Library. Boost libraries are intended to be widely useful, and usable
across a broad spectrum of applications. The Boost license encourages
both commercial and non-commercial use.

Boost aims to establish "existing practice" and provide reference
implementations so that Boost libraries are suitable for eventual
standardization. Ten Boost libraries are already included in the C++
Standards Committee's Library Technical Report (TR1) as a step toward
becoming part of a future C++ Standard. More Boost libraries are
proposed for the upcoming TR2.

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


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
#%include mpi-defines.inc
module purge
%include compiler-load.inc
#module load intel/18.0.2 
module load gcc/5.2.0
module load python3

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

  ICU_MODE=Linux
  %if "%{comp_fam}" == "intel"
        export CONFIGURE_FLAGS=--with-toolset=intel-linux
        ICU_MODE=Linux/ICC
  %endif


  %if "%{mpi_fam}" != "none"
        CXX=mpicxx
  %endif

  %if "%{comp_fam}" == "gcc"
        export CONFIGURE_FLAGS=--with-toolset=gcc
  %endif

  rm -f icu4c-56_1-src.tgz*
  rm -f boost_1_68_0.tar.gz*
  wget http://download.icu-project.org/files/icu4c/56.1/icu4c-56_1-src.tgz
  wget http://downloads.sourceforge.net/project/boost/boost/1.68.0/boost_1_68_0.tar.gz 
  tar -xzf icu4c-56_1-src.tgz
  tar -xzf boost_1_68_0.tar.gz
  WD=`pwd`

#  if [ "$CXX" != mpicxx ]; then
    	cd icu/source
    	./runConfigureICU  $ICU_MODE --prefix=%{INSTALL_DIR}
    	make -j 10
    	make install
    	rm -f ~/user-config.jam
#  fi

  cd $WD
  cd boost_1_68_0
  EXTRA="-sICU_PATH=%{INSTALL_DIR}"
  #if [ "$CXX" = mpicxx ]; then
 # 	CONFIGURE_FLAGS="$CONFIGURE_FLAGS --with-libraries=mpi"
 # 	EXTRA=""
 # 	mpipath=`which mpicxx`
#	cat > $WD/tools/build/v2/user-config.jam << EOF
#	#using mpi $mpipath ;
#	using mpi ;
#	EOF
#  else
  	CONFIGURE_FLAGS="$CONFIGURE_FLAGS --with-libraries=all --without-libraries=mpi"
#  fi


  echo "using python : 3.7 : /opt/apps/gcc5_2/python3/3.7.0/bin/python3 ;" >> user-config.jam 
  ./bootstrap.sh --prefix=%{INSTALL_DIR} ${CONFIGURE_FLAGS}
  ./b2 -j 10 --prefix=%{INSTALL_DIR} $EXTRA install

  mkdir -p              $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..


  rm -f ~/tools/build/v2/user-config.jam

  if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  	mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  fi

  cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}

#---------------------- - 
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
help([[
The boost module file defines the following environment variables:"
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_INC for"
the location of the boost distribution."

To load the mpi boost      do "module load boost-mpi"
To load the rest of boost  do "module load boost"

It is save to load both.

Version %{version}"
]])

whatis("Name: boost")
whatis("Version: %{version}")
whatis("Category: %{group}")
whatis("Keywords: System, Library, C++")
whatis("URL: http://www.boost.org")
whatis("Description: Boost provides free peer-reviewed portable C++ source libraries %{BOOST_TYPE}.")


setenv("TACC_%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_%{MODULE_VAR}_INC","%{INSTALL_DIR}/include")

always_load("python3")
conflict("boost","boost-mpi","boost-p3")

-- Add boost to the LD_LIBRARY_PATH
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{MODULE_VAR}%{version}
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

