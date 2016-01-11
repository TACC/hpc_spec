#
# W. Cyrus Proctor
# 2016-01-08
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
%define pkg_base_name filter
%define MODULE_VAR    FILTER

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
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

Release:   2
License:   GPLv2
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

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
Manages slurm submissions via the TACC filter.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
# Load Compiler
%include compiler-load.inc
# Load MPI Library
#%include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  export filter=`pwd`
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  mount -t tmpfs tmpfs %{INSTALL_DIR}
  export  boost=%{INSTALL_DIR}/boost
  export   grvy=%{INSTALL_DIR}/grvy
  mkdir -p ${boost} 
  mkdir -p ${grvy}
%define tacc_bin /opt/apps/tacc/bin
  mkdir -p $RPM_BUILD_ROOT%{tacc_bin}
  
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

# Boost
###########################################################################
###########################################################################
###########################################################################

date

ml purge
ml gcc/4.9.3

# System GCC would be nice... (waiting on system /usr/bin/gfortran)
type -a gcc

echo "PATH:\n${PATH}"
echo "LD_LIBRARY_PATH:\n${LD_LIBRARY_PATH}"


export boost_install=${boost}/install

export icu=${boost}
export icu_install=${icu}/install

export icu_major=56
export icu_minor=1
export icu_version=${icu_major}.${icu_minor}
export icu_uversion=${icu_major}_${icu_minor}

export boost_major=1
export boost_minor=60
export boost_micro=0
export boost_version=${boost_major}.${boost_minor}.${boost_micro}
export boost_uversion=${boost_major}_${boost_minor}_${boost_micro}

export       CC=gcc
export      CXX=g++
export   CFLAGS=-fPIC
export CXXFLAGS=-fPIC
export  LDFLAGS=-fPIC
export ncores=16

cd ${boost}
wget http://download.icu-project.org/files/icu4c/${icu_version}/icu4c-${icu_uversion}-src.tgz
tar xvfz icu4c-${icu_uversion}-src.tgz
cd icu/source
${icu}/icu/source/runConfigureICU \
Linux                             \
--prefix=${icu_install}           \
--enable-static                   \
--enable-shared

make -j ${ncores}
make -j ${ncores} install

###########################################################################

cd ${boost}
wget http://sourceforge.net/projects/boost/files/boost/${boost_version}/boost_${boost_uversion}.tar.gz
tar xvfz boost_${boost_uversion}.tar.gz
cd boost_${boost_uversion}
${boost}/boost_${boost_uversion}/bootstrap.sh \
--prefix=${boost_install}                     \
--with-toolset=gcc                            \
--with-libraries=all                          \
--without-libraries=mpi                       \
--with-icu=${icu_install}

${boost}/boost_${boost_uversion}/b2 \
-j ${ncores}                        \
--prefix=${boost_install}           \
install

# Clean up except install dir
rm -rf ${boost}/boost_*  ${boost}/icu*

# grvy
###########################################################################
###########################################################################
###########################################################################
date

ml purge
ml gcc/4.9.3

# System GCC ONLY!
type -a gcc

# Boost (built with system gcc) installation dir
export    BOOST_ROOT=${boost_install}

export grvy_install=${grvy}/install

export            PATH=${boost_install}/bin:${PATH}
export LD_LIBRARY_PATH=${boost_install}/lib:${LD_LIBRARY_PATH}

echo "PATH:\n${PATH}"
echo "LD_LIBRARY_PATH:\n${LD_LIBRARY_PATH}"

export grvy_major=0
export grvy_minor=32
export grvy_micro=0
export grvy_version=${grvy_major}.${grvy_minor}.${grvy_micro}

export      CC=gcc
export     CXX=g++
export      FC=gfortran
export LDFLAGS=-Wl,-rpath,${BOOST_ROOT}/lib

export ncores=16

cd ${grvy}
tar xvfz %{_sourcedir}/grvy-${grvy_version}.tar.gz
cd grvy-${grvy_version}

${grvy}/grvy-${grvy_version}/configure \
--prefix=${grvy_install}               \
--enable-static                        \
--enable-shared                        \
--with-pic                             \
--with-boost=${BOOST_ROOT}

make -j ${ncores}
make -j ${ncores} install

# Clean up except install dir
rm -rf ${grvy}/grvy*

# tacc_filter_submission.so
###########################################################################
###########################################################################
###########################################################################

export BOOST=${boost_install}
export  GRVY=${grvy_install}
export SLURM=/opt/slurm/default

cd ${filter}

gcc -g -fPIC -shared                   -I${SLURM}/include -o tacc_welcome.so           tacc_welcome.c 
gcc -g -fPIC -shared                   -I${SLURM}/include -o tacc_deny.so              tacc_deny.c
gcc -g -fPIC -shared -I${GRVY}/include -I${SLURM}/include -o tacc_submission_filter.so filesystem_availability.cpp driver.cpp queue_acls.cpp queue_limits.cpp submit_host.cpp tacc_submission_filter.c ssh_keys.cpp accounting.cpp vmcalo.cpp jobname.cpp check_reservation.cpp -L$GRVY/lib64 -Wl,-rpath,$GRVY/lib64 -lgrvy 

chmod 755 *.so


# Copy all *.so's over to the installation directory
cp -r ${filter}/*.so %{INSTALL_DIR}

# Create symbolic links to the shared object libraries created
ln -sf %{INSTALL_DIR}/tacc_welcome.so           $RPM_BUILD_ROOT%{tacc_bin}/tacc_welcome.so          
ln -sf %{INSTALL_DIR}/tacc_deny.so              $RPM_BUILD_ROOT%{tacc_bin}/tacc_deny.so             
ln -sf %{INSTALL_DIR}/tacc_submission_filter.so $RPM_BUILD_ROOT%{tacc_bin}/tacc_submission_filter.so

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

# Nothing to do!

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

  %{tacc_bin}/tacc_welcome.so          
  %{tacc_bin}/tacc_deny.so             
  %{tacc_bin}/tacc_submission_filter.so

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

