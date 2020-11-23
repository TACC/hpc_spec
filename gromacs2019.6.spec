#
# rpmbuild -bb --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_5' gromacs2019.4.spec 2>&1 | tee gromacs2019.4.spec_ic+im1905#_r1_a.log
# rpmbuild -bb --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_5' gromacs2019.6_gpu.spec 2>&1 | tee gromacs2019.6.log
# rpmbuild -bb --define "is_gcc73 1" --define "is_python 0" gromacs2019.6.spec 2>&1 | tee gromacs2019.6.log
# r=/admin/build/admin/rpms/frontera/RPMS/x86_64
#rpm -hiv --nodeps --relocate /tmprpm=/opt/apps    $r/tacc-gromacs-intel19-impi19_0-package-2019.4-2.el7.x86_64.rpm
#rpm -hiv --nodeps --relocate /tmpmod=/opt/apps $r/tacc-gromacs-intel19-impi19_0-modulefile-2019.4-2.el7.x86_64.rpm

#rpm -e tacc-gromacs-intel19-impi19_0-package-2019.4-1.el7.x86_64
#rpm -e tacc-gromacs-intel19-impi19_0-modulefile-2019.4-1.el7.x86_64

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

Summary: A Nice little relocatable skeleton spec file for Gromacs.

# Give the package a base name
%define pkg_base_name gromacs
%define MODULE_VAR    GROMACS_GPU
%define name_prefix tacc
# Create some macros (spec file variables)
%define major_version 2019
%define minor_version 6

%define pkg_version %{major_version}.%{minor_version}
%define dbg %{nil}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc

#%include mpi-defines.inc

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
BuildRoot: /var/tmp/%{pkg_base_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   GPL
Group:     Development/Tools
Group:     Applications/Biology
URL: http://www.gromacs.org
Packager:  TACC - alu@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE} 
Summary: Gromacs local binary install
Group: Applications/Biology

%description package
GROMACS is a versatile and extremely well optimized package
to perform molecular dynamics computer simulations and
subsequent trajectory analysis. It is developed for
biomolecules like proteins, but the extremely high
performance means it is used also in several other fields
like polymer chemistry and solid state physics. This
version has the dynamic libs and executables; to hack new
utility programs you also need the headers and static
libs in gromacs-dev.


%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
GROMACS is a versatile and extremely well optimized package
to perform molecular dynamics computer simulations and
subsequent trajectory analysis.

%description
GROMACS is a versatile and extremely well optimized package
to perform molecular dynamics computer simulations and
subsequent trajectory analysis. It is developed for
biomolecules like proteins, but the extremely high
performance means it is used also in several other fields
like polymer chemistry and solid state physics. This
version has the dynamic libs and executables; to hack new
utility programs you also need the headers and static
libs in gromacs-dev.


#---------------------------------------
%prep
#---------------------------------------
#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -q -n %{pkg_base_name}-%{pkg_version}
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
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

#%include mpi-load.inc

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
  
  # Create some dummy directories and files for fun
 
#####################################################################################

module load gcc/7.3.0
module load openmpi/3.1.2
module load cmake

# Build g_single_serial

rm -rf g_single_serial
mkdir g_single_serial
cd g_single_serial

env CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX=../install \
                            -DGMX_X11=OFF \
                            -DBUILD_SHARED_LIBS=OFF \
                            -DGMX_PREFER_STATIC_LIBS=ON \
                            -DGMX_BUILD_MDRUN_ONLY=OFF \
                            -DGMX_MPI=OFF \
                            -DGMX_OPENMP=OFF \
                            -DGMX_XML=OFF \
                            -DGMX_OPENMP_MAX_THREADS=256 \
                            -DCMAKE_C_FLAGS="-O3 -g " \
                            -DCMAKE_CXX_FLAGS="-O3 -g " \
                            -DGMX_DEFAULT_SUFFIX=ON \
                            -DGMX_BUILD_SHARED_EXE=OFF \
                            -DGMX_EXTERNAL_BOOST=OFF \
                            -DGMX_BUILD_OWN_FFTW=ON

make -j8
make install

# Build g_single_parallel

cd ..
rm -rf g_single_parallel
mkdir g_single_parallel
cd g_single_parallel

env CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX=../install \
                            -DGMX_X11=OFF \
                            -DBUILD_SHARED_LIBS=OFF \
                            -DGMX_PREFER_STATIC_LIBS=ON \
                            -DGMX_BUILD_MDRUN_ONLY=ON \
                            -DGMX_MPI=ON \
                            -DGMX_OPENMP=ON \
                            -DGMX_XML=OFF \
                            -DGMX_OPENMP_MAX_THREADS=256 \
                            -DCMAKE_C_FLAGS="-O3 -g " \
                            -DCMAKE_CXX_FLAGS="-O3 -g " \
                            -DGMX_DEFAULT_SUFFIX=OFF \
                            -DGMX_BUILD_SHARED_EXE=OFF \
                            -DGMX_EXTERNAL_BOOST=OFF \
                            -DGMX_BUILD_OWN_FFTW=ON \
                            -DGMX_BINARY_SUFFIX=_mpi

make -j8
make install

# Build g_double_parallel

cd ../
rm -rf g_double_parallel
mkdir g_double_parallel
cd g_double_parallel

env CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX=../install \
                            -DGMX_X11=OFF \
                            -DBUILD_SHARED_LIBS=OFF \
                            -DGMX_PREFER_STATIC_LIBS=ON \
                            -DGMX_BUILD_MDRUN_ONLY=ON \
                            -DGMX_MPI=ON -DGMX_OPENMP=ON \
                            -DGMX_XML=OFF \
                            -DGMX_SOFTWARE_INVSQRT=OFF \
                            -DGMX_SKIP_DEFAULT_CFLAGS=ON \
                            -DGMX_OPENMP_MAX_THREADS=256
                            -DCMAKE_C_FLAGS="-O3 -g " \
                            -DCMAKE_CXX_FLAGS="-O3 -g " \
                            -DGMX_DEFAULT_SUFFIX=OFF \
                            -DGMX_BUILD_SHARED_EXE=OFF \
                            -DGMX_EXTERNAL_BOOST=OFF \
                            -DGMX_BUILD_OWN_FFTW=ON \
                            -DGMX_DOUBLE=ON \
                            -DGMX_BINARY_SUFFIX=_mpi_d \
                            -DGMX_LIBS_SUFFIX=_mpi_d

make -j8
make install

# GPU-MPI

cd ../
rm -rf g_gpu_parallel
mkdir g_gpu_parallel
cd g_gpu_parallel

module load cuda/10.2

env CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX=../install  \
                            -DGMX_X11=OFF \
                            -DBUILD_SHARED_LIBS=OFF \
                            -DGMX_PREFER_STATIC_LIBS=ON \
                            -DGMX_BUILD_MDRUN_ONLY=ON \
                            -DGMX_MPI=ON \
                            -DGMX_OPENMP=ON \
                            -DGMX_XML=OFF \
                            -DGMX_OPENMP_MAX_THREADS=256 \
                            -DCMAKE_C_FLAGS="-O3 -g " \
                            -DCMAKE_CXX_FLAGS="-O3 -g " \
                            -DGMX_DEFAULT_SUFFIX=ON \
                            -DGMX_EXTERNAL_BOOST=OFF \
                            -DGMX_BUILD_SHARED_EXE=OFF \
                            -DGMX_GPU=ON \
                            -DGMX_BUILD_OWN_FFTW=ON \
                            -DGMX_DEFAULT_SUFFIX=OFF \
                            -DGMX_BINARY_SUFFIX=_mpi_gpu \
                            -DGMX_LIBS_SUFFIX=_mpi_gpu
make -j8
make install
cd ..

###############################################################################

##############################################################################

  # Copy everything from tarball over to the installation directory
  cp -r install/* $RPM_BUILD_ROOT/%{INSTALL_DIR}
  rm -rf install/*
#  rm -rf /admin/rpms/BUILD/gromacs*
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

You will need to load gcc/7.3.0 and openmpi/3.1.2 to run this %{name} module.

The %{name} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN, TACC_%{MODULE_VAR}_DOC, TACC_%{MODULE_VAR}_LIB, and
TACC_%{MODULE_VAR}_INC for the location of the %{name} distribution, binaries,
documentation, libraries, and include files, respectively. Also, GMXLIB has been
set to the topology-file directory in %{INSTALL_DIR}/share/gromacs/top.

The parallel component of gromacs is the molecular dynamics engine, mdrun_mpi.
It can be invoked in a job script:

 E.g. (Run 16 MPI tasks on 4 nodes, with 4 tasks/node and 4 threads/task)

 #SBATCH -N 4  # Total # of nodes
 #SBATCH -n 16 # Total # of mpi tasks

 module load gcc/7.3.0 
 module load openmpi/3.1.2 

 srun -N 4 -n 16 --ntasks-per-node=4 hostname | grep edu > myhostlist
 mpirun -np 16 -hostfile myhostlist mdrun_mpi -ntomp 4 -s topol.tpr -o traj.trr -c confout.gro -e ener.edr -g md.log

The topology file topol.tpr, mdout.md, and deshuf.ndx should be generated with the
grompp command:

  grompp ... -po mdout.mdp -deshuf deshuf.ndx -o topol.tpr

TACC also provides a double-precision version of the mdrun application,
called mdrun_mpi_d.  To use the double-precision version, simply replace
mdrun_mpi in the commands above with mdrun_mpi_d.

In addition, TACC provides GPU enabled version of mdrun with the suffix of _gpu. 
You must load cuda/10.2 before running mdrun_mpi_gpu:

 E.g. (16 MPI tasks on 4 V100 GPU nodes, with 4 tasks/node, 4 threads/task, and 4 GPUs/node)

 #SBATCH -p v100 # Queue name
 #SBATCH -N 4    # Total # of nodes
 #SBATCH -n 16   # Total # of mpi tasks

 module load gcc/7.3.0 
 module load openmpi/3.1.2 
 module load cuda/10.2 

 srun -N 4 -n 16 --ntasks-per-node=4 hostname | grep edu > myhostlist
 mpirun -np 16 -hostfile myhostlist mdrun_mpi_gpu -ntomp 4 -s topol.tpr -o traj.trr -c confout.gro -e ener.edr -gpu_id 0123 

To use the %{pkg_base_name} libraries, compile the source code with the option:

 -I\$TACC_%{MODULE_VAR}_INC

and add the following options to the link step:

 -L\$TACC_%{MODULE_VAR}_LIB -l%{pkg_base_name}

Here is an example command to compile test.c:

   gcc -I\$TACC_%{MODULE_VAR}_INC test.c -L\$TACC_%{MODULE_VAR}_LIB -l%{pkg_base_name}

Version %{pkg_version}

]]



--help(help_msg)
help(help_msg)

whatis("Name: gromacs")

whatis("Version: %{pkg_base_name}")
whatis("Category: Application, Biology")
whatis("Keywords: Biology, Chemistry, Molecular Dynamics, Application")
whatis("URL: http://www.gromacs.org")
whatis("Description: molecular dynamics simulation package")

-- Prerequisites

-- Create environment variables.

local gromacs_dir   = "%{INSTALL_DIR}"

family("gromacs")
prepend_path(    "PATH",    pathJoin(gromacs_dir, "bin"))
prepend_path(  "LD_LIBRARY_PATH", pathJoin(gromacs_dir, "lib64"))
setenv( "TACC_%{MODULE_VAR}_DIR",                      gromacs_dir)
setenv( "TACC_%{MODULE_VAR}_INC", pathJoin(gromacs_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB", pathJoin(gromacs_dir, "lib64"))
setenv( "TACC_%{MODULE_VAR}_BIN", pathJoin(gromacs_dir, "bin"))

setenv("TACC_%{MODULE_VAR}_DOC",pathJoin(gromacs_dir,"share"))
setenv("GMXLIB",pathJoin(gromacs_dir,"share/gromacs/top"))
append_path("MANPATH",pathJoin(gromacs_dir,"share/man"))
append_path("PKG_CONFIG_PATH",pathJoin(gromacs_dir,"lib/pkgconfig"))

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

