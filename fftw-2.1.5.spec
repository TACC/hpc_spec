#
# Spec file for FFTW2
#
Summary:   FFTW2 local binary install
Name:      fftw2
Version:   2.1.5
Release:   2
License: GPL
Vendor:    www.fftw.org 
Group:     System Environment/Base
Source:    fftw-%{version}.tar.gz
Packager:  alamas@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define __spec_install_post /usr/lib/rpm/brp-compress

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles


%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: FFTW 2.x local binary install
Group: System Environment/Base

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
FFTW is a C subroutine library for computing the discrete Fourier
transform (DFT) in one or more dimensions, of arbitrary input size, and of
both real and complex data (as well as of even/odd data, i.e. the discrete
cosine/sine transforms or DCT/DST).

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n fftw-%{version}


%build

%install

%include compiler-load.inc
%include mpi-load.inc

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

unset PHG_CONFIG_PATH

#./configure CFLAGS="-O3 " FFLAGS="-O3 -mcmodel=medium" --prefix=%{INSTALL_DIR} --enable-shared --enable-mpi --enable-threads 
#make
#make DESTDIR=$RPM_BUILD_ROOT install
#make clean
COMMON_CONFIG_ARGS="--prefix=%{INSTALL_DIR} --enable-type-prefix --enable-threads --enable-mpi"

./configure CFLAGS="-O3 -xAVX" FFLAGS="-O3 -mcmodel=medium" ${COMMON_CONFIG_ARGS}
 make -j 16 
make DESTDIR=$RPM_BUILD_ROOT install

make clean
./configure CFLAGS="-O3 -xAVX" FFLAGS="-O3 -mcmodel=medium" ${COMMON_CONFIG_ARGS} --enable-float
make -j16
make DESTDIR=$RPM_BUILD_ROOT install


cp fortran/fftw_f77.i $RPM_BUILD_ROOT/%{INSTALL_DIR}/include

## Module for fftw2
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
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

whatis("Name: FFTW")
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
#%Module3.1.1#################################################
##
## version file for netcdf
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(755,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT
