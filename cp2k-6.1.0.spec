Summary: cp2k

# Give the package a base name
%define pkg_base_name cp2k
%define MODULE_VAR    CP2K

# Create some macros (spec file variables)
%define major_version 6.1.0
#%define minor_version
#%define micro_version

#%define pkg_version %{major_version}.%{minor_version}
%define pkg_version %{major_version}
### Toggle On/Off ###
%include rpm-dir.inc

%include compiler-defines.inc
%include mpi-defines.inc

#%include name-defines-noreloc.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines.inc

Name:      cp2k
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
Release:   1
License:   GPL
Group:     Applications/Chemistry
Packager:  TACC - huang@tacc.utexas.edu
Source0:   cp2k-6.1.0.tar.gz
Source1:   libxsmm-1.10.tar.gz
Source2:   libxc-4.2.3_install.tar.gz
#Source2:   libxc-4.2.3.tar.gz
Source3:   libint-1.1.5.tar.gz
#Source4:   elpa-2017.05.002.tar.gz
Source4:   elpa-2017.05.002_install.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: CP2K
Group: Applications/Chemistry
%description package
CP2K, program to perform atomistic and molecular simulations of solid state, 
liquid, molecular, and biological systems. It provides a general framework 
for different methods such as e.g., density functional theory (DFT) using 
a mixed Gaussian and plane waves approach (GPW) and classical pair and 
many-body potentials.

%package %{MODULEFILE}
Summary: CP2K modulefile
Group: Lmod/Modulefiles
%description modulefile
CP2K, program to perform atomistic and molecular simulations of solid state, 
liquid, molecular, and biological systems. It provides a general framework 
for different methods such as e.g., density functional theory (DFT) using 
a mixed Gaussian and plane waves approach (GPW) and classical pair and 
many-body potentials.

%description
CP2K, program to perform atomistic and molecular simulations of solid state, 
liquid, molecular, and biological systems. It provides a general framework 
for different methods such as e.g., density functional theory (DFT) using 
a mixed Gaussian and plane waves approach (GPW) and classical pair and 
many-body potentials.

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


%setup

# The first file will be untared as BUILD/cp2k-2.5.1
# The second call untars the second source, in a subdirectory
# of the first.
# -b <n> means unpack the nth source *before* changing directories.
# -a <n> means unpack the nth source *after* changing to the top-level build directory.
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!

%setup -T -D -a 1
# Untar and get BUILD/cp2k-6.1.0/libxsmm-1.10
%setup -T -D -a 2
# Untar and get BUILD/cp2k-6.1.0/libxc-4.2.3
%setup -T -D -a 3
# Untar and get BUILD/cp2k-6.1.0/libint-1.1.5
%setup -T -D -a 4
# Untar and get BUILD/cp2k-6.1.0/elpa-2017.05.002

%build

%install

%include system-load.inc
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

#echo "DBG> PWD = $PWD"
cp $RPM_SOURCE_DIR/cp2k_compile_Linux-x86-64-intel.popt arch/Linux-x86-64-intel.popt
cp $RPM_SOURCE_DIR/cp2k_dbcsr_operations.F src/dbcsr/ops/dbcsr_operations.F

#env &> /tmp/log_env
#env_save=$RPM_OPT_FLAGS
unset RPM_OPT_FLAGS
#export RPM_OPT_FLAGS="-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions --param=ssp-buffer-size=4 -grecord-gcc-switches   -m64 -mtune=generic"
cd libxsmm-1.10
#cp $RPM_SOURCE_DIR/libssp.a .
cp $RPM_SOURCE_DIR/cp2k_libxsmm_Makefile.inc Makefile.inc
CC=icc CXX=icpc F77=ifort make -j24 AVX=3

#export RPM_OPT_FLAGS=$env_save
#cd ../libint-1.1.5
#CC=icc CXX=icpc F77=ifort FCFLAGS="-O3 -xCORE-AVX512" CPPFLAGS="-O3 -xCORE-AVX512" CFLAGS="-O3 -xCORE-AVX512" ./configure ; make -j 24
# libint-1.1.5 does not support cross-compiling. A compiled lib is provided. 

#cd ../libxc-4.2.3
#./configure CFLAGS="-O2 -fp-model strict -xCORE-AVX512" CC=icc CXX=icpc FC=ifort --prefix=`pwd`/../libxc-4.2.3_install
#make -j 24
#make install
# libxc-4.2.3 does not support cross-compiling. A compiled lib is provided.

#cd ../elpa-2017.05.002

#export FLAGS="-O2 ${TARGET} -I${MKLROOT}/include -xCORE-AVX512"
#export LDFLAGS="-L${MKLROOT}/lib/intel64"
#export CFLAGS="${FLAGS} ${FPFLAGS} -xCORE-AVX512"
#export CXXFLAGS="${CFLAGS}"
#export FCFLAGS="${FLAGS} -I${MKLROOT}/include/intel64/lp64 -threads"
#export LIBS="-lmkl_intel_lp64 -lmkl_sequential -lmkl_core -Wl,--as-needed -liomp5 -Wl,--no-as-needed"
#export SCALAPACK_LDFLAGS="-lmkl_scalapack_lp64 -lmkl_blacs_intelmpi_lp64"

#AR="xiar" FC="mpiifort" CC="mpiicc" CXX="mpiicpc" ./configure  --prefix=`pwd`/../elpa-2017.05.002_install --enable-openmp
#make clean
#make -j 24
#make install
# elpa-2017.05.002 does not support cross-compiling.

cd ..

export cp2k_home=`pwd`

cd makefiles

make -j 24 ARCH=Linux-x86-64-intel VERSION=popt
cd ..

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

cp -P exe/Linux-x86-64-intel/cp2k.popt $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -P elpa-2017.05.002_install/lib/libelpa_openmp.so.8* $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/

#cp  -p  exe/Linux-x86-64-intel/cp2k.popt $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
#cp  -p  lib/Linux-x86-64-intel/popt/lib/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/
#cp  -r  tools $RPM_BUILD_ROOT/%{INSTALL_DIR}/
chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Copy everything from tarball over to the installation directory
#  cp * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#############################    MODULES  ######################################
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
The TACC CP2K module appends the path to the cp2k executable
to the PATH environment variable. Also TACC_CP2K_DIR is set 
to CP2K home directories. 
Since CP2K has bad performance on KNL nodes, CP2K only supports 
running on SKX nodes on Stampede 2. Intel 17 and impi 17 are needed. 
Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: CP2K")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Ab Initio Molecular Dynamics, Application")
whatis("URL: http://www.cp2k.org/")
whatis("Description: Open source Ab Initio Molecular Dynamics software")

-- Create environment variables.
local cp2k_dir="%{INSTALL_DIR}"

setenv("TACC_CP2K_DIR",cp2k_dir)
append_path("PATH",cp2k_dir)
append_path("LD_LIBRARY_PATH",pathJoin(cp2k_dir,"lib"))

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
#rm -rf $RPM_BUILD_ROOT


