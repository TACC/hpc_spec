#
# Spec file for p3dfft 2.7
#
Summary: p3dfft 2.7.7
Name: p3dfft
Version: 2.7.7
Release: 1%{?dist}
License: GPL V3
Vendor: https://code.google.com/p/p3dfft/
Group: System Environment/Base
Source: p3dfft-%{version}.tar.gz
Packager: cazes@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: p3dfft {version} local binary install
Group: System Environment/Base

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Parallel Three-Dimensional Fast Fourier Transforms, dubbed P3DFFT, is a 
library for large-scale computer simulations on parallel platforms. 3D 
FFT is an important algorithm for simulations in a wide range of fields, 
including studies of turbulence, climatology, astrophysics and material
science. 

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}


%setup -n p3dfft-%{version}

%build

%install

%include compiler-load.inc
%include mpi-load.inc
%include mpi-env-vars.inc

module load fftw3

#Remove "-lmpich" flag from Intel compile.  Not needed for mpiifort or mpif90.
sed -i -e's/-lmpichf90 -limf/-limf/' configure

#Default build, stride-1,double precision 
# make clean
export FCFLAGS="-O3 -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512 -save-temps" 
export CFLAGS="-O3 -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512"
export LDFLAGS="-O3 -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512"
./configure \
    FC=$FC \
    CC=$CC  \
  --enable-intel \
  --enable-openmp \
  --enable-stride1 \
  --enable-fftw \
  --with-fftw=${TACC_FFTW3_DIR} \
  --prefix=%{INSTALL_DIR}
make 
make DESTDIR=$RPM_BUILD_ROOT install

#Double precision, non-contiguous build
make clean
./configure \
    FC=$FC \
    CC=$CC  \
  --enable-intel \
  --enable-openmp \
  --enable-fftw \
  --with-fftw=${TACC_FFTW3_DIR} \
  --prefix=%{INSTALL_DIR}/noncontiguous
make 
make DESTDIR=$RPM_BUILD_ROOT install

#Single precision build, stride1
make clean
./configure \
    FC=$FC \
    CC=$CC  \
  --enable-intel \
  --enable-openmp \
  --enable-fftw \
  --enable-single \
  --enable-stride1 \
  --with-fftw=${TACC_FFTW3_DIR} \
  --prefix=%{INSTALL_DIR}/single_stride1
make 
make DESTDIR=$RPM_BUILD_ROOT install

#Single precision build, non-contiguous
make clean
./configure \
    FC=$FC \
    CC=$CC  \
  --enable-intel \
  --enable-openmp \
  --enable-fftw \
  --enable-single \
  --with-fftw=${TACC_FFTW3_DIR} \
  --prefix=%{INSTALL_DIR}/single_noncontiguous
make 
make DESTDIR=$RPM_BUILD_ROOT install

## Module for p3dfft
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_message=[[
P3DFFT is a highly scalable numerical library for programs running on 
parallel computers. P3DFFT implements Fourier Transforms in three 
dimensions as well as related algorithms, in a highly efficient manner.
More information may be found at: https://portal.xsede.org/software/p3dfft

The p3dfft modulefile defines the following environment variables
for the double-precison, stride-1 optimized version of the 
library:
    $TACC_P3DFFT_DIR 
    $TACC_P3DFFT_LIB
    $TACC_P3DFFT_INC
    $TACC_P3DFFT_TESTS

To use the p3dfft library, compile your source code with:

	-I$TACC_P3DFFT_INC

and add the following options to the link step:

	-Wl,-rpath,$TACC_P3DFFT_LIB  -L$TACC_P3DFFT_LIB -lp3dfft

Other versions of the p3dfft libraries that are optimized for 
single-precision calculations or non-contiguous data are available.  
Please refer to the software distribution page for more details:
    https://code.google.com/p/p3dfft 

To use one of the the other libraries, use the appropriate environment 
variable for compiling and linking.

Single Precision, stride-1:
    $TACC_P3DFFT_SINGLE_LIB
    $TACC_P3DFFT_SINGLE_INC

Single Precision, non-contiguous:
    $TACC_P3DFFT_SINGLE_NONCONTIG_LIB
    $TACC_P3DFFT_SINGLE_NONCONTIG_INC

Double Precision, non-contiguous:
    $TACC_P3DFFT_NONCONTIG_LIB
    $TACC_P3DFFT_NONCONTIG_INC


Version %{version}
]]

help(help_message,"\n")

whatis("Name: p3dfft ")
whatis("Version: %{version}")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, FFT, Parallel")
whatis("URL: https://code.google.com/p/p3dfft ")
whatis("Description: Numerical library, contains discrete Fourier transformation")

--  Regular build, double precision, stride 1
local p3dfft_dir="%{INSTALL_DIR}"
setenv("TACC_P3DFFT_DIR",p3dfft_dir)
setenv("TACC_P3DFFT_LIB",pathJoin(p3dfft_dir,"lib"))
setenv("TACC_P3DFFT_INC",pathJoin(p3dfft_dir,"include"))
setenv("TACC_P3DFFT_TESTS",pathJoin(p3dfft_dir,"share/p3dfft-samples"))

--  build, double precision, non-contiguous
local p3dfft_dir="%{INSTALL_DIR}/noncontiguous"
setenv("TACC_P3DFFT_NONCONTIG_LIB",pathJoin(p3dfft_dir,"lib"))
setenv("TACC_P3DFFT_NONCONTIG_INC",pathJoin(p3dfft_dir,"include"))

--  build, single precision, stride1
local p3dfft_dir="%{INSTALL_DIR}/single_stride1"
setenv("TACC_P3DFFT_SINGLE_LIB",pathJoin(p3dfft_dir,"lib"))
setenv("TACC_P3DFFT_SINGLE_INC",pathJoin(p3dfft_dir,"include"))

--  build, single precision, non-contiguous
local p3dfft_dir="%{INSTALL_DIR}/single_noncontiguous"
setenv("TACC_P3DFFT_SINGLE_NONCONTIG_LIB",pathJoin(p3dfft_dir,"lib"))
setenv("TACC_P3DFFT_SINGLE_NONCONTIG_INC",pathJoin(p3dfft_dir,"include"))

--
-- Append paths
-- only for default install
append_path("LD_LIBRARY_PATH",pathJoin(p3dfft_dir,"lib"))
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for p3dfft
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
