#
# Spec file for PnetCDF
#
%define version_short 1.11

Summary:   Parallel NetCDF is a parallel version of netcdf(NOT NetCDF 4.)
Name:      pnetcdf
Version:   1.11.2
Release:   1
License:   BSD
Group:     applications/io
Source:    pnetcdf-%{version}.tar.gz
URL:       https://parallel-netcdf.github.io/
Distribution: RedHat Linux
Vendor:    Unidata Program Center, UCAR
Packager:  TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%define APPS /opt/apps
%define MODULES modulefiles

%include rpm-dir.inc
%include compiler-defines.inc

# This is a hack to prevent mpi-defines.inc to complain if mpi is not set.
%include mpi-defines.inc

# build parallel version of package
%define PNAME           pnetcdf
%define INSTALL_DIR     %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR      %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define RPM_NAME        %{PNAME}-%{comp_fam_ver}-%{mpi_fam_ver}
%define NETCDF_VERSION    (PnetCDF)
%{echo: WITH MPI %PNAME-%{comp_fam_ver}-%{mpi_fam_ver}}
%{echo: WITH MPI %RPM_NAME}

#  package -n %{name}-%{comp_fam_ver}
%package -n %{RPM_NAME}
Summary: Parallel netCDF(PnetCDF) is a library providing high-performance I/O while maintaining compatibility with Unidata's NetCDF. 
Group: applications/io

%description
%description -n %{RPM_NAME}
Parallel netCDF (PnetCDF) is a library providing high-performance I/O while still maintaining file-format compatibility with Unidata's NetCDF.
NetCDF gives scientific programmers a space-efficient and portable means for storing data. However, it does so in a serial manner, making it difficult to achieve high I/O performance. By making some small changes to the NetCDF APIs, PnetCDF can use MPI-IO to achieve high-performance parallel I/O. 

%prep

rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# The first call to setup untars the main netcdf source
%setup
pwd

%build

%install

pwd
%include compiler-load.inc
%include mpi-load.inc

%if "%{is_intel}" == "1" || "%{is_intel19}" == "1" || "%{is_intel18}" == "1"

	# environment used for configure with intel compiler
        export CFLAGS="-O3 -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512 "
        export FFLAGS="-O3 -assume buffered_io -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512 "
        export CXXFLAGS="-O3 -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512 "
        export LDFLAGS="-O3 -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512 "
%endif

%if "%{mpi_fam}" != "none"
   CC=mpicc
   CXX=mpicxx
   FC=mpif90
   F77=mpif77
   F90=$FC
%endif


%if "%{mpi_fam}" == "impi"
   CC=mpiicc
   CXX=mpiicxx
   FC=mpiifort
   F77=mpiifort
   F90=$FC
%endif

#
# config/make:
#

# Create temporary directory for the install.  We need this to
#mkdir -p             %{INSTALL_DIR}
#mount -t tmpfs tmpfs %{INSTALL_DIR}
#tacctmpfs --mount %{INSTALL_DIR}

pwd
./configure --prefix=%{INSTALL_DIR} --enable-fortran --with-mpi=$MPICH_HOME/intel64
make 
make install


# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
#umount %{INSTALL_DIR}
# tacctmpfs --umount %{INSTALL_DIR}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--netcdf

local help_message = [[
IMPORTANT NOTE: TACC has several different versions of netcdf
installed.  Below is a list of each module type:

netcdf/3.6.3           -- Classic netcdf (serial)
netcdf/4.x.x           -- Serial version of Netcdf4 based upon hdf5 and
is backwards compatiable with classic netcdf (serial)
parallel-netcdf/4.x.x  -- Parallel version of Netcdf4 based upon parallel hdf5 (parallel)
pnetcdf/1.x.x          -- Parallel netcdf(PnetCDF) that supports netcdf in the classic formats, CDF-1 and CDF-2 (parallel)

The command "module avail netcdf" will show which versions of netcdf are
available for your current compiler/mpi module environment.

The %{name} module file defines the following environment variables:
TACC_PNETCDF_DIR, TACC_PNETCDF_BIN, TACC_PNETCDF_LIB, and 
TACC_PNETCDF_INC forthe location of the NETCDF distribution, binaries,
libraries, and include files, respectively.

Parallel netCDF (PnetCDF) is a library providing high-performance I/O while still maintaining file-format compatibility with Unidata's NetCDF.  NetCDF gives scientific programmers a space-efficient and portable means for storing data. However, it does so in a serial manner, making it difficult to achieve high I/O performance. By making some small changes to the NetCDF APIs, PnetCDF can use MPI-IO to achieve high-performance parallel I/O. 

To use the NETCDF library, compile the source code with the option:

	-I${TACC_PNETCDF_INC} 

Add the following options to the link step: 

	-L${TACC_PNETCDF_LIB} -lpnetcdf 

Version %{version}

]]

help(help_message,"\n")


whatis("Parallel-netCDF(Pnetcdf)")
whatis("Version: %{version}")
whatis("Category: library, runtime support")
whatis("Keywords: I/O, Library")
whatis("Description: I/O library which stores and retrieves data in self-describing, machine-independent datasets%{NETCDF_VERSION}." )
whatis(" URL: https://parallel-netcdf.github.io/index.html")

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH",           "%{INSTALL_DIR}/bin")
prepend_path("MANPATH",        "%{INSTALL_DIR}/share/man")

--Env variables 
setenv("PNETCDF", "%{INSTALL_DIR}")
setenv("TACC_PNETCDF_DIR", "%{INSTALL_DIR}")
setenv("TACC_PNETCDF_INC", "%{INSTALL_DIR}/include")
setenv("TACC_PNETCDF_LIB", "%{INSTALL_DIR}/lib")
setenv("TACC_PNETCDF_BIN", "%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for NetCDF
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{RPM_NAME}
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post


%clean
rm -rf $RPM_BUILD_ROOT

%changelog

