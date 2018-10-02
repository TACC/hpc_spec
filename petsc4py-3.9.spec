#
# Portable Extendible Toolkit for Scientific Computing
# spec file by Victor Eijkhout
#
# Adapted from Bar.spec, Cyrus Proctor & Antonio Gomez
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

Summary: Petsc4py rpm build script

# Give the package a base name
%define pkg_base_name petsc4py
%define MODULE_VAR    PETSC4PY

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 9
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}
%define pkg_full_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc

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
Group:     Development/Tools
URL:       https://bitbucket.org/petsc/petsc4py/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Petsc4py rpm building
Group: HPC/libraries
%description %{PACKAGE}
Portable Extendible Toolkit for Scientific Computations

%package %{PACKAGE}-xx
Summary: Petsc4py rpm building
Group: HPC/libraries
%description %{PACKAGE}-xx
Portable Extendible Toolkit for Scientific Computations

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
The longer-winded description of the package that will 
end in up inside the rpm and is queryable if installed via:
rpm -qi <rpm-name>


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_full_version}

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
%include compiler-load.inc
%include mpi-load.inc

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
  
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

##
## setup a tmpfs
##
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 

##
## configure install loop
##
export dynamiccc="uni unidebug debug i64 i64debug complexi64 complexi64debug"
export dynamiccxx="cxx cxxdebug complex complexdebug cxxcomplex cxxcomplexdebug cxxi64 cxxi64debug"

export EXTENSIONS="single ${dynamiccc} ${dynamiccxx}"
#export EXTENSIONS="single ${dynamiccc}"

##
## start of for ext loop, installation only
##
for ext in "" ${EXTENSIONS} ; do
#for ext in "" ; do

echo "configure install for ${ext}"
module unload petsc
if [ -z ${ext} ] ; then
  export modulefilename=%{pkg_version}
else
  export modulefilename=%{pkg_version}-${ext}
fi
module load petsc/${modulefilename}

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

python2 \
  setup.py install \
  --prefix=%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The petsc4py module defines the following environment variables:
TACC_PETSC4PY_DIR, TACC_PETSC4PY_BIN, and
TACC_PETSC4PY_LIB for the location
of the Petsc4py distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Petsc4py" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: https://bitbucket.org/petsc/petsc4py/" )
whatis( "Description: Numerical library for sparse linear algebra" )

local             petsc4py_arch =    "${architecture}"
local             petsc4py_dir =     "%{INSTALL_DIR}/"

--prepend_path("PATH",            pathJoin(petsc4py_dir,"bin") )
--prepend_path("PATH",            pathJoin(petsc4py_dir,petsc4py_arch,"bin") )
--prepend_path("LD_LIBRARY_PATH", pathJoin(petsc4py_dir,petsc4py_arch,"lib") )
prepend_path("PYTHONPATH", 
    pathJoin(petsc4py_dir,"lib64","python$TACC_PYTHON_VER","site-packages") )

setenv("PETSC4PY_ARCH",            petsc4py_arch)
setenv("PETSC4PY_DIR",             petsc4py_dir)
setenv("TACC_PETSC4PY_DIR",        petsc4py_dir)
--setenv("TACC_PETSC4PY_BIN",        pathJoin(petsc4py_dir,petsc4py_arch,"bin") )
--setenv("TACC_PETSC4PY_LIB",        pathJoin(petsc4py_dir,petsc4py_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Petsc4py %version
##

set     ModulesVersion      "${modulefilename}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

##
## end of for ext loop
##
done 

cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

umount %{INSTALL_DIR}  

echo "Directory to package up: $RPM_BUILD_ROOT/%{INSTALL_DIR}"
echo "listing:"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

#------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
#------------------------

%defattr(-,root,install,)
%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

%defattr(-,root,install,)
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
%preun %{PACKAGE}-xx
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Aug 09 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release of 3.9
