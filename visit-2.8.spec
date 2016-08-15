#
# Spec file for visit
#

Summary:  visit 2.8 local binary install
Name:     visit2.8
Version:  2.8
Release:  1
License:  GPL
Vendor:   wci.llnl.gov/codes/visit/
Group:    Visualization 
Packager:  pnav@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define is_intel14 1
%include compiler-defines.inc

%define is_mvapich2 1
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/visit
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/visit

%define VISIT_SRC visit.%{version}.%{mpi_fam_ver}.%{release}.tar.gz

%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: visit %{version} local binary install
Group: Visualization

%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
VisIt is a free interactive parallel visualization and graphical analysis tool.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd $RPM_BUILD_ROOT/%{INSTALL_DIR}
tar xvzf $RPM_SOURCE_DIR/%{VISIT_SRC}

test -e current && /bin/rm -f current
ln -s 2.8.1 current

## Module for visit-%{version}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#####################################################################
##
## VisIt visualization framework
##
proc ModulesHelp { } {
        puts stderr "\tVisIt visualization framework\n"
        puts stderr "\tThis module loads the VisIt visualization framework.\n"
        puts stderr "\t{ The command directory is added to PATH.             } \n"
        puts stderr "\t{ The library directory is added to LD_LIBRARY_PATH.  } \n"
        puts stderr "\t{ The include directory is added to INCLUDE.          } \n"
        puts stderr "\n\tVersion %{version}\n"
}

module-whatis   "VisIt visualization suite"
module-whatis   "Version: %{version}"
module-whatis   "Category: application, visualization"
module-whatis   "Description: a parallel visualization suite based in part on VTK"
module-whatis   "URL: https://wci.llnl.gov/codes/visit/"

conflict visit

set-alias visit "visit -v %{version}"

prepend-path    PATH            %{INSTALL_DIR}/bin
prepend-path    PYTHONPATH      %{INSTALL_DIR}/current/linux-x86_64/lib/site-packages/visit
prepend-path    INCLUDE         %{INSTALL_DIR}/current/linux-x86_64/include
prepend-path    LD_LIBRARY_PATH /opt/apps/limic2/0.5.5/lib
prepend-path    LD_LIBRARY_PATH %{INSTALL_DIR}/current/linux-x86_64/lib

setenv TACC_VISIT_DIR %{INSTALL_DIR}
setenv TACC_VISIT_INC %{INSTALL_DIR}/%{version}/linux-x86_64/include
setenv TACC_VISIT_LIB %{INSTALL_DIR}/%{version}/linux-x86_64/lib
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################################
##
## version file for %{name} %{version}
##

set     ModulesVersion     "%version"

EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}
