#
# W. Cyrus Proctor
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
%define pkg_base_name gcc
%define MODULE_VAR    GCC

# Create some macros (spec file variables)
%define major_version 7
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define gcc_ver gcc7_3

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
The GNU Compiler Collection includes front ends for C, C++, Objective-C,
Fortran, Java, Ada, and Go, as well as libraries for these languages
(libstdc++, libgcj,...). GCC was originally written as the compiler for the GNU
operating system. The GNU system was developed to be 100% free software, free
in the sense that it respects the user's freedom.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the modulefile RPM...
The GNU Compiler Collection includes front ends for C, C++, Objective-C,
Fortran, Java, Ada, and Go, as well as libraries for these languages
(libstdc++, libgcj,...). GCC was originally written as the compiler for the GNU
operating system. The GNU system was developed to be 100% free software, free
in the sense that it respects the user's freedom.

%description
The GNU Compiler Collection includes front ends for C, C++, Objective-C,
Fortran, Java, Ada, and Go, as well as libraries for these languages
(libstdc++, libgcj,...). GCC was originally written as the compiler for the GNU
operating system. The GNU system was developed to be 100% free software, free
in the sense that it respects the user's freedom.

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
#module load TACC
#module load gcc/4.9.3

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

export gmp_major=6
export gmp_minor=1
#export gmp_patch=0
export gmp_patch=2

export isl_major=0
#export isl_minor=16
#export isl_patch=1
export isl_minor=19

export mpfr_major=3
export mpfr_minor=1
#export mpfr_patch=4
export mpfr_patch=6

export mpc_major=1
export mpc_minor=0
export mpc_patch=3

export binutils_major=2
#export binutils_minor=26
#export binutils_minor=27
export binutils_minor=30

export gcc_major=7
export gcc_minor=3
export gcc_patch=0

export gmp_version=${gmp_major}.${gmp_minor}.${gmp_patch}
#export isl_version=${isl_major}.${isl_minor}.${isl_patch}
export isl_version=${isl_major}.${isl_minor}
export mpfr_version=${mpfr_major}.${mpfr_minor}.${mpfr_patch}
export mpc_version=${mpc_major}.${mpc_minor}.${mpc_patch}
export binutils_version=${binutils_major}.${binutils_minor}
export gcc_version=${gcc_major}.${gcc_minor}.${gcc_patch}

export ncores=48

export CC=gcc 
export CFLAGS=-fPIC 
export CPPFLAGS=-I${gcc_install}/include


cd ${gcc}

printf "\n\n************************************************************\n"
printf "gmp\n"
printf "************************************************************\n\n"

wget ftp://ftp.gnu.org/gnu/gmp/gmp-${gmp_version}.tar.bz2
tar xvfj gmp-${gmp_version}.tar.bz2

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
tar xvfz mpfr-${mpfr_version}.tar.gz

cd mpfr-${mpfr_version}

${gcc}/mpfr-${mpfr_version}/configure \
--prefix=${gcc_install} \
--with-gmp=${gcc_install}

make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "mpc\n"
printf "************************************************************\n\n"

wget ftp://ftp.gnu.org/gnu/mpc/mpc-${mpc_version}.tar.gz
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
--enable-gold=yes                             \
--enable-ld=default                           \
--enable-plugins                              \
--enable-lto                                  \
--with-gmp=${gcc_install}                     \
--with-mpfr=${gcc_install}                    \
--with-mpc=${gcc_install}                     \
--with-isl=${gcc_install}


make -j ${ncores}
make install -j ${ncores}

export cc=gcc

cd ${gcc}

printf "\n\n************************************************************\n"
printf "gcc\n"
printf "************************************************************\n\n"

wget ftp://gcc.gnu.org/pub/gcc/releases/gcc-${gcc_version}/gcc-${gcc_version}.tar.xz
tar xvfJ gcc-${gcc_version}.tar.xz

cd gcc-${gcc_version}

${gcc}/gcc-${gcc_version}/configure \
--enable-libssp                     \
--enable-gold=yes                   \
--enable-ld=default                 \
--enable-plugins                    \
--enable-lto                        \
--with-tune=generic                 \
--enable-languages='c,c++,fortran'  \
--disable-multilib                  \
--prefix=${gcc_install}             \
--with-gmp=${gcc_install}           \
--with-mlgmp=${gcc_install}         \
--with-mpfr=${gcc_install}          \
--with-mpc=${gcc_install}           \
--with-isl=${gcc_install}

make BOOT_CFLAGS='-O2' bootstrap -j ${ncores}
make install -j ${ncores}


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

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
The GNU Compiler Collection %{pkg_version} includes front ends for C, C++,
Objective-C, Fortran, Java, Ada, and Go, as well as libraries for these
languages (libstdc++, libgcj,...). GCC was originally written as the compiler
for the GNU operating system. The GNU system was developed to be 100% free
software, free in the sense that it respects the users freedom.

This module loads GCC Compiler variables.
The command directory is added to PATH.
The library directory is added to LD_LIBRARY_PATH.
The include directory is added to INCLUDE.
The man     directory is added to MANPATH.

Also Defined:
TACC_%{MODULE_VAR}_DIR   = %{MODULE_VAR} base             directory
TACC_%{MODULE_VAR}_BIN   = %{MODULE_VAR} binary           directory
TACC_%{MODULE_VAR}_LIB   = %{MODULE_VAR} library          directory
TACC_%{MODULE_VAR}_LIB64 = %{MODULE_VAR} library (64-bit) directory
TACC_%{MODULE_VAR}_INC   = %{MODULE_VAR} include          directory

Version %{pkg_version}
]]

help(help_message,"\n")

whatis("Name: GCC Compilers")
whatis("Version: %{pkg_version}")
whatis("Category: compiler")
whatis("Keywords: System, compiler")
whatis("URL: http://gcc.gnu.org")

-- Create environment variables
local gcc_dir                              = "%{INSTALL_DIR}"
prepend_path( "PATH"                     , pathJoin(gcc_dir,"bin"       )               )
prepend_path( "LD_LIBRARY_PATH"          , pathJoin(gcc_dir,"lib"       )               )
prepend_path( "LD_LIBRARY_PATH"          , pathJoin(gcc_dir,"lib64"     )               )
prepend_path( "MANPATH"                  , pathJoin(gcc_dir,"share/man" )               )
prepend_path( "INCLUDE"                  , pathJoin(gcc_dir,"include"   )               )
prepend_path( "MODULEPATH"               , "%{MODULE_PREFIX}/%{gcc_ver}/modulefiles" )
setenv(       "%{MODULE_VAR}_LIB"        , pathJoin(gcc_dir,"lib64"     )               )
setenv(       "TACC_%{MODULE_VAR}_DIR"   , gcc_dir                                      )
setenv(       "TACC_%{MODULE_VAR}_BIN"   , pathJoin(gcc_dir,"bin"       )               )
setenv(       "TACC_%{MODULE_VAR}_LIB"   , pathJoin(gcc_dir,"lib"       )               )
setenv(       "TACC_%{MODULE_VAR}_LIB64" , pathJoin(gcc_dir,"lib64"     )               )
setenv(       "TACC_%{MODULE_VAR}_INC"   , pathJoin(gcc_dir,"include"   )               )

if (os.getenv("TACC_SYSTEM") == "stampede2") then
  setenv( "TACC_VEC_FLAGS" ,      "-march=broadwell -mtune=knl" )
elseif (os.getenv("TACC_SYSTEM") == "ls5") then
  setenv( "TACC_VEC_FLAGS" ,      "-march=ivybridge -mtune=haswell" )
else
  setenv( "TACC_VEC_FLAGS" ,      "-march=haswell -mtune=haswell" )
end

family("compiler")
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

