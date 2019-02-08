#
# W. Cyrus Proctor
# 2015-11-07
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
%define pkg_base_name qiskit
%define MODULE_VAR    QISKIT

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 7
%define micro_version 0

%define python_major 3
%define python_minor 7
%define python_micro 0

%global _python_bytecompile_errors_terminate_build 0

%define python_version %{python_major}.%{python_minor}.%{python_micro} 
%define pip pip%{python_major}

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc-home1.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   Apache-2.0
Group:     System/Utils
URL:       https://github.com/Qiskit/qiskit
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
Qiskit is a software development kit for writing quantum computing experiments,
programs, and applications.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Qiskit is a software development kit for writing quantum computing experiments,
programs, and applications.

%description
Qiskit is a software development kit for writing quantum computing experiments,
programs, and applications.

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
%include compiler-load.inc
module load python%{python_major}
module list

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  #mount -t tmpfs tmpfs %{INSTALL_DIR}
  
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


%{pip} list
%{pip} install --prefix=%{INSTALL_DIR} --no-binary :all: --install-option="--prefix=%{INSTALL_DIR}" qiskit


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
#umount %{INSTALL_DIR}/

 
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
local help_message = [[

Qiskit is an open-source framework for quantum computing whose goal is to be
accessible to people with many backgrounds: quantum researchers, other
scientists, teachers, developers, and general tech enthusiasts. Our vision for
Qiskit consists of four foundational elements: Terra (the code foundation, for
composing quantum programs at the level of circuits and pulses), Aqua (for
building algorithms and applications), Ignis (for addressing noise and errors),
and Aer (for accelerating development via simulators, emulators and debuggers).
Today, we bring you Terra and Aqua, and a commitment to deliver Ignis and Aer
in the near future.

This module defines the environmental variables TACC_%{MODULE_VAR}_DIR,
TACC_%{MODULE_VAR}_BIN and TACC_%{MODULE_VAR}_LIB for the location of the main
%{pkg_name} directory, binaries, and the libraries respectivley. Your $PATH,
$LD_LIBRARY_PATH, $PYTHONPATH, and $MANPATH variables are also updated.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: Python Package")
whatis("Keywords: Quantum, Circuit, Simulation")
whatis("Description: Quantum Circuit Simulation")
whatis("URL: https://github.com/Qiskit/qiskit")

-- Export environmental variables
local qiskit_dir="%{INSTALL_DIR}"
local qiskit_bin=pathJoin(qiskit_dir,"bin")
local qiskit_lib=pathJoin(qiskit_dir,"lib")

setenv("TACC_%{MODULE_VAR}_DIR",qiskit_dir)
setenv("TACC_%{MODULE_VAR}_BIN",qiskit_bin)
setenv("TACC_%{MODULE_VAR}_LIB",qiskit_lib)

-- Prepend the qiskit directories to the adequate PATH variables
prepend_path("PATH",           qiskit_bin)
prepend_path("LD_LIBRARY_PATH", qiskit_lib)
prepend_path("MANPATH",         pathJoin(qiskit_dir,"share/man"))
prepend_path("PYTHONPATH",      pathJoin(qiskit_lib, "python%{python_major}.%{python_minor}/site-packages"))

depends_on("python%{python_major}")

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
ln -s %{INSTALL_DIR}/lib/python%{python_major}.%{python_minor}/site-packages/qiskit /opt/apps/%{comp_fam_ver}/python%{python_major}/%{python_version}/lib/python%{python_major}.%{python_minor}/site-packages/qiskit
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
%preun %{MODULEFILE}
unlink /opt/apps/%{comp_fam_ver}/python%{python_major}/%{python_version}/lib/python%{python_major}.%{python_minor}/site-packages/qiskit
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

