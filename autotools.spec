#
# W. Cyrus Proctor
# 2015-11-10
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
%define pkg_base_name autotools
%define MODULE_VAR    AUTOTOOLS

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 2
%define micro_version 0

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

Release:   1
License:   GPL
Group:     Utility
URL:       http://www.gnu.org
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
Autoconf produces a configuration shell script, named configure, which probes
the installer platform for portability related information which is required to
customize makefiles, configuration header files, and other application specific
files. Then it proceeds to generate customized versions of these files from
generic templates. This way, the user will not need to customize these files
manually.  Automake produces makefile templates, Makefile.in to be used by
Autoconf, from a very high level specification stored in a file called
Makefile.am. Automake produces makefiles that conform to the GNU makefile
standards, taking away the extraordinary effort required to produce them by
hand. Automake requires Autoconf in order to be used properly.  Libtool makes
it possible to compile position independent code and build shared libraries in
a portable manner. It does not require either Autoconf, or Automake and can be
used independently. Automake however supports libtool and interoperates with it
in a seamless manner.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Autoconf produces a configuration shell script, named configure, which probes
the installer platform for portability related information which is required to
customize makefiles, configuration header files, and other application specific
files. Then it proceeds to generate customized versions of these files from
generic templates. This way, the user will not need to customize these files
manually.  Automake produces makefile templates, Makefile.in to be used by
Autoconf, from a very high level specification stored in a file called
Makefile.am. Automake produces makefiles that conform to the GNU makefile
standards, taking away the extraordinary effort required to produce them by
hand. Automake requires Autoconf in order to be used properly.  Libtool makes
it possible to compile position independent code and build shared libraries in
a portable manner. It does not require either Autoconf, or Automake and can be
used independently. Automake however supports libtool and interoperates with it
in a seamless manner.

%description
Autoconf produces a configuration shell script, named configure, which probes
the installer platform for portability related information which is required to
customize makefiles, configuration header files, and other application specific
files. Then it proceeds to generate customized versions of these files from
generic templates. This way, the user will not need to customize these files
manually.  Automake produces makefile templates, Makefile.in to be used by
Autoconf, from a very high level specification stored in a file called
Makefile.am. Automake produces makefiles that conform to the GNU makefile
standards, taking away the extraordinary effort required to produce them by
hand. Automake requires Autoconf in order to be used properly.  Libtool makes
it possible to compile position independent code and build shared libraries in
a portable manner. It does not require either Autoconf, or Automake and can be
used independently. Automake however supports libtool and interoperates with it
in a seamless manner.

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


##################################################
export auto=`pwd`
export auto_install=%{INSTALL_DIR}
##################################################

export m4_major=1
export m4_minor=4
export m4_patch=18

export autoconf_major=2
export autoconf_minor=69

export automake_major=1
export automake_minor=15

export libtool_major=2
export libtool_minor=4
export libtool_patch=6

export       m4_version=${m4_major}.${m4_minor}.${m4_patch}
export autoconf_version=${autoconf_major}.${autoconf_minor}
export automake_version=${automake_major}.${automake_minor}
export  libtool_version=${libtool_major}.${libtool_minor}.${libtool_patch}

export ncores=48

export CC=gcc
#  export CFLAGS="-fPIC -march=core-avx -mtune=core-avx2"
#  export CXXFLAGS="-march=core-avx -mtune=core-avx2"
#  export LDFLAGS="-march=core-avx -mtune=core-avx2"
export CFLAGS="-fPIC -mtune=generic"
export CXXFLAGS="-mtune=generic"
export LDFLAGS="-mtune=generic"


### M4
cd ${auto}
wget https://ftp.gnu.org/gnu/m4/m4-${m4_version}.tar.gz
tar xvfz m4-${m4_version}.tar.gz
cd m4-${m4_version}
${auto}/m4-${m4_version}/configure \
--prefix=${auto_install}
make -j ${ncores}
make -j ${ncores} install

### Autoconf
export M4=${auto_install}/bin/m4
cd ${auto}
wget https://ftp.gnu.org/gnu/autoconf/autoconf-${autoconf_version}.tar.gz
tar xvfz autoconf-${autoconf_version}.tar.gz
cd autoconf-${autoconf_version}
${auto}/autoconf-${autoconf_version}/configure \
--prefix=${auto_install}
make -j ${ncores}
make -j ${ncores} install

### Automake
export PATH=${auto_install}/bin:${PATH}
cd ${auto}
wget https://ftp.gnu.org/gnu/automake/automake-${automake_version}.tar.gz
tar xvfz automake-${automake_version}.tar.gz
cd automake-${automake_version}
${auto}/automake-${automake_version}/configure \
--prefix=${auto_install}
make -j ${ncores}
make -j ${ncores} install

### Libtool
cd ${auto}
wget ftp://ftp.gnu.org/gnu/libtool/libtool-${libtool_version}.tar.gz
tar xvfz libtool-${libtool_version}.tar.gz
cd libtool-${libtool_version}
${auto}/libtool-${libtool_version}/configure \
--prefix=${auto_install}
make -j ${ncores}
make -j ${ncores} install

# add support for pkg-config macros
cp $RPM_SOURCE_DIR/pkg.m4 %{INSTALL_DIR}/share/aclocal
chmod a+r %{INSTALL_DIR}/share/aclocal/pkg.m4


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}



#---------------------- - 
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
The %{MODULE_VAR} module file defines the environment variable
TACC_%{MODULE_VAR}_DIR for the location of the GNU autotools
package which provides a collection of common development utilties.
TACC_%{MODULE_VAR}_BIN is also defined for the location of the
tools.

Loading the %{MODULE_VAR} module will update your PATH to access a
recent version of m4, autoconf, automake, and libtool.

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: %{pkg_name}")
whatis("Version: %{pkg_version}%{dbg}")

-- Create environment variables.
local autotools_dir           = "%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(autotools_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_DIR",                autotools_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(autotools_dir, "bin"))
EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{MODULE_VAR}%{version}
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

