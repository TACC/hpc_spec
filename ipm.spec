#
# Amit Ruhela
# Sept 19, 2020
#
# Typical Command-Line Example:
# ./build_rpm.sh  -i19 -j19_7 ipm.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps ipm-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps ipm-modulefile-1.1-1.x86_64.rpm
# rpm -e ipm-package-1.1-1.x86_64 ipm-modulefile-1.1-1.x86_64

Summary: IPM is a portable profiling infrastructure for parallel codes.

# Give the package a base name
%define pkg_base_name ipm
%define MODULE_VAR    IPM

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
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
License:   GPL
Group:     System Environment/Base
URL:       http://ipm-hpc.sourceforge.net
Packager:  aruhela@tacc.utexas.edu

Source:    ipm-%{pkg_version}.tar.gz


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
Integrated Performance Monitoring for HPC (IPM) is a portable profiling
infrastructure for parallel codes. It provides a low-overhead performance
summary of the computation and communication in a parallel program.  IPM
has extremely low overhead, is scalable and easy to use requiring no 
source code modification.


%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Integrated Performance Monitoring for HPC (IPM) is a portable profiling
infrastructure for parallel codes. It provides a low-overhead performance
summary of the computation and communication in a parallel program.  IPM
has extremely low overhead, is scalable and easy to use requiring no 
source code modification.

%description
Integrated Performance Monitoring for HPC (IPM) is a portable profiling
infrastructure for parallel codes. It provides a low-overhead performance
summary of the computation and communication in a parallel program.  IPM
has extremely low overhead, is scalable and easy to use requiring no 
source code modification.

#---------------------------------------
%prep
#---------------------------------------

%define debug_package %{nil}

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  cd %{_topdir}/BUILD
  rm -rf IPM-%{version}
  rm -rf IPM ploticus242_linuxbin64.tar.gz  
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  wget https://master.dl.sourceforge.net/project/ploticus/ploticus/2.42/ploticus242_linuxbin64.tar.gz
  tar -xzf ploticus242_linuxbin64.tar.gz
  git clone https://github.com/nerscadmin/IPM.git

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

cd IPM
module load papi
./bootstrap.sh
cd utils/
./make_mxml
cd ..
 ./configure --prefix=%{INSTALL_DIR} --with-papi=$TACC_PAPI_DIR --enable-posixio --enable-parser --enable-coll-details  --enable-papi-multiplexing    --enable-pmon   --enable-shared  CFLAGS="-I$TACC_IMPI_INC -I$TACC_PAPI_INC -DMPICH_DEFINE_2COMPLEX"   --enable-parser=$PWD/utils/mxml LIBS="-Wl,-rpath,$TACC_PAPI_LIB -L$TACC_PAPI_LIB -lpapi -lpthread"
make -j 20 
make DESTDIR=$RPM_BUILD_ROOT install
cd ..
cp -rf ploticus242/prefabs $RPM_BUILD_ROOT/%{INSTALL_DIR}/.
rm -rf ploticus242
rm -rf ploticus242_linuxbin64.tar.gz

  # Copy everything from tarball over to the installation directory

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
local help_message=[[
The IPM modulefile defines the following environment variables:
TACC_IPM_DIR, TACC_IPM_BIN, TACC_IPM_INC, and TACC_IPM_LIB 
for the location of the IPM distribution, binaries, include,
and libraries respectively.

You might need to change IPM_KEYFILE environment variable to one
of ipm_key_cublas  ipm_key_cuda  ipm_key_cufft  ipm_key_mem  
ipm_key_mpi  ipm_key_mpiio  ipm_key_posixio as per your requirements.

Please load the ipm module and set the LD_PRELOAD variable
directly within your job script as follows:

-- Example Job Script Excerpt (csh syntax) --
module load ipm
setenv LD_PRELOAD \$TACC_IPM_LIB/libipm.so
ibrun ./a.out

-- Example Job Script Excerpt (bash syntax) --
module load ipm
export LD_PRELOAD=\$TACC_IPM_LIB/libipm.so
export IPM_KEYFILE=\$TACC_IPM_DIR/etc/ipm_key_mpi
ibrun ./a.out


Important Note:
TACC staff recommend that you set the LD_PRELOAD environment
only within your job script as opposed to making permanent
environment changes via shell startup scripts.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: IPM")
whatis("Version: %{version}")
whatis("Category: library, profilling")
whatis("URL: http://ipm-hpc.sourceforge.net")
whatis("Description: Integrated Performance Monitoring")

-- Create environment variables --

local base_dir = "%{INSTALL_DIR}"

setenv("TACC_IPM_DIR",          base_dir)
setenv("TACC_IPM_BIN",          pathJoin( base_dir , "bin"))
setenv("TACC_IPM_LIB",          pathJoin( base_dir , "lib"))
setenv("TACC_IPM_INC",          pathJoin( base_dir , "include"))
setenv("IPM_KEYFILE",           pathJoin( base_dir , "etc/ipm_key_mpi"))
setenv("PLOTICUS_PREFABS",      pathJoin( base_dir , "prefabs"))
prepend_path("PATH",            pathJoin( base_dir , "bin"))
prepend_path("LD_LIBRARY_PATH", pathJoin( base_dir , "lib"))

setenv("IPM_REPORT","full")
setenv("IPM_MPI_THRESHOLD","0.3")
setenv("IPM_MPI_THRESHOLD","0.3")
setenv("IPM_HPM", "PAPI_L1_DCM,PAPI_L1_ICM,PAPI_L2_DCM,PAPI_L2_ICM,PAPI_L1_TCM,PAPI_L2_TCM,PAPI_L3_TCM")

depends_on( "papi" )

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

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

%changelog

