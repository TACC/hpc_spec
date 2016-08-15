#
# W. Cyrus Proctor
# 2016-08-08 Forked off for separate binutils
# 2016-02-06 Hikari Provisioning
# 2015-12-01 Build version 493 to support cray_mpich and fortran modules
# 2015-12-01 Add name-defines-noreloc.inc
# 2015-11-20 Need to investigate relocation -- use /opt/apps for now
# 2015-11-10 Update for LS5 Chroot Jail
# 2015-10-27
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
# rpm -i Bar-package-1.1-1.x86_64.rpm
# rpm -i Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: A Nice little non-relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name binutils
%define MODULE_VAR    BINUTILS

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 25

%define pkg_version %{major_version}.%{minor_version}

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

Release:   1%{?dist}
License:   GPL
Group:     Development/Tools
URL:       http://www.gnu.org/software
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the package RPM...
The GNU Binary Utilities, or binutils, are a set of programming tools for creating and managing binary programs, object files, libraries, profile data, and assembly source code originally written by programmers at Cygnus Solutions.
The GNU binutils are typically used in conjunction with compilers such as the GNU Compiler Collection (gcc), build tools like make, and the GNU Debugger (gdb).

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the modulefile RPM...
The GNU Binary Utilities, or binutils, are a set of programming tools for creating and managing binary programs, object files, libraries, profile data, and assembly source code originally written by programmers at Cygnus Solutions.
The GNU binutils are typically used in conjunction with compilers such as the GNU Compiler Collection (gcc), build tools like make, and the GNU Debugger (gdb).

%description
The GNU Binary Utilities, or binutils, are a set of programming tools for creating and managing binary programs, object files, libraries, profile data, and assembly source code originally written by programmers at Cygnus Solutions.
The GNU binutils are typically used in conjunction with compilers such as the GNU Compiler Collection (gcc), build tools like make, and the GNU Debugger (gdb).


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
# module load TACC
# module load crayswitch
# source crayswitch
# module load gcc/4.9.3

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

##################################################
export gcc=`pwd`
export gcc_install=%{INSTALL_DIR}
##################################################

export PATH=${gcc_install}/bin:${PATH}
export PATH=${gcc_install}/x86_64-unknown-linux-gnu/bin:${PATH}
export LD_LIBRARY_PATH=${gcc_install}/lib:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${gcc_install}/x86_64-unknown-linux-gnu/lib:${LD_LIBRARY_PATH}

export gmp_major=5
export gmp_minor=1
export gmp_patch=3

export isl_major=0
export isl_minor=12
export isl_patch=2

export mpfr_major=3
export mpfr_minor=1
export mpfr_patch=2

export ppl_major=1
export ppl_minor=1

export cloog_major=0
export cloog_minor=18
export cloog_patch=1

export mpc_major=1
export mpc_minor=0
export mpc_patch=2

export binutils_major=2
export binutils_minor=25

export gcc_major=4
export gcc_minor=9
export gcc_patch=3

export gmp_version=${gmp_major}.${gmp_minor}.${gmp_patch}
export isl_version=${isl_major}.${isl_minor}.${isl_patch}
export mpfr_version=${mpfr_major}.${mpfr_minor}.${mpfr_patch}
export ppl_version=${ppl_major}.${ppl_minor}
export cloog_version=${cloog_major}.${cloog_minor}.${cloog_patch}
export mpc_version=${mpc_major}.${mpc_minor}.${mpc_patch}
export binutils_version=${binutils_major}.${binutils_minor}
export gcc_version=${gcc_major}.${gcc_minor}.${gcc_patch}

export ncores=16

export CC=gcc 
export CFLAGS=-fPIC 
export CPPFLAGS=-I${gcc_install}/include

cd ${gcc}

printf "\n\n************************************************************\n"
printf "gmp\n"
printf "************************************************************\n\n"

wget ftp://ftp.gnu.org/gnu/gmp/gmp-${gmp_version}.tar.gz
#wget ftp://mirror.vexxhost.com/gnu/gmp/gmp-${gmp_version}.tar.gz
tar xvfz gmp-${gmp_version}.tar.gz

cd gmp-${gmp_version}

${gcc}/gmp-${gmp_version}/configure \
--prefix=${gcc_install} \
--enable-cxx

make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "isl\n"
printf "************************************************************\n\n"

wget http://isl.gforge.inria.fr/isl-${isl_version}.tar.gz
tar xvfz isl-${isl_version}.tar.gz

cd isl-${isl_version}

${gcc}/isl-${isl_version}/configure \
--prefix=${gcc_install} \
--with-gmp-prefix=${gcc_install}

make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "mpfr\n"
printf "************************************************************\n\n"
wget ftp://ftp.gnu.org/gnu/mpfr/mpfr-${mpfr_version}.tar.gz
#wget ftp://mirror.vexxhost.com/gnu/mpfr/mpfr-${mpfr_version}.tar.gz
tar xvfz mpfr-${mpfr_version}.tar.gz

cd mpfr-${mpfr_version}

${gcc}/mpfr-${mpfr_version}/configure \
--prefix=${gcc_install} \
--with-gmp=${gcc_install}

make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "ppl\n"
printf "************************************************************\n\n"

#wget http://bugseng.com/products/ppl/download/ftp/releases/${ppl_version}/ppl-${ppl_version}.tar.gz
wget http://bugseng.com/external/ppl/download/ftp/releases/${ppl_version}/ppl-${ppl_version}.tar.gz
tar xvfz ppl-${ppl_version}.tar.gz

cd ppl-${ppl_version}

${gcc}/ppl-${ppl_version}/configure \
--prefix=${gcc_install} \
--with-gmp=${gcc_install}

make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "cloog\n"
printf "************************************************************\n\n"

wget http://ftp.vim.org/languages/gcc/infrastructure/cloog-${cloog_version}.tar.gz
tar xvfz cloog-${cloog_version}.tar.gz

cd cloog-${cloog_version}

${gcc}/cloog-${cloog_version}/configure \
--prefix=${gcc_install} \
--with-gmp-prefix=${gcc_install} \
--with-gmp=system \
--with-isl=system \
--with-isl-prefix=${gcc_install}

make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "mpc\n"
printf "************************************************************\n\n"

wget ftp://ftp.gnu.org/gnu/mpc/mpc-${mpc_version}.tar.gz
#wget ftp://mirror.vexxhost.com/gnu/mpc/mpc-${mpc_version}.tar.gz
tar xvfz mpc-${mpc_version}.tar.gz

cd mpc-${mpc_version}

${gcc}/mpc-${mpc_version}/configure \
--prefix=${gcc_install} \
--with-mpfr=${gcc_install} \
--with-gmp=${gcc_install}

make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "binutils\n"
printf "************************************************************\n\n"

wget https://ftp.gnu.org/gnu/binutils/binutils-${binutils_version}.tar.gz
tar xvfz binutils-${binutils_version}.tar.gz

cd binutils-${binutils_version}

${gcc}/binutils-${binutils_version}/configure \
--prefix=${gcc_install}                       \
--with-gmp=${gcc_install}                     \
--with-mpfr=${gcc_install}                    \
--with-mpc=${gcc_install}                     \
--with-isl=${gcc_install}

make -j ${ncores}
make install -j ${ncores}


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

#cp -pr %{INSTALL_DIR}/x86_64-unknown-linux-gnu/* %{INSTALL_DIR}
#rm -rf %{INSTALL_DIR}/x86_64-unknown-linux-gnu
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
local help_message = [[
The GNU Binary Utilities, or binutils, are a set of programming tools for creating and managing binary programs, object files, libraries, profile data, and assembly source code originally written by programmers at Cygnus Solutions. The GNU binutils are typically used in conjunction with compilers such as the GNU Compiler Collection (gcc), build tools like make, and the GNU Debugger (gdb).

This module loads GNU Binutils variables.
The command directory is added to PATH.
The library directory is added to LD_LIBRARY_PATH.
The include directory is added to INCLUDE.
The man     directory is added to MANPATH.

Also Defined:
TACC_%{MODULE_VAR}_DIR   = %{MODULE_VAR} base             directory
TACC_%{MODULE_VAR}_BIN   = %{MODULE_VAR} binary           directory
TACC_%{MODULE_VAR}_LIB   = %{MODULE_VAR} library          directory
TACC_%{MODULE_VAR}_INC   = %{MODULE_VAR} include          directory

Version %{pkg_version}
]]

help(help_message,"\n")

whatis("Name: GNU Binutils")
whatis("Version: %{pkg_version}")
whatis("Category: system")
whatis("Keywords: System, utiliies")
whatis("URL: https://www.gnu.org/software/binutils")

-- Create environment variables
local binutils_dir                              = "%{INSTALL_DIR}"
prepend_path( "PATH"                     , pathJoin(binutils_dir,"bin"       )               )
prepend_path( "LD_LIBRARY_PATH"          , pathJoin(binutils_dir,"lib"       )               )
prepend_path( "MANPATH"                  , pathJoin(binutils_dir,"share/man" )               )
prepend_path( "INCLUDE"                  , pathJoin(binutils_dir,"include"   )               )
setenv(       "TACC_%{MODULE_VAR}_DIR"   , binutils_dir                                      )
setenv(       "TACC_%{MODULE_VAR}_BIN"   , pathJoin(binutils_dir,"bin"       )               )
setenv(       "TACC_%{MODULE_VAR}_LIB"   , pathJoin(binutils_dir,"lib"       )               )
setenv(       "TACC_%{MODULE_VAR}_INC"   , pathJoin(binutils_dir,"include"   )               )

EOF

 
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version << 'EOF'
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

