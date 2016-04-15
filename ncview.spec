#
# Spec file for Ncview
#
Summary:   Ncview is a library for generating platform-independent data files
Name:      ncview
Version:   2.1.6
Release:   1
License:   GPL
Group:     applications/io
Source:    ncview-%{version}.tar.gz
URL:       http://meteora.ucsd.edu/~pierce/ncview_home_page.html
Distribution: RedHat Linux
Vendor:    Unidata Program Center, UCAR
Packager:  TACC - cazes@tacc.utexas.edu

%define APPS /opt/apps
%define MODULES modulefiles

%include rpm-dir.inc
%include compiler-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%package -n tacc-%{name}-%{comp_fam_ver}
Summary: Ncview is a program for viewing NetCDF files
Group: applications/io

%description
%description -n tacc-%{name}-%{comp_fam_ver}
Ncview is a GUI viewer for NetCDF (network Common Data Form) files

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

module load hdf5 netcdf udunits
./configure  --prefix=%{INSTALL_DIR}  \
    -with-udunits2_incdir=${TACC_UDUNITS_INC} \
    -with-udunits2_libdir=${TACC_UDUNITS_LIB}
make -j 3
make DESTDIR=$RPM_BUILD_ROOT install

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--ncview

local help_message = [[
The %{name} module file defines the following environment variables:
TACC_NCVIEW_DIR, TACC_NCVIEW_BIN,
for the location of the NCVIEW distribution and binaries, respectively.

Version %{version}

]]

help(help_message,"\n")


whatis("Ncview: NetCDF data viewer")
whatis("Version: %{version}")
whatis("Category: visualization, application")
whatis("Keywords: I/O")
whatis("Description: Visualization program for NetCDF files")
whatis("URL: http://meteora.ucsd.edu/~pierce/ncview_home_page.html")

-- Prerequisites
prereq("hdf5","netcdf","udunits")

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH",           "%{INSTALL_DIR}/bin")

--Env variables 
setenv("TACC_NCVIEW_DIR", "%{INSTALL_DIR}")
setenv("TACC_NCVIEW_BIN", "%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################
##
## version file for Ncview
##
 
set     ModulesVersion      "%{version}"
EOF


%files -n tacc-%{name}-%{comp_fam_ver}
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post


%clean
rm -rf $RPM_BUILD_ROOT

