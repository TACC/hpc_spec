# Amit Ruhela
# Sept 29, 2021
#
# Typical Command-Line Example:
# ./build_rpm.sh  -i19 charliecloud.spec
# ./build_rpm.sh  --gcc=91 charliecloud.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps tacc-charliecloud-package-0.24-1.el7.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps tacc-charliecloud-modulefile-0.24-1.el7.x86_64.rpm
# rpm -e tacc-charliecloud-package tacc-charliecloud-modulefile

Summary: Charliecloud provides user-defined software stacks (UDSS) for HPC.

# Give the package a base name
%define pkg_base_name charliecloud
%define MODULE_VAR    charliecloud

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 25
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc
#%include compiler-defines.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc
#%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

%define INSTALL_DIR  %{INSTALL_PREFIX}/%{pkg_base_name}/%{pkg_version}

Release:   1%{?dist}
License:   GPL
Group:     System Environment/Base
URL:       https://github.com/hpc/charliecloud
Packager:  aruhela@tacc.utexas.edu

Source:    charliecloud-%{pkg_version}.tar.gz

%package %{PACKAGE}
Summary: Containerization Library
Group: Development/Libraries
%description package

%package %{MODULEFILE}
Summary: Containerization Library
Group: Lmod/Modulefiles
%description modulefile
Charliecloud provides containerization runtime for various applictaions.

%description
Charliecloud provides containerization runtime for various applictaions.

#---------------------------------------
%prep
#---------------------------------------

%define debug_package %{nil}
%define dbg           %{nil}

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  cd %{_topdir}/BUILD
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  rm -rf charliecloud-*
  #git clone https://github.com/hpc/charliecloud.git
  wget https://github.com/hpc/charliecloud/releases/download/v%{pkg_version}/charliecloud-%{pkg_version}.tar.gz
  tar -xzf charliecloud-%{pkg_version}.tar.gz
  rm charliecloud-%{pkg_version}.tar.gz

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

# Insert necessary module commands
module purge
#ml use /opt/apps/intel19/modulefiles
#module available
#module load python3

# Insert further module commands
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

  cd charliecloud-%{pkg_version}
  #echo "INSTALLDIR=%{INSTALL_DIR}"
  ./configure --prefix=%{INSTALL_DIR}  CC=gcc
  make -j 20
  make DESTDIR=$RPM_BUILD_ROOT install
  cd ..
  #ls $RPM_BUILD_ROOT

# Copy everything from tarball over to the installation directory
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
local help_message=[[
The charliecloud modulefile defines the following environment variables:
TACC_CHARLIECLOUD_DIR, TACC_CHARLIECLOUD_BIN, and TACC_CHARLIECLOUD_LIB
for the location of the charliecloud distribution, binaries, include,
and libraries respectively.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: charliecloud")
whatis("Version: %{version}")
whatis("Category: library, containerization")
whatis("URL: https://hpc.github.io/charliecloud/")
whatis("Description: Containerization Runtime")

-- Create environment variables --

local base_dir = "%{INSTALL_DIR}"

setenv("TACC_charliecloud_DIR",          base_dir)
setenv("TACC_charliecloud_BIN",          pathJoin( base_dir , "bin"))
setenv("TACC_charliecloud_LIB",          pathJoin( base_dir , "lib"))
prepend_path("PATH",            pathJoin( base_dir , "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin( base_dir , "lib"))

family("containers")
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
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#---------------------------

  %defattr(-,root,install,)
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

