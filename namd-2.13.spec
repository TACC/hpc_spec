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
%define pkg_base_name namd
%define MODULE_VAR    NAMD

# Create some macros (spec file variables)
%define major_version 2.13
#%define minor_version
#%define micro_version

#%define pkg_version %{major_version}.%{minor_version}
%define pkg_version %{major_version}
### Toggle On/Off ###
%include rpm-dir.inc

%include compiler-defines.inc
%include mpi-defines.inc

#%include name-defines-noreloc.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines.inc


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
Group:     Theoretical and Computational Biophysics Group, UIUC
URL:       http://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=NAMD
Packager:  TACC - huang@tacc.utexas.edu
Source:    NAMD_2.13_Source.tar.gz
Source1:   tcl8.5.9-linux-x86_64-threaded.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The NAMD RPM 
Group: Applications/Chemistry
%description package
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

%description
NAMD, recipient of a 2002 Gordon Bell Award, is a parallel molecular dynamics
code designed for high-performance simulation of large biomolecular systems.
Based on Charm++ parallel objects, NAMD scales to hundreds of processors on
high-end parallel platforms and tens of processors on commodity clusters
using gigabit ethernet.

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

%setup -n NAMD_%{pkg_version}_Source


#---------------------------------------
%build
#---------------------------------------
%include compiler-load.inc
%include mpi-load.inc

tar -zxvf $RPM_SOURCE_DIR/tcl8.5.9-linux-x86_64-threaded.tar.gz

tar -xvf charm-6.8.2.tar
cd charm-6.8.2/

env MPICXX=mpicxx CC=icc CXX=icpc ./build charm++ mpi-linux-x86_64-smp-iccstatic --incdir $TACC_IMPI_INC --libdir $TACC_IMPI_LIB --no-build-shared --with-production -j16 -xCORE-AVX2
cd ..

sed -i 's/xMIC-AVX512/xCORE-AVX2/' arch/Linux-KNL-icc.arch
./config Linux-KNL-icc --charm-arch mpi-linux-x86_64-smp-iccstatic --with-mkl --mkl-prefix $TACC_MKL_DIR --with-tcl --tcl-prefix `pwd`/tcl8.5.9-linux-x86_64-threaded
cd Linux-KNL-icc
make -j 16

mkdir ../bin
mv {psfgen,flipbinpdb,flipdcd,sortreplicas} ../bin/
cd .. ; rm -Rf Linux-KNL-icc


sed -i 's/xCORE-AVX2/xCORE-AVX512/' arch/Linux-KNL-icc.arch
./config Linux-KNL-icc --charm-arch mpi-linux-x86_64-smp-iccstatic --with-mkl --mkl-prefix $TACC_MKL_DIR --with-tcl --tcl-prefix `pwd`/tcl8.5.9-linux-x86_64-threaded
cd Linux-KNL-icc
make -j 16
mv namd2 ../bin/namd2_skx

cd .. ; rm -Rf Linux-KNL-icc

sed -i 's/xCORE-AVX512/xMIC-AVX512/' arch/Linux-KNL-icc.arch
./config Linux-KNL-icc --charm-arch mpi-linux-x86_64-smp-iccstatic --with-mkl --mkl-prefix $TACC_MKL_DIR --with-tcl --tcl-prefix `pwd`/tcl8.5.9-linux-x86_64-threaded
cd Linux-KNL-icc
make -j 16

mv namd2 ../bin/namd2_knl


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

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
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

  cp -p bin/{namd2_knl,namd2_skx,psfgen,flipbinpdb,flipdcd,sortreplicas} $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
  cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}
  chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}


  # Copy everything from tarball over to the installation directory
#  cp * $RPM_BUILD_ROOT/%{INSTALL_DIR}

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
local help_msg=[[
The TACC NAMD module appends the path to the namd2 executable
to the PATH environment variable. Also TACC_NAMD_DIR,
TACC_NAMD_BIN, and TACC_NAMD_LIB are set to NAMD home
bin, and lib directories; lib directory contains information for
ABF, random acceleration MD(RAMD), replica exchange MD(REMD).


Note: The way to run NAMD on KNL and SKX are different. Please read 
the following instructions carefully. 

## On KNL 
Two recommended settings are shown in the following example slurm 
scripts for KNL nodes. 

#  Example for one or two nodes. four tasks per node
#SBATCH -J test # Job Name
#SBATCH -o test.o%j
#SBATCH -N 1    # Total number of nodes
#SBATCH -n 4    # Total number of mpi tasks
#SBATCH -p normal # Queue (partition) name -- normal, development, etc.
#SBATCH -t 24:00:00 # Run time (hh:mm:ss) - 24 hours

module load intel/16.0.3 impi namd/2.13
ibrun namd2_knl +ppn 32 +pemap 0-63+68 +commap 64-67 input &> output

For two nodes, you only to change node number and task number. 
#SBATCH -N 2    # Total number of nodes
#SBATCH -n 8    # Total number of mpi tasks


#  Example for more than one nodes. 13 tasks per node. Scales better!!
#SBATCH -J test # Job Name
#SBATCH -o test.o%j
#SBATCH -N 3     # Total number of nodes
#SBATCH -n 39    # Total number of mpi tasks
#SBATCH -p normal # Queue (partition) name -- normal, development, etc.
#SBATCH -t 24:00:00 # Run time (hh:mm:ss) - 24 hours

module load intel/16.0.3 impi namd/2.13
ibrun namd2_knl +ppn 8 +pemap 0-51+68 +commap 52-67 input &> output

For four nodes,
#SBATCH -N 4    # Total number of nodes
#SBATCH -n 52    # Total number of mpi tasks


You may need to change some parameters if necessary. You can try 
both settings then use the optimal one. If your system is small 
or the number of nodes are large, you can try "+ppn 16 +pemap 
0-63 +commap 64-67" for 4 tasks per node or "+ppn 4 +pemap 0-51 
+commap 52-67" for 13 tasks per node.


## For jobs on SKX nodes
#SBATCH -J test # Job Name
#SBATCH -o test.o%j
#SBATCH -N 2     # Total number of nodes
#SBATCH -n 8    # Total number of mpi tasks
#SBATCH -p skx-normal # Queue (partition) name -- skx-normal, skx-dev, etc.
#SBATCH -t 24:00:00 # Run time (hh:mm:ss) - 24 hours

module load intel/16.0.3 impi namd/2.13
ibrun namd2_skx +ppn 11 +pemap 2-22:2,26-46:2,3-23:2,27-47:2 +commap 0,24,1,25 input &> output

4 tasks per node is recommended on SKX nodes. 
You may also try other settings if necessary. 
6 tasks per node, ibrun namd2_skx +ppn 7 +pemap 2-14:2,18-30:2,34-46:2,3-15:2,19-31:2,35-47:2 +commap 0,16,32,1,17,33 input &> output
2 tasks per node, ibrun namd2_skx +ppn 23 +pemap 2-47:2,3-47:2 +commap 0,1 input &> output
1 tasks per node, ibrun namd2_skx +ppn 47 +pemap 2-47:2,1-47:2 +commap 0 input &> output

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: NAMD")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL: http://www.ks.uiuc.edu/Research/namd/")
whatis("Description: Scalable Molecular Dynamics software")

-- Create environment variables.
local namd_dir           = "%{INSTALL_DIR}"

family("namd")
prepend_path(    "PATH",                pathJoin(namd_dir, "bin"))
prepend_path(    "MODULEPATH",         "/opt/apps/intel16/impi17_0/modulefiles/namd_2.13/modulefiles")
setenv( "TACC_%{MODULE_VAR}_DIR",                namd_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(namd_dir, "bin"))

local nag_message = [[
Note: 

  Please note that the way to run NAMD on Stampede 2 has been changed. 
The executable files for KNL and SKX nodes are different to get best 
performance. For more information please execute:

module load intel/16.0.3 namd/2.13
module help namd

]]

LmodMessage(nag_message,"\n")



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

