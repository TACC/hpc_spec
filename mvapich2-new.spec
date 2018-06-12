#
# Si Liu
# 2017-05-18
#

Summary: MVvapich2 new spec file 

# Give the package a base name
%define pkg_base_name mvapich2
%define MODULE_VAR    MVAPICH2

# Create some macros (spec file variables)

%define pkg_version 2.3rc2
%define underscore_version 2_3

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

Release:   1%{?dist}
License: BSD License
Group:   Development/Libraries
Packager: TACC - siliu@tacc.utexas.edu
Source: %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: OSU MPI-3 implementation
Group: Development/Libraries

%description package
MVAPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.
MVAPICH includes all of the routines in MPI 3.1.
MVAPICH is developed at the Ohio State University. See whttp://mvapich.cse.ohio-state.edu/

%package %{MODULEFILE}
Summary: OSU MPI-3 implementation
Group: Development/Libraries

%description modulefile
Module RPM for Mvapich2
MVAPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.
MVAPICH includes all of the routines in MPI 3.1.
MVAPICH is developed at the Ohio State University. See whttp://mvapich.cse.ohio-state.edu/

%description
MVAPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.
MVAPICH includes all of the routines in MPI 3.1.
MVAPICH is developed at the Ohio State University. See whttp://mvapich.cse.ohio-state.edu/

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n  %{pkg_base_name}-%{pkg_version}

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
%include compiler-load.inc
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

  # Removed from config:
  # --enable-sharedlibs=gcc  --enable-shared

  ./configure --prefix=%{INSTALL_DIR}   \
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
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{pkg_version}.lua << 'EOF'
local help_msg=[[
This module loads the MVAPICH2 MPI environment built with Intel compilers.
By loading this module, the following commands will be automatically available
for compiling MPI applications:
mpif77       (F77 source)
mpif90       (F90 source)
mpicc        (C   source)
mpiCC/mpicxx (C++ source)

Version %{version}
]]

help(help_msg)

whatis( "Name: %{pkg_base_name}"                                       )
whatis( "Version: %{version}"                                          )
whatis( "Category: library, runtime support"                           )
whatis( "Keywords: System, Library"                                    )
whatis( "Description:  MPI-3.1 implementation"                         )
whatis( "URL: http://mvapich.cse.ohio-state.edu/overview/mvapich2"     )

local base_dir = "%{INSTALL_DIR}"

setenv( "MPICH_HOME"             , base_dir                            )
setenv( "TACC_MPI_GETMODE"       , "mvapich2_ssh"                      )
setenv( "MV2_FASTSSH_THRESHOLD"  , "10000"                             )
setenv( "MV2_HOMOGENEOUS_CLUSTER", "1"                                 )

prepend_path( "PATH"             , pathJoin( base_dir , "bin"          ) )
prepend_path( "MANPATH"          , pathJoin( base_dir , "share/man"    ) )
prepend_path( "INFOPATH"         , pathJoin( base_dir , "doc"          ) )
prepend_path( "LD_LIBRARY_PATH"  , pathJoin( base_dir , "lib/shared"   ) )
prepend_path( "LD_LIBRARY_PATH"  , pathJoin( base_dir , "lib"          ) )
prepend_path( "PKG_CONFIG_PATH"  , pathJoin( base_dir , "lib/pkgconfig") )
prepend_path( "MODULEPATH"       ,"%{INSTALL_PREFIX}/%{comp_fam_ver}/%{pkg_base_name}-%{underscore_version}/modulefiles" )

family("MPI")

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

  #RPM This is a tricky setting by Si to avoid some Jerome problems.
  #%exclude %dir /opt/apps/intel17/modulefiles/mvapich2
  %exclude %dir %{MODULE_DIR}

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
