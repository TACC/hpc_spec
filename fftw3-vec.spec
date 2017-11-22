# Antia Lamas-Linares
# 2017-05-17
# Modified for Stampede 2 deployment and avx512
# This version is patch 2 with the missing fortran hearders
# 
# 2017-07-10 
# User ticket TUP:38819 pointed out incorrect files in libtool files
# It appears this will not work as a relocatable
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
%define pkg_base_name fftw3-%{suf}
%define MODULE_VAR    FFTW3

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 3
%define micro_version 6

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
#%include name-defines-noreloc.inc
%include name-defines-scratch-noreloc.inc
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

Release:   2%{?dist}
License:   GPL
Group:     System Environment/Base
URL:       http://www.fftw.org
Packager:  TACC - alamas@tacc.utexas.edu
Source:    fftw-%{pkg_version}.tar.gz

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
FFTW is a C subroutine library for computing the discrete Fourier                                             |                                                                                                             
transform (DFT) in one or more dimensions, of arbitrary input size, and of                                    |%package %{PACKAGE}                                                                                          
both real and complex data (as well as of even/odd data, i.e. the discrete                                    |Summary: The package RPM                                                                                     
cosine/sine transforms or DCT/DST). 

#---------------------------------------
%prep
#---------------------------------------

echo %{dovec}
echo %{suf}

%if "%{suf}" == "default"
  echo "Define suf please."
  exit -1
%endif



#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n fftw-%{pkg_version}

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
ml use /scratch/projects/compilers/modulefiles
# Load Compiler
%include compiler-load.inc
# Load MPI Library
%include mpi-load.inc

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


## Notes on fftw3 configure options
## --with-pic try to use only PIC/non-PIC objects [default=use both]
## --disable-dependency-tracking  speeds up one-time build (?)
## --enable-static[=PKGS]  build static libraries [default=yes]
## --enable-shared[=PKGS]  build shared libraries [default=no]
## --enable-single         compile fftw in single precision
## --enable-mpi            compile FFTW MPI library (default?)

### Make double-precision version w/o mpi support
#./configure --with-pic \
#            --enable-shared \
#            --enable-openmp \
#            --enable-threads \
#            --disable-dependency-tracking \
#            --prefix=%{INSTALL_DIR}
#make -j 4
#make DESTDIR=$RPM_BUILD_ROOT install
#
### Make single-precision version w/o mpi support
#make clean
#./configure --with-pic \
#            --enable-single \
#            --enable-shared \
#            --enable-openmp \
#            --enable-threads \
#            --disable-dependency-tracking \
#            --prefix=%{INSTALL_DIR}
#make -j 4
#make DESTDIR=$RPM_BUILD_ROOT install

## Make double-precision version w/ mpi support
%if "%{is_mvapich2}" == "1"
  export MPICC=mpicc
#  export LDFLAGS=-L${MPICH_HOME}/lib
%endif
%if "%{is_cmpich}" == "1"
    export MPICC=mpicc
  #  export LDFLAGS=-L${MPICH_HOME}/lib
%endif

%if "%{is_impi}" == "1"
  export MPICC=mpiicc
  export LDFLAGS=-L${MPICH_HOME}/intel64/lib
%endif

%if "%is_intel" == "1"
  #export CFLAGS="-O3 -xAVX -axCORE-AVX2"
  #export LDFLAGS="-xAVX -axCORE-AVX2"
  export CFLAGS="-O3 %{TACC_VEC_OPT}"
  export LDFLAGS="%{TACC_VEC_OPT}"
  echo "I'm intelling"
%endif

%if "%is_gcc" == "1"
  #export CFLAGS="-O3 -march=sandybridge -mtune=haswell"
  #export LDFLAGS="-march=sandybridge -mtune=haswell"
  #per Todd's prescription for gcc KNL fat binaries
  export CFLAGS="-O3 %{TACC_VEC_OPT}"
  export LDFLAGS="%{TACC_VEC_OPT}"
%endif

### Antia adding --enable-avx512 line for the KNL build
./configure --prefix=%{INSTALL_DIR} \
            --host=x86_64 \
            --with-pic \
            --enable-shared \
            --enable-openmp \
            --enable-threads \
            --disable-dependency-tracking \
            --enable-mpi \
            --enable-sse2 \
            --enable-avx \
            --enable-avx2 \
%if %{dovec}
	    --enable-avx512
%endif


make -j 28
make DESTDIR=$RPM_BUILD_ROOT install

## Make single-precision version w/ mpi support
### Antia adding --enable-avx2 line for the KNL build
make clean
./configure --prefix=%{INSTALL_DIR} \
            --host=x86_64 \
            --with-pic \
            --enable-single \
            --enable-shared \
            --enable-openmp \
            --enable-threads \
            --disable-dependency-tracking \
            --enable-mpi \
            --enable-sse \
            --enable-sse2 \
            --enable-avx \
            --enable-avx2 \
%if %{dovec}
	    --enable-avx512
%endif


make -j 28
make DESTDIR=$RPM_BUILD_ROOT install

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
The FFTW 3.3 modulefile defines the following environment variables:
TACC_FFTW3_DIR, TACC_FFTW3_LIB, and TACC_FFTW3_INC
for the location of the FFTW %{version} distribution,
libraries, and include files, respectively.

To use the FFTW3 library, compile your source code with:

	-I$TACC_FFTW3_INC

and add the following options to the link step for serial codes:

	-Wl,-rpath,$TACC_FFTW3_LIB  -L$TACC_FFTW3_LIB -lfftw3

for MPI codes:

	-Wl,-rpath,$TACC_FFTW3_LIB -L$TACC_FFTW3_LIB -lfftw3_mpi -lfftw3

In addition, a single-precision fftw library is also available
by adding an 'f' suffix to the library names above:

(serial):	-L$TACC_FFTW3_LIB -lfftw3f
(mpi): 		-L$TACC_FFTW3_LIB -lfftw3f_mpi -lfftw3f


Version %{version}
]]

help(help_message,"\n")

whatis("Name: FFTW 3.3")
whatis("Version: %{version}")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, FFT, Parallel")
whatis("URL: http://www.fftw.org")
whatis("Description: Numerical library, contains discrete Fourier transformation")

local fftw_dir="%{INSTALL_DIR}"

setenv("TACC_FFTW3_DIR",fftw_dir)
setenv("TACC_FFTW3_LIB",pathJoin(fftw_dir,"lib"))
setenv("TACC_FFTW3_INC",pathJoin(fftw_dir,"include"))

--
-- Append paths
--
append_path("LD_LIBRARY_PATH",pathJoin(fftw_dir,"lib"))
append_path("PATH",pathJoin(fftw_dir,"bin"))
append_path("MANPATH",pathJoin(fftw_dir,"man"))
append_path("PKG_CONFIG_PATH",pathJoin(fftw_dir,"lib/pkgconfig"))

family("fftw3")

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

