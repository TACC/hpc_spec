#
# Spec file for FFTW 3.3.4
#
# Prepared for Wrangler - 2015-05-07

Summary: FFTW 3.3
Name: fftw3
Version: 3.3.4
Release: 1
License: GPL
Vendor: www.fftw.org 
Group: System Environment/Base
Source: fftw-%{version}.tar.gz
Packager: alamas@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: FFTW %{version} local binary install
Group: System Environment/Base

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
FFTW is a C subroutine library for computing the discrete Fourier
transform (DFT) in one or more dimensions, of arbitrary input size, and of
both real and complex data (as well as of even/odd data, i.e. the discrete
cosine/sine transforms or DCT/DST). 

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


%setup -n fftw-%{version}

%build

%install

%include compiler-load.inc
%include mpi-load.inc

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
%if "%{is_impi}" == "1"
  export MPICC=mpiicc
  export LDFLAGS=-L${MPICH_HOME}/intel64/lib
%endif

%if "%is_intel" == "1"
  export CFLAGS="-O3 -xAVX"
%endif

./configure --with-pic \
            --enable-shared \
            --enable-openmp \
            --enable-threads \
            --disable-dependency-tracking \
            --enable-mpi \
            --enable-sse2 \
            --enable-avx \
            --prefix=%{INSTALL_DIR}
make -j 16
make DESTDIR=$RPM_BUILD_ROOT install

## Make single-precision version w/ mpi support
make clean
./configure --with-pic \
            --enable-single \
            --enable-shared \
            --enable-openmp \
            --enable-threads \
            --disable-dependency-tracking \
            --enable-mpi \
            --enable-sse \
            --enable-sse2 \
            --enable-avx \
            --prefix=%{INSTALL_DIR}
make -j 16
make DESTDIR=$RPM_BUILD_ROOT install


## Module for fftw-3.3
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

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

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for FFTW3
##

set     ModulesVersion      "%version"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}


%post
%clean
rm -rf $RPM_BUILD_ROOT
