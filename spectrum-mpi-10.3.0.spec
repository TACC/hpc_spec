#
# W. Cyrus Proctor
# 2015-11-20 Need to investigate relocation -- use /opt/apps for now
# 2015-11-20
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
%define pkg_base_name spectrum_mpi
%define MODULE_VAR    SPECTRUM_MPI

# Create some macros (spec file variables)
%define major_version 10
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pkg_version_dash %{major_version}_%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
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
License:   BSD
Group:     MPI
URL:       https://www.open-mpi.org
Packager:  TACC - cproctor@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


#%package %{PACKAGE}
#Summary: The package RPM
#Group: Development/Tools
#%description package
#This is the long description for the package RPM...
#The Open MPI Project is an open source Message Passing Interface implementation
#that is developed and maintained by a consortium of academic, research, and
#industry partners. Open MPI is therefore able to combine the expertise,
#technologies, and resources from all across the High Performance Computing
#community in order to build the best MPI library available. Open MPI offers
#advantages for system and software vendors, application developers and computer
#science researchers.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
IBM Spectrum MPI is a high-performance, production-quality implementation of
Message Passing Interface (MPI). It accelerates application performance in
distributed computing environments. It provides a familiar portable interface
based on the open-source MPI. It goes beyond Open MPI and adds some unique
features of its own, such as advanced CPU affinity features, dynamic selection
of interface libraries, superior workload manager integrations and better
performance. 

%description
IBM Spectrum MPI is a high-performance, production-quality implementation of
Message Passing Interface (MPI). It accelerates application performance in
distributed computing environments. It provides a familiar portable interface
based on the open-source MPI. It goes beyond Open MPI and adds some unique
features of its own, such as advanced CPU affinity features, dynamic selection
of interface libraries, superior workload manager integrations and better
performance. 


#---------------------------------------
%prep
#---------------------------------------

#------------------------
#%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
#  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------
#%endif # BUILD_PACKAGE |
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
ml purge
ml %{comp_module}
ml

#echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
#%if %{?BUILD_PACKAGE}
#------------------------

#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
#  mkdir -p %{INSTALL_DIR}
#  mount -t tmpfs tmpfs %{INSTALL_DIR}
    
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
#  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
 

#if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
#fi

#cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
#umount %{INSTALL_DIR}/
  

#-----------------------  
#%endif # BUILD_PACKAGE |
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
IBM Spectrum MPI is a high-performance, production-quality implementation of
Message Passing Interface (MPI). It accelerates application performance in
distributed computing environments. It provides a familiar portable interface
based on the open-source MPI. It goes beyond Open MPI and adds some unique
features of its own, such as advanced CPU affinity features, dynamic selection
of interface libraries, superior workload manager integrations and better
performance. 

This module loads the spectrum MPI environment built with
XL compilers. By loading this module, the following commands
will be automatically available for compiling MPI applications:
mpif77       (F77 source)
mpif90       (F90 source)
mpicc        (C   source)
mpicxx       (C++ source)

The %{MODULE_VAR} module also defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

Version %{version}
]]

--help(help_msg)
help(help_msg)


whatis("Name: Spectrum MPI"                                                  )
whatis("Version: %{version}"                                                 )
whatis("Category: MPI library, Runtime Support"                              )
whatis("Description: Spectrum MPI Library (C/C++/Fortran for ppcle64)"       )
whatis("URL: https://www.ibm.com/us-en/marketplace/spectrum-mpi"             )


-- Create environment variables
local base = "/opt/ibm/spectrum_mpi"
setenv(       "MPI_ROOT"              , base )
setenv(       "OMPI_MCA_routed"       , "binomial" )
prepend_path( "PATH"                  , pathJoin( base, "bin" ))
prepend_path( "LD_LIBRARY_PATH"       , pathJoin( base, "lib" ))
prepend_path( "LD_LIBRARY_PATH"       , "/opt/ibmmath/essl/6.2/lib64" )
prepend_path( "MANPATH"               , pathJoin( base, "share/man" ))
prepend_path( "MODULEPATH"            , "%{MODULE_PREFIX}/%{comp_fam_ver}/spectrum_mpi_%{pkg_version_dash}/modulefiles" )

setenv(       "TACC_SPECTRUM_MPI_DIR"        , base )
setenv(       "TACC_SPECTRUM_MPI_BIN"        , pathJoin( base, "bin" ))
setenv(       "TACC_SPECTRUM_MPI_LIB"        , pathJoin( base, "lib" ))
setenv(       "TACC_SPECTRUM_MPI_INC"        , pathJoin( base, "include" ))

setenv(       "TACC_MPI_GETMODE"      , "spectrum_ssh" )

family("MPI")

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
#    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
#%if %{?BUILD_PACKAGE}
#%files package
#------------------------

#  %defattr(-,root,install,)
  # RPM package contains files within these directories
#  %{INSTALL_DIR}

#-----------------------
#%endif # BUILD_PACKAGE |
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
#%post %{PACKAGE}
#export PACKAGE_POST=1
#%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
#%preun %{PACKAGE}
#export PACKAGE_PREUN=1
#%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

