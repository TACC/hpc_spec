#
# W. Cyrus Proctor
# 2015-08-20
#
# WARNING: spec files are strange creatures.
# Lines with define macros (percent define etc.) will be
# ingested, even if you comment out the line with a # *$?@!

Summary: A Nice little relocatable skeleton spec file example.

# Create some macros (spec file variables)
%define gcc_major 4
%define gcc_minor 9
%define gcc_patch 1

%define gcc_version %{gcc_major}.%{gcc_minor}.%{gcc_patch}

# Give the package a base name
%define pkg_base_name gcc
%define pkg_version %{gcc_version}

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


#######################################
### TOGGLE ON/OFF WITH COMMENT ########
#######################################
# Include for basic macro definitions
%include rpm-dir.inc                  
# Include if compiler specific
#%include compiler-defines.inc
# Include if mpi wrapper specific
#%include mpi-defines.inc
#######################################
#######################################
#######################################


# Compiler Specific?
%if "%{?comp_fam_ver}"
  # Compiler *and* MPI Specific
  %if "%{?mpi_fam_ver}"
    %define pkg_name       %{pkg_base_name}-%{comp_fam_ver}-%{mpi_fam_ver}
    %define MODULE_SUFFIX  %{comp_fam_ver}/%{mpi_fam_ver}/modulefiles/%{pkg_base_name}
    %define INSTALL_SUFFIX %{comp_fam_ver}/%{mpi_fam_ver}/%{pkg_base_name}/%{pkg_version}
  # Compiler Specific Only
  %else
    %define pkg_name       %{pkg_base_name}-%{comp_fam_ver}
    %define MODULE_SUFFIX  %{comp_fam_ver}/modulefiles/%{pkg_base_name}
    %define INSTALL_SUFFIX %{comp_fam_ver}/%{pkg_base_name}/%{pkg_version}
  %endif
# Compiler Non-specific
%else
  %define pkg_name       %{pkg_base_name}
  %define MODULE_SUFFIX  modulefiles/%{pkg_base_name}
  %define INSTALL_SUFFIX %{pkg_base_name}/%{pkg_version}
%endif

# SPEC File Tags
Name:      %{pkg_name}
Version:   %{pkg_version}
Release:   3
License:   GPL
Group:     Development/Tools
URL:       http://www.gnu.org/software
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# NOTES:
# Leave MODULE_PREFIX and INSTALL_PREFIX as /tmpmod and /tmprpm!
# These are temporary placeholders that allow for install-time
# relocation via rpm. They must be unique and *not* nested. 
# /tmpmod and /tmprpm should *never* be the final install locations.


# Module macros
%define MODULE_PREFIX   /tmpmod 
%define MODULE_DIR      %{MODULE_PREFIX}/%{MODULE_SUFFIX}
%define MODULE_VAR      GCC
%define GCC_VER         %{gcc_major}_%{gcc_minor}
%define MODULE_FILENAME %{version}.lua

# Install macros
%define INSTALL_PREFIX  /tmprpm
%define INSTALL_DIR     %{INSTALL_PREFIX}/%{INSTALL_SUFFIX}

# Subpackage macros
%define PACKAGE             package
%define MODULEFILE          modulefile
%define BUILD_PACKAGE       %( if [ ${NO_PACKAGE:=0}    = 0 ]; then echo "1"; else echo "0"; fi )
%define BUILD_MODULEFILE    %( if [ ${NO_MODULEFILE:=0} = 0 ]; then echo "1"; else echo "0"; fi )
%define RPM_PACKAGE_NAME    %{name}-%{PACKAGE}-%{version}-%{release}
%define RPM_MODULEFILE_NAME %{name}-%{MODULEFILE}-%{version}-%{release}

#---------------------------------------
#---------------------------------------
#---------------------------------------
# Default installation prefixes
# May be overridden at install
# with:
# rpm --relocate /foo=/bar <rpm-name>.rpm 
Prefix:    %{MODULE_PREFIX}
Prefix:    %{INSTALL_PREFIX}
#---------------------------------------
#---------------------------------------
#---------------------------------------

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the rpm for the package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the rpm for the modulefile.

%description
The GNU Compiler Collection

# NOTE:
# If creating subpackages with the %package
# or %package -n directives, be sure to have
# appropriate %files, %pre, %post, %preun and
# %postun directvies as well.

#---------------------------------------
#---------------------------------------
#---------------------------------------
%prep
#---------------------------------------
#---------------------------------------
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

echo "bp: %{BUILD_PACKAGE}"
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

#--------
# untar |
#--------
# Source assumed to be located in ../SOURCES
# The first call to setup untars the first source.  
# The second call untars the second source, in a subdirectory of the first. 
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory.
# -T prevents the 'default' source file from re-unpacking.  
#    If you don't have this, the default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!


#---------------------------------------
#---------------------------------------
#---------------------------------------
%build
#---------------------------------------
#---------------------------------------
#---------------------------------------



#---------------------------------------
#---------------------------------------
#---------------------------------------
%install
#---------------------------------------
#---------------------------------------
#---------------------------------------

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"


# -----------------
# Package Section |
# -----------------

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
export gcc_patch=1

export gmp_version=${gmp_major}.${gmp_minor}.${gmp_patch}
export isl_version=${isl_major}.${isl_minor}.${isl_patch}
export mpfr_version=${mpfr_major}.${mpfr_minor}.${mpfr_patch}
export ppl_version=${ppl_major}.${ppl_minor}
export cloog_version=${cloog_major}.${cloog_minor}.${cloog_patch}
export mpc_version=${mpc_major}.${mpc_minor}.${mpc_patch}
export binutils_version=${binutils_major}.${binutils_minor}
export gcc_version=${gcc_major}.${gcc_minor}.${gcc_patch}

export ncores=24

export CC=gcc 
export CFLAGS=-fPIC 
export CPPFLAGS=-I${gcc_install}/include


cd ${gcc}

printf "\n\n************************************************************\n"
printf "gmp\n"
printf "************************************************************\n\n"


wget ftp://mirror.vexxhost.com/gnu/gmp/gmp-${gmp_version}.tar.gz
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

wget ftp://mirror.vexxhost.com/gnu/mpfr/mpfr-${mpfr_version}.tar.gz
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

wget http://bugseng.com/products/ppl/download/ftp/releases/${ppl_version}/ppl-${ppl_version}.tar.gz
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

wget ftp://mirror.vexxhost.com/gnu/mpc/mpc-${mpc_version}.tar.gz
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
--with-cloog=${gcc_install}                   \
--with-mpc=${gcc_install}                     \
--with-isl=${gcc_install}


make -j ${ncores}
make install -j ${ncores}

cd ${gcc}

printf "\n\n************************************************************\n"
printf "gcc\n"
printf "************************************************************\n\n"

wget http://mirrors-usa.go-parts.com/gcc/releases/gcc-${gcc_version}/gcc-${gcc_version}.tar.gz
tar xvfz gcc-${gcc_version}.tar.gz

cd gcc-${gcc_version}

${gcc}/gcc-${gcc_version}/configure \
--disable-cloog-version-check       \
--disable-ppl-version-check         \
--enable-cloog-backend=isl          \
--enable-lto                        \
--enable-libssp                     \
--enable-gold                       \
--with-arch=native                  \
--with-tune=native                  \
--enable-languages='c,c++,fortran'  \
--disable-multilib                  \
--prefix=${gcc_install}             \
--with-gmp=${gcc_install}           \
--with-mlgmp=${gcc_install}         \
--with-mpfr=${gcc_install}          \
--with-ppl=${gcc_install}           \
--with-cloog=${gcc_install}         \
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



#------------------
# Modules Section |
#------------------

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
# Use the %{INSTALL_DIR} macro for package path locations inside the modulefile!
# Use the %{MODULE_DIR} macro for modulefile path locations inside the modulefile!
# The cat command and 'EOF' must be left justified to work correctly.
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message = [[
GNU Compiler Collection %{pkg_version}

This module loads GCC Compiler variables.
The command directory is added to PATH.
The library directory is added to LD_LIBRARY_PATH.
The include directory is added to INCLUDE.
The man     directory is added to MANPATH.
]]

help(help_message,"\n")

whatis("Name: GCC Compilers")
whatis("Version: %{pkg_version}")
whatis("Category: compiler")
whatis("Keywords: System, compiler")
whatis("URL: http://gcc.gnu.org")

-- Create environment variables
local gcc_dir                      = "%{INSTALL_DIR}"
prepend_path("PATH",               pathJoin(gcc_dir,"bin"))
prepend_path("LD_LIBRARY_PATH",    pathJoin(gcc_dir,"lib"))
prepend_path("LD_LIBRARY_PATH",    pathJoin(gcc_dir,"lib64"))
prepend_path("MANPATH",            pathJoin(gcc_dir,"man"))
prepend_path("INCLUDE",            pathJoin(gcc_dir,"include"))
prepend_path("MODULEPATH",         "%{MODULE_PREFIX}/gcc%{GCC_VER}/modulefiles")
setenv(      "GCC_LIB",            pathJoin(gcc_dir,"lib64"))

family("compiler")
EOF


  #----------------
  #  version file |
  #----------------

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


#---------------------------------------
#---------------------------------------
#---------------------------------------
# files section
# NOTE:
# If creating subpackages with the %package
# or %package -n directives, be sure to have
# appropriate %files, %pre, %post, %preun and
# %postun directvies as well.
#---------------------------------------
#---------------------------------------
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  # File attributes %defattr(<file mode>, <user>, <group>, <dir mode>)
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

  # File attributes %defattr(<file mode>, <user>, <group>, <dir mode>)
  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#---------------------------------------
#---------------------------------------
#---------------------------------------
# post section
# NOTE:
# If creating subpackages with the %package
# or %package -n directives, be sure to have
# appropriate %files, %pre, %post, %preun and
# %postun directvies as well.
#---------------------------------------
#---------------------------------------
#---------------------------------------



%post %{PACKAGE}
R='\033[1;31m'
G='\033[1;32m'
B='\033[1;34m'
W='\033[0m'
NC='\033[0m'
F='\033[0m'
printf "${F}===================================================${NC}\n"
printf "${F}||${B}MMP\"\"MM\"\"YMM   db ${W}      .g8\"\"\"bgd   .g8\"\"\"bgd  ${F}||${NC}\n"
printf "${F}||${B}P\'   MM   \`7  ;MM: ${W}   .dP\'     \`M .dP\'     \`M  ${F}||${NC}\n"
printf "${F}||${B}     MM      ,V^MM. ${W}  dM\'       \` dM\'       \`  ${F}||${NC}\n"
printf "${F}||${B}     MM     ,M  \`MM ${W}  MM          MM           ${F}||${NC}\n"
printf "${F}||${B}     MM     Ab${W}mmm${B}qMA ${R} MM.         MM.          ${F}||${NC}\n"
printf "${F}||${B}     MM    A\'     VML${R} \`Mb.     ,\' \`Mb.     ,\'  ${F}||${NC}\n"
printf "${F}||${B}   .JMML..AMA.   .AMMA.${R} \`\"bmmmd'    \`\"bmmmd\'   ${F}||${NC}\n"
printf "${F}===================================================${NC}\n"
echo "This is the %{RPM_PACKAGE_NAME} subpackage postinstall script"
# Query rpm after installation for location of canary files ---------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                       # |
  export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                    # |
  export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                     # |
  echo "Using default RPM database path:                             %{_dbpath}"                                              # |
else                                                                                                                          # |
  export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)             # |
  export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)              # |
  echo "Using user-specified RPM database path:                      ${RPM_DBPATH}"                                           # |
fi                                                                                                                            # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")              # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                # |
# -------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
echo "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       "                       > /dev/stderr # |
echo "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      "                       > /dev/stderr # |
echo "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          "                       > /dev/stderr # |
echo "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         "                       > /dev/stderr # |
if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                      # |
  echo -e "${R}ERROR: POST_INSTALL_PREFIX is currently set but null or unset"                                     > /dev/stderr # |
  echo -e "${R}ERROR: tacc_install_canary was not found"                                                          > /dev/stderr # |
  echo -e "${R}ERROR: Something is not right. Exiting!"                                                           > /dev/stderr # |
  exit -1                                                                                                                       # |
else                                                                                                                            # |
  echo "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} "                     > /dev/stderr # |
  echo "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"    > /dev/stderr # |
fi                                                                                                                              # |
if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                       # |
  echo -e "${G}POST_MODULE_PREFIX set but null or unset${NC}"                                                     > /dev/stderr # |
  echo -e "${G}Has %{RPM_MODULEFILE_NAME} been installed in this rpm database yet?${NC}"                          > /dev/stderr # |
  echo -e "${G}Install %{RPM_MODULEFILE_NAME} to automatically update %{MODULE_SUFFIX}/%{MODULE_FILENAME}${NC}"   > /dev/stderr # |
else                                                                                                                            # |
  echo "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  "                     > /dev/stderr # |
  echo "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  "    > /dev/stderr # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
  echo "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       "                     > /dev/stderr # |
  echo "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         "                     > /dev/stderr # |
  sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}               # |
  sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}                 # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
  cat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}            | \
      GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
      GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                         > /dev/stderr # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------

%post %{MODULEFILE}
R='\033[1;31m'
G='\033[1;32m'
B='\033[1;34m'
W='\033[0m'
NC='\033[0m'
F='\033[0m'
printf "${F}===================================================${NC}\n"
printf "${F}||${B}MMP\"\"MM\"\"YMM   db ${W}      .g8\"\"\"bgd   .g8\"\"\"bgd  ${F}||${NC}\n"
printf "${F}||${B}P\'   MM   \`7  ;MM: ${W}   .dP\'     \`M .dP\'     \`M  ${F}||${NC}\n"
printf "${F}||${B}     MM      ,V^MM. ${W}  dM\'       \` dM\'       \`  ${F}||${NC}\n"
printf "${F}||${B}     MM     ,M  \`MM ${W}  MM          MM           ${F}||${NC}\n"
printf "${F}||${B}     MM     Ab${W}mmm${B}qMA ${R} MM.         MM.          ${F}||${NC}\n"
printf "${F}||${B}     MM    A\'     VML${R} \`Mb.     ,\' \`Mb.     ,\'  ${F}||${NC}\n"
printf "${F}||${B}   .JMML..AMA.   .AMMA.${R} \`\"bmmmd'    \`\"bmmmd\'   ${F}||${NC}\n"
printf "${F}===================================================${NC}\n"
echo "This is the %{RPM_MODULEFILE_NAME} subpackage postinstall script"
# Query rpm after installation for location of canary files ---------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                       # |
  export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                    # |
  export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                     # |
  echo "Using default RPM database path:                             %{_dbpath}"                                              # |
else                                                                                                                          # |
  export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)             # |
  export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)              # |
  echo "Using user-specified RPM database path:                      ${RPM_DBPATH}"                                           # |
fi                                                                                                                            # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")              # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                # |
# -------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
echo "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       "                       > /dev/stderr # |
echo "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      "                       > /dev/stderr # |
echo "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          "                       > /dev/stderr # |
echo "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         "                       > /dev/stderr # |
if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                      # |
  echo -e "${G}POST_INSTALL_PREFIX is set but null or unset${NC}"                                                 > /dev/stderr # |
  echo -e "${G}Has %{RPM_PACKAGE_NAME} been installed in this rpm database yet?${NC}"                             > /dev/stderr # |
  echo -e "${G}Install %{RPM_PACKAGE_NAME} to automatically update %{MODULE_SUFFIX}/%{MODULE_FILENAME}${NC}"      > /dev/stderr # |
else                                                                                                                            # |
  echo "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} "                     > /dev/stderr # |
  echo "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"    > /dev/stderr # |
fi                                                                                                                              # |
if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                       # |
  echo -e "${R}ERROR: POST_MODULE_PREFIX is currently set but null or unset"                                      > /dev/stderr # |
  echo -e "${R}ERROR: tacc_module_canary was not found"                                                           > /dev/stderr # |
  echo -e "${R}ERROR: Something is not right. Exiting!"                                                           > /dev/stderr # |
  exit -1                                                                                                                       # |
else                                                                                                                            # |
  echo "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  "                     > /dev/stderr # |
  echo "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  "    > /dev/stderr # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
  echo "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       "                     > /dev/stderr # |
  echo "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         "                     > /dev/stderr # |
  sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}               # |
  sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}                 # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
  cat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}            | \
      GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
      GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                         > /dev/stderr # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------
#---------------------------------------
#---------------------------------------
%clean
#---------------------------------------
#---------------------------------------
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

