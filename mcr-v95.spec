#
# Si Liu
# 2018-12-012
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location

Summary:  Matlab Compiler Runtime (MCR)

# Give the package a base name
%define pkg_base_name mcr
%define MODULE_VAR    MCR

# Create some macros (spec file variables)
%define major_version 9
%define minor_version 5
%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   Mathworks License
Vendor: Mathworks
Group:     Matlab
URL:       https://www.mathworks.com/products/compiler/matlab-runtime.html
Packager:  TACC - siliu@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

%description
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

#%setup -n %{pkg_base_name}-%{pkg_version}

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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'

help(
[[
The MATLAB Compiler Runtime (MCR) is a standalone set of
shared libraries that enables the execution of compiled
MATLAB applications or components on computers that do
not have MATLAB installed. When used together, MATLAB,
MATLAB Compiler, and the MCR enable you to create and
distribute numerical applications or software components
quickly and securely.

Version v9.5
]]
)

whatis("Name: MCR")
whatis("Version: v9.5")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab v9.5 Compiler Runtime from MathWorks")

append_path("PATH", "/home1/apps/mcr/9.5/bin")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.5/bin/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.5/runtime/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.5/bin/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.5/sys/os/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.5/sys/java/jre/glnxa64/jre/lib/amd64/server")
append_path("LD_LIBRARY_PATH", "/home1/apps/mcr/9.5/sys/java/jre/glnxa64/jre/lib/amd64")

setenv ("TACC_MCR_DIR", "/home1/apps/mcr/9.5")
setenv ("XAPPLRESDIR", "/home1/apps/mcr/9.5/X11/app-defaults")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"

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

