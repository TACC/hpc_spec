#
# rpmbuild -bb --define 'is_xl161 1' --define 'is_spectrum 1' --define 'mpiV 10_2' namd-gpu.spec 2>&1 | tee namd-gpu_1a.log
#
# r=/admin/build/admin/rpms/frontera/RPMS/x86_64
#rpm -hiv --nodeps $r/
#rpm -hiv --nodeps $r/

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
%define pkg_base_name namd_gpu
%define MODULE_VAR    NAMD_GPU

# Create some macros (spec file variables)
%define major_version 2
%define minor_version 13
%define micro_version 0

#%define pkg_version %{major_version}.%{minor_version}
%define pkg_version %{major_version}.%{minor_version}
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
#Source:    namd_gpu_2.13.tgz
#Source:     NAMD_Git-2019-12-13_Source.tar
Source:     namd_gpu_2.13.tar

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

%setup -n namd_gpu_%{pkg_version}


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
%include mpi-load.inc


# Insert necessary module commands
#module purge

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

  tar -xvf charm-6.10.0-pre.tar
  mv       charm-6.10.0-pre     charm-6.10.0
  
  #BUILD charm++
  
  cd charm-6.10.0
  
   ./build charm++ verbs-linux-ppc64le xlc smp --no-build-shared --with-production -j10 
   #there is a cd .. at the end of a sucessful build
  
  #            Should be in NAMD_Git-2019-12-13_Source
  cd arch
  
  cp -p Linux-POWER-xlC.arch Linux-POWER-xlC.arch.0
  sed -i s/-qarch=auto/-qarch=pwr9/ Linux-POWER-xlC.arch
  
  sed -i s/-lnuma// Linux-POWER-xlC.arch
  
  module load cuda/10.0
  
  cd ..  # should be in .../NAMD_Git-2019-12-13_Source after executing this cmd
  
  ./config Linux-POWER-xlC --charm-arch verbs-linux-ppc64le-smp-xlc \
                           --with-cuda \
                           --cuda-prefix $TACC_CUDA_DIR \
                           --cuda-gencode arch=compute_70,code=sm_70 
  
  cd Linux-POWER-xlC
  
  make 
  
  # Careful, do not cut and paste.  The "-" of <<- removes only tabs, not spaces
  #          If you must cut and space, remove "-" and put EOF in column 1
  #          Also, 'EOF' does not do any variable substitution ($'s remain $'s)
  cat <<-'EOF' > runscript
  #!/bin/csh -f
  # Taken from Jim Phillips, jim@ks.uiuc.edu.  
  #
  setenv LD_LIBRARY_PATH "${1:h}:$LD_LIBRARY_PATH"
  setenv LD_PRELOAD "/opt/ibm/spectrum_mpi/lib/pami_451/libpami.so"
  exec $*
  EOF
  
  
  cat <<'EOF' > mpiexec
  #!/bin/csh -f
  # Taken from Jim Phillips, jim@ks.uiuc.edu.  
  shift
  shift
  exec ibrun $*
  EOF
  
  chmod 755 runscript mpiexec

  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

  cp -p bin/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
  cp -r lib   $RPM_BUILD_ROOT/%{INSTALL_DIR}
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


Note: In most cases, once task per node is recommended. gtx queue 
should be used. 

#!/bin/bash
#SBATCH -J test   # Job Name
#SBATCH -o test.o%j
#SBATCH -N 2      # Total number of nodes
#SBATCH -n 2      # Total number of mpi tasks
#SBATCH -p gtx    # Queue name
#SBATCH -t 24:00:00 # Run time (hh:mm:ss) - 24 hours

run_namd_gpu namd_inpu output

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
setenv( "TACC_%{MODULE_VAR}_DIR",                namd_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(namd_dir, "bin"))
add_property("arch","gpu")

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
