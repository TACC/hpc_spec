#
# Si Liu
# 2019-03-01
#

Summary: Boost spec file (www.boost.org)

# Give the package a base name
%define pkg_base_name boost-mpi
%define MODULE_VAR    BOOST_MPI

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 69
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

%define mpi_fam intel

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include python-defines.inc
%define  unified_directories 1
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
#%include  name-defines-python-noreloc.inc
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
Group:     Utility
URL:       http://www.boost.org
Packager:  TACC - siliu@tacc.utexas.edu
Source0:   boost_1_69_0.tar.gz
Source1:   icu4c-63_1-src.tgz

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
  rm -rf $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}

%setup -n boost_%{major_version}_%{minor_version}_%{micro_version}  %{name}-%{version}
%setup -n boost_%{major_version}_%{minor_version}_%{micro_version}  -T -D -a 1

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}
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
# Load Compiler
%include compiler-load.inc
# Load MPI Library
%include mpi-load.inc
# Load Python Library
%include python-load.inc


echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
  mkdir -p %{PYTHON_INSTALL_DIR}
  mount -t tmpfs tmpfs %{PYTHON_INSTALL_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/.tacc_install_canary
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

  WD=`pwd`
 
  TACC_OPT="-xAVX -axCORE-AVX2"
 
  cd icu/source
  CXXFLAGS="%{TACC_OPT}" CFLAGS="%{TACC_OPT}" ./runConfigureICU  $ICU_MODE --prefix=%{PYTHON_INSTALL_DIR}
  make -j 24
  make install
  rm -f ~/user-config.jam

  cd $WD
  EXTRA="-sICU_PATH=%{PYTHON_INSTALL_DIR}"
  CONFIGURE_FLAGS="$CONFIGURE_FLAGS --with-libraries=all"

  CC=mpicxx
  CXX=mpicxx

  ./bootstrap.sh --prefix=%{PYTHON_INSTALL_DIR} ${CONFIGURE_FLAGS}
  echo "using mpi : /opt/apps/intel18/impi/18.0.2/bin/mpicxx ;" >> ~/projet-config.jam

  ./b2 -j 24 --prefix=%{PYTHON_INSTALL_DIR} $EXTRA cxxflags="%{TACC_OPT}" cflags="%{TACC_OPT}" linkflags="%{TACC_OPT}" install
  
  mkdir -p              $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
  cp -r %{PYTHON_INSTALL_DIR}/ $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/..


  rm -f ~/tools/build/v2/user-config.jam

  if [ ! -d $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR} ]; then
        mkdir -p $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
  fi

  cp -r %{PYTHON_INSTALL_DIR} $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}/..
  umount %{PYTHON_INSTALL_DIR}

#---------------------- -
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
 
  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/%{version}.lua << 'EOF'
help([[
The boost module file defines the following environment variables:
BOOST_ROOT, TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_INC for
the location of the boost distribution.

To load the mpi boost      do "module load boost-mpi"
To load the rest of boost  do "module load boost"

Version %{version}
]])

whatis("Name: boost")
whatis("Version: %{version}")
whatis("Category: %{group}")
whatis("Keywords: System, Library, C++")
whatis("URL: http://www.boost.org")
whatis("Description: Boost provides free peer-reviewed portable C++ source libraries.")


setenv("TACC_%{MODULE_VAR}_DIR","%{PYTHON_INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_LIB","%{PYTHON_INSTALL_DIR}/lib")
setenv("TACC_%{MODULE_VAR}_INC","%{PYTHON_INSTALL_DIR}/include")
setenv("TACC_%{MODULE_VAR}_BIN","%{PYTHON_INSTALL_DIR}/bin")
setenv("BOOST_ROOT","%{PYTHON_INSTALL_DIR}")

conflict("boost","boost-mpi")

-- Add boost to the LD_LIBRARY_PATH
prepend_path("LD_LIBRARY_PATH","%{PYTHON_INSTALL_DIR}/lib")
prepend_path("PATH", "%{PYTHON_INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PYTHON_MODULE_VAR}%{version}
##

set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/%{MODULE_FILENAME}

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

  %if %{?WITH_PYTHON}
    %if %{undefined unified_directories}
      %{PYTHON_INSTALL_DIR}
    %endif
  %endif

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
  
  %if %{?WITH_PYTHON}
    %if %{undefined unified_directories}
      %{PYTHON_MODULE_DIR}
    %endif
  %endif

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
