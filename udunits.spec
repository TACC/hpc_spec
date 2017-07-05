#
# Spec file for Udunits
#
Summary:   Udunits is a utility for netcdf
Name:      udunits
Version:   2.2.25
Release:   1%{?dist}
License:   GPL
Group:     applications/io
Source:    udunits-%{version}.tar.gz
URL:       http://www.unidata.ucar.edu/downloads/udunits/index.jsp
Distribution: RedHat Linux
Vendor:    Unidata Program Center, UCAR
Packager:  TACC - cazes@tacc.utexas.edu

%define APPS /opt/apps
%define MODULES modulefiles

%include rpm-dir.inc
%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n %{name}-%{comp_fam_ver}
Summary: Udunits is utility for NetCDF
Group: applications/io

%description
%description -n %{name}-%{comp_fam_ver}
Udunits

%prep

rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup

%build

%install

%include compiler-load.inc

#
# config/make:
#

module load hdf5
module load netcdf
./configure --prefix=%{INSTALL_DIR}
make -j 3
make DESTDIR=$RPM_BUILD_ROOT install

#
# make test

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--udunits

local help_message = [[
The %{name} module file defines the following environment variables:
TACC_UDUNITS_DIR, TACC_UDUNITS_BIN, TACC_UDUNITS_LIB, and 
TACC_UDUNITS_INC forthe location of the UDUNITS distribution, binaries,
libraries, and include files, respectively.

UDUNITS 4.1.1 uses the hdf5 libraries to support the UDUNITS 4 file format 
in addition to the classic UDUNITS file format. 

To use the UDUNITS library, compile the source code with the option:

	-I${TACC_UDUNITS_INC} 

and add the following options to the link step: 

	-L${TACC_UDUNITS_LIB} -ludunits -L${TACC_HDF5_LIB} -lhdf5_hl -lhdf5 -lz -lm

Version %{version}

]]

help(help_message,"\n")


whatis("Udunits: Network Common Data Form")
whatis("Version: %{version}")
whatis("Category: library, runtime support")
whatis("Keywords: I/O, Library")
whatis("Description: I/O library which stores and retrieves data in self-describing, machine-independent datasets." )
whatis("URL: http://www.unidata.ucar.edu/software/udunits/")

-- Prerequisites
prereq("hdf5")

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH",           "%{INSTALL_DIR}/bin")
prepend_path("MANPATH",        "%{INSTALL_DIR}/share/man")
prepend_path("PKG_CONFIG_PATH","%{INSTALL_DIR}/lib/pkgconfig")

--Env variables 
setenv("TACC_UDUNITS_DIR", "%{INSTALL_DIR}")
setenv("TACC_UDUNITS_INC", "%{INSTALL_DIR}/include")
setenv("TACC_UDUNITS_LIB", "%{INSTALL_DIR}/lib")
setenv("TACC_UDUNITS_BIN", "%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Udunits
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n %{name}-%{comp_fam_ver}
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Apr 27 2015 cazes <cazes@tacc.utexas.edu>
- release 1: updated version 2.2.19
* Fri Apr 12 2013 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial install
