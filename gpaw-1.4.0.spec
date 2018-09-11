################################################################
#
#    GPAW SPEC FILE
#
#    MACHINE       :   TACC STAMPEDE2
#    VERSION       :   1.4.0
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   08-09-2018
#
################################################################

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
#
# rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1'  gpaw-1.4.0.spec | tee log_gpaw_1.4.0
#

%define pkg_base_name gpaw
%define MODULE_VAR    GPAW

%define major_version 1
%define minor_version 4
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

################################################################

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc

################################################################

Summary:   GPAW is a density-functional theory (DFT) Python code based on the projector-augmented wave (PAW) method and the atomic simulation environment (ASE).
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   1%{?dist}
License:   GNU General Public License
Vendor:    https://wiki.fysik.dtu.dk/gpaw/index.html
Group:     applications/chemistry
URL:       https://wiki.fysik.dtu.dk/gpaw/index.html
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Packager:  TACC Albert Lu - alu@tacc.utexas.edu

%define    buildroot   /var/tmp/%{name}-%{version}-buildroot
%define    gpaw_src     %{pkg_base_name}-%{pkg_version}

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

################################################################

%package %{PACKAGE}
Summary: The package RPM
Group: applications/chemistry
%description package
Gpaw package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Gpaw modulefile.

# Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
GPAW is a density-functional theory (DFT) Python code based on the 
projector-augmented wave (PAW) method and the atomic simulation environment (ASE).

################################################################

%prep

%if %{?BUILD_PACKAGE}

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -q -n %{pkg_base_name}-%{pkg_version}

%endif # BUILD_PACKAGE 

%if %{?BUILD_MODULEFILE}

  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif # BUILD_MODULEFILE 

################################################################

%build

%if %{?BUILD_PACKAGE}

  set +x
  %include system-load.inc
  %include compiler-load.inc
  %include mpi-load.inc
  set -x

  build_dir=`pwd`

  cd ./libxc

  ./configure --enable-shared --disable-fortran CC=icc CFLAGS="-O3 -fp-model strict -unroll -ip -qopenmp -mkl" --prefix=${build_dir}
  make
  make install

  module load cmake
  module load python3/3.6.3

  mkdir -p ../lib/python3.6/site-packages/
  cd ../lib/python3.6/site-packages/
  export PYTHONPATH=`pwd`:$PYTHONPATH
  cd -

  export CMAKE_C_COMPILER="icc"
  export CMAKE_C_FLAGS="-O3 -fp-model strict -unroll -ip -qopenmp -mkl"
  export CMAKE_INSTALL_PREFIX=${build_dir}
  python3 setup.py install --prefix=${build_dir}

  cd ..

  cd ./libvdwxc

  ml fftw3

  ./configure --enable-shared  CC="icc" FC="ifort" MPICC="mpiicc" MPIFC="mpiifort" CFLAGS="-O3 -fp-model strict -unroll -ip -qopenmp -mkl" FCFLAGS="-O3 -fp-model strict -unroll -ip"  --with-fftw3=$TACC_FFTW3_DIR --prefix=${build_dir}
  make
  make install

  cd ..


  cd ./gpaw

  python3 setup.py install --prefix=${build_dir}

  cd ${build_dir}/bin

for i in {gpaw,gpaw-analyse-basis};do echo $i;sed 's/\/env\ python/\/env\ python3/' $i> tmp_$i;done

  for i in {gpaw,gpaw-analyse-basis,gpaw-basis,gpaw-mpisim,gpaw-plot-parallel-timings,gpaw-setup,gpaw-upfplot}; do

    sed 's/\/env\ python/\/env\ python3/' $i > tmp;
    mv tmp $i;
  done

  cd ../

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

# INSTALL GPAW

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  # install gpaw
  cp -r ./bin     $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r ./lib     $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r ./include $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r ./ase     $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r ./gpaw-setups-0.9.20000 $RPM_BUILD_ROOT/%{INSTALL_DIR}

  #chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*

%endif # BUILD_PACKAGE

################################################################

%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua <<EOF
local help_message = [[
GPAW is a density-functional theory (DFT) Python code based on the 
projector-augmented wave (PAW) method and the atomic simulation 
environment (ASE). The wave functions can be described with:

  * Plane-waves (pw)
  * Real-space uniform grids, multigrid methods and the finite-difference approximation (fd)
  * Atom-centered basis-functions (lcao)

- To run GPAW program, use the following lines in the job script. 
  Vary the "-N" and "-n" directives base on your need.

     #SBATCH -N 1          # E.g. requesting 1 node
     #SBATCH -n 16         #      and 16 MPI tasks

     module load gpaw

     gpaw script.py               (serial)

     or

     ibrun gpaw-python script.py  (parallel)

- ENVIRONMENT VARIABLES 
      
  The GPAW module defines a set of environment variables for the locations of the 
  GPAW home, binaries, libraries and more with the prefix "TACC_GPAW_"
  Use the "env" command to display the variables:

      $ env | grep "TACC_GPAW"

- DATABASE and EXTERNAL LIBRARIES

  * Atomic PAW Setups
    gpaw-setups-0.9.20000 is located in the directory \$GPAW_SETUP_PATH
    https://wiki.fysik.dtu.dk/gpaw/setups/setups.html    

  * LIBXC (%{VERSION_XC})
    http://www.tddft.org/programs/libxc/

  * LIBVDWXC (%{VERSION_VDW})
    https://libvdwxc.org/

  * FFTW3 (3.3.6)
    http://www.fftw.org/

  * BLAS/BLACS/LAPACK/ScaLAPACK/Intel MKL (2017.4.196)

- REFERENCE
      
  Gpaw website: https://wiki.fysik.dtu.dk/gpaw

  Version %{version}
]]

help(help_message,"\n")

whatis("Name: Gpaw")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Quantum, DFT, Application")
whatis("URL:  https://wiki.fysik.dtu.dk/gpaw")
whatis("Description: GPAW is a density-functional theory (DFT) Python code")

local gpaw_dir="%{INSTALL_DIR}"

setenv("TACC_GPAW_DIR"              ,gpaw_dir)
setenv("TACC_GPAW_BIN"              ,pathJoin(gpaw_dir,"bin"))
setenv("TACC_GPAW_LIB"              ,pathJoin(gpaw_dir,"lib"))
setenv("TACC_GPAW_INC"              ,pathJoin(gpaw_dir,"include"))
setenv("GPAW_SETUP_PATH"            ,pathJoin(gpaw_dir,"gpaw-setups-0.9.20000"))

load("fftw3/3.3.6")
load("python3/3.6.3")

append_path("PATH",pathJoin(gpaw_dir,"bin"))
append_path("PATH",pathJoin(gpaw_dir,"ase/tools"))
prepend_path("PYTHONPATH",pathJoin(gpaw_dir,"lib"))
prepend_path("PYTHONPATH",pathJoin(gpaw_dir,"lib/python3.6/site-packages/"))
prepend_path("PYTHONPATH",pathJoin(gpaw_dir,"lib/python3.6/site-packages/pylibxc-4.2.3-py3.6-linux-x86_64.egg/"))
prepend_path("PYTHONPATH",pathJoin(gpaw_dir,"ase"))
prepend_path("LD_LIBRARY_PATH",pathJoin(gpaw_dir,"lib"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} <<EOF
#%Module3.1.1#################################################
##
## version file for GPAW
##
    
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%endif # BUILD_MODULEFILE

################################################################

%if %{?BUILD_PACKAGE}
%files package
  %defattr(775,root,install,775)
  %{INSTALL_DIR}
%endif # BUILD_PACKAGE |

%if %{?BUILD_MODULEFILE}
%files modulefile 
  %defattr(775,root,install,775)
  %{MODULE_DIR}
%endif # BUILD_MODULEFILE |

################################################################

# Fix Modulefile During Post Install

%post %{PACKAGE}

export PACKAGE_POST=1

%include post-defines.inc

%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc

%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc

################################################################

%clean
rm -rf $RPM_BUILD_ROOT

################################################################
