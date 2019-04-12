#
# Si Liu
# 2019-04-01
#

Summary: Local TACC parametric-launcher install.

%define pkg_base_name launcher
%define MODULE_VAR LAUNCHER

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 4
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

Release: 2
Vendor: TACC
License: none
Group: Utility
Source: %{pkg_base_name}-%{pkg_version}.tar.gz
Packager: siliu@tacc.utexas.edu

%include rpm-dir.inc
%include name-defines-noreloc.inc

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: Launcher package RPM
Group: Applications
%description package
TACC Parametric Job Launcher is a simple utility for submitting multiple serial applications simultaneously.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Modulefiles
%description modulefile
TACC Parametric Job Launcher is a simple utility for submitting multiple serial applications simultaneously.

%description
TACC Parametric Job Launcher is a simple utility for submitting multiple serial applications simultaneously.

#---------------------------------------
%prep
#- --------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

#-----------------------
%endif # BUILD_PACKAGE |
#----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------



#---------------------------------------
%build
#---------------------------------------

#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

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

#cp -r extensions $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r extras $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r paper $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r plugins $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp -r tests  $RPM_BUILD_ROOT/%{INSTALL_DIR}

#cp init_launcher  $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp init_launcher_phi $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp INSTALL $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp launcher $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp LICENSE $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp paramrun $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp pass_env $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp README.md $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp tskserver $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp tskserver.sh $RPM_BUILD_ROOT/%{INSTALL_DIR}
#cp UpdateLog $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Copy everything from tarball over to the installation directory
cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------



#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

# Write out the modulefile associated with the application

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_message=[[
The %{name} module file defines the environment variable:
$%{MODULE_VAR}_DIR for the location of the TACC Parametric 
Job Launcher which is a simple utility for submitting multiple
serial applications simultaneously.

For more information on using the Launcher, please consult
the README.launcher file located in $%{MODULE_VAR}_DIR

Version %{version}
]]

help(help_message,"\n")

whatis ("Name: TACC Parametric Job Launcher")
whatis ("Version: %{version}")
whatis ("Category: utility, runtime support")
whatis ("Keywords: System, Utility, Tools")
whatis ("Description: Utility for starting parametric job sweeps")

family("launcher")
local launcher_dir           = "%{INSTALL_DIR}"
setenv("TACC_LAUNCHER_DIR", "/opt/apps/launcher/3.4" )
setenv("LAUNCHER_DIR",      "/opt/apps/launcher/3.4" )
setenv("LAUNCHER_PLUGIN_DIR", "/opt/apps/launcher/3.4/plugins")
setenv("LAUNCHER_RMI", "SLURM")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

# Check the syntax of the generated lua modulefile
%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

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

