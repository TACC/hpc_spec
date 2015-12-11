%global debug_package %{nil}
%global __jar_repack 0
# Tweak to have debuginfo - part 1/2
%define __debug_install_post %{_builddir}/%{?buildsubdir}/find-debuginfo.sh %{_builddir}/%{?buildsubdir}\
%{nil}

%global pkgver sles11.3
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/cuda/%{version}
%define MODULE_DIR %{APPS}/%{MODULES}/cuda

Summary:	NVIDIA CUDA Toolkit libraries
Version:	7.0
Name:		tacc-cuda-%{version}
Release:        28	
License:	Redistributable, no modification permitted
Group:		Development/Languages
URL:		http://www.nvidia.com/cuda
%if !0%{?rhel}
Source0:	http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers/cuda_7.0.28_linux.run
%endif
Source1:	http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers/cuda_7.0.28_linux.run
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

ExclusiveArch:  		x86_64
Provides:			cuda-7.0 = %{version}-%{release}
AutoReqProv: 			no



# Filter out provides
#%filter_provides_in (%{_datadir}|%{_libdir}/cuda/libnvvp)

%description
NVIDIA(R)CUDA(TM) is a general purpose parallel computing architecture
that leverages the parallel compute engine in NVIDIA graphics
processing units (GPUs) to solve many complex computational problems
in a fraction of the time required on a CPU. It includes the CUDA
Instruction Set Architecture (ISA) and the parallel compute engine in
the GPU. To program to the CUDATM architecture, developers can, today,
use C, one of the most widely used high-level programming languages,
which can then be run at great performance on a CUDATM enabled
processor. Other languages will be supported in the future, including
FORTRAN and C++.

This package contains the libraries and attendant files needed to run
programs that make use of CUDA.

#%package libs
#Summary:	Libraries for %{name}
#Group:		Development/Libraries
#
#%description libs
#This package contains libraries needed for running CUDA based applications.
#

%ifarch x86_64
%package libs-32bit
Summary:	32bit Libraries for %{name}
Group:		Development/Libraries
Requires:	cuda-7.0 = %{version}-%{release}
AutoReqProv: 	no

%description libs-32bit
This package contains libraries needed for running 32-bit CUDA based applications.
%endif

%package doc
Summary:        Documentation for CUDA Toolkit
Group:		Documentation
Requires:	cuda-7.0 = %{version}-%{release}
AutoReqProv: 	no

%description doc
Documentation for CUDA Toolkit

%package nsight
Summary:        NSight CUDA Integrated Development Environment 
Group:		Development/Tools
Requires:	cuda-7.0 = %{version}-%{release}
AutoReqProv: 	no

%description nsight
This package contains NSight CUDA Integrated Development Environment


%prep
%setup -q -T -c %{name}-%{version}.%{release}

%build
# Nothing to build
echo "Nothing to build"

%install
export TMPDIR=/var/tmp
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
#   -toolkit            : Install CUDA 6.0 Toolkit
#   -toolkitpath=<PATH> : Specify path for CUDA location (default: /usr/local/cuda-7.0)
#   -samples            : Install CUDA 6.0 Samples
#   -samplespath=<PATH> : Specify path for Samples location (default: /usr/local/cuda-7.0/samples)
%global install_options -silent -override -toolkit -toolkitpath=$RPM_BUILD_ROOT%{INSTALL_DIR} -samples -samplespath=$RPM_BUILD_ROOT%{INSTALL_DIR}/samples
%ifarch %{ix86}
bash %{SOURCE0} %{install_options}
%else
bash %{SOURCE1} %{install_options}
%endif

# Tweak to have debuginfo - part 2/2
cp -p %{_prefix}/lib/rpm/find-debuginfo.sh .
sed -i -e 's|strict=true|strict=false|' find-debuginfo.sh

#Remove the error about gcc 4.6, it's what we have and seems to work
sed -i -e '/error -- unsupported GNU version/d' $RPM_BUILD_ROOT%{INSTALL_DIR}/include/host_config.h

# Remove buildroot
sed -i -e s,$RPM_BUILD_ROOT,,g $RPM_BUILD_ROOT%{INSTALL_DIR}/bin/nsight
sed -i -e s,$RPM_BUILD_ROOT,,g $RPM_BUILD_ROOT%{INSTALL_DIR}/bin/.uninstall_manifest_do_not_delete.txt
find $RPM_BUILD_ROOT%{INSTALL_DIR}/samples -name Makefile | 
   xargs sed -i -e s,$RPM_BUILD_ROOT,,g

find $RPM_BUILD_ROOT%{INSTALL_DIR}/pkgconfig -name "*.pc" | 
   xargs sed -i -e s,$RPM_BUILD_ROOT,,g
# Remove shipped cairo library
rm $RPM_BUILD_ROOT%{INSTALL_DIR}/libnsight/libcairo-swt.so
rm $RPM_BUILD_ROOT%{INSTALL_DIR}/libnvvp/libcairo-swt.so
rm $RPM_BUILD_ROOT%{INSTALL_DIR}/bin/uninstall_cuda_7.0.pl
rm $RPM_BUILD_ROOT%{INSTALL_DIR}/bin/.uninstall_manifest_do_not_delete.txt

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}/

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#####################################################################
##
## CUDA Toolkit
##
proc ModulesHelp { } {

puts stderr ""
puts stderr "This module loads the NVIDIA CUDA Toolkit and updates the \$PATH "
puts stderr "\$LD_LIBRARY_PATH, \$INCLUDE, and \$MANPATH environment "
puts stderr "variables to access the toolkit binaries, libraries, include "
puts stderr "files, and available man pages, respectively."
puts stderr ""
puts stderr "The following additional environment variables are also defined:"
puts stderr ""
puts stderr "\$TACC_CUDA_DIR"
puts stderr "\$TACC_CUDA_BIN"
puts stderr "\$TACC_CUDA_INC"
puts stderr "\$TACC_CUDA_LIB"
puts stderr " "
puts stderr "Version %{version}\n"

}

module-whatis "Name: NVIDIA CUDA Toolkit"
module-whatis "Version: %{version}"
module-whatis "Category: compiler, runtime support"
module-whatis "Description: NVIDIA CUDA Toolkit for Linux"
module-whatis "URL: http://www.nvidia.com/object/cuda_get.html"

# for Tcl script use only

set     version         	%{version}

prepend-path    PATH            %{INSTALL_DIR}/bin/
prepend-path    MANPATH         %{INSTALL_DIR}/man/
prepend-path    INCLUDE         %{INSTALL_DIR}/include/
prepend-path    LD_LIBRARY_PATH %{INSTALL_DIR}/lib64/

append-path     PATH            %{INSTALL_DIR}/computeprof/bin
append-path     LD_LIBRARY_PATH %{INSTALL_DIR}/computeprof/bin

setenv TACC_CUDA_DIR  %{INSTALL_DIR}/
setenv TACC_CUDA_BIN  %{INSTALL_DIR}/bin/
setenv TACC_CUDA_LIB  %{INSTALL_DIR}/lib64/
setenv TACC_CUDA_INC  %{INSTALL_DIR}/include
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## Version file for %{version}.
##
 
set     ModulesVersion     "%{version}"

EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%ifarch x86_64
%post libs-32bit -p /sbin/ldconfig

%postun libs-32bit -p /sbin/ldconfig
%endif


%files
%{INSTALL_DIR}/bin/bin2c
%{INSTALL_DIR}/bin/computeprof
%{INSTALL_DIR}/bin/crt
%{INSTALL_DIR}/bin/cudafe
%{INSTALL_DIR}/bin/cudafe++
%{INSTALL_DIR}/bin/cuda-gdb
%{INSTALL_DIR}/bin/cuda-gdbserver
%{INSTALL_DIR}/bin/cuda-install-samples-7.0.sh
%{INSTALL_DIR}/bin/cuda-memcheck
%{INSTALL_DIR}/bin/cuobjdump
%{INSTALL_DIR}/bin/fatbinary
%{INSTALL_DIR}/bin/filehash
%{INSTALL_DIR}/bin/nvcc
%{INSTALL_DIR}/bin/nvcc.profile
%{INSTALL_DIR}/bin/nvdisasm
%{INSTALL_DIR}/bin/nvlink
%{INSTALL_DIR}/bin/nvprof
%{INSTALL_DIR}/bin/nvvp
%{INSTALL_DIR}/bin/nvprune
%{INSTALL_DIR}/bin/ptxas
%{INSTALL_DIR}/include
%{INSTALL_DIR}/nvvm
%{INSTALL_DIR}/pkgconfig
%{INSTALL_DIR}/src
%{INSTALL_DIR}/tools
%{INSTALL_DIR}/%{_lib}
%{INSTALL_DIR}/extras
%{INSTALL_DIR}/libnvvp
%{INSTALL_DIR}/jre
%{INSTALL_DIR}/samples
%{INSTALL_DIR}/share
%{MODULE_DIR}

#%files libs
#%config(noreplace) %{_sysconfdir}/ld.so.conf.d/cuda-%{_arch}.conf
#%{INSTALL_DIR}/%{_lib}

%ifarch x86_64
%files libs-32bit
#%config(noreplace) %{_sysconfdir}/ld.so.conf.d/cuda-i386.conf
%{INSTALL_DIR}/lib
%endif

%files nsight
%{INSTALL_DIR}/bin/nsight
%{INSTALL_DIR}/libnsight
%{INSTALL_DIR}/jre

%files doc
%{INSTALL_DIR}/doc

%changelog

