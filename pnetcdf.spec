#
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

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name pnetcdf
%define MODULE_VAR    PNETCDF
%define SOURCE_NAME pnetcdf

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 12
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc
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

Release:   1
License:   BSD
Group:     applications/io
Source:    %{SOURCE_NAME}-%{version}.tar.gz
URL:       parallel-netcdf.github.io
Distribution: RedHat Linux
Vendor:    Northwestern University & Argonne National Lab
Packager:  TACC - cazes@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
Parallel netCDF (PnetCDF) is a library providing high-performance I/O while
still maintaining file-format compatibility with Unidata's NetCDF.  NetCDF
gives scientific programmers a space-efficient and portable means for storing
data. However, it does so in a serial manner, making it difficult to achieve
high I/O performance. By making some small changes to the NetCDF APIs, PnetCDF
can use MPI-IO to achieve high-performance parallel I/O. 


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{SOURCE_NAME}-%{version}

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
%include compiler-load.inc
# Load MPI Library
%include mpi-load.inc

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  # Create temporary directory for the install.  We need this to
  mkdir -p             %{INSTALL_DIR}
  mount -t tmpfs tmpfs %{INSTALL_DIR}
  #tacctmpfs --mount %{INSTALL_DIR}

  
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
  
  %if "%{is_intel}" == "1" || "%{is_intel13}" == "1" || "%{is_intel16}" == "1"
  
  	# environment used for configure with intel compiler
          export CFLAGS="-O3 -mcmodel=medium"
          export FFLAGS="-O3 -mcmodel=medium"
          export CXXFLAGS="-O3 -mcmodel=medium"
  %endif
  
  %if "%{mpi_fam}" != "none"
     CC=mpicc
     CXX=mpicxx
     FC=mpif90
     F77=mpif77
     F90=$FC
  %endif
  
  
  %if "%{mpi_fam}" == "impi"
     CC=mpiicc
     CXX=mpiicxx
     FC=mpiifort
     F77=mpiifort
     F90=$FC
  %endif

  pwd
  ./configure --prefix=%{INSTALL_DIR} 
  make 
  make install


  # Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
  # place for the rest of the RPM.  Then, unmount the tmpfs.
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}
  #tacctmpfs --umount %{INSTALL_DIR}

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
--netcdf

local help_message = [[
IMPORTANT NOTE: TACC has several different versions of netcdf
installed.  Below is a list of each module type:

netcdf/3.6.3           -- Classic netcdf (serial)
netcdf/4.x.x           -- Serial version of Netcdf4 based upon hdf5 and
is backwards compatiable with classic netcdf (serial)
parallel-netcdf/4.x.x  -- Parallel version of Netcdf4 based upon
parallel hdf5 (parallel)
pnetcdf/1.x.x          -- Parallel netcdf(PnetCDF) that supports netcdf
in the classic formats, CDF-1 and CDF-2 (parallel)

The command "module avail netcdf" will show which versions of netcdf are
available for your current compiler/mpi module environment.

The %{pkg_base_name} module file defines the following environment variables:
TACC_PNETCDF_DIR, TACC_PNETCDF_BIN, TACC_PNETCDF_LIB, and 
TACC_PNETCDF_INC forthe location of the NETCDF distribution, binaries,
libraries, and include files, respectively.

Parallel netCDF (PnetCDF) is a library providing high-performance I/O while still maintaining file-format compatibility with Unidata's NetCDF.  NetCDF gives scientific programmers a space-efficient and portable means for storing data. However, it does so in a serial manner, making it difficult to achieve high I/O performance. By making some small changes to the NetCDF APIs, PnetCDF can use MPI-IO to achieve high-performance parallel I/O. 

To use the NETCDF library, compile the source code with the option:

	-I${TACC_PNETCDF_INC} 

Add the following options to the link step: 

	-L${TACC_PNETCDF_LIB} -lpnetcdf 

Version %{version}

]]

help(help_message,"\n")


whatis("Parallel-netCDF(Pnetcdf)")
whatis("Version: %{version}")
whatis("Category: library, runtime support")
whatis("Keywords: I/O, Library")
whatis("Description: I/O library which stores and retrieves data in self-describing, machine-independent datasets%{NETCDF_VERSION}." )
whatis(" URL: parallel-netcdf.github.io")

--Prepend paths
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("PATH",           "%{INSTALL_DIR}/bin")
prepend_path("MANPATH",        "%{INSTALL_DIR}/share/man")

--Env variables 
setenv("PNETCDF", "%{INSTALL_DIR}")
setenv("TACC_PNETCDF_DIR", "%{INSTALL_DIR}")
setenv("TACC_PNETCDF_INC", "%{INSTALL_DIR}/include")
setenv("TACC_PNETCDF_LIB", "%{INSTALL_DIR}/lib")
setenv("TACC_PNETCDF_BIN", "%{INSTALL_DIR}/bin")

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
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
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

