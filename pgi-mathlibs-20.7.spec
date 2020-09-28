#
# Amit Ruhela
# 2020-10-08 Add name-defines-noreloc.inc
# 2020-10-08 Need to investigate relocation -- use /opt/apps for now
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
# rpm -qilp tacc-pgi-package-20.7.0-1.el7.x86_64.rpm
# rpm -qilp tacc-pgi-modulefile-20.7.0-1.el7.x86_64.rpm
# rpm –hiv --relocate /tmprpm=/opt/apps tacc-pgi-package-20.7.0-1.el7.x86_64.rpm
# rpm –hiv --relocate /tmpmod=/opt/apps tacc-pgi-modulefile-20.7.0-1.el7.x86_64.rpm
# rpm -e tacc-pgi-package-20.7.0-1.el7.x86_64.rpm tacc-pgi-modulefile-20.7.0-1.el7.x86_64.rpm

Summary: A Nice little non-relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name pgi-mathlibs
%define MODULE_VAR    PGIMATHLIBS

%define year 2020

# Create some macros (spec file variables)
%define major_version 11
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define underscore_version %{major_version}_%{minor_version} 

%define pgi_major_version 20
%define pgi_minor_version 7
%define pgi_micro_version 0
%define pgi_version    pgi%{pgi_major_version}.%{pgi_minor_version}.%{pgi_micro_version }
%define pgi_prequisiteversion    pgi/%{pgi_major_version}.%{pgi_minor_version}.%{pgi_micro_version }

%global __os_install_post %{nil}

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc

#%define MODULE_PREFIX /opt/apps

%define lib_dir Linux_x86_64/%{pgi_major_version}.%{pgi_minor_version}


########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   Community
Group:     Development/Tools
URL:       https://www.pgroup.com/products/community.htm
Packager:  TACC - aruhela@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

#--------------------------------------- '
%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the package RPM...
This module contain math libraries provided with NVIDIA HPC SDK.

#--------------------------------------- '
%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the modulefile RPM...
This module contain math libraries provided with NVIDIA HPC SDK.

#--------------------------------------- '
%description
This module contain math libraries provided with NVIDIA HPC SDK.

#--------------------------------------- '
%prep
#---------------------------------------
echo "RPM_BUILD_ROOT=$RPM_BUILD_ROOT"

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
#echo "pgi_install = %{pgi_install}"

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
export LMOD_SH_DBG_ON=1
##################################################
export pgi=`pwd`
##################################################

#export PATH=${pgi_install}/${lib_dir}/bin:${PATH}
#export LD_LIBRARY_PATH=${pgi_install}/${lib_dir}/lib:${LD_LIBRARY_PATH}

cd ${pgi}

printf "\n\n************************************************************\n"
printf "Installing PGI MATH Libraries\n"
printf "************************************************************\n\n"

#wget https://www.pgroup.com/support/download_community.php?file=pgi-community-linux-x64
#cp /admin/build/admin/rpms/frontera/amit/pgilinux-2019-1910-x86-64.tar.gz pgi-%{pgi_version}.tar.gz
#tar xpfz pgi-%{pgi_version}.tar.gz


set -x
cd /admin/build/admin/rpms/frontera/amit/nvhpc20.7/nvhpc_2020_207_Linux_x86_64_cuda_11.0

export NVHPC_SILENT=true
export NVHPC_INSTALL_DIR=%{INSTALL_DIR}
export NVHPC_INSTALL_TYPE=single
export NVHPC_DEFAULT_CUDA=11.0

./install

cd  %{INSTALL_DIR}
rm -rf modulefiles

cd %{INSTALL_DIR}/%{lib_dir}
rm -rf ../%{year}
rm -rf comm_libs  
rm -rf compilers
rm -rf cuda
rm -rf examples
rm -rf REDIST
rm -rf profilers 
echo -e "\nThe directory contents are:"
ls

if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
cd ${pgi}
umount %{INSTALL_DIR}/
set +x

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
This module %{pkg_version} contain math libraries provided with NVIDIA HPC SDK.


This module loads PGI Maths Libraries variables.
The command directory is added to PATH.
The library directory is added to LD_LIBRARY_PATH.
The include directory is added to CPATH.

Version %{pkg_version}
]]

help(help_message,"\n")

whatis("Name: PGI MATH Libraries")
whatis("Version: %{pkg_version}")
whatis("Category: compiler")
whatis("Keywords: System, compiler")
whatis("URL: https://www.pgroup.com")

-- Create environment variables
local nvmathdir = "/opt/apps/%{INSTALL_SUFFIX}/%{lib_dir}/math_libs"

prepend_path( "PATH"                     , pathJoin(nvmathdir,"bin"                 ))
prepend_path( "LD_LIBRARY_PATH"          , pathJoin(nvmathdir,"lib64"               ))
prepend_path( "CPATH"                    , pathJoin(nvmathdir,"include"                         ))
prepend_path( "MODULEPATH"               , "/opt/apps/%{comp_fam_ver}/%{pkg_base_name}-%{underscore_version}/modulefiles" )

prereq("%{pgi_prequisiteversion}")
EOF


cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile
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
%{echo: "PKG_BASE = %{PKG_BASE}" }

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


