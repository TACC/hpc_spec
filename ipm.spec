Summary: IPM is a portable profiling infrastructure for parallel codes.
Name: ipm
Version: 2.0.6
Release: 1
License: GPL
Group: System Environment/Base
Source: %{name}-%{version}.tgz
Packager: rtevans@tacc.utexas.edu 
Buildroot: /var/tmp/%{name}%{version}-buildroot
AutoReqProv: no

%define debug_package %{nil}

%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: IPM
Group: System Environment/Base

%description 
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Integrated Performance Monitoring for HPC (IPM) is a portable profiling infrastructure for parallel codes. It provides a low-overhead performance summary of the computation and
communication in a parallel program.  IPM has extremely low overhead, is scalable
and easy to use requiring no source code modification.

%prep
rm -f %{version}.tar.gz
wget https://github.com/nerscadmin/IPM/archive/%{version}.tar.gz
rm -rf %{_topdir}/BUILD/IPM-%{version}
tar xvf %{version}.tar.gz

%build
%install
cd %{_topdir}/BUILD/IPM-%{version}
%include system-load.inc
%include compiler-load.inc
%include mpi-load.inc
module load papi

./bootstrap.sh
./configure --prefix=%{INSTALL_DIR} --with-papi=$TACC_PAPI_DIR --enable-posixio --enable-parser LDFLAGS="-pthread"
make 
make install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r %{_topdir}/BUILD/IPM-%{version}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}

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

#----------------------------------------------------------
# Lua syntax check 
#----------------------------------------------------------
if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
   echo "testing module file syntax"
   export PATH=$PATH:%{INSTALL_DIR_COMP}/bin/
   $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}/%{version}.lua
   %if "%{build_mpi4py}" == "1"
   	$RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua
   %endif
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
%clean
rm -rf $RPM_BUILD_ROOT


