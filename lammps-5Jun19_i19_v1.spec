################################################################
#
#    LAMMPS SPEC FILE
#
#    MACHINE       :   TACC FRONTERA
#    VERSION       :   5 Jun 2019 - patch_5Jun2019
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   06-09-2019
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
# rpmbuild -bb --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_4' lammps-5Jun19_i19_v1.spec | tee log_lammps_5Jun19
#

%define pkg_base_name lammps
%define MODULE_VAR    LAMMPS 

%define major_version 5Jun19
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}

################################################################

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc
#%include name-defines-noreloc.inc

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
%define    kimver   2.0.2
%define    vorover  0.4.6
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
  %include system-load.inc
  %include compiler-load.inc
  %include mpi-load.inc
 
  ml use /opt/apps/intel19/modulefiles
  module load intel
  module load impi 
  module load python3
  module load hdf5
  #module load qt5
  #module load vtk/8.1.1
  module load netcdf
  module load gsl
  module load cmake
  set -x

  #----------------------------#
  #                            #
  #      Build libraries       #
  #                            #
  #----------------------------#

  echo "Working on libraries ......."

  mkliblist=()

  # List of additional library to be installed
  #liblist="atc awpmd colvars compress h5md kim linalg netcdf plumed poems python quip scafacos smd voronoi vtk ffmpeg"

  #liblist=""
  liblist="atc awpmd colvars compress h5md kim linalg netcdf plumed poems python quip scafacos smd voronoi     ffmpeg"

  # Include all packages which don't need external libraries
  # Remove the packges that's not in the liblist

  cd src  
  make yes-all
  make no-ext
  make no-gpu
  make no-reax
  make no-kokkos
  make no-latte
  make no-message
  make no-user-adios

  if [[ ! $liblist =~ "atc"      ]]; then make no-user-atc     ; fi
  if [[ ! $liblist =~ "awpmd"    ]]; then make no-user-awpmd   ; fi
  if [[ ! $liblist =~ "colvars"  ]]; then make no-user-colvars ; fi
  if [[ ! $liblist =~ "compress" ]]; then make no-compress     ; fi
  if [[ ! $liblist =~ "kim"      ]]; then make no-kim          ; fi
  if [[ ! $liblist =~ "poems"    ]]; then make no-poems        ; fi
  if [[ ! $liblist =~ "python"   ]]; then make no-python       ; fi
  if [[ ! $liblist =~ "scafacos" ]]; then make no-user-scafacos; fi

  # External libraries required
  if [[ $liblist =~ "h5md"      ]]; then make yes-user-h5md    ; fi
  if [[ $liblist =~ "kim"       ]]; then make yes-kim          ; fi
  if [[ $liblist =~ "latte"     ]]; then make yes-latte        ; fi
  if [[ $liblist =~ "quip"      ]]; then make yes-user-quip    ; fi
  if [[ $liblist =~ "netcdf"    ]]; then make yes-user-netcdf  ; fi
  if [[ $liblist =~ "plumed"    ]]; then make yes-user-plumed  ; fi
  if [[ $liblist =~ "scafacos"  ]]; then make yes-user-scafacos; fi
  if [[ $liblist =~ "smd"       ]]; then make yes-user-smd     ; fi
  if [[ $liblist =~ "voronoi"   ]]; then make yes-voronoi      ; fi
  if [[ $liblist =~ "vtk"       ]]; then make yes-user-vtk     ; fi

  make package-status
  cd ..

  # -----------
  # LIBRARIES
  # -----------

  # ATC

  if [[ $liblist =~ "atc" ]]; then

    echo "Working on atc ..."
    cd lib/atc

    make -j 4 -f Makefile.mpic++

cat > Makefile.lammps <<EOF
    user-atc_SYSINC =
    user-atc_SYSLIB = -mkl
    user-atc_SYSPATH =
EOF

    # use lammps linalg library
    #cp Makefile.lammps.linalg Makefile.lammps
    cd ../..
  fi

  # ............................................

  # AWPMD

  if [[ $liblist =~ "awpmd" ]]; then

    echo "Working on awpmd ..."
    cd lib/awpmd

    make -j 4 -f Makefile.mpicc

cat > Makefile.lammps <<EOF
    user-awpmd_SYSINC =
    user-awpmd_SYSLIB = -mkl
    user-awpmd_SYSPATH =
EOF

    # use lammps linalg library 
    #cp Makefile.lammps.linalg Makefile.lammps
    cd ../..
  fi

  # ............................................

# COLVARS

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

  # ............................................

  # COMPRESS

  if [[ $liblist =~ "compress" ]]; then

    echo "Working on compress ..."
    cd lib/compress
    cd ../..
  fi

  # ............................................

  # H5MD

  if [[ $liblist =~ "h5md" ]]; then

    echo "Working on h5md ..."
    cd lib/h5md

    make -f Makefile.h5cc CC="${TACC_HDF5_BIN}/h5cc" HDF5_PATH="${TACC_HDF5_DIR}" CFLAGS="-D_DEFAULT_SOURCE -O2 -DH5_NO_DEPRECATED_SYMBOLS -Wall -fPIC" INC="-I include -I${TACC_HDF5_INC}"

    # Must make lammps at end, otherwise it is overwritten by make (above)
    cat >Makefile.lammps <<EOF
       h5md_SYSINC  = -I../../lib/h5md/include -I${TACC_HDF5_INC}
       h5md_SYSLIB  = -lch5md  ${TACC_HDF5_LIB}/libhdf5.a -lsz -lz
       h5md_SYSPATH = -L${TACC_HDF5_LIB} -L../../lib/h5md
EOF
    cd ../..
  fi

  # ............................................

  # KIM

  if [[ $liblist =~ "kim" ]]; then

    echo "Working on kim ..."
    cd lib/kim

    KIM_ROOT_DIR=`pwd`
    KIM_VERSION=%{kimver}

    # KIM-API
    mkdir -p /opt/apps/intel19/impi19_0/lammps/%{major_version}/lib/kim
    tar -xf kim-api-${KIM_VERSION}.txz
    rm kim-api-${KIM_VERSION}.txz

    mv kim-api-${KIM_VERSION} /opt/apps/intel19/impi19_0/lammps/%{major_version}/lib/kim
    cd /opt/apps/intel19/impi19_0/lammps/%{major_version}/lib/kim

    mkdir installed-kim-api
    export KIM_INSTALL_DIR=`pwd`/installed-kim-api
    export PKG_CONFIG_PATH=${KIM_INSTALL_DIR}/lib64/pkgconfig

    cd kim-api-${KIM_VERSION}
    mkdir build
    cd build

    cmake .. -DCMAKE_INSTALL_PREFIX="${KIM_INSTALL_DIR}"  \
            -DCMAKE_BUILD_TYPE=Release \
            -DCMAKE_CXX_COMPILER=icpc \
            -DCMAKE_C_COMPILER=icc \
            -DCMAKE_Fortran_COMPILER=ifort 

    make -j4
    make install
    cd ${KIM_ROOT_DIR}

    export KIM_API_CMAKE_PREFIX_DIR=${KIM_INSTALL_DIR}/lib64/kim-api/cmake
    export KIM_API_MODEL_DRIVERS_DIR=`pwd`/kim_env_collection/model_drivers
    export KIM_API_MODELS_DIR=`pwd`/kim_env_collection/models
    export KIM_API_SIMULATOR_MODELS_DIR=`pwd`/kim_env_collection/simulators
    export CXX=icpc
    export CC=icc
    export FC=ifort

    # Install model drivers

    cd ./kim_env_collection/model_drivers

    while read  mo; do

      echo $mo
      tar -xf "${mo}.txz"
      cd "${mo}"
      if [ -f CMakeLists.txt ]; then
        mkdir build
        cd build
        cmake .. -DKIM_API_INSTALL_COLLECTION=ENVIRONMENT

        make
        make install
        cd ..
        rm -r build
        cd ..
        rm "${mo}.txz"
      else
        echo "no cmakelist"
        cd ..
      fi
    done < drivers.txt            

    # Install models

    cd ../models

    while read  mo; do

      echo $mo
      tar -xf "${mo}.txz"
      cd "${mo}"
      if [ -f CMakeLists.txt ]; then
        mkdir build
        cd build
        cmake .. -DKIM_API_INSTALL_COLLECTION=ENVIRONMENT

        make
        make install
        cd ..
        rm -r build
        cd ..
        rm "${mo}.txz"
      else
        echo "no cmakelist"
        cd ..
      fi

    done < models.txt
    cd ../../

cat > Makefile.KIM_DIR <<EOF
KIM_INSTALL_DIR=../../lib/kim/installed-kim-api

.DUMMY: print_dir

print_dir:
        @printf \$(KIM_INSTALL_DIR)
EOF

    cp -r /opt/apps/intel19/impi19_0/lammps/%{major_version}/lib/kim/installed-kim-api .

    cd ../../
  fi

  # ............................................

  # LINALG (needed by atc and awpmd)

  if [[ $liblist =~ "linalg" ]]; then

    echo "Working on linalg ..."
    cd lib/linalg

    make -f Makefile.mpi FC="mpiifort"

    cd ../..
  fi

  # ............................................

  # NETCDF

  if [[ $liblist =~ "netcdf" ]]; then

    echo "Working on netcdf ..."
    cd lib/netcdf

cat > Makefile.lammps <<EOF
      netcdf_SYSINC = -DLMP_HAS_NETCDF $(nc-config --cflags)
      netcdf_SYSLIB = $(nc-config --libs)
      netcdf_SYSPATH = $(nc-config --cflags)
EOF
    cp Makefile.lammps ../../src/USER-NETCDF

    cd ../..
  fi

  # ............................................

  # PLEMED

  if [[ $liblist =~ plumed ]]; then

    echo "Working on plumed ..."
    cd lib/plumed

    mkdir plumed2

    PLUMED_INSTALL_DIR=`pwd`/plumed2
    #OPT="-O2 -fPIC -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512 -diag-disable=cpu-dispatch"
    OPT="-O2 -fPIC"

    cd plumed2-src
    #./configure --prefix=${PLUMED_INSTALL_DIR} CC=icc CXX=icpc CFLAGS="${OPT}" CXXFLAGS="${OPT}"
    ./configure --prefix=${PLUMED_INSTALL_DIR} CC="/usr/bin/gcc" CXX="/usr/bin/g++" CFLAGS="${OPT}" CXXFLAGS="${OPT}"
    make -j 10
    make install

    cd ../

    ln -s ${PLUMED_INSTALL_DIR}/include includelink
    ln -s ${PLUMED_INSTALL_DIR}/lib liblink

cat > Makefile.lammps <<EOF
plumed_SYSINC = -D__PLUMED_WRAPPER_CXX=1
plumed_SYSLIB = "${PLUMED_INSTALL_DIR}/lib/libplumed.a" -ldl -lz -ldl -rdynamic -Wl,-Bsymbolic -fopenmp
plumed_SYSPATH = 
EOF

    cd ../..
  fi

  # ............................................

  # PYTHON

  if [[ $liblist =~ python ]]; then

    echo "Working on python ..."
    cd lib/python

    cp Makefile.lammps.python3 Makefile.lammps
    cd ../..
  fi

  # ............................................

  # POEMS

  if [[ $liblist =~ "poems" ]]; then

    echo "Working on poems ..."
    cd lib/poems

    make -j 4 -f Makefile.mpi

    cd ../..
  fi

  # ............................................

  # QUIP

  if [[ $liblist =~ "quip" ]]; then

    echo "Working on quip ..."
    cd lib/quip/QUIP

    export F95=ifort
    export QUIP_ARCH=linux_x86_64_ifort_icc
    export QUIP_ROOT=`pwd`

    mkdir -p build/$QUIP_ARCH
    cp Makefile.inc_quip build/$QUIP_ARCH/Makefile.inc

    make libquip

    rm -rf src
    rm -rf tests
    rm -rf doc
    rm -rf docker
    rm -rf Singularity

    cd ../../..

  fi

  # ............................................

  # SCAFACOS

  if [[ $liblist =~ "scafacos" ]]; then

    echo "Working on scafacos ..."
    cd lib/scafacos

    mkdir scafacos
    SCAFACOS_DIR=`pwd`/scafacos
    OPT="-fPIC -I${TACC_GSL_INC}"

    cd scafacos-src
    ./bootstrap

    unset F77

    ./configure --prefix=${SCAFACOS_DIR} --disable-doc --enable-fcs-solvers=fmm,p2nfft,direct,ewald,p3m --with-internal-fftw --with-internal-pfft --with-internal-pnfft --with-mpi  CC=mpiicc CXX=mpiicpc FC=mpiifort CFLAGS="${OPT}" CXXFLAGS="${OPT}" FCFLAGS="${OPT}" LDFLAGS="-L${TACC_GSL_LIB}"

    make -j4
    make install

    cd ../

    ln -s ${SCAFACOS_DIR}/include includelink
    ln -s ${SCAFACOS_DIR}/lib liblink

    # FIX UNBALANCED QUOTE ISSUE
    cd ${SCAFACOS_DIR}/lib/pkgconfig
    cp scafacos.pc scafacos.pc.bk
    cat scafacos.pc.bk | sed 's/-lpthread"/-lpthread/' > scafacos.pc
    cd ../../../
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${SCAFACOS_DIR}/lib
    export PKG_CONFIG_PATH=${SCAFACOS_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}
    cd ../../
  fi

  # ............................................

  # SMD

  if [[ $liblist =~ "smd" ]]; then

    echo "Working on smd ..."
    cd lib/smd

    ln -s eigen includelink

cat > Makefile.lammps <<EOF
    user-smd_SYSINC  = -I../../lib/smd/includelink
    user-smd_SYSLIB  =
    user-smd_SYSPATH =
EOF

    cd ../..
  fi

  # ............................................
  # VORONOI

  if [[ $liblist =~ "voronoi" ]]; then

    echo "Working on voronoi ..."

    vorover=0.4.6

    # voronoi library source code
    cd lib/voronoi/src/voro++-${vorover}

    make -j 4 CXX="mpiicpc" CFLAGS="-O3 -Wall -fPIC -ansi -pedantic -xCORE-AVX512"

    rm -rf examples
    rm -rf html

    cd ../..

    ln -s src/voro++-${vorover}/src includelink
    ln -s src/voro++-${vorover}/src liblink

    cd ../../
  fi

  # ............................................

  # VTK

  if [[ $liblist =~ "vtk" ]]; then

    echo "Working on vtk ..."

    cd lib/vtk

cat > Makefile.lammps <<EOF
    vtk_SYSINC = -I${TACC_VTK_INC}/vtk-8.1
    vtk_SYSPATH = -L${TACC_VTK_LIB}
    vtk_SYSLIB = ${TACC_VTK_LIB}/libvtkCommonCore-8.1.so ${TACC_VTK_LIB}/libvtkIOCore-8.1.so ${TACC_VTK_LIB}/libvtkIOXML-8.1.so ${TACC_VTK_LIB}/libvtkIOLegacy-8.1.so ${TACC_VTK_LIB}/libvtkCommonDataModel-8.1.so ${TACC_VTK_LIB}/libvtkIOParallel-8.1.so ${TACC_VTK_LIB}/libvtkParallelCore-8.1.so ${TACC_VTK_LIB}/libvtkParallelMPI-8.1.so ${TACC_VTK_LIB}/libvtkIOImage-8.1.so ${TACC_VTK_LIB}/libvtkCommonExecutionModel-8.1.so ${TACC_VTK_LIB}/libvtkFiltersCore-8.1.so ${TACC_VTK_LIB}/libvtkIOParallelXML-8.1.so
EOF

    cd ../../
  fi

  # ............................................
  # ffmpeg

  if [[ $liblist =~ "ffmpeg" ]]; then

    echo "Working on ffmpeg ..."

    # ffmpeg library source code

    cd lib/ffmpeg

    mkdir -p ffmpeg_build bin lib
    FFMPEG_DIR=`pwd`

    cd ffmpeg_src

    # NASM
    tar -xf nasm-2.14rc15.tar.gz
    cd nasm-2.14rc15
    ./autogen.sh
    PATH="$FFMPEG_DIR/bin:$PATH" CC=icc CXX=icpc ./configure --prefix="${FFMPEG_DIR}/ffmpeg_build" --bindir="${FFMPEG_DIR}/bin"                   
    make -j10 && \
    make install
    cd ..

    # YASM
    tar -xf yasm-1.3.0.tar.gz
    cd yasm-1.3.0
    CC=icc CXX=icpc ./configure --prefix="${FFMPEG_DIR}/ffmpeg_build" --bindir="${FFMPEG_DIR}/bin" && \
    make -j10 && \
    make install
    cd ..

    # LIBX264
    cd x264
    PATH="${FFMPEG_DIR}/bin:$PATH" PKG_CONFIG_PATH="${FFMPEG_DIR}/ffmpeg_build/lib/pkgconfig" CC=icc CXX=icpc ./configure  --prefix="${FFMPEG_DIR}/ffmpeg_build" --bindir="${FFMPEG_DIR}/bin" --enable-static --enable-pic && \
    PATH="$FFMPEG_DIR/bin:$PATH" make -j10 && \
    make install
    cd ..
    
    # LIBVPX
    cd libvpx
    PATH="${FFMPEG_DIR}/bin:$PATH" CC=icc CXX=icpc ./configure  --prefix="${FFMPEG_DIR}/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm && \
    PATH="${FFMPEG_DIR}/bin:$PATH" make -j10 && \
    make install
    cd ..

    # LIBFDK-AAC
    cd fdk-aac
    autoreconf -fiv && \
    CC=icc CXX=icpc ./configure --prefix="${FFMPEG_DIR}/ffmpeg_build" --disable-shared && \
    make -j10 && \
    make install
    cd ..

    # LIBMP3LAME
    tar -xf lame-3.100.tar.gz
    cd lame-3.100
    PATH="${FFMPEG_DIR}/bin:$PATH" CC=icc CXX=icpc ./configure  --prefix="${FFMPEG_DIR}/ffmpeg_build" --bindir="${FFMPEG_DIR}/bin" --disable-shared --enable-nasm && \
    PATH="$FFMPEG_DIR/bin:$PATH" make -j10 && \
    make install
    cd ..
    
    # LIBOPUS
    cd opus
    ./autogen.sh
    CC=icc CXX=icpc ./configure --prefix="${FFMPEG_DIR}/ffmpeg_build" --disable-shared && \
    make -j10 && \
    make install
    cd ..

    # LIBAOM
    mkdir aom_build
    cd aom_build
    PATH="${FFMPEG_DIR}/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_C_COMPILER=icc -DCMAKE_CXX_COMPILER=icpc -DCMAKE_INSTALL_PREFIX="${FFMPEG_DIR}/ffmpeg_build" -DENABLE_SHARED=off -DENABLE_NASM=on ../aom && \
    PATH="${FFMPEG_DIR}/bin:$PATH" make -j10 && \
    make install
    cd ..

    # FFMPEG
    cd ffmpeg

    PATH="${FFMPEG_DIR}/bin:$PATH" PKG_CONFIG_PATH="${FFMPEG_DIR}/ffmpeg_build/lib/pkgconfig" ./configure \
    --cc=icc --cxx=icpc \
    --prefix="${FFMPEG_DIR}/ffmpeg_build"  \
    --pkg-config-flags="--static" \
    --extra-cflags="-I${FFMPEG_DIR}/ffmpeg_build/include" \
    --extra-ldflags="-L${FFMPEG_DIR}/ffmpeg_build/lib" \
    --bindir="${FFMPEG_DIR}/bin" \
    --enable-gpl  \
    --enable-libfdk-aac  \
    --enable-libfreetype  \
    --enable-libmp3lame \
    --enable-libopus  \
    --enable-libx264  \
    --enable-nonfree && \
    PATH="${FFMPEG_DIR}/bin:$PATH" make -j10 && \
    make install

    cd ../..
    rm -rf ffmpeg_build ffmpeg_src
    cd ../..
  fi

  #----------------------------#
  #                            #
  #        Build LAMMPS        #
  #                            #
  #----------------------------#
        
  # Now make the program:

  cd src

  # Make lammmps (use src/MAKE/MACHINES/Makefile.frontera)

  cat MAKE/OPTIONS/Makefile.intel_cpu_intelmpi | sed 's/-xHost/-xCORE-AVX512/g' | sed 's/-restrict/-restrict -diag-disable=cpu-dispatch/g'> MAKE/MACHINES/Makefile.frontera

  make -j 10 frontera \
            LMP_INC="-DLAMMPS_GZIP -DLAMMPS_EXCEPTIONS -DLAMMPS_FFMPEG -DLAMMPS_PNG" \
            FFT_INC="-DFFT_SINGLE" \
            FFT_LIB="-lmkl_intel_lp64 -lmkl_sequential -lmkl_core" \
            JPG_INC="-I/usr/lib64" \
            JPG_PATH="-L/usr/lib64" \
            JPG_LIB="-lpng"

  make -j 10 frontera mode=shlib \
            LMP_INC="-DLAMMPS_GZIP -DLAMMPS_EXCEPTIONS -DLAMMPS_FFMPEG -DLAMMPS_PNG" \
            FFT_INC="-DFFT_SINGLE" \
            FFT_LIB="-lmkl_intel_lp64 -lmkl_sequential -lmkl_core" \
            JPG_INC="-I/usr/lib64" \
            JPG_PATH="-L/usr/lib64" \
            JPG_LIB="-lpng"
  cd ..

  rm -rf /opt/apps/intel19/impi19_0/lammps/%{major_version}

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
  
  # cleanup lib directories that we won't use
  rm -rf lib/gpu lib/kokkos lib/molfile lib/mscg
  rm -rf lib/qmmm lib/reax

  # cleanup tools directories
  rm -rf tools

  # cleanup examples directories
  rm -rf examples

  # cleanup lib directories

  find lib -name \*\*.o   -exec rm {} \;
  find lib -name \*\*.c   -exec rm {} \;
  find lib -name \*\*.cpp -exec rm {} \;
  find lib -name \*\*.f   -exec rm {} \;
  find lib -name \*\*.f90 -exec rm {} \;
  find lib -name \*\*.py  -exec rm {} \;
  find lib -name \*\*.cu  -exec rm {} \;
  find lib -name \*\*.blk -exec rm {} \;

  # cleanup obj files
  rm -rf src/Obj_frontera

  # clean doc files
  rm -rf doc

  # create bin
  mkdir                                 $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mv src/lmp_frontera                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_frontera

  # create lib/lammps
  mkdir -p                              $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/lammps
  mv src/liblamm*                       $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/lammps
  cp python/lammps.py                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/lammps

  # back to lammps build root
  cd $lmp_build_dir
  cp -pR lib/*           $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
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

Load required modules and set library paths

  $ module load intel/intel/19.0.4
  $ module load impi/19.0.4
  $ module load lammps/%{major_version}

Run LAMMPS program

  * Basic

    ibrun lmp_frontera -in lammps_input

  * Use USER-OMP package (E.g. with 2 omp threads)

    ibrun lmp_frontera -sf omp -pk omp 2 -in lammps_input 

  * Use USER-INTEL package (E.g. with 2 omp threads)

    ibrun lmp_frontera -sf intel -pk intel 0 omp 2 -in lammps_input 

- ENVIRONMENT VARIABLES 

The LAMMPS modulefile defines the following environment 
variables (with the prefix "TACC_LAMMPS_"):

TACC_LAMMPS_DIR/BIN/LIB/POT/PYTHON/SRC

for the location of the LAMMPS home, binaries, libraries, potentials, 
python, and source respectively. The modulefile also appends TACC_LAMMPS_BIN to PATH.

- PACKAGES

The following packages were not installed:

  GPU, KOKKOS, LATTE, MESSAGE, MSCG, REAX, USER-ADIOS USER-MOLFILE, USER-QMMM, USER-VTK

Information of external libraries:

  * OpenKIM
    kim-api-v%{kimver}
    https://openkim.org

    The KIM package defines environment variables KIM_API_MODELS_DIR and 
    KIM_API_MODEL_DRIVERS_DIR for the locations of the installed KIM models 
    and model drivers. Use command : 
    
      $ kim-api-v1-collections-management list
    
    to show the collections.

  * QUIP (No GAP)
    https://github.com/libAtoms/QUIP.git

  * VORONOI  
    voro++-%{vorover}
    http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz
    
- LIBRARIES

  LAMMPS library liblammps_frontera.so is kept in TACC_LAMMPS_LIB/lammps.

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

local kim_dir="%{INSTALL_DIR}/lib/kim/"
local kim_model_dir="%{INSTALL_DIR}/lib/kim/kim_env_collection/models"
local kim_driver_dir="%{INSTALL_DIR}/lib/kim/kim_env_collection/model_drivers"
local kim_simulator_dir="%{INSTALL_DIR}/lib/kim/kim_env_collection/simulators"
local kim_bin_dir="%{INSTALL_DIR}/lib/kim/installed-kim-api/bin"

append_path("PATH",pathJoin(lmp_dir,"bin"))
append_path("PATH",pathJoin(lmp_dir,"lib/ffmpeg/bin"))
append_path("PATH",kim_bin_dir)

setenv("TACC_KIM_DIR"              ,kim_dir)
setenv("TACC_KIM_API"              ,pathJoin(kim_dir,"installed-kim-api"))
setenv("TACC_KIM_MODEL"            ,kim_model_dir)
setenv("TACC_KIM_DRIVER"           ,kim_driver_dir)
setenv("KIM_API_MODELS_DIR"        ,kim_model_dir)
setenv("KIM_API_MODEL_DRIVERS_DIR" ,kim_driver_dir)
setenv("KIM_API_SIMULATORS_DIR"    ,kim_simulator_dir)

append_path("LD_LIBRARY_PATH",pathJoin(lmp_dir,"lib/ffmpeg/lib"))
append_path("LD_LIBRARY_PATH",pathJoin(lmp_dir,"lib/lammps"))
append_path("LD_LIBRARY_PATH","/opt/apps/intel19/hdf5/1.10.4/x86_64/lib/")

prepend_path("PYTHONPATH", pathJoin(lmp_dir,"python"))
prepend_path("PYTHONPATH", pathJoin(lmp_dir,"lib/lammps"))

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
