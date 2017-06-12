# See http://ipm-hpc.sourceforge.net/overview.html -- project page
#     http://sourceforge.net/projects/ipm-hpc/files/ -- source code 
# Notes on deprecation http://glennklockwood.blogspot.com/2013/05/building-ipm-0983-for-lightweight-mpi.html
Summary: IPM is a portable profiling infrastructure for parallel codes.
Name: ipm
Version: 0.983
Release: 4
License: GPL
Group: System Environment/Base
Source0: %{name}-%{version}.tgz
Source1: ploticus242_linuxbin64.tar.gz
Packager: rtevans@tacc.utexas.edu 
Buildroot: /var/tmp/%{name}%{version}-buildroot
AutoReqProv: no

%define debug_package %{nil}
%include rpm-dir.inc

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: IPM
Group: System Environment/Base

%description 
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}

IPM is a portable profiling infrastructure for parallel codes. It
provides a low-overhead performance summary of the computation and
communication in a parallel program. The amount of detailed reported
is selectable at runtime via environment variables or through a
MPI_Pcontrol interface. IPM has extremely low overhead, is scalable
and easy to use requiring no source code modification.

%prep
if [ ! -f ploticus242_linuxbin64.tar.gz]; then
   wget http://sourceforge.net/projects/ploticus/files/ploticus/2.42/ploticus242_linuxbin64.tar.gz
fi
%setup -n %{name}
%setup -n %{name} -T -D -a 1

%build

if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   module purge
   clearMT
   export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
 fi

module purge
module load TACC

# We want papi
module load papi
module load %{comp_module}

export ARCH=x86_64
export CFLAGS="-fPIC"
%if "%{comp_fam}" == "intel"
  %define ipm_comp INTEL
%endif
%if "%{comp_fam}" == "gcc"
  %define ipm_comp GCC
%endif
export CXX=icpc

sed -i 's/count/count_lo/' configure

./configure --prefix=%{INSTALL_DIR} --with-os=LINUX  --with-arch=X86 --with-hpcname=stampede --with-compiler=%{ipm_comp} --with-cpu=NEHALEM --switch=INFINIBAND --with-papiroot=$TACC_PAPI_DIR --with-hpm=PAPI --with-io=mpiio

chmod +x ipm_key
echo $PATH
make
make shared
make install

%install

rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

cp -r %{_topdir}/BUILD/ipm/ploticus242/bin $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r %{_topdir}/BUILD/ipm/bin $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r %{_topdir}/BUILD/ipm/lib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp -r %{_topdir}/BUILD/ipm/include $RPM_BUILD_ROOT/%{INSTALL_DIR}/
cp %{_topdir}/BUILD/ipm/ipm_key $RPM_BUILD_ROOT/%{INSTALL_DIR}/include/

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'

#%Module1.0##################################################################
#
# This module file sets up the environment variables and path for the
# IPM profiling library.
#
#############################################################################

proc ModulesHelp { } {
puts stderr "The IPM modulefile defines the following environment variables:"
puts stderr "TACC_IPM_DIR, TACC_IPM_BIN and TACC_IPM_LIB for the location of the "
puts stderr "IPM distribution, binaries, and libraries respectively.\n"

puts stderr "To use the IPM profiling library, please load the appropriate ipm module" 
puts stderr "and then set the LD_PRELOAD variable directly within your job script as follows:"
puts stderr " "
puts stderr "#-- Example Job Script Excerpt (csh syntax)"
puts stderr "module load ipm"
puts stderr "setenv LD_PRELOAD \$TACC_IPM_LIB/libipm.so"
puts stderr "ibrun ./a.out"
puts stderr " "
puts stderr "#-- Example Job Script Excerpt (bash syntax)"
puts stderr "module load ipm"
puts stderr "export LD_PRELOAD=\$TACC_IPM_LIB/libipm.so"
puts stderr "ibrun ./a.out"
puts stderr " "
puts stderr "** Important Note:\n"
puts stderr "TACC staff recommend that you set the LD_PRELOAD environment"
puts stderr "only within your job script as opposed to making permanent"
puts stderr "environment changes via shell startup scripts."


puts stderr "\nVersion %{version}"

}

module-whatis "Name: IPM"
module-whatis "Version: %{version}"
module-whatis "Category: library, profiling"
module-whatis "URL: http://ipm-hpc.sourceforge.net"
module-whatis "Description: Integrated Performance Monitoring"

#
# Load papi if necessary
#

if [ expr [ module-info mode load ] || [module-info mode display ] ] {
	if {  ![is-loaded papi]  } {
                module load papi
        }
}


#
# Create environment variables.
#
setenv          TACC_IPM_DIR        %{INSTALL_DIR}
setenv          TACC_IPM_LIB        %{INSTALL_DIR}/lib
setenv          TACC_IPM_BIN        %{INSTALL_DIR}/bin
setenv  	IPM_KEYFILE         %{INSTALL_DIR}/include/ipm_key

#
# Append path
#

prepend-path    PATH   		%{INSTALL_DIR}/bin

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for %{name}
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(755,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT


