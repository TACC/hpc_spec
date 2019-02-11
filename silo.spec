#
# Si Liu
# 2017-05-18
#

Summary: SILO spec file 
Need to rewrite it!!!!

# Give the package a base name
%define pkg_base_name silo
%define MODULE_VAR    SILO

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 66
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
#%include mpi-defines.inc
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

Release:   3%{?dist}
License: BSD Open Source License
Group:   Data/Visualization
Packager: TACC - siliu@tacc.utexas.edu
Source: %{name}-%{version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: Silo
Group: Data/Visualization

%description package
Silo is a library for reading and writing a wide variety of scientific data to binary, disk files. 
The files Silo produces and the data within them can be easily shared and exchanged 
between wholly independently developed applications running on disparate computing platforms. 
Consequently, Silo facilitates the development of general purpose tools for processing scientific data. 

%package %{MODULEFILE}
Summary: Silo
Group: Data/Visualization 

%description modulefile
Module RPM for Silo

%description
Silo is a library for reading and writing a wide variety of scientific data to binary, disk files. 
The files Silo produces and the data within them can be easily shared and exchanged 
between wholly independently developed applications running on disparate computing platforms. 
Consequently, Silo facilitates the development of general purpose tools for processing scientific data.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-%{pkg_version} 

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
%include compiler-defines.inc
#%include mpi-defines.inc
module purge


%include compiler-load.inc
module load intel/17.0.4
module list

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

export MPIINSTALL_OPTS="-noman"
export RSHCOMMAND=ssh

# We will define an extra variable to decide what gets
# removed from the final mpi wrappers.

export CFLAGS=" "
export CFLAGS_TACC_BUILD_ONLY="-pipe"
export CXXFLAGS=$CFLAGS
export FFLAGS=$CFLAGS
export FCFLAGS=$FFLAGS

%if "%{comp_fam}" == "intel"

  export CFLAGS="$CFLAGS -Wl,-rpath,$IFC_LIB -Wl,-rpath,$ICC_LIB"
#  export CFLAGS="$CFLAGS -Wl,-rpath,$IFC_LIB -Wl,-rpath,$ICC_LIB -i-dynamic"
  export CFLAGS_TACC_BUILD_ONLY="$CFLAGS_TACC_BUILD_ONLY -fno-strict-aliasing"
  export FFLAGS_TACC_BUILD_ONLY=$CFLAGS_TACC_BUILD_ONLY

  export CXXFLAGS=$CFLAGS
  export FFLAGS=$CFLAGS
  export FCFLAGS=$FFLAGS

%endif

%if "%{comp_fam}" == "gcc"
  export LDFLAGS="$LDFLAGS -Wl,-rpath,$GCC_LIB"
  export CFLAGS_TACC_BUILD_ONLY="$CFLAGS_TACC_BUILD_ONLY"
  export FFLAGS_TACC_BUILD_ONLY=$CFLAGS_TACC_BUILD_ONLY

  export CXXFLAGS=$CFLAGS
  export FFLAGS=$CFLAGS
  export FCFLAGS=$FFLAGS

%endif

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

  export CFLAGS="$CFLAGS $CFLAGS_TACC_BUILD_ONLY"
  export FFLAGS="$FFLAGS $FFLAGS_TACC_BUILD_ONLY"
  export CXXFLAGS="$CXXFLAGS $CFLAGS_TACC_BUILD_ONLY"

  OPT_LEVEL="--enable-fast=O3"
  DEBUG_OPTIONS="--enable-g=dbg"

  %if "%{is_debug}" == "1"
  module load valgrind
  OPT_LEVEL="--disable-fast"
  DEBUG_OPTIONS="--enable-g=dbg,mem,meminit --with-valgrind=$TACC_VALGRIND_INC --enable-debuginfo  --enable-error-messages=all"
  %endif

  INSTALL_DIR=%{INSTALL_DIR}

  # Removed from config:
  # --enable-sharedlibs=gcc  --enable-shared

  ./configure --prefix=$INSTALL_DIR   \
        --with-device=ch3:psm  \
        --with-ch3-rank-bits=32 \
        --enable-cxx --enable-romio \
        $OPT_LEVEL                  \
        $DEBUG_OPTIONS               \
        --with-file-system=lustre     \

  make -j 16

  make DESTDIR=$RPM_BUILD_ROOT install

  export CFLAGS_TACC_BUILD_ONLY="-pipe -fno-strict-aliasing"
  export FFLAGS_TACC_BUILD_ONLY=$CFLAGS_TACC_BUILD_ONLY
  for i in $CFLAGS_TACC_BUILD_ONLY $FFLAGS_TACC_BUILD_ONLY; do
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicc
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpicxx
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif77
        sed -i s^"$i"^^ $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mpif90
  done



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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

#%Module1.0#####################################################################
##
## MVAPICH2
##
proc ModulesHelp { } {
global version MPICHhome

puts stderr " "
puts stderr "Mvapich2 2.3RC2 "
puts stderr " "
puts stderr "This module loads the MVAPICH2 MPI environment built with"
puts stderr "%{comp_fam_name} compilers. By loading this module, the following commands"
puts stderr "will be automatically available for compiling MPI applications:"
puts stderr "\n"
puts stderr "mpif77       (F77 source)"
puts stderr "mpif90       (F90 source)"
puts stderr "mpicc        (C   source)"
puts stderr "mpiCC/mpicxx (C++ source)"
puts stderr "\n"
puts stderr "Version $version\n"
}

module-whatis "MVAPICH2"
module-whatis "Version: %{version}"
module-whatis "Category: library, runtime support"
module-whatis "Keywords: System, Library"
module-whatis "Description: MPI-3.1 implementation for Infiniband"
module-whatis "URL: http://mvapich.cse.ohio-state.edu/overview/mvapich2/"

# for Tcl script use only
set     version         %version
set     MPICHhome       %{INSTALL_DIR}

# Export to User.

setenv MPICH_HOME       $MPICHhome
setenv TACC_MPI_GETMODE mvapich2_ssh
setenv MV2_FASTSSH_THRESHOLD 10000
setenv MV2_HOMOGENEOUS_CLUSTER 1

prepend-path    PATH            $MPICHhome/bin
prepend-path    MANPATH         $MPICHhome/share/man
prepend-path    INFOPATH        $MPICHhome/doc
prepend-path    LD_LIBRARY_PATH $MPICHhome/lib/shared

prepend-path    LD_LIBRARY_PATH $MPICHhome/lib

prepend-path    MODULEPATH      %{SUBMODULES}
prepend-path    PKG_CONFIG_PATH $MPICHhome/lib/pkgconfig

%if "%{is_debug}" == "1"
setenv  MPICH_TRMEM_VALIDATE YES
setenv  MPICH_TRMEM_INITZERO YES
%endif

family "MPI"

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