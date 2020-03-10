Summary: Mvapich2-X new spec file 

# Give the package a base name
%define pkg_base_name mvapich2-x
%define MODULE_VAR    MVAPICH2-X

# Create some macros (spec file variables)

%define major_version 2
%define minor_version 3rc3

%define pkg_version %{major_version}.%{minor_version}

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
Packager: TACC - siliu@tacc.utexas.edu,aruhela@tacc.utexas.edu
#Source: %{pkg_base_name}-%{pkg_version}.tar.gz

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
Module RPM for Mvapich2-X
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
echo %{INSTALL_DIR}
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{pkg_version}.lua << 'EOF'
local help_msg=[[

Mvapich2-X 2.3rc3

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
setenv( "MPI_ROOT"               , base_dir                            )
setenv( "TACC_MPI_GETMODE"       , "mvapich2_ssh"                      )

setenv( "MV2_HOMOGENEOUS_CLUSTER", "1"                                 )
setenv( "MV2_HYBRID_ENABLE_THRESHOLD", "10000000"                      )

setenv( "MV2_USE_RDMA_CM"        , "0"                                 )
setenv( "MV2_USE_MCAST"          , "1"                                 )

--setenv( "MV2_USE_RDMA_CM_MCAST"  , "1"                               )
--setenv( "MV2_CPU_BINDING_POLICY" , "hybrid"                          )
--setenv( "MV2_HYBRID_BINDING_POLICY", "spread"                        )
--setenv( "MV2_USE_DC"             , "0"                               )

prepend_path( "PATH"             , pathJoin( base_dir , "bin"          ) )
prepend_path( "MANPATH"          , pathJoin( base_dir , "share/man"    ) )
prepend_path( "INFOPATH"         , pathJoin( base_dir , "share/doc"          ) )
prepend_path( "LD_LIBRARY_PATH"  , pathJoin( base_dir , "lib64"          ) )
prepend_path( "PKG_CONFIG_PATH"  , pathJoin( base_dir , "lib64/pkgconfig") )

prepend_path( "MODULEPATH"       , "/opt/apps/gcc9_1/impi19_0/modulefiles" )

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
