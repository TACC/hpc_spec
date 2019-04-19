################################################################
#
#    LAMMPS SPEC FILE
#
#    MACHINE       :   TACC LONESTAR 5
#    VERSION       :   12 DEC 2018
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   4-4-2019
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
# ./build_rpm.sh -l -i18 -c7_7_3 lammps_12Dec18_ls5_v1.spec

%define pkg_base_name lammps
%define MODULE_VAR    LAMMPS 

%define major_version 12Dec18
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
Packager:  TACC Albert Lu- alu@tacc.utexas.edu

%define    lmp_src_dir  /work/apps/lammps/lmp_src/%{version}
%define    buildroot   /var/tmp/%{name}-%{version}-buildroot

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

# External packages
%define    kimver   1.9.6
%define    vorover  0.4.6
%define    eigenver 3.3.4
%define    kim_src  kim-api-v%{kimver}

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

  set -x

  #----------------------------#
  #                            #
  #       Make the tools       #
  #                            #
  #----------------------------#

  # NOT included : eff, moltemplate, phonon, pymol_asphere, reax, smd, xmgrace

  echo "Working on tools ......."
  cd tools

  if [ 1 = 1 ]; then

    rm -rf *.o

    # binary2txt
    echo "Working on binary2txt ..."
    icpc binary2txt.cpp -o binary2txt 

    # chain
    echo "Working on chain ..."
    ifort chain.f -o chain

    # colvars
    echo "Working on colvars ..."
    cd colvars
    rm -rf *.o
    make CXX=icpc CXXFLAGS=-O2
    cd ..
    
    # createatoms
    echo "Working on createatoms ..."
    cd createatoms
    rm -rf *.o
    ifort createAtoms.f -o createAtoms
    cd ..

    # eam_database
    echo "Working on eam_database ..."
    cd eam_database
    rm -rf *.o
    ifort create.f -o create
    cd ..

    # eam_generate
    echo "Working on eam_generate ..."
    cd eam_generate
    rm -rf *.o
    icc Al_Zhou.c    -o Zl_Zhou
    icc Cu_Mishin1.c -o Mishin1
    icc Cu_Zhou.c    -o Cu_Zhou
    icc W_Zhou.c     -o W_Zhou
    cd ..

    # i-pi
    echo "Working on i-pi ..."
    cd i-pi/drivers
    rm -rf *.o
    ifort -O3 -c distance.f90 LJ.f90 SG.f90
    icc -c -o sockets.o sockets.c
    ifort -O3 -c driver.f90
    ifort -O3 -o driver.x distance.o driver.o LJ.o SG.o sockets.o
    cd ../..
    
    # lmp2arc
    echo "Working on lmp2arc ..."
    cd lmp2arc/src
    # See compiler warning. Changed gcc to icc -w0
    sed -i.bak 's/gcc/icc/' Makefile
    sed -i 's/-O2/-w0 -O2/' Makefile
    make
    chmod u+rwX,g+rwX,o=rX lmp2arc.exe
    mv lmp2arc.exe ..
    cd ../..

    # lmp2cfg
    echo "Working on lmp2cfg ..."
    cd lmp2cfg
    ifort lmp2cfg.f -o lmp2cf
    cd ..

    # micelle2d
    #echo "Working on micell2d ..."
    #ifort micelle2d.f -o micelle2d

    # msi2lmp
    echo "Working on msi2lmp ..."
    cd msi2lmp/src
    rm -rf *.o
    make CC=icc CFLAGS=-g
    cd ../..

    # clean up
    find . -name \*\.o -exec rm {} \; 

    # remove examples and tests
    rm -rf ./amber2lmp
    rm -rf ./ch2lmp
    rm -rf ./eff
    rm -rf ./lmp2arc/test
    rm -rf ./lmp2cfg/examples
    rm -rf ./moltemplate
    rm -rf ./msi2lmp/test
    rm -rf ./phonon
    rm -rf ./pymol_asphere
    rm -rf ./reax
    rm -rf ./smd
    rm -rf ./xmgrace

  fi  # END OF TOOLS

  cd ..

  #----------------------------#
  #                            #
  #      Build libraries       #
  #                            #
  #----------------------------#

  echo "Working on libraries ......."

  mkliblist=()

  # List of additional library to be installed
  liblist="atc awpmd colvars compress      h5md    linalg meam netcdf poems        quip smd voronoi"
  #liblist="atc awpmd colvars compress gpu h5md kim linalg meam netcdf poems python quip smd voronoi"
  # Include all packages which don't need external libraries
  # Remove the packges that's not in the liblist

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
  #if [[ $liblist =~ "mscg"      ]]; then make yes-mscg         ; fi
  if [[ $liblist =~ "netcdf"    ]]; then make yes-user-netcdf  ; fi
  if [[ $liblist =~ "smd"       ]]; then make yes-user-smd     ; fi
  if [[ $liblist =~ "voronoi"   ]]; then make yes-voronoi      ; fi

  make package-status

  cd ..
  
  # FC flags (KNL-SKX fat binary)
  KNSX_FOPTS="-O2 -xAVX -axCORE-AVX2 -diag-disable=cpu-dispatch -fp-model precise -qno-offload -qoverride-limits -fno-alias -ansi-alias -no-prec-div"
  # CC flags (KNL-SKX fat binary)
  KNSX_OPTS="$KNSX_FOPTS -qopenmp -restrict"
  # CC flags for lammps
  KNSX_LOPTS="$KNSX_FOPTS -qopenmp -restrict -DLAMMPS_MEMALIGN=64 -DLMP_INTEL_USELRT -DLMP_USE_MKL_RNG"

  # atc

  if [[ $liblist =~ "atc" ]]; then

    echo "Working on atc ..."
    cd lib/atc

    make -j 4 -f Makefile.icc \
    CC="mpicxx"  LINK="mpicxx" \
    CCFLAGS="-g -fPIC $KNSX_OPTS  -I../../src -DMPICH_IGNORE_CXX_SEEK -diag-disable 858"
    
    # use lammps linalg library
    cp Makefile.lammps.linalg Makefile.lammps
    cp Makefile.lammps ../../src/USER-ATC
    cd ../..
  fi

  # awpmd

  if [[ $liblist =~ "awpmd" ]]; then

    echo "Working on awpmd ..."
    cd lib/awpmd

    make -j 4 -f Makefile.mpicc \
    CC="mpicxx" \
    CCFLAGS="-g -fPIC $KNSX_OPTS -Isystems/interact/TCP/ -Isystems/interact -Iivutils/include -DMPICH_IGNORE_CXX_SEEK -DOMPI_SKIP_MPICXX=1"
    
    # use lammps linalg library 
    cp Makefile.lammps.linalg Makefile.lammps
    cp Makefile.lammps ../../src/USER-AWPMD
    cd ../..
  fi

  # colvars

  if [[ $liblist =~ "colvars" ]]; then

    echo "Working on colvars ..."
    cd lib/colvars
        
    make -j 4 -f Makefile.g++ 
    #CXX="g++" \
    #CXXFLAGS="-g -O2 -fPIC -funroll-loops"

    cat > Makefile.lammps <<EOF
      colvars_SYSINC =  -I../../lib/colvars
      colvars_SYSLIB =  -lcolvars
      colvars_SYSPATH = -L../../lib/colvars
EOF
    
    cp Makefile.lammps  ../../src/USER-COLVARS
    cd ../..
  fi

  # compress

  if [[ $liblist =~ "compress" ]]; then
    
    echo "Working on compress ..."
    cd lib/compress

    cp Makefile.lammps  ../../src/COMPRESS
    cd ../..
  fi

  # gpu

  if [[ $liblist =~ "gpu" ]]; then

    echo "Working on gpu ..."
    cd lib/gpu
  
    #module load cuda/6.5
    module load cuda

    make -f Makefile.mpi
    cd ../..    
  fi

  # h5md

  if [[ $liblist =~ "h5md" ]]; then

    echo "Working on h5md ..."
    cd lib/h5md

    module load hdf5
    make -f Makefile.h5cc CFLAGS="-xAVX -axCORE-AVX2 -D_DEFAULT_SOURCE -O2 -DH5_NO_DEPRECATED_SYMBOLS -Wall -fPIC" HDF5_PATH="${TACC_HDF5_DIR}"

    # Must make lammps at end, otherwise it is overwritten by make (above)
    cat >Makefile.lammps <<EOF
       h5md_SYSINC  = -I${TACC_HDF5_INC} -I../../lib/h5md/include
       h5md_SYSLIB  = -lhdf5 -lch5md
       h5md_SYSPATH = -L${TACC_HDF5_LIB} -L../../lib/h5md
EOF

    module unload hdf5
    cp Makefile.lammps  ../../src/USER-H5MD
    cd ../..
  fi

  # kim

  if [[ $liblist =~ "kim" ]]; then

    ml gcc/7.3.0
    kim_build_dir=/opt/apps/gcc7_3/cray_mpich_7_7/kim/1.9.6/kim-api

    cd lib/kim

    tar -xf %{kim_src}.tar.gz
    mv %{kim_src} tmp
    mv ./tmp/* .
    rm -r ./tmp %{kim_src}.tar.gz

    cd ./kim_env_collection/models
    ${kim_build_dir}/bin/kim-api-v1-build-config --makefile-kim-config > ./Makefile.KIM_Config
    kim_model_dir=`pwd`

    cp -r ../../kim-api-v%{kimver}/examples/models/ex_* .

    for i in ex_*; do echo $i | sed 's/.txz//' >> models.txt; done

    cd ../model_drivers
    ${kim_build_dir}/bin/kim-api-v1-build-config --makefile-kim-config > ./Makefile.KIM_Config
    kim_driver_dir=`pwd`

    cp -r ../../kim-api-v%{kimver}/examples/model_drivers/ex_* .

    for i in ex_*; do echo $i | sed 's/.txz//' >> drivers.txt; done

    export KIM_API_MODELS_DIR=${kim_model_dir}
    export KIM_API_MODEL_DRIVERS_DIR=${kim_driver_dir}

    # Install drivers

    while read  mo; do
  
      echo $mo
      tar -xf "${mo}.txz"
      cd "${mo}"
      cmake -DKIM_API_INSTALL_COLLECTION=ENVIRONMENT
      make
      rm -rf *.o *.cpp *.hpp RE* LIC*
      cd ..
      rm "${mo}.txz"

    done < drivers.txt

    # Install models

    cd ../models

    while read  mo; do
  
      echo $mo
      tar -xf "${mo}.txz"
      cd "${mo}"
      cmake -DKIM_API_INSTALL_COLLECTION=ENVIRONMENT
      make
      rm -rf *.o RE* LIC*
      cd ..
      rm "${mo}.txz"

    done < models.txt

    cd ../../

cat > Makefile.KIM_DIR <<EOF
KIM_INSTALL_DIR=${kim_build_dir}

.DUMMY: print_dir

print_dir:
	@printf \$(KIM_INSTALL_DIR)
EOF

    cd ../../

    ml intel/18.0.2

  fi

  # latte

  if [[ $liblist =~ "latte" ]]; then

    echo "Working on latte ..."
    cd lib/latte

    module load gcc/7.3.0
    module load cmake
    module load mkl

    # build bml library
    # git clone https://github.com/lanl/bml.git

    echo "Building BML library ..."
    cd bml

    mkdir install build
    PWD=`pwd`
    CC=mpicc FC=mpif90 \
    BLAS_VENDOR=Intel \
    CMAKE_BUILD_TYPE=Release \
    BML_OPENMP=yes BML_MPI=yes \
    EXTRA_CFLAGS="-fPIC -fopenmp" \
    EXTRA_FFLAGS="-fPIC -fopenmp" \
    EXTRA_FCFLAGS="-fPIC -fopenmp" \
    EXTRA_LINK_FLAGS="-fopenmp /opt/apps/gcc/5.2.0/lib64/libstdc++.so" \
    CMAKE_INSTALL_PREFIX=${PWD}/install \
    CMAKE_BUILD_PREFIX=${PWD}/build \
    ./build.sh install
    
    cd install
    BMLDIR=`pwd`
    cd ../..

    # build qmd-progress
    # git clone https://github.com/lanl/qmd-progress.git

    echo "Building PROGRESS library ..."
    cd qmd-progress

    mkdir install build
    PWD=`pwd`
    CC=mpicc FC=mpif90 CXX=mpicxx \
    BLAS_VENDOR=Intel \
    CMAKE_BUILD_TYPE=Release \
    PROGRESS_OPENMP=yes PROGRESS_MPI=yes \
    PROGRESS_GRAPHLIB=no \
    PROGRESS_TESTING=no PROGRESS_EXAMPLES=no \
    CMAKE_C_FLAGS="-fPIC -fopenmp" \
    EXTRA_FCFLAGS="-fPIC -fopenmp" \
    EXTRA_LINK_FLAGS="-fopenmp /opt/apps/gcc/5.2.0/lib64/libstdc++.so" \
    CMAKE_PREFIX_PATH=${BMLDIR} \
    CMAKE_INSTALL_PREFIX=${PWD}/install \
    ./build.sh install
    
    cd install
    PROGRESSDIR=`pwd`
    cd ../..

    # build latte
    # git clone https://github.com/lanl/LATTE.git

    echo "Building LATTE library ..."
    cd LATTE-master

    # LATTE-master
    
    # makefile.CHOICE modified
    make FC="mpif90" PROGRESS_PATH="${PROGRESSDIR}/lib64" BML_PATH="${BMLDIR}/lib64"

    cd ../
    
    ln -s ./LATTE-master/src includelink
    ln -s ./LATTE-master liblink
    ln -s ./LATTE-master/src/latte_c_bind.o filelink.o

    # for -lg2c
    #ln -s /usr/lib64/libg2c.so.0.0.0 libg2c.so

    cat > Makefile.lammps <<EOF
      latte_SYSINC  =  -I../../lib/latte/LATTE-master/src
      latte_SYSINC += -I../../lib/latte/bml/install/include
      latte_SYSINC += -I../../lib/latte/qmd-progress/install/include
      latte_SYSLIB  = ../../lib/latte/filelink.o -llatte -lifcore -lsvml -limf -lpthread -llinalg -lgfortran
      latte_SYSLIB += -L../../lib/latte/qmd-progress/install/lib64 -lprogress
      latte_SYSLIB += -L../../lib/latte/bml/install/lib64 -lbml_fortran -lbml
      latte_SYSPATH = -L../../lib/linalg -L/opt/intel/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64 -L../../lib/latte
EOF

    module unload cmake
    module unload gcc
    module load intel/18.0.2
    cd ../.. 

  fi

  # linalg (needed by atc and awpmd)

  if [[ $liblist =~ "linalg" ]]; then

    echo "Working on linalg ..."
    cd lib/linalg

    make -f Makefile.mpi FC="mpif90" FFLAGS="${KNSX_FOPTS}" FFLAGS0="${KNSX_FOPTS}"

    #no Makefile.lammps required
    cd ../..
  fi        

  # meam

  if [[ $liblist =~ "meam" ]]; then

    echo "Working on meam ..."
    cd lib/meam

    make -f Makefile.ifort F90="ifort $KNSX_FOPTS"
    sed -e "s@/opt/intel/fce/10.0.023/lib@${IFC_LIB} ${IFC_RPATH}@"  Makefile.lammps.ifort | \
    sed -e "s/-lompstub/${OMP_STUBS_LIB}/"                          >Makefile.lammps

    #no Makefile.lammps required
    cd ../..
  fi

  # Serial ONLY

  # mscg

  #if [[ $liblist =~ "mscg" ]]; then

    #echo "Working on mscg ..."
    #cd lib/mscg

    #cd MSCG-release/src

    #module load gsl

    #make -f Make/Makefile.intel_simple libmscg.a

    #mv libmscg.a lib_mscg.a

    #cd ../..

    #ln -s MSCG-release/src includelink
    #ln -s MSCG-release/src liblink

    #cp Makefile.lammps.default Makefile.lammps

    #module unload gsl

    #cd ../..
  #fi

  # netcdf

  if [[ $liblist =~ "netcdf" ]]; then

    echo "Working on netcdf ..."
    cd lib/netcdf

    module load netcdf
    module load pnetcdf

    cat > Makefile.lammps <<EOF
      netcdf_SYSINC = -DLMP_HAS_NETCDF $(nc-config --cflags)
      netcdf_SYSLIB = $(nc-config --libs)
      netcdf_SYSINC += -DLMP_HAS_PNETCDF -I$(which ncmpidump | sed -e 's,bin/ncmpidump,,')/include
      netcdf_SYSLIB += -L$(which ncmpidump | sed -e 's,bin/ncmpidump,,')/lib -lpnetcdf
      netcdf_SYSPATH = $(nc-config --libs) -L$(which ncmpidump | sed -e 's,bin/ncmpidump,,')/lib -lpnetcdf
EOF

    cp Makefile.lammps ../../src/USER-NETCDF

    module unload netcdf
    module unload pnetcdf

    cd ../..
  fi

  # python

  if [[ $liblist =~ python ]]; then

    echo "Working on python ..."
    cd lib/python

    module load python

    # Must make Makefile.lammps lammps 
    cat > Makefile.lammps <<EOF
      python_SYSINC  = $(python-config --include)   
      python_SYSLIB  = $(python-config --ldflags)
      python_SYSPATH = -L$(python-config --prefix)/lib 
      PYTHON=python
EOF

    # PYTHON/install.sh will include Makefile.lammps

    module unload python

    cd ../..
  fi

  # poems

  if [[ $liblist =~ "poems" ]]; then

    echo "Working on poems ..."
    cd lib/poems
    
    make -j 4 -f Makefile.icc CC="mpicxx" LINK="mpicxx" \
    CCFLAGS="-g -fPIC $KNSX_OPTS -diag-disable 869,981,1572"

    #no Makefile.lammps required
    cd ../..
  fi

  # quip

  if [[ $liblist =~ "quip" ]]; then

    echo "Working on quip ..."
    cd lib/quip/QUIP

    export F95=ifort
    export QUIP_ARCH=linux_x86_64_ifort_icc
    export QUIP_ROOT=`pwd`

    mkdir -p build/$QUIP_ARCH    
    cp Makefile.inc_quip build/$QUIP_ARCH/Makefile.inc
  
    OPTS="-xAVX -axCORE-AVX2 -fp-model precise -qno-offload -qoverride-limits"
    sed -i "s/-vec-report0 -unroll -xP/$OPTS -diag-disable=7712/" arch/Makefile.$QUIP_ARCH
    sed -i "s/COPTIM = -O3/COPTIM = -O3 $OPTS -diag-disable=7712/" arch/Makefile.$QUIP_ARCH

    make libquip

    cd ../../..

  fi

  # smd

  if [[ $liblist =~ "smd" ]]; then

    echo "Working on smd ..."
    cd lib/smd

    # download eigen
    # git clone https://github.com/eigenteam/eigen-git-mirror.git

    ln -s eigen includelink

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

    make -j 4 CXX="mpicxx" CFLAGS="-g -fPIC $KNSX_OPTS -ansi -pedantic"

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
        
  # Now make the program:

  #export LD_LIBRARY_PATH=/opt/apps/gcc/7.3.0/lib64/:$LD_LIBRARY_PATH

  cd src

  # Make lammmps (use src/MAKE/MACHINES/Makefile.lonestar)

  echo Making lammps binary

  make -j 10 lonestar CC="mpicxx" LINK="mpicxx" CCFLAGS="$KNSX_LOPTS" LINKFLAGS="-O2 -qopenmp -xAVX -axCORE-AVX2 -fp-model precise -no-prec-div -qoverride-limits /opt/apps/gcc/7.3.0/lib64/libstdc++.so" #2>&1 | tee make_lonestar.log

  echo make lammps library

  make -j 10 lonestar mode=lib CC="mpicxx" LINK="mpicxx" CCFLAGS="$KNSX_LOPTS" LINKFLAGS="-O2 -qopenmp -xAVX -axCORE-AVX2 -fp-model precise -no-prec-div -qoverride-limits /opt/apps/gcc/7.3.0/lib64/libstdc++.so"

  echo make lammps shared library

  if [[ $liblist =~ "netcdf"    ]]; then make no-user-netcdf  ; fi

  make -j 10 lonestar mode=shlib CC="mpicxx" LINK="mpicxx" CCFLAGS="$KNSX_LOPTS" LINKFLAGS="-O2 -qopenmp -xAVX -axCORE-AVX2 -fp-model precise -no-prec-div -qoverride-limits /opt/apps/gcc/7.3.0/lib64/libstdc++.so"

  cd ..

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

  # cleanup tools directories
  rm -rf tools/amber2lmp tools/ch2lmp
  rm -rf tools/eff tools/moltemplate tools/phonon 
  rm -rf tools/pymol_asphere tools/reax tools/smd tools/xmgrace

  # cleanup examples directories
  rm -rf examples/*

  # cleanup tools and lib directories

  find lib -name \*\*.o   -exec rm {} \;
  find lib -name \*\*.c   -exec rm {} \;
  find lib -name \*\*.cpp -exec rm {} \;
  find lib -name \*\*.f   -exec rm {} \;
  find lib -name \*\*.f90 -exec rm {} \;
  find lib -name \*\*.py  -exec rm {} \;
  find lib -name \*\*.cu  -exec rm {} \;
  find lib -name \*\*.blk -exec rm {} \;

  find tools -name \*\*.o   -exec rm {} \;
  find tools -name \*\*.c   -exec rm {} \;
  find tools -name \*\*.cpp -exec rm {} \;
  find tools -name \*\*.h   -exec rm {} \;
  find tools -name \*\*.f   -exec rm {} \;
  find tools -name \*\*.f90 -exec rm {} \;

  # cleanup obj files

  rm -rf src/Obj_lonestar
  rm -f src/fix_signal*

  # clean doc files
  rm -rf doc/*

  mkdir                           $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mv src/lmp_lonestar             $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/

  cp -pR lib             $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  cp -pR potentials      $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials
  cp -pR python          $RPM_BUILD_ROOT/%{INSTALL_DIR}/python
  cp -pR tools           $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools
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
    
- ENVIRONMENT VARIABLES 
      
  The LAMMPS modulefile defines the following environment 
  variables (with the prefix "TACC_LAMMPS_"):

    TACC_LAMMPS_DIR/BIN/BENCH/EXAM/LIB/POT/PYTH/SRC/TOOLS

  for the location of the LAMMPS home, binaries, benchmarks, examples, 
  libraries, potentials, python scripts, source, and tools, respectively.
  The modulefile also appends TACC_LAMMPS_BIN & TACC_LAMMPS_TOOLS to PATH.

  Folders "benchmark", "doc", "examples" are now kept in the
  /work/apps/lammps/production_src/16Mar18 directory.

  Not all the tools are compiled and included in the TOOLS directory.

- PACKAGES

  The following packages were not installed:

    GPU, KIM, KOKKOS, LATTE, MESSAGE, MSCG, PYTHON, REAX, USER-SCAFACOS, USER-MOLFILE, USER-QMMM, USER-VTK

  Library REAX was not compiled with this version, because the default virtual 
  space of the library consumes 1.6 GB/task (for a total of 2.2 GB per task), and
  the TACC monitor kills jobs that use over 2.0 GB/task (32 GB for 16 tasks).

  Information of external libraries:

    * QUIP
      https://github.com/libAtoms/QUIP.git

    * VORONOI  
      voro++-%{vorover}
      http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz
      
    * USER-SMD
      Eigen-%{eigenver}
      https://github.com/eigenteam/eigen-git-mirror.git

- LIBRARIES

  LAMMPS libraries liblammps_lonestar.a (static), liblammps_lonestar.so (dynamic) are kept in TACC_LAMMPS_SRC.

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
local lmp_example_dir="/work/apps/lammps/production_src/16Mar18/"

setenv("TACC_LAMMPS_DIR"       ,lmp_dir)
setenv("TACC_LAMMPS_BIN"       ,pathJoin(lmp_dir,"bin"))
setenv("TACC_LAMMPS_LIB"       ,pathJoin(lmp_dir,"lib"))
setenv("TACC_LAMMPS_POT"       ,pathJoin(lmp_dir,"potentials"))
setenv("TACC_LAMMPS_TOOLS"     ,pathJoin(lmp_dir,"tools"))

setenv("TACC_LAMMPS_BENCH"     ,pathJoin(lmp_example_dir,"bench"))
setenv("TACC_LAMMPS_EXAM"      ,pathJoin(lmp_example_dir,"examples"))
setenv("TACC_LAMMPS_DOC"       ,pathJoin(lmp_example_dir,"doc"))
setenv("TACC_LAMMPS_SRC"       ,pathJoin(lmp_dir,"src"))

load("hdf5")
load("netcdf")
load("pnetcdf")

append_path("PATH",pathJoin(lmp_dir,"bin"))
append_path("PATH",pathJoin(lmp_dir,"tools"))

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
