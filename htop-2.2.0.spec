#
# Kent Milfeld  rpmbuild -bb htop-2.2.0.spec 2>&1 | tee htop-2.2.0_r1_a.log

# r=/admin/build/admin/rpms/frontera/RPMS/x86_64
# rpm -hiv --relocate /tmprpm=/opt/apps  $r/tacc-htop-modulefile-2.2.0-1.el7.x86_64.rpm
# rpm -hiv --relocate /tmpmod=/opt/apps  $r/tacc-htop-package-2.2.0-1.el7.x86_64.rpm

# 2019-06-29
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

#   rpmbuild -bb htop-2.2.0.spec 2>&1 | tee htop-2.2.0.log2

# rpm -hiv --relocate /tmprpm=/opt/apps $r/tacc-htop-package-2.2.0-1.el7.centos.x86_64.rpm
# rpm -hiv --relocate /tmpmod=/opt/apps $r/tacc-htop-modulefile-2.2.0-1.el7.centos.x86_64.rpm
# rpm -e tacc-htop-package-2.2.0 tacc-htop-modulefile-2.2.0

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name htop
%define MODULE_VAR    HTOP

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 2 
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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
License:   GPL
Group:     System Environment/Base
URL:       https://hisham.hm/htop/
Packager:  TACC - milfeld@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar
Source:    htop-2.2.0.tar

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
Htop is a ncurses-based process viewer for Linux.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Htop is a ncurses-based process viewer for Linux.

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

# make cpu number beging with 0 (to match proc-ids)  5/2/2019 KFM
sed -i 's/countCPUsFromZero = false/countCPUsFromZero = true/' Settings.c

./configure --prefix=%{INSTALL_DIR}
make 
make install

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
Htop is a ncurses-based process viewer for Linux.

The %{MODULE_VAR} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN and TACC_%{MODULE_VAR}_MAN 
for the location of the %{MODULE_VAR} distribution, binaries, and man
pages, respectively.
The binary and man directories are pre-appended to the PATH and MANPATH variables.

To run htop, execute:

htop

Version %{version}
]])

whatis("Name: HTOP")
whatis("Version: %{version}")
whatis("Category: library, tools")
whatis("Keywords: System, Process Viewer, Tools")
whatis("URL: https://hisham.hm/htop/")
whatis("Description: Process Viewer using ncurses, info is similar to top")


prepend_path(                  "PATH" , "%{INSTALL_DIR}/bin"              )
prepend_path(               "MANPATH" , "%{INSTALL_DIR}/share/man"        )
setenv (     "TACC_%{MODULE_VAR}_DIR" , "%{INSTALL_DIR}"                  )
setenv (     "TACC_%{MODULE_VAR}_BIN" , "%{INSTALL_DIR}/bin"              )
setenv (     "TACC_%{MODULE_VAR}_MAN" , "%{INSTALL_DIR}/share/man"              )

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

