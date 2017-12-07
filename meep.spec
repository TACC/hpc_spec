# $Id: meep.spec,v 1.3 2015/04/22 

Summary: Meep is a free finite-difference time-domain simulation software package
Name: meep
Version: 1.3
Release: 3
License: GPL
URL: http://ab-initio.mit.edu/wiki/index.php/Meep
Group: applications/electromagnetics
Source: meep-1.3.tar.gz
Source1: libctl-3.2.1.tar.gz
Source2: harminv-1.3.1.tar.gz
Packager: cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define  MODULE_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%package -n tacc-%{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: Meep is a free finite-difference time-domain simulation software package
Group: applications/electromagnetics

%description
%description -n tacc-%{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Meep (or MEEP) is a free finite-difference time-domain (FDTD)
simulation software package developed at MIT to model electromagnetic
systems, along with our MPB eigenmode package. Its features include:
Free software under the GNU GPL.  Simulation in 1d, 2d, 3d, and
cylindrical coordinates.  Distributed memory parallelism on any system
supporting the MPI standard. Portable to any Unix-like system
(GNU/Linux is fine).  Dispersive and nonlinear (Kerr & Pockels)
materials.  Magnetic permeability and electric/magnetic
conductivities.

# The prep stage.  To execute just the prep stage do 'rpmbuild -bp'
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# The first call to setup untars the first source.  
%setup

# The second call untars the second source, in a subdirectory
# of the first. 
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory. 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup -T -D -a 1

# We should now have a ../BUILD/meep-<version> and, within that, a
# ../BUILD/meep-<version>/libctl-3.2.1 directory.

# Third call to setup, untar the third source (harminv) in a subdirectory
%setup -T -D -a 2

# The build step.  To just test the build step do 'rpmbuild -bc'
%build

set +x
%include compiler-load.inc
%include mpi-load.inc

# Load additional modules needed for meep
#Don't need for intel
#module load mkl
module load fftw3
module load hdf5
module load gsl

set -x

# Create temporary directory for the install.  We need this to
# trick meep into thinking libctl is installed in its final location!
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
#tacctmpfs --mount %{INSTALL_DIR}

# First build libctl.  Requires guile-devel RPM.
# We will build libctl in its own directory off of the meep install.
mkdir %{INSTALL_DIR}/libctl
cd libctl-3.2.1
./configure --prefix=%{INSTALL_DIR}/libctl
make
make install


# Next, build harminv.  Also in its own directory off of the meep install.
# Note also that we set a value close to DBL_MAX for the #define'd variable INFINITY
# which is used in the code.  This is required to prevent a divide by zero.
#./configure \
#  CFLAGS="-DINFINITY=1.79769e+308 -vec-report0" \
#  --prefix=%{INSTALL_DIR}/harminv \
#  --with-blas="-Wl,-rpath,${TACC_MKL_LIB} -L${TACC_MKL_LIB} -lmkl_intel_lp64 -lmkl_rt -lpthread -lm" \
#  --with-lapack="-Wl,-rpath,${TACC_MKL_LIB} -L${TACC_MKL_LIB} -lmkl_lapack95_lp64 -lmkl_rt -lpthread -lm"
#Updated for intel 15/mkl 11.2
export HARMINV_MKL="-L${MKLROOT}/lib/intel64 -lmkl_intel_lp64 -lmkl_core -lmkl_sequential -lpthread -lm"
mkdir %{INSTALL_DIR}/harminv
cd ../harminv-1.3.1
./configure \
  CFLAGS="-DINFINITY=1.79769e+308 -vec-report0" \
  --prefix=%{INSTALL_DIR}/harminv \
  --with-blas="$HARMINV_MKL" \
  --with-lapack="$HARMINV_MKL"
make
make install


# Now, build meep
cd ..

# To make configuring easier, create an environment variable which points
# to where we just installed ctl.
export MY_CTL_DIR=%{INSTALL_DIR}/libctl

# The gen-ctl-io program must be in your PATH to pass configure!
export PATH=${MY_CTL_DIR}/bin:$PATH

# Also, ensure that the harminv installation dir is set so we can refer to it below.
export MY_HARMINV_DIR=%{INSTALL_DIR}/harminv

# The -DMPICH_IGNORE_CXX_SEEK flag is only needed for mvapich2
# builds, it should have no effect on mvapich1, but we have not 
# tested that yet...
./configure --prefix=%{INSTALL_DIR} \
  CC=mpicc \
  CXX=mpicxx \
  F77=mpif77 \
  LDFLAGS="-L${TACC_FFTW3_LIB} -lfftw3 -L${TACC_HDF5_LIB} -L${TACC_GSL_LIB} -L${MY_CTL_DIR}/lib -L${MY_HARMINV_DIR}/lib" \
  CPPFLAGS="-DMPICH_IGNORE_CXX_SEEK -I${TACC_FFTW3_INC} -I${TACC_HDF5_INC} -I${TACC_GSL_INC} -I${MY_CTL_DIR}/include  -I${MY_HARMINV_DIR}/include" \
  CXXFLAGS="-O3 -vec-report0" \
  --with-libctl="${MY_CTL_DIR}/share/libctl" \
  --with-mpi \
  --with-blas="-Wl,-rpath,${TACC_MKL_LIB} -L${TACC_MKL_LIB} -lmkl_blas95_lp64 -lmkl_rt -lpthread -lm" \
  --with-lapack="-Wl,-rpath,${TACC_MKL_LIB} -L${TACC_MKL_LIB} -lmkl_lapack95_lp64 -lmkl_rt -lpthread -lm"

# The argument of --with-libctl *must* point to (what will be) the
# *final* location of base/ctl.scm.  This is the reason we need the tmpfs trick.

make 
make install

# Temporarily exit
# exit 1

# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.
cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/
#tacctmpfs --umount %{INSTALL_DIR}

# Remove any old module files and create anew
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#################################################################
#
# This module file sets up the environment variables and path for meep.
#
#############################################################################

proc ModulesHelp { } {
puts stderr "The %{name} module file defines the following environment variables:\n"
puts stderr "TACC_MEEP_DIR, TACC_MEEP_LIB, TACC_MEEP_INC, and TACC_MEEP_BIN."
puts stderr ""
puts stderr "The meep executable is \$TACC_MEEP_BIN/meep-mpi"
puts stderr ""
puts stderr "Version %{version}"
}
-- Prerequisites
prereq("gsl")

module-whatis "Name: Meep"
module-whatis "Version: %{version}"
module-whatis "Category: Applications/IO"
module-whatis "Description: Meep is a free finite-difference time-domain simulation software package" 
module-whatis "URL: http://ab-initio.mit.edu/wiki/index.php/Meep"

setenv TACC_MEEP_DIR %{INSTALL_DIR}
setenv TACC_MEEP_INC %{INSTALL_DIR}/include
setenv TACC_MEEP_LIB %{INSTALL_DIR}/lib
setenv TACC_MEEP_BIN %{INSTALL_DIR}/bin

# Also add libctl env vars.
setenv TACC_CTL_DIR %{INSTALL_DIR}/libctl
setenv TACC_CTL_INC %{INSTALL_DIR}/libctl/include
setenv TACC_CTL_LIB %{INSTALL_DIR}/libctl/lib
setenv TACC_CTL_BIN %{INSTALL_DIR}/libctl/bin

# Also add harminv env vars.
setenv TACC_HARMINV_DIR %{INSTALL_DIR}/harminv
setenv TACC_HARMINV_INC %{INSTALL_DIR}/harminv/include
setenv TACC_HARMINV_LIB %{INSTALL_DIR}/harminv/lib
setenv TACC_HARMINV_BIN %{INSTALL_DIR}/harminv/bin

prepend-path    PATH                %{INSTALL_DIR}/bin

# And libctl binary files location.
prepend-path    PATH                %{INSTALL_DIR}/libctl/bin

# No man pages for meep
#prepend-path    MANPATH             %{INSTALL_DIR}/man

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0###################################################
##
## version file for %{name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}


%files -n tacc-%{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
