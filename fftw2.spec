#
# Spec file for FFTW2
#
# Prepared on 2017-05-30 for Stampede 2.

Summary:   FFTW2 local binary install

# Give the package a base name
%define pkg_base_name fftw2 
%define MODULE_VAR FFTW2

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 1
%define micro_version 5

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

# Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc-home1.inc
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
FFTW is a C subroutine library for computing the discrete Fourier
transform (DFT) in one or more dimensions, of arbitrary input size, and of
both real and complex data (as well as of even/odd data, i.e. the discrete
cosine/sine transforms or DCT/DST).


#---------------------------------------
%prep
#---------------------------------------

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


%if "%{is_mvapich2}" == "1"
  export MPICC=mpicc
  export MPIF77=mpif90
#  export LDFLAGS=-L${MPICH_HOME}/lib
%endif
%if "%{is_impi}" == "1"
  export MPICC=mpiicc
  export MPIF77=mpiifort
#  export LDFLAGS=-L${MPICH_HOME}/intel64/lib
%endif

%if "%is_intel" == "1"
  export CFLAGS="-O3 %{TACC_VEC_OPT}"
  export LDFLAGS="%{TACC_VEC_OPT}"
  echo "I'm intelling"
%endif

%if "%is_gcc" == "1"
  export CFLAGS="-O3 %{TACC_VEC_OPT}"
  export LDFLAGS="%{TACC_VEC_OPT}"
%endif

unset PHG_CONFIG_PATH

#./configure CFLAGS="-O3 " FFLAGS="-O3 -mcmodel=medium" --prefix=%{INSTALL_DIR} --enable-shared --enable-mpi --enable-threads 
COMMON_CONFIG_ARGS="--prefix=%{INSTALL_DIR} --enable-type-prefix --enable-threads --enable-mpi"

#./configure CFLAGS="-O3 -xAVX" FFLAGS="-O3 -mcmodel=medium" ${COMMON_CONFIG_ARGS}

./configure FFLAGS="-O3 -mcmodel=medium" ${COMMON_CONFIG_ARGS}
 
make -j 16
make DESTDIR=$RPM_BUILD_ROOT install

make clean
#./configure CFLAGS="-O3 -xAVX" FFLAGS="-O3 -mcmodel=medium" ${COMMON_CONFIG_ARGS} --enable-float

./configure FFLAGS="-O3 -mcmodel=medium" ${COMMON_CONFIG_ARGS} --enable-float

make -j16
make DESTDIR=$RPM_BUILD_ROOT install


cp fortran/fftw_f77.i $RPM_BUILD_ROOT/%{INSTALL_DIR}/include
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


## Module for fftw2
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The FFTW2 modulefile defines the following environment variables:
TACC_FFTW2_DIR, TACC_FFTW2_LIB, and TACC_FFTW2_INC
for the location of the FFTW %{version} distribution,
libraries, and include files, respectively.

To use the FFTW library, compile the source code with the option:

        -I$TACC_FFTW2_INC

and add the following options to the link step for double precision:

        -L$TACC_FFTW2_LIB -ldrfftw -ldfftw

For single precison, link with:

        -L$TACC_FFTW2_LIB -lsrfftw -lsfftw

Version %{version}
]]

help(help_message,"\n")

whatis("Name: FFTW 2")
whatis("Version: %{version}")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, FFT")
whatis("URL: http://www.fftw.org")
whatis("Description: Numerical library, contains discrete Fourier transformation")


local fftw_dir="%{INSTALL_DIR}"

setenv("TACC_FFTW2_DIR",fftw_dir)
setenv("TACC_FFTW2_LIB",pathJoin(fftw_dir,"lib"))
setenv("TACC_FFTW2_INC",pathJoin(fftw_dir,"include"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'

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

########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

