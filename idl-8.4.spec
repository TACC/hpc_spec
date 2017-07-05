Summary:  IDL 8.4 local binary install

%define pkg_base_name idl
%define MODULE_VAR    IDL

%define major_version 8
%define minor_version 4
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc                  

%include name-defines.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

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

%setup -n %{pkg_base_name}-%{pkg_version}

%endif

%if %{?BUILD_MODULEFILE}
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif

%build

%install

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

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

  if [ -e %{APPS}/%{pkg_base_name}/%{version} ] ; then rm -rf %{APPS}/%{pkg_base_name}/%{version} ;  fi
  sed "s?INSTALLDIR?%{APPS}/%{pkg_base_name}/%{version}?" < setup_answers  | ./install.sh -s


  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  echo #######################################
  pwd
  echo #######################################

  # cp -r %{pkg_base_name}-%{pkg_version}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r %{APPS}/%{pkg_base_name}/%{version}/*  $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/license
  cp %{_sourcedir}/idl8.4_license_221797.dat $RPM_BUILD_ROOT/%{INSTALL_DIR}/license/license.dat

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
  
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
TACC_%{MODULE_VAR}_DIR, ITT_DIR and IDL_DIR
]]

--help(help_msg)
help(help_msg)

whatis("Name: idl")
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
setenv("IDL_DIR",  		  pathJoin(idl_dir, "idl"))
setenv("ITT_DIR",  		  idl_dir)
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

