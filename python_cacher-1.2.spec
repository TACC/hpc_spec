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

Summary: A Nice little relocatable skeleton spec file.

# Give the package a base name
%define pkg_base_name python_cacher
%define MODULE_VAR    python_cacher

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 2
%define micro_version 0

#%define pkg_version %{major_version}.%{minor_version}
%define pkg_version %{major_version}.%{minor_version}
### Toggle On/Off ###
%include rpm-dir.inc

#%include compiler-defines.inc
#%include mpi-defines.inc

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
URL:       NULL
Packager:  TACC - huang@tacc.utexas.edu
Source:    python_cacher-1.2.tgz
#Source1:   tcl8.5.9-linux-x86_64-threaded.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The python cacher RPM
Group: Tools/Optimization
%description package
A library is designed to automatically cache user's python related files on local storage (/dev/shm or /tmp) during the first access. When access the same files later, the file in local storage will be used. This not only redirect the IO on $WORK to local storage and resolve the related MDS issue, it also make IO faster since local storage is utilized instead of accessing $WORK.

%package %{MODULEFILE}
Summary: The python cacher modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
A library is designed to automatically cache user's python related files on local storage (/dev/shm or /tmp) during the first access. When access the same files later, the file in local storage will be used. This not only redirect the IO on $WORK to local storage and resolve the related MDS issue, it also make IO faster since local storage is utilized instead of accessing $WORK.

%description
A library is designed to automatically cache user's python related files on local storage (/dev/shm or /tmp) during the first access. When access the same files later, the file in local storage will be used. This not only redirect the IO on $WORK to local storage and resolve the related MDS issue, it also make IO faster since local storage is utilized instead of accessing $WORK.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

%setup -n python_cacher-%{pkg_version}


#---------------------------------------
%build
#---------------------------------------

#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
module purge
#%include compiler-load.inc
#%include mpi-load.inc


# Insert necessary module commands
#module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

  # Create some dummy directories and files for fun

  cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
  chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}


  # Copy everything from tarball over to the installation directory
#  cp * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

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
A library is designed to automatically cache user python related files on local storage (/dev/shm or /tmp) during the first access. When access the same files later, the file in local storage will be used. This not only redirect the IO on $WORK to local storage and resolve the related MDS issue, it also make IO faster since local storage is utilized instead of accessing $WORK.

export PYTHON_IO_LocalDir="/dev/shm"
or
export PYTHON_IO_LocalDir="/tmp"

If PYTHON_IO_LocalDir is not set, "/dev/shm" is set as default. 

Please ONLY load this module in your production jobs or the test jobs for production runs. If you are installing or removing Python packages, you NEED to unload then reload this tool to avoid out of date cached data.

Lei Huang (huang@tacc.utexas.edu)
]]

--help(help_msg)
help(help_msg)

whatis("Name: python_cacher")
whatis("Version: 1.0")
whatis("Category: Tools/Optimization ")
whatis("Keywords: Tools, IO, Optimization")
whatis("Description: Tool for optimal Python IO")

-- Create environment variables.
local python_cacher_dir           = "%{INSTALL_DIR}"

family("python_cacher")
prepend_path( "LD_LIBRARY_PATH",        pathJoin(python_cacher_dir, "lib"))
append_path( "LD_PRELOAD",             pathJoin(python_cacher_dir, "lib/myopen.so") )
setenv( "PYTHON_IO_CACHE_NONEXISTING_FILE", "1")
setenv( "PYTHON_IO_CACHE_CWD", "1")

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

