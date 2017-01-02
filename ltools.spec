#
# W. Cyrus Proctor
# 2016-01-31
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
%define pkg_base_name ltools
%define MODULE_VAR    LTOOLS

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 1

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
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
Group:     Development/Tools
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
TACC %{MODULE_VAR} (Lustre Tools) provides a customized set of core utilities
that have been modified to be Lustre-aware. This allows for automatic striping
of large files across multiple Object Storage Targets (OSTs) on Lustre file
systems.  This not only will help read/write performance in most cases but will
also minimize the potential for user-generated files to negatively impact
others on the system. Utilities include cp, tar, gzip, bzip2, and rsync.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
TACC %{MODULE_VAR} (Lustre Tools) provides a customized set of core utilities
that have been modified to be Lustre-aware. This allows for automatic striping
of large files across multiple Object Storage Targets (OSTs) on Lustre file
systems.  This not only will help read/write performance in most cases but will
also minimize the potential for user-generated files to negatively impact
others on the system. Utilities include cp, tar, gzip, bzip2, and rsync.

%description
TACC %{MODULE_VAR} (Lustre Tools) provides a customized set of core utilities
that have been modified to be Lustre-aware. This allows for automatic striping
of large files across multiple Object Storage Targets (OSTs) on Lustre file
systems.  This not only will help read/write performance in most cases but will
also minimize the potential for user-generated files to negatively impact
others on the system. Utilities include cp, tar, gzip, bzip2, and rsync.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  rm -rf %{_builddir}/%{pkg_base_name}-%{pkg_version}

%setup -n %{pkg_base_name}-%{pkg_version}

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
module purge
module load autotools
module list
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

#############################################
####### coreutils ###########################
#############################################

export base=`pwd`

type -a gcc

export default_stripe_size=1000000000 # In bytes (1 GB)
export stripe_size=25000000000        # In bytes (25 GB)

export tc=${base}
export tc_install=%{INSTALL_DIR}
export tc_major=8
export tc_minor=22
export tc_version=${tc_major}.${tc_minor}

export CC=gcc
export CFLAGS="-g -O2 -DHAVE_LIBLUSTREAPI"
export LIBS="-llustreapi"
export ncores=64
export FORCE_UNSAFE_CONFIGURE=1

cd ${tc}
wget http://ftp.gnu.org/gnu/coreutils/coreutils-${tc_version}.tar.xz
tar xvfJ coreutils-${tc_version}.tar.xz
cd coreutils-${tc_version}

# Apply Lustre Patch
sed -i "s/${default_stripe_size}/${stripe_size}/g" ${base}/coreutils-${tc_version}.patch
patch -p1 < ${base}/coreutils-${tc_version}.patch

autoreconf
${tc}/coreutils-${tc_version}/configure \
--prefix=${tc_install}
automake

make -j ${ncores}
# NO "make install" with patched lustre version
# DO NOT ATTEMPT as ROOT if you value your system!

# Manual installation of modified cp and md5sum
mkdir -p ${tc_install}
mkdir -p ${tc_install}/bin
mkdir -p ${tc_install}/man/man1

cp src/cp ${tc_install}/bin/cp
cp src/md5sum ${tc_install}/bin/md5sum
cp man/cp.1 ${tc_install}/man/man1/cp.1
cp man/md5sum.1 ${tc_install}/man/man1/md5sum.1

#############################################
####### tar #################################
#############################################

type -a gcc

export tt=${base}
export tt_install=%{INSTALL_DIR}
export tt_major=1
export tt_minor=27
export tt_micro=1
export tt_version=${tt_major}.${tt_minor}.${tt_micro}

export CC=gcc
export CFLAGS="-g -O2 -DHAVE_LIBLUSTREAPI"
export LIBS="-llustreapi"
export ncores=64

cd ${tt}
wget http://ftp.gnu.org/gnu/tar/tar-${tt_version}.tar.xz
tar xvfJ tar-${tt_version}.tar.xz
cd tar-${tt_version}

# Apply Lustre Patch
sed -i "s/${default_stripe_size}/${stripe_size}/g" ${base}/tar-${tt_version}.patch
patch -p1 < ${base}/tar-${tt_version}.patch

${tt}/tar-${tt_version}/configure \
--prefix=${tt_install}

make -j ${ncores}
make -j ${ncores} install

#############################################
####### rsync ###############################
#############################################

type -a gcc

export tr=${base}
export tr_install=%{INSTALL_DIR}
export tr_major=3
export tr_minor=1
export tr_micro=0
export tr_version=${tr_major}.${tr_minor}.${tr_micro}

export CC=gcc
export CFLAGS="-g -O2 -DHAVE_LIBLUSTREAPI"
export LIBS="-llustreapi"
export ncores=64

cd ${tr}
wget http://mirrors.ibiblio.org/rsync/src/rsync-${tr_version}.tar.gz
#wget https://download.samba.org/pub/rsync/rsync-${tr_version}.tar.gz
tar xvfz rsync-${tr_version}.tar.gz
cd rsync-${tr_version}

# Apply Lustre Patch
sed -i "s/${default_stripe_size}/${stripe_size}/g" ${base}/rsync-${tr_version}.patch
patch -p1 < ${base}/rsync-${tr_version}.patch

${tr}/rsync-${tr_version}/configure \
--prefix=${tr_install}

make -j ${ncores}
make -j ${ncores} install

#############################################
####### gzip ################################
#############################################

type -a gcc

export tg=${base}
export tg_install=%{INSTALL_DIR}
export tg_major=1
export tg_minor=6
export tg_version=${tg_major}.${tg_minor}

export CC=gcc
export CFLAGS="-g -O2 -DHAVE_LIBLUSTREAPI"
export LIBS="-llustreapi"
export ncores=64

cd ${tg}
wget http://ftp.gnu.org/gnu/gzip/gzip-${tg_version}.tar.xz
tar xvfJ gzip-${tg_version}.tar.xz
cd gzip-${tg_version}

# Apply Lustre Patch
sed -i "s/${default_stripe_size}/${stripe_size}/g" ${base}/gzip-${tg_version}.patch
patch -p1 < ${base}/gzip-${tg_version}.patch

${tg}/gzip-${tg_version}/configure \
--prefix=${tg_install}

make -j ${ncores}
make -j ${ncores} install

#############################################
####### bzip2 ###############################
#############################################

type -a gcc

export tb=${base}
export tb_install=%{INSTALL_DIR}
export tb_major=1
export tb_minor=0
export tb_micro=6
export tb_version=${tb_major}.${tb_minor}.${tb_micro}

export CC=gcc
export CFLAGS="-g -O2 -DHAVE_LIBLUSTREAPI"
export LIBS="-llustreapi"
export ncores=64

cd ${tb}
wget http://www.bzip.org/${tb_version}/bzip2-${tb_version}.tar.gz
tar xvfz bzip2-${tb_version}.tar.gz
cd bzip2-${tb_version}

# Apply Lustre Patch
sed -i "s/${default_stripe_size}/${stripe_size}/g" ${base}/bzip2-${tb_version}.patch
patch -p1 < ${base}/bzip2-${tb_version}.patch

make install PREFIX=${tb_install}

#############################################
#############################################
#############################################

  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}/
  
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
TACC %{MODULE_VAR} (Lustre Tools) provides a customized set of core utilities
that have been modified to be Lustre-aware. This allows for automatic striping
of large files across multiple Object Storage Targets (OSTs) on Lustre file
systems.  This not only will help read/write performance in most cases but will
also minimize the potential for user-generated files to negatively impact
others on the system. Utilities include cp, tar, gzip, bzip2, and rsync.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution,
libraries, include files, and tools respectively.

Version %{pkg_version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: %{pkg_name}")
whatis("Version: %{pkg_version}")

-- Create environment variables.
local base_dir           = "%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(base_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(base_dir, "lib"))
prepend_path(    "INCLUDE",             pathJoin(base_dir, "include"))
prepend_path(    "MANPATH",             pathJoin(base_dir, "man"))
prepend_path(    "MANPATH",             pathJoin(base_dir, "share/man"))
setenv( "TACC_%{MODULE_VAR}_DIR",                base_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(base_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(base_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(base_dir, "bin"))
-- set_alias("cp", "cp --stripe-count=25s")
-- set_alias("rsync", "rsync --rsync-path=%{INSTALL_DIR}/bin/rsync")
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

