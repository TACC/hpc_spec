#
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
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
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name ooops
%define MODULE_VAR    ooops

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 1
%define micro_version 0

#%define pkg_version %{major_version}.%{minor_version}
%define pkg_version %{major_version}.%{minor_version}
### Toggle On/Off ###
%include rpm-dir.inc

##%include compiler-defines.inc
##%include mpi-defines.inc

#%include name-defines-noreloc.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
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
License:   GPL
URL:       https://github.com/TACC/ooops
Packager:  TACC - huang@tacc.utexas.edu
Source:    ooops-1.1.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: ooops
Group: Tools/Optimization
%description package
Optimal Overloaded IO Protection System (OOOPS) is an easy to use tool that helps HPC users optimize heavy IO requests.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Optimal Overloaded IO Protection System (OOOPS) is an easy to use tool that helps HPC users optimize heavy IO requests.

%description
Optimal Overloaded IO Protection System (OOOPS) is an easy to use tool that helps HPC users optimize heavy IO requests.

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

%setup -n ooops-%{pkg_version}


#---------------------------------------
%build
#---------------------------------------
##%include compiler-load.inc

%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

  rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  mkdir $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  cp -p bin/set_io_param $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
  cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
  cp -r conf $RPM_BUILD_ROOT/%{INSTALL_DIR}/
  chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}

echo "Building the modulefile?: %{BUILD_MODULEFILE}"


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################


cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message=[[
Optimal Overloaded IO Protection System (OOOPS) is an easy to use tool that helps HPC users optimize heavy IO requests.

It will also help system administrator prevent IO overload caused by improper IO request.

Lei Huang (huang@tacc.utexas.edu)
Si Liu    (siliu@tacc.utexas.edu)

]]

help(help_message,"\n")

whatis("Name: OOOPS")
whatis("Version: 1.1")
whatis("Category: Tools/Optimization ")
whatis("Keywords: Tools, IO, Optimization")
whatis("Description: Optimal Overloaded IO Protection System (OOOPS) us an easy to use tool ")


-- Create environment variables.
local ooops_dir           = "%{INSTALL_DIR}"
family("ooops")

prepend_path(    "PATH",                pathJoin(ooops_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(ooops_dir, "lib"))
append_path(    "LD_PRELOAD",          pathJoin(ooops_dir, "lib/ooops.so") )

setenv( "IO_LIMIT_CONFIG", "/opt/apps/ooops/1.1/conf/config_sp2")
setenv( "LIMIT_IO_DEBUG", "0")

EOF


  # Check the syntax of the generated lua modulefile
#  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

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

