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
%define pkg_base_name namd
%define MODULE_VAR    NAMD

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 10
%define micro_version 0

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
License:   GPL
Group:     Theoretical and Computational Biophysics Group, UIUC
URL:       http://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=NAMD
Packager:  TACC - huang@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Source1:   tcl8.5.9-crayxe.tar.gz
Source2:   fftw-crayxt3.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: The namd distribution for login and compute nodes. Uses charm 6.6.1
Group: Applications/Chemistry
%description package
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

%description
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

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

%setup -n %{pkg_base_name}-%{pkg_version}

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
%include mpi-load.inc

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

tar -xvf charm-6.6.1.tar
cd charm-6.6.1/
cp src/arch/mpi-linux-x86_64/cc-mpicxx.sh cc-mpicxx.sh.bak
cat src/arch/mpi-linux-x86_64/cc-mpicxx.sh | sed 's/\-show 2>\/dev\/null/\-v 2>\&1 \| head -n 1/g' > 1 ; mv 1 src/arch/mpi-linux-x86_64/cc-mpicxx.sh
env MPICXX=mpicxx CC=icc CXX=icpc ./build charm++ mpi-linux-x86_64 mpicxx --no-build-shared --with-production -j10
cd ..

tar -zxvf $RPM_SOURCE_DIR/fftw-crayxt3.tar.gz
#tar -zxvf $RPM_SOURCE_DIR/tcl8.5.9-crayxe.tar.gz
tar -zxvf $RPM_SOURCE_DIR/tcl8.5.9-crayxe-threaded.tar.gz


export namd_home=`pwd`
cat arch/Linux-x86_64-icc.arch  | sed 's/-ip -no-vec/-ip -xCORE-AVX2 -no-vec/g' > 1.tmp ; mv 1.tmp arch/Linux-x86_64-icc.arch
./config Linux-x86_64-icc --charm-arch mpi-linux-x86_64-mpicxx --with-fftw --fftw-prefix $namd_home/fftw-crayxt3 --with-tcl --tcl-prefix $namd_home/tcl8.5.9-crayxe-threaded
cd Linux-x86_64-icc
make -j 20
  
# Create some dummy directories and files for fun
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

cd ..
cp -p Linux-x86_64-icc/{namd2,psfgen,flipbinpdb,flipdcd,sortreplicas} $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}
chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}


# Copy everything from tarball over to the installation directory
#  cp * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  echo "Here: -----"
  echo $RPM_BUILD_ROOT
  echo "cyrus %{MODULE_PREFIX}"
  echo "cyrus %{MODULE_SUFFIX}"
  echo "cyrus %{MODULE_DIR}"
  echo "cyrus %{MODULE_FILENAME}"
  echo "cyrus %{INSTALL_PREFIX}"
  echo "cyrus %{INSTALL_SUFFIX}"
  echo "cyrus %{INSTALL_DIR}"

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

The TACC NAMD module appends the path to the namd2 executable
to the PATH environment variable. Also TACC_NAMD_DIR, 
TACC_NAMD_BIN, and TACC_NAMD_LIB are set to NAMD home 
bin, and lib directories; lib directory contains information for
ABF, random acceleration MD(RAMD), replica exchange MD(REMD). 
Usage: ibrun namd2          INPUT 
Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: NAMD")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL: http://www.ks.uiuc.edu/Research/namd/")
whatis("Description: Scalable Molecular Dynamics software")

-- Create environment variables.
local namd_dir           = "%{INSTALL_DIR}"

family("namd")
prepend_path(    "PATH",                pathJoin(namd_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_DIR",                namd_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(namd_dir, "bin"))
EOF

#prepend_path(    "MODULEPATH",         "%{MODULE_PREFIX}/namd_1/modulefiles")
  
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

