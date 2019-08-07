Summary:  ParaView 5.6.0 local binary install

%define pkg_base_name paraview
%define MODULE_VAR    PARAVIEW

%define major_version 5
%define minor_version 6
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define is_intel19 1
%define is_impi    1
%define mpiV       19_4

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%include name-defines.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   0%{?dist}
License:   GPL
Group:     Visualization
URL:       //www.kitware.com
Packager:  TACC - gda@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}-0.tgz

%define dbg           %{nil}

%package %{PACKAGE}
Summary: The package RPM
Group: Visualization
%description package
The paraview package contains the paraview visualization software from Kitware. The package
contains the precompiled binary and any libraries needed to support the various
third party components

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Visualization/Modulefiles
%description modulefile
The module sets the required user environment needed to run paraview on TACC systems. It
sets paths to executables and modifies LD_LIBRARY_PATH


%description
The Paraview visualization software supports visualization of large scale scientific data
in a variety of formats. The software runs in parallel or serial on a variety of compute
platforms. Paraview supports a large number of visualization methods. It also supports
python scripting for batch use

%prep

%if %{?BUILD_PACKAGE}
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_version}

%endif

%if %{?BUILD_MODULEFILE}
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif

%build

%install
echo XXXXXXXXXXXXXXXXXXX here XXXXXXXXXXXXXXXXXXXXX


#### # Setup modules
#### %include system-load.inc
#### module purge
#### # Load Compiler
#### %include compiler-load.inc
#### # Load MPI Library
#### %include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}

echo AAAAAAAAAAAAAAAAAAAA
#------------------------
%files package
#------------------------
echo BBBBBBBBBBBBBBBBBBBB

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT



