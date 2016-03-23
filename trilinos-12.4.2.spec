#
# Adapted from Bar.spec by Victor Eijkhout 2015/11/30
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

Summary: Trilinos rpm build script

# Give the package a base name
%define pkg_base_name trilinos
%define MODULE_VAR    TRILINOS

# Create some macros (spec file variables)
%define major_version 12
%define minor_version 4
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
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

Release:   4
License:   GPL
Group:     Development/Tools
URL:       https://trilinos.org/
Packager:  TACC - eijkhout@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_full_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Trilinos rpm building
Group: HPC/libraries
%description package
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

export modulefilename=%{pkg_version}

# Insert necessary module commands
module load boost cmake phdf5 parallel-netcdf python swig
# python

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

# VLE here is where we start copying from the old spec file
mkdir -p %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR} 

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

export INSTALL_LOCATION=%{INSTALL_DIR}
rm -rf CMakeCache.txt CMakeFiles
echo "cmaking in" `pwd`

rm -rf /tmp/trilinos-build
mkdir -p /tmp/trilinos-build
pushd /tmp/trilinos-build

export VERSION=%{version}
export TRILINOS_LOCATION=%{_topdir}/BUILD/

## VLE remove this when Cyrus adds them to 
%if "%{comp_fam}" != "intel"
  export MKLROOT=/opt/apps/intel/16/compilers_and_libraries_2016.0.109/linux/mkl
%endif
export TACC_MKL_DIR=${MKLROOT}
export TACC_MKL_LIB=${MKLROOT}/lib/intel64
export TACC_MKL_INC=${MKLROOT}/include

%if "%{comp_fam}" == "intel"
#  export MY_C_CXX_FLAGS="-D CMAKE_C_FLAGS:STRING=\"${COPTFLAGS} -mkl\" -D CMAKE_CXX_FLAGS:STRING=\"${COPTFLAGS} -mkl\" "
# -DMPICH_SKIP_MPICXX
#  export MY_C_CXX_FLAGS="-D CMAKE_C_FLAGS:STRING=\" -mkl -cxxlib-nostd \" -D CMAKE_CXX_FLAGS:STRING=\" -mkl -cxxlib-nostd \" "
%endif

#%include trilinos.cmake
export TRILINOS_PACKAGES=" \
  -D Trilinos_ENABLE_Amesos:BOOL=ON \
  -D Amesos2_ENABLE_Basker:BOOL=ON \
  -D Trilinos_ENABLE_Anasazi:BOOL=ON \
  -D Trilinos_ENABLE_AztecOO:Bool=ON \
  -D Trilinos_ENABLE_Belos:BOOL=ON \
  -D Trilinos_ENABLE_Epetra:Bool=ON \
  -D Trilinos_ENABLE_EpetraExt:Bool=ON \
  -D                 Epetra_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_Ifpack:Bool=ON \
  -D Trilinos_ENABLE_Intrepid:BOOL=ON \
  -D                 Intrepid_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_ML:BOOL=ON \
  -D Trilinos_ENABLE_MOOCHO:BOOL=ON \
  -D Trilinos_ENABLE_NOX=ON \
  -D                 NOX_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_Pamgen:Bool=ON \
  -D Trilinos_ENABLE_Phalanx:BOOL=ON \
  -D Phalanx_EXPLICIT_TEMPLATE_INSTANTIATION=ON \
  -D Trilinos_ENABLE_Rythmos:BOOL=ON \
  -D Trilinos_ENABLE_Sacado:Bool=ON \
  -D Trilinos_ENABLE_SEACASIoss:BOOL=ON \
  -D Trilinos_ENABLE_SEACAS:BOOL=ON \
  -D Trilinos_ENABLE_SEACASBlot:BOOL=ON \
  -D Trilinos_ENABLE_Shards:BOOL=ON \
  -D Trilinos_ENABLE_ShyLU:BOOL=OFF \
  -D Trilinos_ENABLE_STK:BOOL=ON \
  -D Trilinos_ENABLE_Stokhos:BOOL=ON \
  -D Trilinos_ENABLE_Stratimikos:BOOL=ON \
  -D Trilinos_ENABLE_Sundance:BOOL=ON \
  -D Trilinos_ENABLE_Teko:BOOL=ON \
  -D Trilinos_ENABLE_Teuchos:BOOL=ON \
  -D Trilinos_ENABLE_TriKota:BOOL=ON \
  -D Trilinos_ENABLE_Zoltan:BOOL=ON \
   \
   -D CMAKE_PYTHON_INCLUDE_DIR:PATH="${TACC_PYTHON_INC}" \
   -D CMAKE_PYTHON_LIBRARIES:STRING="${TACC_PYTHON_LIB}" \
   -D Trilinos_ENABLE_PyTrilinos:Bool=ON \
  "
export NO_TRILINOS_PACKAGES=" \
  -D Trilinos_ENABLE_MueLu:BOOL=ON \
  "
export packageslisting="Amesos,Anasazi,AztecOO,Belos,Epetra,EpetraExt,Ifpack,Intrepid,ML,MOOCHO,NOX,Pamgen,Phalanx,Rythmos,Sacado,SEACAS(+Ioss,+Blot),Shards,ShyLU,STK,Stokhos,Stratimikos,Sundance,Teko,Teuchos,TriIota,Zoltan"

which icc
export GCC_VERSION=4.9.3
export CPP_PATHS="-I/opt/apps/gcc/${GCC_VERSION}/include/c++/${GCC_VERSION} -I/opt/apps/gcc/${GCC_VERSION}/include/c++/${GCC_VERSION}/x86_64-unknown-linux-gnu "
# leads to: /opt/apps/gcc/4.9.3/include/c++/4.9.3/ext/atomicity.h(49): error: identifier "__ATOMIC_ACQ_REL" is undefined

# see: http://trilinos.sandia.gov/Trilinos10CMakeQuickstart.txt
cmake -VV \
  -D BUILD_SHARED_LIBS:BOOL=ON \
  -D Trilinos_VERBOSE_CONFIGURE=OFF \
  -D CMAKE_VERBOSE_MAKEFILE=ON \
  -D Trilinos_ENABLE_ALL_PACKAGES:BOOL=OFF \
  -D Trilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF \
  -D Trilinos_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_EXAMPLES:BOOL=ON \
  -D Trilinos_ENABLE_Fortran:BOOL=ON \
  \
  -D CMAKE_INSTALL_PREFIX:PATH=${INSTALL_LOCATION} \
  -D CMAKE_BUILD_TYPE:STRING=RELEASE \
  -D CMAKE_Fortran_FLAGS:STRING="-mkl ${CPP_PATHS} -lifcore" \
  -D Trilinos_EXTRA_LINK_FLAGS:STRING="-lifcore" \
  -D CMAKE_C_FLAGS:STRING="-mkl ${CPP_PATHS}" \
  -D CMAKE_CXX_FLAGS:STRING="-mkl ${CPP_PATHS}" \
  -D Trilinos_CXX11_FLAGS="-std=c++11" \
  \
  -D BLAS_INCLUDE_DIRS:PATH="${TACC_MKL_INC}" \
  -D BLAS_LIBRARY_DIRS:PATH="${TACC_MKL_LIB}" \
  -D BLAS_LIBRARY_NAMES:STRING="mkl_intel_lp64;mkl_sequential;mkl_core;pthread" \
  -D LAPACK_INCLUDE_DIRS:PATH="${TACC_MKL_INC}" \
  -D LAPACK_LIBRARY_DIRS:PATH="${TACC_MKL_LIB}" \
  -D LAPACK_LIBRARY_NAMES:STRING="mkl_intel_lp64;mkl_sequential;mkl_core;pthread" \
  \
  -D TPL_ENABLE_MPI:BOOL=ON \
  -D MPI_EXEC:FILEPATH="/opt/apps/xalt/0.4.6/bin/ibrun" \
  -D TPL_ENABLE_GLM=OFF \
  -D TPL_ENABLE_Matio=OFF \
  \
  -D TPL_ENABLE_Boost:BOOL=ON \
  -D Boost_INCLUDE_DIRS:PATH=$TACC_BOOST_INC      \
  -D Boost_LIBRARY_DIRS:PATH=$TACC_BOOST_LIB      \
  -D TPL_ENABLE_BoostLib:BOOL=ON \
  -D BoostLib_INCLUDE_DIRS:PATH=$TACC_BOOST_INC      \
  -D BoostLib_LIBRARY_DIRS:PATH=$TACC_BOOST_LIB      \
  \
  -D TPL_ENABLE_HDF5:BOOL=ON \
  -D HDF5_INCLUDE_DIRS:PATH=$TACC_HDF5_INC    \
  -D HDF5_LIBRARY_DIRS:PATH=$TACC_HDF5_LIB    \
  -D TPL_ENABLE_Netcdf:BOOL=ON \
  -D Netcdf_INCLUDE_DIRS:PATH=$TACC_NETCDF_INC    \
  -D Netcdf_LIBRARY_DIRS:PATH=$TACC_NETCDF_LIB    \
  \
  -D Trilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=ON \
  \
  ${TRILINOS_PACKAGES} \
  \
  -D CMAKE_PYTHON_INCLUDE_DIR:PATH="${TACC_PYTHON_INC}" \
  -D CMAKE_PYTHON_LIBRARIES:STRING="${TACC_PYTHON_LIB}" \
  -D Trilinos_ENABLE_PyTrilinos:Bool=ON \
  \
  -D SWIG_EXECUTABLE:FILEPATH=${TACC_SWIG_DIR}/bin/swig \
  \
  ${TRILINOS_LOCATION}/trilinos-${VERSION} \
  | tee /admin/rpms/SPECS/trilinos-${VERSION}-cmake.log 2>&1

# /bin/true \
#   \
#   notrue

####
#### Compilation
####
echo "Going to compile!"
make #make -j 8             # Trilinos can compile in parallel
# make -j 4 tests           # (takes forever...)
#make runtests-serial # (requires queue submission)
#make runtests-mpi    # (requires queue submission)

####
#### Testing
####
#ctest -VV

####
#### Install permanently
####

make install

popd

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua << EOF
help( [[
The trilinos module defines the following environment variables:
TACC_TRILINOS_DIR, TACC_TRILINOS_BIN, and
TACC_TRILINOS_LIB for the location
of the Trilinos distribution, documentation, binaries,
and libraries.

Version %{version}${versionextra}
external packages installed: ${packageslisting}
]] )

whatis( "Name: Trilinos" )
whatis( "Version: %{version}${versionextra}${dynamicextra}" )
whatis( "Version-notes: external packages installed: ${packages}" )
whatis( "Category: library, mathematics" )
whatis( "URL: http://www-unix.mcs.anl.gov/trilinos/trilinos-as/" )
whatis( "Description: Numerical library for sparse linear algebra" )

local             trilinos_arch =    "${architecture}"
local             trilinos_dir =     "%{INSTALL_DIR}/"

prepend_path("PATH",            pathJoin(trilinos_dir,trilinos_arch,"bin") )
prepend_path("LD_LIBRARY_PATH", pathJoin(trilinos_dir,trilinos_arch,"lib") )

setenv("TRILINOS_ARCH",            trilinos_arch)
setenv("TRILINOS_DIR",             trilinos_dir)
setenv("TACC_TRILINOS_DIR",        trilinos_dir)
setenv("TACC_TRILINOS_BIN",        pathJoin(trilinos_dir,trilinos_arch,"bin") )
setenv("TACC_TRILINOS_LIB",        pathJoin(trilinos_dir,trilinos_arch,"lib") )
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.${modulefilename} << EOF
#%Module1.0#################################################
##
## version file for Trilinos %version
##

set     ModulesVersion      "${modulefilename}"
EOF

  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/${modulefilename}.lua

##
## end of configure install section
##

module unload python
cp -r %{INSTALL_DIR}/* ${RPM_BUILD_ROOT}/%{INSTALL_DIR}/

#tacctmpfs -u %{INSTALL_DIR}
umount tmpfs

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
#
* Mon Mar 21 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 4:  adding python bindings now that we have swig
* Fri Mar 18 2016 eijkhout <eijkhout@tacc.utexas.edu>
- release 3: adding Sundance
* Tue Dec 08 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 2: no longer relocatable
* Mon Dec 07 2015 eijkhout <eijkhout@tacc.utexas.edu>
- release 1: no packages
