Summary:  ParaView 5.4.1 local binary install

%define pkg_base_name paraview
%define MODULE_VAR    PARAVIEW

%define major_version 5
%define minor_version 4
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%define is_intel17 1
%define is_impi    1

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
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
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

%setup -n %{pkg_base_name}-%{pkg_version}/pv

%endif

%if %{?BUILD_MODULEFILE}
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif

%build

%install

# Setup modules
%include system-load.inc
module purge
# Load Compiler
%include compiler-load.inc
# Load MPI Library
%include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
  echo "TACC_OPT %{TACC_OPT}"
  
  # Copy everything from tarball over to the installation directory

  echo #######################################
  pwd
  echo #######################################

  cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
%endif


%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[ 
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC,
TACC_%{MODULE_VAR}_BIN and TACC_%{MODULE_VAR}_PYTHONPATH for the location of the
%{MODULE_VAR} distribution, libraries, include files, tools, and python packages
respectively.
]]

--help(help_msg)
help(help_msg)

whatis("Name: paraview")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local paraview_dir           = "%{INSTALL_DIR}"

family("paraview")

prereq("swr", "qt5")

prepend_path("PATH",              pathJoin(paraview_dir, "bin"))
prepend_path("LD_LIBRARY_PATH",   pathJoin(paraview_dir, "lib"))
prepend_path("LD_LIBRARY_PATH",   pathJoin(paraview_dir, "ospray", "lib64"))
prepend_path("LD_LIBRARY_PATH",   pathJoin(paraview_dir, "embree", "lib64"))
prepend_path("PYTHONPATH",        pathJoin(paraview_dir, "lib", "paraview-5.1", "site-packages"))
prepend_path("PYTHONPATH",        pathJoin(paraview_dir, "lib", "paraview-5.1", "site-packages", "vtk"))

prepend_path("MODULEPATH",        "%{MODULE_PREFIX}/paraview5_4/modulefiles")

setenv("OSPRAY_SET_AFFINITY", 0)

setenv("TACC_%{MODULE_VAR}_DIR",  paraview_dir)
setenv("TACC_%{MODULE_VAR}_INC",  pathJoin(paraview_dir, "include"))
setenv("TACC_%{MODULE_VAR}_LIB",  pathJoin(paraview_dir, "lib"))
setenv("TACC_%{MODULE_VAR}_BIN",  pathJoin(paraview_dir, "bin"))

setenv("OSPRAY_SET_AFFINITY",  "0")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

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

