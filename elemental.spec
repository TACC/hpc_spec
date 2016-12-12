Summary: Elemental install

# Give the package a base name
%define pkg_base_name elemental
%define MODULE_VAR    ELEMENTAL

# Create some macros (spec file variables)
%define major_version 0
%define minor_version 87
%define micro_version 3
%define versionpatch 0.87.3

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

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

Release: 1%{?dist}
License: BSD-2, see http://opensource.org/licenses/BSD-2-Clause
Vendor: Jack Poulson
Group: Development/Numerical-Libraries
Packager: TACC -- eijkhout@tacc.utexas.edu
Source0: %{pkg_base_name}-%{major_version}.%{minor_version}.%{micro_version}.tar.gz

%define debug_package %{nil}
## %global _missing_build_ids_terminate_build 0
%global _python_bytecompile_errors_terminate_build 0


%package %{PACKAGE}
Summary: Elemental local binary install
Group: System Environment/Base
%package %{MODULEFILE}
Summary: Elemental local binary install
Group: System Environment/Base

%description
%description %{PACKAGE}
Elemental is open-source, openly-developed, software for distributed-memory dense and 
sparse-direct linear algebra and optimization which supports a wide range of functionality
not available elsewhere.
%description %{MODULEFILE}
Elemental is open-source, openly-developed, software for distributed-memory dense and 
sparse-direct linear algebra and optimization which supports a wide range of functionality
not available elsewhere.

%prep

%setup -n elemental-%{versionpatch}

#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
%include compiler-defines.inc
%include mpi-defines.inc
module purge
%include compiler-load.inc
%include mpi-load.inc

## 17 update 1, courtesy of djames
export INTELDIR="/work/01875/djames/apps/intel"
export XEDIR="$INTELDIR/parallel_studio_xe_2017.1.043"
source $XEDIR/bin/psxevars.sh
export MPICH_HOME="$INTELDIR/impi/2017.1.132"
## courtesy of Carlos
source /scratch/projects/compilers/sourceme17.sh

#
# Set Up Installation Directory and tmp file system
#
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

module load cmake
%if "%{comp_fam}" == "gcc"
  module load mkl
%endif

#
# make the regular version of elemental
#
export ELEMENTAL_DIR=`pwd`

export CC=mpicc
export CXX=mpicxx
%if "%{comp_fam}" == "intel"
  export XOPTFLAGS="-xAVX -axCORE-AVX2,CORE-AVX-I -g"
#### "-xCORE-AVX2 -xMIC-AVX512 -g"
%endif
%if "%{comp_fam}" == "gcc"
  module load mkl
  export XOPTFLAGS="-O2 -g"
%endif
export COPTFLAGS=${XOPTFLAGS}

mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 

for ext in Release ; do
#for ext in PureDebug PureRelease HybridDebug HybridRelease ; do

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

            # -C CMAKE_C_COMPILER=${CC} \
            # -D CMAKE_C_FLAGS= "-xAVX -axCORE-AVX2,CORE-AVX-I -g" \
            # -C CMAKE_CXX_COMPILER=${CXX} \
            # -D CMAKE_CXX_FLAGS= "-xAVX -axCORE-AVX2,CORE-AVX-I -g" \
#

  ( mkdir -p build/${ext} ; \
      cd build/${ext} ; \
      cmake -D CMAKE_BUILD_TYPE=${ext} \
      	    -D CMAKE_INSTALL_PREFIX=%{INSTALL_DIR}/${ext} \
	    -D MATH_LIBS="-mkl" \
	    ../.. ; \
      make -j 2 VERBOSE=1 2>&1 | tee make.log ; \
      make install ; \
      rm -rf bin/tests \
  )

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

##
## module file
##

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
export modulefilename=%{version}-${ext}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The ELEMENTAL modulefile defines the following environment variables:
TACC_ELEMENTAL_DIR, TACC_ELEMENTAL_LIB, and TACC_ELEMENTAL_INC
for the location of the ELEMENTAL %{version} distribution,
libraries, and include files, respectively.

Documentation:
http://libelemental.org/

Version ${modulefilename}
]] )

whatis( "Name: Elemental" )
whatis( "Version: %{version}-${ext}" )
whatis( "Version-notes: ${modulefilename}" )
whatis( "Category: library, mathematics" )
whatis( "Keywords: Linear Algebra, Library, Mathematics, Parallel" )
whatis( "URL: http://libelemental.org/" )
whatis( "Description: Library for distributed dense linear algebra" )

local             elemental_dir = "%{INSTALL_DIR}"

setenv( "TACC_ELEMENTAL_DIR",        elemental_dir )
setenv( "TACC_ELEMENTAL_LIB",        pathJoin(elemental_dir,"${ext}","lib64" ) )
setenv( "TACC_ELEMENTAL_INC",        pathJoin(elemental_dir,"${ext}","include" ) )
setenv( "TACC_ELEMENTAL_VARIANT",    "${ext}" )
setenv( "TACC_ELEMENTAL_VERSION",    "%{version}" )

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0##################################################
##
## version file for elemental
##
 
set     ModulesVersion      "${modulefilename}"
EOF


#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

done

cp -r src %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
umount tmpfs

#------------------------
%if %{?BUILD_PACKAGE}
%files package
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
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Dec 09 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: modulefile fix, using Carlos secret compiler
* Mon Nov 21 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: initial release
