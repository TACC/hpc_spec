Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name idl
%define MODULE_VAR    IDL

# Create some macros (spec file variables)
%define major_version 8
%define minor_version 4
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc                  

%include name-defines.inc

Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   1%{?dist}
License:   Exelis
Group:     Visualization
URL:       Exelis
Packager:  TACC - gda@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: The package RPM
Group: Visualization
%description package
The IDL package contains the IDL visualization software from Exelis. The package
contains the precompiled binary and any libraries needed to support the various
third party components

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Visualization/Modulefiles
%description modulefile
The module sets the required user environment needed to run IDL on TACC systems. It
sets paths to executables and modifies LD_LIBRARY_PATH

%description
The IDL visualization software supports visualization and analysis of large scale scientific data.


%prep 

%if %{?BUILD_PACKAGE}
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -c -n %{pkg_base_name}-%{pkg_version}

%endif # BUILD_PACKAGE 

%if %{?BUILD_MODULEFILE}
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif 


%build


%install

# Setup modules
%include system-load.inc
module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

%if %{?BUILD_PACKAGE}

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
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.
]]

--help(help_msg)
help(help_msg)

whatis("Name: xx")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local idl_dir           = "%{INSTALL_DIR}"

family("idl")

prepend_path("PATH",              pathJoin(idl_dir, "idl", "bin"))
prepend_path("MODULEPATH",        "%{MODULE_PREFIX}/idl8_4/modulefiles")

setenv("TACC_%{MODULE_VAR}_DIR",  idl_dir)
setenv("IDL_DIR",                 pathJoin(idl_dir, "idl"))
setenv("ITT_DIR",                 idl_dir)

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

%endif


%if %{?BUILD_PACKAGE}
%files package

%defattr(-,root,install,)
%{INSTALL_DIR}

%endif


%if %{?BUILD_MODULEFILE}
%files modulefile 

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

%endif 

########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc

echo XXXXXXXXXXXXXXX POST
pushd ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}/%{pkg_base_name}-%{pkg_version}
ls

cat > setup_answers << 'EOF'
y
INSTALLDIR
y
y
y
n
n
n
y
y
y
y
y
n
n

EOF

sed "s?INSTALLDIR?${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}?" < setup_answers  | ./install.sh -s
cd ..
rm -rf idl-8.4

popd

%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

%postun
echo POSTUN ==========================
ls -lt ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

