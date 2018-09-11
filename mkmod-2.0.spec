#
# Kent Milfeld  rpmbuild -bb mkmod-2.0.spec 2>&1 | tee mkmod-2.0.log
# 2018-07-16
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64

#   rpmbuild -bb mkmod-2.0.spec 2>&1 | tee mkmod-2.0.log2

# rpm -hiv --relocate /tmprpm=/opt/apps    $r/tacc-mkmod-package-2.0-1.el7.centos.x86_64.rpm
# rpm -hiv --relocate /tmpmod=/opt/apps $r/tacc-mkmod-modulefile-2.0-1.el7.centos.x86_64.rpm
# rpm -e tacc-mkmod-package-2.0 tacc-mkmod-modulefile-2.0

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name mkmod
%define MODULE_VAR    MKMOD

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 0 
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
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
License:   MIT
Group:     System Environment/Base
URL:       https://github.com/tacc/mkmod
Packager:  TACC - milfeld@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar
Source:    mkmod-2.0.tar

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
Mkmod generates tmod|lmod modulefiles.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Mkmod generates tmod|lmod modulefiles.

%description
Git is easy to learn and has a tiny footprint with lightning fast performance.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

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
  mkdir -p                 %{INSTALL_DIR}
  mount -t tmpfs tmpfs     %{INSTALL_DIR}
  
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


  #./configure --prefix=%{INSTALL_DIR}
  #make 
  #make install
  cp -rp * %{INSTALL_DIR}

if [ !  -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

echo "ID %{INSTALL_DIR}"
echo "RID $RPM_BUILD_ROOT/%{INSTALL_DIR}"

cp -r  %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/


  
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
help([[
mkmod creates modulefiles using three environment varibles:
NAME, VER, and TOPDIR (having values of the name, version,
and top-level directory of the package.

The %{MODULE_VAR} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN and TACC_%{MODULE_VAR}_DOC
and TACC_%{MODULE_VAR}_EXM for the location of the %{MODULE_VAR} 
distribution, binaries, docs and examples, respectively.
The binary dirrectory is pre-appended to the PATH variable.

Version %{version}
]])

whatis("Name: MKMOD")
whatis("Version: %{version}")
whatis("Category: library, tools")
whatis("Keywords: System, Process Viewer, Tools")
whatis("URL: https://github.com/tacc/mkmod")
whatis("Description: Modulefile Maker")


prepend_path(                  "PATH" , "%{INSTALL_DIR}/bin"              )
setenv (     "TACC_%{MODULE_VAR}_DIR" , "%{INSTALL_DIR}"                  )
setenv (     "TACC_%{MODULE_VAR}_BIN" , "%{INSTALL_DIR}/bin"              )
setenv (     "TACC_%{MODULE_VAR}_DOC" , "%{INSTALL_DIR}/docs"             )
setenv (     "TACC_%{MODULE_VAR}_EXM" , "%{INSTALL_DIR}/examples"         )

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

