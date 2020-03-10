################################################################
#
#    LAMMPS SPEC FILE
#
#    MACHINE       :   TACC LONESTAR 5
#    VERSION       :   9 Jan 2020
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   1-24-2020
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
# ./build_rpm.sh -l -i18 -c7_7_3 lammps_9Jan20_ls5_v1.spec

%define pkg_base_name lammps
%define MODULE_VAR    LAMMPS 

%define major_version 9Jan20
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}

################################################################

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc

################################################################

Summary:   LAMMPS is a Classical Molecular Dynamics package.
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   1%{?dist}
License:   GPL
Vendor:    Sandia
Group:     applications/chemistry
URL:       http://lammps.sandia.gov
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Packager:  TACC Albert Lu - alu@tacc.utexas.edu
%define    buildroot   /var/tmp/%{name}-%{version}-buildroot

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

# External packages
%define    vorover  0.4.6

################################################################

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
LAMMPS Molecular Dynamics package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
LAMMPS Molecular Dynamics modulefile.

# Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
LAMMPS is a classical molecular dynamics code with the following functionality: 
It can be run on a single processor or in parallel.  
It is written in highly portable C++.  
It is easy to extend with new features and functionality.
It has a syntax for defining and using variables and formulas, 
as well as a syntax for looping over runs and breaking out of loops.

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

  unset MODULEPATH
  if [ -f "$BASH_ENV" ]; then
    . $BASH_ENV
    module purge
    clearMT
    MP="/opt/apps/tools/modulefiles:/opt/apps/modulefiles:/opt/apps/intel18/modulefiles/"

    if [ -z "$MODULEPATH" ]; then
     export MODULEPATH=$(/opt/apps/lmod/lmod/libexec/addto --append MODULEPATH ${MP//:/ })
    fi
  fi

  module --ignore-cache load %{comp_module}
  module --ignore-cache load %{mpi_module}

  module load python3
  module load hdf5
  module load netcdf
  module load cuda
  module load cmake
  module load eigen

  set -x

  #----------------------------#
  #                            #
  #      Build libraries       #
  #                            #
  #----------------------------#

  echo "Working on libraries ......."

  mkliblist=()

  # List of additional library to be installed
  liblist="atc awpmd colvars compress gpu h5md      linalg      netcdf poems python      smd voronoi"
  #liblist="atc awpmd colvars compress gpu h5md kim linalg meam netcdf poems python quip smd voronoi"

  cd src
  
  make yes-all
  make no-ext
  make no-reax
  make no-kokkos
  make no-kim
  make no-message
  make no-user-scafacos

  if [[ ! $liblist =~ "atc"      ]]; then make no-user-atc     ; fi
  if [[ ! $liblist =~ "awpmd"    ]]; then make no-user-awpmd   ; fi
  if [[ ! $liblist =~ "colvars"  ]]; then make no-user-colvars ; fi
  if [[ ! $liblist =~ "compress" ]]; then make no-compress     ; fi
  if [[ ! $liblist =~ "gpu"      ]]; then make no-gpu          ; fi
  if [[ ! $liblist =~ "latte"    ]]; then make no-latte        ; fi
  if [[ ! $liblist =~ "meam"     ]]; then make no-meam         ; fi
  if [[ ! $liblist =~ "poems"    ]]; then make no-poems        ; fi
  if [[ ! $liblist =~ "python"   ]]; then make no-python       ; fi

  # External libraries required
  if [[ $liblist =~ "gpu"       ]]; then make yes-gpu          ; fi
  if [[ $liblist =~ "h5md"      ]]; then make yes-user-h5md    ; fi
  if [[ $liblist =~ "kim"       ]]; then make yes-kim          ; fi
  if [[ $liblist =~ "latte"     ]]; then make yes-latte        ; fi
  if [[ $liblist =~ "quip"      ]]; then make yes-user-quip    ; fi
  if [[ $liblist =~ "netcdf"    ]]; then make yes-user-netcdf  ; fi
  if [[ $liblist =~ "smd"       ]]; then make yes-user-smd     ; fi
  if [[ $liblist =~ "voronoi"   ]]; then make yes-voronoi      ; fi

  make package-status

  cd ..

  # Building Packages

  # atc

  if [[ $liblist =~ "atc" ]]; then

    echo "Working on atc ..."
    cd lib/atc
    make -j 4 -f Makefile.icc \
    CC="mpicxx"  LINK="mpicxx"
    
    # use lammps linalg library
    cp Makefile.lammps.linalg Makefile.lammps
    cd ../..
  fi

  # awpmd

  if [[ $liblist =~ "awpmd" ]]; then

    echo "Working on awpmd ..."
    cd lib/awpmd
    make -j 4 -f Makefile.mpicc \
    CC="mpicxx" 
    
    # use lammps linalg library 
    cp Makefile.lammps.linalg Makefile.lammps
    cd ../..
  fi

  # colvars

  if [[ $liblist =~ "colvars" ]]; then

    echo "Working on colvars ..."
    cd lib/colvars
    make -j 4 -f Makefile.mpi

cat > Makefile.lammps <<EOF
      colvars_SYSINC =  -I../../lib/colvars
      colvars_SYSLIB =  -lcolvars
      colvars_SYSPATH = -L../../lib/colvars
EOF
    cd ../..
  fi

  # gpu

  if [[ $liblist =~ "gpu" ]]; then

    echo "Working on gpu ..."
    cd lib/gpu
    export CUDA_HOME=${TACC_CUDA_DIR}
    sed -i 's/lib64/lib64 -L$(CUDA_HOME)\/lib64\/stubs/g' Makefile.lammps.standard
    make -f Makefile.mpi CUDA_ARCH="-arch=sm_35" CUDA_LIB="-L${CUDA_HOME}/lib64 -L${CUDA_HOME}/lib64/stubs"
    cd ../..    
  fi

  # h5md

  if [[ $liblist =~ "h5md" ]]; then

    echo "Working on h5md ..."
    cd lib/h5md
    make -f Makefile.h5cc CFLAGS="-xAVX -axCORE-AVX2 -D_DEFAULT_SOURCE -O2 -DH5_NO_DEPRECATED_SYMBOLS -Wall -fPIC" HDF5_PATH="${TACC_HDF5_DIR}"

# Must make lammps at end, otherwise it is overwritten by make (above)
cat >Makefile.lammps <<EOF
       h5md_SYSINC  = -I${TACC_HDF5_INC} -I../../lib/h5md/include
       h5md_SYSLIB  = -lhdf5 -lch5md
       h5md_SYSPATH = -L${TACC_HDF5_LIB} -L../../lib/h5md
EOF
    cd ../..
  fi

  # linalg (needed by atc and awpmd)

  if [[ $liblist =~ "linalg" ]]; then

    echo "Working on linalg ..."
    cd lib/linalg
    make -f Makefile.mpi FC="mpif90"
    cd ../..
  fi        

  # netcdf

  if [[ $liblist =~ "netcdf" ]]; then

    echo "Working on netcdf ..."
    cd lib/netcdf

cat > Makefile.lammps <<EOF
    netcdf_SYSINC = -DLMP_HAS_NETCDF $(nc-config --cflags)
    netcdf_SYSLIB = $(nc-config --libs)
    netcdf_SYSPATH = $(nc-config --cflags) -L$(which ncdump | sed -e 's,bin/ncdump,,')/lib
EOF
    cp Makefile.lammps ../../src/USER-NETCDF
    cd ../..
  fi

  # python

  if [[ $liblist =~ python ]]; then

    echo "Working on python ..."
    cd lib/python
    cp Makefile.lammps.python3 Makefile.lammps
    cd ../..
  fi

  # poems

  if [[ $liblist =~ "poems" ]]; then

    echo "Working on poems ..."
    cd lib/poems
    make -j 4 -f Makefile.icc CC="mpicxx" LINK="mpicxx" 
    cd ../..
  fi

  # smd

  if [[ $liblist =~ "smd" ]]; then

    echo "Working on smd ..."
    cd lib/smd
    ln -s ${TACC_EIGEN_INC} includelink

cat > Makefile.lammps <<EOF
user-smd_SYSINC  = -I../../lib/smd/includelink
user-smd_SYSLIB  =
user-smd_SYSPATH =
EOF
    cd ../..
  fi

  # voronoi

  if [[ $liblist =~ "voronoi" ]]; then

    echo "Working on voronoi ..."

    # voronoi library source code
    cd lib/voronoi/src/voro++-%{vorover}

    make -j 4 CXX="mpicxx" CFLAGS="-g -fPIC -ansi -pedantic"

    rm -rf examples
    rm -rf html

    cd ../..

    ln -s src/voro++-%{vorover}/src includelink
    ln -s src/voro++-%{vorover}/src liblink 

    cd ../../
  fi

  #----------------------------#
  #                            #
  #        Build LAMMPS        #
  #                            #
  #----------------------------#
        
  cd src

  # Make lammmps (use src/MAKE/MACHINES/Makefile.lonestar)

  cat MAKE/OPTIONS/Makefile.intel_cpu_mpich | sed 's/-xHost/-xAVX -axCORE-AVX2/g' | sed 's/-cxx=icc//g' | sed 's/-restrict/-restrict -diag-disable=cpu-dispatch/g'> MAKE/MACHINES/Makefile.lonestar

  make -j 10 lonestar \
             LMP_INC="-DLAMMPS_GZIP -DLAMMPS_JPEG -DLAMMPS_FFMPEG -DLAMMPS_EXCEPTIONS" \
             MPI_INC="-DMPICH_SKIP_MPICXX -DOMPI_SKIP_MPICXX=1 -I${TACC_CRAY_PMI_INC}" \
             MPI_PATH="-L${TACC_CRAY_PMI_LIB}" \
             MPI_LIB="-lmpich -lmpl -lpthread" \
             FFT_INC="-DFFT_MKL -DFFT_SINGLE" \
             FFT_LIB="-lmkl_intel_lp64 -lmkl_sequential -lmkl_core" \
             JPG_INC="-I/usr/lib64" \
             JPG_PATH="-L/usr/lib64" \
             JPG_LIB="-ljpeg"

   mv lmp_lonestar lmp_gpu

   make no-gpu

   make -j 10 lonestar \
              LMP_INC="-DLAMMPS_GZIP -DLAMMPS_JPEG -DLAMMPS_FFMPEG -DLAMMPS_EXCEPTIONS" \
              MPI_INC="-DMPICH_SKIP_MPICXX -DOMPI_SKIP_MPICXX=1 -I${TACC_CRAY_PMI_INC}" \
              MPI_PATH="-L${TACC_CRAY_PMI_LIB}" \
              MPI_LIB="-lmpich -lmpl -lpthread" \
              FFT_INC="-DFFT_MKL -DFFT_SINGLE" \
              FFT_LIB="-lmkl_intel_lp64 -lmkl_sequential -lmkl_core" \
              JPG_INC="-I/usr/lib64" \
              JPG_PATH="-L/usr/lib64" \
              JPG_LIB="-ljpeg"

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"
 
# INSTALL LAMMPS

%if %{?BUILD_PACKAGE}

  lmp_build_dir=`pwd`

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  
  # cleanup lib directories
  rm -rf lib/kokkos lib/molfile lib/mscg
  rm -rf lib/qmmm lib/reax lib/vtk
  rm -rf lib/kim lib/message

  # cleanup tools and lib directories

  find lib -name \*\*.o   -exec rm {} \;
  find lib -name \*\*.c   -exec rm {} \;
  find lib -name \*\*.cpp -exec rm {} \;
  find lib -name \*\*.f   -exec rm {} \;
  find lib -name \*\*.f90 -exec rm {} \;
  find lib -name \*\*.py  -exec rm {} \;
  find lib -name \*\*.cu  -exec rm {} \;
  find lib -name \*\*.blk -exec rm {} \;

  # cleanup obj files
  rm -rf src/Obj_lonestar

  mkdir                           $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mv src/lmp_lonestar             $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mv src/lmp_gpu                  $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

  cp -pR lib             $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  cp -pR potentials      $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials
  cp -pR python          $RPM_BUILD_ROOT/%{INSTALL_DIR}/python
  cp -pR src             $RPM_BUILD_ROOT/%{INSTALL_DIR}/src  
  
  chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*

%endif # BUILD_PACKAGE

################################################################

%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua <<EOF
local help_message = [[
LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator) 
is a classical molecular dynamics code developed at Sandia 
National Laboratories. 

- TO RUN LAMMPS

  Set the number of nodes (N) and MPI tasks (n) in the job script.

    E.g. One node with two MPI tasks 

    #SBATCH -N 1
    #SBATCH -n 2

  Load required modules

    module load intel/18.0.2
    module load cray_mpich/7.7.3
    module load lammps/%{major_version}

  Run LAMMPS program

    * Basic
      
      ibrun lmp_lonestar -in lammps_input

    * Use USER-OMP package (E.g. with 2 omp threads)

      ibrun lmp_lonestar -sf omp -pk omp 2 -in lammps_input

    * Use USER-INTEL package (E.g. with 2 omp threads)
      
      ibrun lmp_lonestar -sf intel -pk intel 0 omp 2 -in lammps_input

    * Use USER-INTEL package

      #SBATCH -p gpu
      ibrun lmp_gpu -sf gpu -pk gpu 1 -in lammps_input 
    
- ENVIRONMENT VARIABLES 
      
  The LAMMPS modulefile defines the following environment 
  variables (with the prefix "TACC_LAMMPS_"):

    TACC_LAMMPS_DIR/BIN/LIB/POT/PYTH/SRC

  for the location of the LAMMPS home, binaries, libraries, potentials, 
  python scripts and source code respectively. The modulefile also appends 
  TACC_LAMMPS_BIN to PATH.

- PACKAGES

  The following packages were not installed:

    KIM, KOKKOS, LATTE, MESSAGE, MSCG, REAX, USER-ADIOS, USER-MOLFILE,
    USER-PLUMED, USER-QMMM, USER-QUIP, USER-SCAFACOS, USER-VTK

  Use command 'ibrun lmp_lonestar -h' (in idev mode) to list all supported functions

  Information of external library:

    * VORONOI  
      voro++-%{vorover}
      http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz

- REFERENCE

  LAMMPS website: http://lammps.sandia.gov
  LAMMPS at TACC: https://portal.tacc.utexas.edu/software/lammps     

Version %{version}
]]

help(help_message,"\n")

whatis("Name: LAMMPS")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Biology, Molecular Dynamics, Application")
whatis("URL:  http://lammps.sandia.gov/index.html")
whatis("Description: Molecular Dynamics Chemistry Package")

local lmp_dir="%{INSTALL_DIR}"

setenv("TACC_LAMMPS_DIR"       ,lmp_dir)
setenv("TACC_LAMMPS_BIN"       ,pathJoin(lmp_dir,"bin"))
setenv("TACC_LAMMPS_LIB"       ,pathJoin(lmp_dir,"lib"))
setenv("TACC_LAMMPS_POT"       ,pathJoin(lmp_dir,"potentials"))
setenv("TACC_LAMMPS_SRC"       ,pathJoin(lmp_dir,"src"))

load("cuda")
load("hdf5")
load("netcdf/4.3.3.1")
load("python3")
load("eigen")

append_path("PATH",pathJoin(lmp_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} <<EOF
#%Module3.1.1#################################################
##
## version file for lammps
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

# -----------------------------------------

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
#rm -rf $RPM_BUILD_ROOT

################################################################
