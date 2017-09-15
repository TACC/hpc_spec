#
# Spec file for ParaView 5.4.0
#

Summary:   ParaView 5.4.0 local binary install
Name:      paraview
Version:   5.4.0
Release:   0
License:   freely distributable
Vendor:    www.kitware.com
Group:     Visualization
Source:    paraview-intel16-cray_mpich_7_3-5.4.0-0.tgz
autoreq:   no

Packager:  gda@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}

%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define is_intel16 1
%include compiler-defines.inc

%define is_cmpich 1
%include mpi-defines.inc

%define RPM_PACKAGE_NAME %{name}-%{comp_fam_ver}-%{mpi_fam_ver}-%{version}-%{release}

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

%define PV_SRC paraview-%{comp_fam_ver}-%{mpi_fam_ver}-%{version}-%{release}.tgz

%package -n tacc-%{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: paraview 5.4.0 local binary install
Group: Visualization

%description
%description -n tacc-%{name}-%{comp_fam_ver}-%{mpi_fam_ver}
ParaView is a free interactive parallel visualization and graphical analysis tool.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd $RPM_BUILD_ROOT/%{INSTALL_DIR}
tar xvzf $RPM_SOURCE_DIR/%{PV_SRC}
chmod -R a+rX .

## Module for %{name}-%{version}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#####################################################################
##
## ParaView 5.4.0 parallel interactive visualization system
##
proc ModulesHelp { } {
        puts stderr "\tParaView 5.4.0 parallel interactive visualization system\n"
        puts stderr "\tThis module loads Paraview environment variables.\n"
        puts stderr "\t{ The command directory is added to PATH.             } \n"
	puts stderr "\t{ The include directory is added to INCLUDE.          } \n"
        puts stderr "\t{ The lib     directory is added to LD_LIBRARY_PATH.  } \n"
        puts stderr "\n\tVersion %{version}\n"

}

module-whatis   "ParaView parallel interactive visualization system"
module-whatis   "Version: %{version}"
module-whatis   "Category: application, library, graphics"
module-whatis   "Description: a parallel interactive visualization system"
module-whatis   "URL: http://www.kitware.com/"

# load only one version of qt at a time
conflict paraview
prereq qt/4.8
prereq python/2.7.12

prepend-path    PATH            %{INSTALL_DIR}/bin
prepend-path    LD_LIBRARY_PATH %{INSTALL_DIR}/lib/paraview-5.4:%{INSTALL_DIR}/lib:%{INSTALL_DIR}/lib64:%{INSTALL_DIR}/ospray/lib64:%{INSTALL_DIR}/embree/lib64
prepend-path	PYTHONPATH	%{INSTALL_DIR}/lib/paraview-5.4/site-packages:%{INSTALL_DIR}/lib/paraview-5.4/site-packages/vtk

setenv TACC_PARAVIEW_DIR  %{INSTALL_DIR}
setenv TACC_PARAVIEW_INC  %{INSTALL_DIR}/include
setenv TACC_PARAVIEW_LIB  %{INSTALL_DIR}/lib
setenv TACC_PARAVIEW_LIB  %{INSTALL_DIR}/lib64

EOF

echo >  $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version}  << 'EOF'
#%Module1.0#################################################################' 
##
## version file for qt %{version}
##

set     ModulesVersion     "%version"'

EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n tacc-%{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}
