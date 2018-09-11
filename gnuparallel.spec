#
# Spec file for Gnu Parallel
# https://www.gnu.org/software/parallel/
#
# Victor Eijkhout, 2018
# based on:
#
# Bar.spec, 
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

Summary:    Set of tools for manipulating geographic and Cartesian data sets

# Give the package a base name
%define pkg_base_name gnuparallel
%define MODULE_VAR    GNUPARALLEL

# Create some macros (spec file variables)
%define major_version git20180620

%define pkg_version %{major_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
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

Release:   1%{?dist}
License:   GNU
Group:     Development/Tools
Vendor:     GNU Foundation
Source:	    gnuparallel-%{version}.tgz
URL:	    https://www.gnu.org/software/parallel/
Packager:   eijkhout@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%global _python_bytecompile_errors_terminate_build 0

%package %{PACKAGE}
Summary: GNUPARALLEL is a job launcher
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: GNUPARALLEL is a job launcher
%description modulefile
This is the long description for the modulefile RPM...

%description
Summary: GNUPARALLEL is a job launcher

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
module purge

# Load Compiler
#%include compiler-load.inc

# Load MPI Library
#%include mpi-load.inc

# Insert further module commands
module load gcc
module load boost cmake python3

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
  
  # Create some dummy directories and files for fun
  #mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  #mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/share
  
#
# config/make
#

PARALLEL_VERSION=%{major_version}
PARALLEL_HOME=${WORK}/parallel/
PARALLEL_SRC=`pwd`
PARALLEL_BUILD=/tmp/parallel-stuff
PARALLEL_INSTALL=$RPM_BUILD_ROOT/%{INSTALL_DIR}
PARALLEL_BIN=${PARALLEL_INSTALL}/bin

####
#### we only support gcc installation
####
export CC=gcc
export CXX=g++
export FC=gfortran

#### configure
export PATH=${PATH}:/usr/bin

#which pod2man
#(echo foo | pod2man ) || /bin/true
#alias pod2man="pod2man -errors=pod"

pushd /tmp && rm -rf gnuparallel && mkdir gnuparallel && cd gnuparallel \
  && git clone https://github.com/ssimms/pdfapi2.git \
  && export PERLLIB=`pwd`/pdfapi2/lib \
  && export PERL5LIB=`pwd`/pdfapi2/lib \
  && git clone https://github.com/gitpan/pod2pdf.git \
  && cd pod2pdf && perl Makefile.PL && make \
  && export PATH=`pwd`/blib/script:${PATH} \
  && export PERLLIB=`pwd`/blib/lib:${PERLLIB} \
  && export PERL5LIB=`pwd`/blib/lib:${PERL5LIB} \
  && popd
which pod2pdf

./configure --prefix=${PARALLEL_INSTALL} \
&& make \
&& ( cd src ; for p in parallel.pdf env_parallel.pdf sem.pdf sql.pdf niceload.pdf parallel_tutorial.pdf parallel_book.pdf parallel_design.pdf parallel_alternatives.pdf parcat.pdf parset.pdf ; do touch $p ; done ) \
&& ( cd src ; for m in ./parallel_design.7 ; do touch $m ; done ) \
&& make install

cp -r %{_topdir}/SOURCES/gnuparallel_scripts ${PARALLEL_INSTALL}/scripts
chmod -R o+rX ${PARALLEL_INSTALL}/scripts

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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help( [[
Module %{name} loads environmental variables defining
the location of GNUPARALLEL directory and binaries:
TACC_GNUPARALLEL_DIR TACC_GNUPARALLEL_BIN

Executing a file of commandlines:

gnuparallel_command_file_execute.sh commands

Version: %{version}
]] )

whatis( "GNUPARALLEL" )
whatis( "Version: %{version}" )
whatis( "Category: system" )
whatis( "Keywords: System, utilities" )
whatis( "Description: GNU Parallel utility" )
whatis( "URL: https://www.gnu.org/software/parallel/" )

local version =  "%{version}"
local gnuparallel_dir =  "%{INSTALL_DIR}"

setenv("TACC_GNUPARALLEL_DIR",gnuparallel_dir)
setenv("TACC_GNUPARALLEL_BIN",pathJoin( gnuparallel_dir,"bin" ) )

prepend_path ("PATH",pathJoin( gnuparallel_dir,"bin" ) )
prepend_path ("PATH",pathJoin( gnuparallel_dir,"scripts" ) )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for %{name} version %{version}
##
set ModulesVersion "%version"
EOF

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
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

%changelog
* Thu Jun 14 2018 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
