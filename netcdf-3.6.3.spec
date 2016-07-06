#
# Spec file for NetCDF
#
Summary: NetCDF is a library for generating platform-independent data files
Name: netcdf-3.6
Version: 3.6.3
Release: 1
License: GPL
Group: applications/io
Source: netcdf-%{version}.tar.gz
URL: www.unidata.ucar.edu/packages/netcdf
Distribution: RedHat Linux
Vendor: Unidata Program Center, UCAR
Packager: TACC - cazes@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%include rpm-dir.inc
%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/netcdf/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/netcdf

%package -n tacc-%{name}-%{comp_fam_ver}
Summary: NetCDF is a library for generating platform-independent data files
Group: applications/io

%description
%description -n tacc-%{name}-%{comp_fam_ver}
NetCDF (network Common Data Form) is an interface for array-oriented data
access and a library that provides an implementation of the interface. The
netCDF library also defines a machine-independent format for representing
scientific data. Together, the interface, library, and format support the
creation, access, and sharing of scientific data. The netCDF software was
developed at the Unidata Program Center in Boulder, Colorado.

%prep

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# Use -n <name> if source file different from <name>-<version>.tar.gz
%setup -n netcdf-%{version}

%build

%include compiler-load.inc

#
# config/make:
#

./configure --prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}
make -j 3
make install

#
# make test

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--netcdf

local help_message = [[
The %{name} module file defines the following environment variables:
TACC_NETCDF_DIR, TACC_NETCDF_BIN, TACC_NETCDF_LIB, and 
TACC_NETCDF_INC for the location of the NETCDF distribution, binaries,
libraries, and include files, respectively.

To use the NETCDF library, compile the source code with the option:

	-I${TACC_NETCDF_INC} 

and add the following options to the link step: 

	-L${TACC_NETCDF_LIB} -lnetcdf

Version %{version}

]]

help(help_message,"\n")


whatis("NetCDF: Network Common Data Form")
whatis("Version: %{version}")
whatis("Category: library, runtime support")
whatis("Keywords: I/O, Library")
whatis("Description: I/O library which stores and retrieves data in self-describing, machine-independent datasets." )
whatis("URL: http://www.unidata.ucar.edu/software/netcdf/")

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH",           "%{INSTALL_DIR}/bin")
prepend_path("MANPATH",        "%{INSTALL_DIR}/share/man")
prepend_path("PKG_CONFIG_PATH","%{INSTALL_DIR}/lib/pkgconfig")

--Env variables 
setenv("TACC_NETCDF_DIR", "%{INSTALL_DIR}")
setenv("TACC_NETCDF_INC", "%{INSTALL_DIR}/include")
setenv("TACC_NETCDF_LIB", "%{INSTALL_DIR}/lib")
setenv("TACC_NETCDF_BIN", "%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for NetCDF
##
 
set     ModulesVersion      "%{version}"
EOF


%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

# Fix Hosed links.

#ln -sf /opt/apps/netcdf/netcdf-%{version}/man/man3/netcdf.3f $RPM_BUILD_ROOT/opt/apps/netcdf/netcdf-%{version}/man/man3f/netcdf.3f
#ln -sf /opt/apps/netcdf/netcdf-%{version}/man/man3/netcdf.3f90 $RPM_BUILD_ROOT/opt/apps/netcdf/netcdf-%{version}/man/man3f90/netcdf.3f90

%files -n tacc-%{name}-%{comp_fam_ver}
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post


%clean
rm -rf $RPM_BUILD_ROOT
