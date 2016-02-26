#
# Antia Lamas-Linares
# 
# 2016-02-10
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

Summary: Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. 

# Give the package a base name
%define pkg_base_name gnuplot
%define MODULE_VAR    GNUPLOT

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 0
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc
#%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc
########################################
############ Do Not Remove #############
########################################


############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   2
License:   http://www.gnuplot.info/faq/faq.html
Group:     Development/Tools
URL:       http://www.gnuplot.info/ 
Packager:  TACC - alamas@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Gnuplot
Group: Development/Tools
%description package
#Long description for the package RPM
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. 

%package %{MODULEFILE}
Summary: Gnuplot
Group: Lmod/Modulefiles
%description modulefile
#Long description for the modulefile RPM
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. 
%description
#The longer description of the package that will end up inside the rpm and is queryable via rpm -qi <rpm-name>
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms. 

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

####This line not in git
#%setup -n %{pkg_base_name}-%{pkg_version}

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
module purge

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  mount -t tmpfs tmpfs %{INSTALL_DIR}
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
  export gnuplot_install=%{INSTALL_DIR}
  export gnuplot_version=%{pkg_version}

  wget http://sourceforge.net/projects/gnuplot/files/gnuplot/%{pkg_version}/gnuplot-%{pkg_version}.tar.gz/download
  tar xvf gnuplot-%{pkg_version}.tar.gz
  cd gnuplot-%{pkg_version}
  ./configure --prefix=${gnuplot_install}
  make 
  make install
  #========================================
  
  # Copy everything from tarball over to the installation directory
  # Don't forget the .. at the end, otherwise malformed installation place
  cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
Gnuplot is a portable command-line driven graphing utility for Linux, OS/2, MS Windows, OSX, VMS, and many other platforms.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries and tools respectively.
]]

--help(help_msg)
help(help_msg)

whatis("Name: gnuplot")
whatis("Version: %{version}")
whatis("Category: library, tools")
whatis("Keywords: System, Tools, Graphics, Visualization")
whatis("URL: http://www.gnuplot.info/")
whatis("Portable command-line driven graphing utility")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local gnuplot_dir           = "%{INSTALL_DIR}"

prepend_path(    "PATH",                "%{INSTALL_DIR}/bin")
prepend_path(    "LD_LIBRARY_PATH",     "%{INSTALL_DIR}/lib")
setenv( "TACC_%{MODULE_VAR}_DIR",       "%{INSTALL_DIR}")
setenv( "TACC_%{MODULE_VAR}_LIB",       "%{INSTALL_DIR}/libexec")
setenv( "TACC_%{MODULE_VAR}_BIN",       "%{INSTALL_DIR}/bin")
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
########################################
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

