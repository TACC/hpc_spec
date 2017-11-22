##rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1'                      lammps_31Mar17_s2.spec 2>&1 | tee log_lammps_31Mar17_s2_comp_17.0
##rpmbuild -bb --define 'is_intel18 1' --define 'is_impi 1' --define 'mpiV 18_0' lammps_31Mar17_s2.spec 2>&1 | tee log_lammps_31Mar17_s2_comp_18.0

# stampede2 will work on KNL and SKX,  stampede2_knl will only work on KNL
# stampede2_knl only provides a subset of potentials.

#lmp_stampede2:    uses -xCORE-AVX2 -axMIC-AVX512,CORE-AVX512   libs and lmps make
#lmp_stampede2_knl uses only -xMIC-AVX512

#LAMMPS

%define pkg_base_name lammps
%define MODULE_VAR    LAMMPS 

%define major_version 31Mar17
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines-noreloc.inc

Summary: LAMMPS is a Classical Molecular Dynamics package.
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   5%{?dist}
License:   GPL
Vendor:    Sandia
Group:     applications/chemistry
URL:       http://lammps.sandia.gov
Source:    %{pkg_base_name}-%{pkg_version}.tar
Packager:  TACC - milfeld@tacc.utexas.edu

%define   kimver   1.7.3
%define   vorover  0.4.6
%define   cudaver  6.5 
%define   cudasm   sm_35

%define   production_src_dir /work/apps/lammps/production_srcs/%{version}
%define              sdk_dir /work/apps/lammps/sdk/%{version}

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


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


#Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
LAMMPS is a classical molecular dynamics code with the following functionality: 
It can be run on a single processor or in parallel.  
It is written in highly portable C++.  
It is easy to extend with new features and functionality.
It has a syntax for defining and using variables and formulas, 
as well as a syntax for looping over runs and breaking out of loops.

%prep

   %if %{?BUILD_PACKAGE}
     rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
    #mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
   %endif # BUILD_PACKAGE |

   %if %{?BUILD_MODULEFILE}
     rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
   %endif # BUILD_MODULEFILE |


   %if %{?BUILD_PACKAGE}
%setup -n %{pkg_base_name}-%{pkg_version}

   %endif # BUILD_PACKAGE |


%build
%if %{?BUILD_PACKAGE}

    set +x
    %include system-load.inc
    %include compiler-load.inc
    %include mpi-load.inc
    set -x


# PREP  v ################################################################################

   OMP_STUBS_LIB=
    KIM_VER=%{kimver}
   VORO_VER=%{vorover}
   CUDA_VER=%{cudaver}
         SM=%{cudasm}
   INSTALL_DIR=%{INSTALL_DIR}

#          Use default IFC_LIB
  IFC_RPATH=-Wl,-rpath,$IFC_LIB


#  PREP
#                          Create kim in real directory 
#                          Uses soname in very complex way.
   LMP_DIR=`pwd`

   mkdir -p             %{INSTALL_DIR}/lib
   mount -t tmpfs tmpfs %{INSTALL_DIR}/lib

 cd                     %{INSTALL_DIR}/lib

    echo "start: untarring $LMP_DIR/kim-api-v${KIM_VER}.tar"
    tar                -xf $LMP_DIR/kim-api-v${KIM_VER}.tar
    mv kim-api-v${KIM_VER} kim
    echo "end:   untarring ../kim-api-v${KIM_VER}.tar"

 cd $LMP_DIR

 
#                          Adding voro++ download
 cd lib

   #echo "start: untarring ../voro++-${VORO_VER}.tar.gz"
   #tar               -xzf ../voro++-${VORO_VER}.tar.gz
   #mv                        voro++-${VORO_VER}   voro
   #echo "end:   untarring ../voro++-${VORO_VER}.tar.gz"

    echo "start: untarring $LMP_DIR/voro++-0.4.6.tar.gz"
    tar               -xzf $LMP_DIR/voro++-0.4.6.tar.gz
    [[ -d voronoi ]] && mv voronoi voronoi.$$
    mv voro++-0.4.6  voronoi
    cp voronoi.$$/install.py voronoi                     #what is this for?
    cp voronoi.$$/README voronoi/README_lammpsdistro                     #what is this for?
    echo "end:   untarring $LMP_DIR/voro++-0.4.6.tar.gz"

#    [[ ! -z quip.0 ]] && mv quip quip.0
#    echo "start: untarring ../../quip.tar"
#    tar                -xf ../../quip.tar
#    echo "end:   untarring ../../quip.tar"

 cd ..


# PREP  ^ ################################################################################


# TOOLS v ################################################################################

# Make the tools

cd tools

echo Working on  binary2txt chain micelle2d data2xmovie -------------------------------

##   #Changed to not print warning for main not returning int
##   sed -i.bak 's/gcc -g -c/gcc -g -c -Wno-implicit-int/' Makefile
##   make binary2txt chain micelle2d data2xmovie

##   rm -rf *.o

########################## Other tools

if [ 1 = 1 ]; then

cd colvars
echo Working on  colvars -------------------------------

   rm -rf *.o
   make CXX=icpc CXXFLAGS=-O2
   rm -rf *.o

   cd ..
   
cd createatoms
echo Working on createatoms -------------------------------

   rm -rf *.o
   ifort createAtoms.f -ocreateAtoms

   cd ..

cd eam_database
echo Working on eam_database -------------------------------

   rm -rf *.o
   ifort create.f -ocreate

   cd ..


cd eam_generate
echo Working on eam_generate -------------------------------
   rm -rf *.o
   icc Al_Zhou.c    -o Zl_Zhou
   icc Cu_Mishin1.c -o Mishin1
   icc Cu_Zhou.c    -o Cu_Zhou
   icc W_Zhou.c     -o  W_Zhou
   rm -rf *.o

   cd ..

##cd eff
##echo Working on eff -------------------------------
##
##   module load python
##   python setup.py build_ext --inplace
##   module unload python
##   rm -rf build/temp*/*.o
##   cd ..


cd lmp2arc
echo Working on lmp2arc -------------------------------
                    #See compiler warning.
     cd src
     #changed make to include -Wno-impicit
     sed -i.bak 's/-O2/-Wno-implicit -O2/' Makefile
     make
     cp lmp2arc.exe ../bin
     rm -rf src/*.o
     cd ../..

cd lmp2cfg
echo Working on lmp2cfg -------------------------------

    ifort lmp2cfg.f -o lmp2cfg

    cd ..

cd msi2lmp
echo Working on msi2lmp -------------------------------

   cd src
   rm -rf *.o
   make CC=icc CFLAGS=-g
   rm -rf *.o

   cd ../..

#cd phonon  #when user asks for this we will provide it.
#   rm -rf *.o
#   make
#   rm -rf *.o
#   cd ..

cd pymol_asphere
echo Working on pymol_asphere -------------------------------

    cd src
    rm -rf *.o

    #make COMPILER=mpi  #this will work, but use has to use MPI.
    #make nodw uses Compiler=intel and -static --> -static-intel
    #had problems in rpm with this.  Just fixed it, and made a new tar:(   KFM 10/15/14
   #grep commandline.h error.cpp > /dev/null
   #if [ $? -ne  0 ]; then 
       sed -e 's/#include <cstring>/#include <cstring>\n#include "commandline.h"/' < error.cpp > tmp
       mv error.cpp error.cpp.$$
       mv tmp error.cpp
   #fi

    make

    rm -rf obj/*.o
    cd ../..

##  Virtual space consumes 1.6GB of space (2.2GB total per task), 
##  and TACC monitor kill jobs.
##  Users can add this library by building lammps from /work/apps/lammps directory.
  cd reax
  echo Working on reax -------------------------------
  
     ifort bondConnectCheck.f90 -obondConnectCheck
     icc -diag-disable 266,810 mol_fra.c -omol_fra
  
     cd ..

#cd xmgrace   When user requests this we will give it to them
#   requires xmgrace plotting package.

#cd xmovie
#echo Working on xmovie -------------------------------

#  rm -rf *.o
#  make WARNS="-w" LIBS="-L/usr/lib64/ -lX11 -lXaw -lm -lXt -lXext -lXmu -lXpm"
#  rm -rf *.o

#  cd ..

#clean up

   find . -name \*\.o -exec rm {} \; 

   #remove sources, examples and tests -- now in /work/apps/<app_name>/version
   #remove sources, examples and tests -- now in /work/apps/lammps/%{version}

   rm -rf ./pymol_asphere/src
   rm -rf ./msi2lmp/src
   rm -rf ./lmp2arc/src
   rm -rf ./moltemplate/src

   rm -rf ./ch2lmp/example
   rm -rf ./pymol_asphere/examples
   rm -rf ./moltemplate/examples
   rm -rf ./moltemplate/examples/CG_biomolecules/protein_folding_examples
   rm -rf ./moltemplate/examples/all_atom_examples
   rm -rf ./moltemplate/examples/all_atom_examples/convert_LAMMPS_to_LT_examples
   rm -rf ./moltemplate/examples/all_atom_examples/OPLSAA_force_field_examples
   rm -rf ./moltemplate/examples/all_atom_examples/AMBER_force_field_examples
   rm -rf ./moltemplate/examples/all_atom_examples/read_PDB_file_examples
   rm -rf ./lmp2cfg/examples

   rm -rf ./msi2lmp/test
   rm -rf ./msi2lmp/test/runtests.sh
   rm -rf ./msi2lmp/test/test.input
   rm -rf ./lmp2arc/test

fi  #END OF TOOL SKIP

cd ..

# TOOLS ^ ################################################################################

# LIBS  v ################################################################################
#            Build libraries
 KNL_OPTS="-xMIC-AVX512"
KNSX_OPTS="-xCORE-AVX2 -axCORE-AVX512,MIC-AVX512 -diag-disable=cpu-dispatch"

mkliblist=()
#         atc awpmd colvars compress h5md kim kokkos linalg meam molfile poems python qmmm quip reax smd voronoi vtk gpu
#liblist="atc awpmd colvars compress h5md kim               meam         poems        qmmm quip          voronoi        "
 liblist="atc awpmd colvars compress h5md kim               meam         poems                           voronoi        "
#liblist="kim meam poems qmmm voronoi"

if [[ $liblist =~ python ]]; then
 cd lib/python

    echo "Working on python"

    ml python

    # Must make Makefile.lammps lammps 
     cat >Makefile.lammps <<EOF
      # python_SYSINC = -I/usr/include/python2.7
      ##python_SYSLIB = -lpython2.7 -lnsl -ldl -lreadline -ltermcap -lpthread -lutil -lm
      # python_SYSLIB = -lpthread -ldl -lutil -lm -lpython2.7
      # python_SYSPATH = -L/usr/lib64 -L/usr/lib/python2.7/site-packages
 
        python_SYSINC  = -I$(TACC_PYTHON_INC)   #or/opt/apps/intel17/python/2.7.12/include
       #python_SYSLIB = -lpython2.7 -lnsl -ldl -lreadline -ltermcap -lpthread -lutil -lm
        python_SYSLIB  = -lpython2.7 -ldl -lpthread -limf -lirc -lutil -limf
        python_SYSPATH = -L$(TACC_PYTHON_LIB)  #or/opt/apps/intel17/python/2.7.12/lib
EOF

    # PYTHON/install.sh will include Makefile.lammps

    module unload python

 cd ../..
fi


if [[ $liblist =~ "atc" ]]; then
 cd lib/atc
    echo "Working on atc"

    make -j 5 -f Makefile.icc \
         CC="mpicxx"  LINK="mpicxx" \
         CCFLAGS="-O3 $KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits -g -fPIC -I../../src -DMPICH_IGNORE_CXX_SEEK -diag-disable 858"
        #CCFLAGS="-O -g -fPIC -I../../src -DMPICH_IGNORE_CXX_SEEK -diag-disable 858"

    cp Makefile.lammps ../../src/USER-ATC

 cd ../..
fi

if [[ $liblist =~ "awpmd" ]]; then
 cd lib/awpmd
    echo "Working on awpmd"

    make -j 4 -f Makefile.mpicc CC="mpicxx " \
     CCFLAGS="-O3 $KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits  -g -fPIC -Isystems/interact/TCP/ -Isystems/interact -Iivutils/include"
    cp Makefile.lammps ../../src/USER-AWPMD


 cd ../..
fi

if [[ $liblist =~ "colvars" ]]; then
 cd lib/colvars
    echo "Working on colvars"

    make -j 4 -f Makefile.g++ CXX="mpicxx " \
        CXXFLAGS="-O2 $KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits -fstrict-aliasing -O2 -g -fPIC -funroll-loops -diag-disable 858"

    cat >Makefile.lammps <<EOF
       colvars_SYSINC =  -I../../colvars
       colvars_SYSLIB =  -lcolvars
       colvars_SYSPATH = -L../../lib/colvars
EOF
    cp Makefile.lammps  ../../src/USER-COLVARS

 cd ../..
fi

if [[ $liblist =~ "compress" ]]; then
 cd lib/compress

    echo "Working on compress"
    cp Makefile.lammps  ../../src/COMPRESS

 cd ../..
fi


if [[ $liblist =~ "h5md" ]]; then
 cd lib/h5md
    echo "Working on h5md"

    ml hdf5
    make

    # Must make lammps at end, otherwise it is overwritten by make (above)
    cat >Makefile.lammps <<EOF
       h5md_SYSINC  = -I/opt/apps/intel17/hdf5/1.8.16/x86_64/include -I../../lib/h5md/include
       h5md_SYSLIB  = -lhdf5 -lch5md
       h5md_SYSPATH = -L/opt/apps/intel17/hdf5/1.8.16/x86_64/lib -L../../lib/h5md
EOF
    cp Makefile.lammps  ../../src/USER-H5MD

 cd ../..
fi

 
if [[ $liblist =~ "kim" ]]; then

 cd         %{INSTALL_DIR}/lib/kim

   echo "Working on kim"
   MY_KIM_HOME=`pwd`
   cat Makefile.KIM_Config.example | \
   sed 's@GCC@INTEL@'              | \
   sed 's@\$(HOME)/.*@'$MY_KIM_HOME'@'         > Makefile.KIM_Config

   cat >Makefile.lammps <<EOF
      kim_SYSINC =  -I../../lib/kim/src
      kim_SYSLIB =  -lkim-api-v1 -nofor_main -cxxlib
      kim_SYSPATH = -L../../lib/kim/src
EOF
   cp Makefile.lammps  $LMP_DIR/src/KIM

    # FIX for examples: they need -cpp -free -Tf  with INTEL compiler
    export INTEL_FIX="$KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits -free -cpp -Tf"
    for i in `ls -d examples/openkim_tests/ex_* examples/openkim_tests/vc_*`; do
    echo $i
      cd $i
      mv Makefile Makefile.$$
      cat Makefile.$$ | \
      sed 's@\$(FC) \$(INCLUDES) \$(FFLAGS) \$(OBJONLYFLAG) \$<@\$(FC) \$(INCLUDES) \$(FFLAGS) \$(OBJONLYFLAG) \$(INTEL_FIX) \$<@' > Makefile
      cd $MY_KIM_HOME
    done

      my_dir=build_system/compiler_defaults
      mv $my_dir/Makefile.INTEL $my_dir/Makefile.INTEL.$$
      cat                       $my_dir/Makefile.INTEL.$$ | \
      sed 's/-warn all//'      >$my_dir/Makefile.INTEL


    #Let's build kim now with examples
    make      KIM_DIR=`pwd` CC="icc $IFC_RPATH" CXX="icpc $IFC_RPATH" FC="ifort $IFC_RPATH" examples
    make      KIM_DIR=`pwd` CC="icc $IFC_RPATH" CXX="icpc $IFC_RPATH" FC="ifort $IFC_RPATH"

    cd src
    ln -s libkim-api-v${KIM_VER}+INTEL.linux.64bit.dynamic-load.so libkim.so
    cd ..

    cd ..
    rm -rf     $LMP_DIR/lib/kim  #remove default library
    cp -pr kim $LMP_DIR/lib/kim    

 cd $LMP_DIR
#   umount %{INSTALL_DIR}/lib

fi


if [[ $liblist =~ "quip" ]]; then
 cd lib/quip

    if [[ "x" = x"$MY_KIM_HOME" ]]; then
       echo "ERROR:  cannot build quip until kim has been built and MY_KIM_HOME is set."
       exit
    fi

       #need this for `kim-api-v1-build-config --includes`
    export PATH=${PATH}:$MY_KIM_HOME/src/utils

    ml python
   #ml netcdf

    cp ../quip.0/Makefile.lammps .

    sed -i '4s/^/\n/' Makefile.lammps
    sed -i '4s/^/include ${QUIP_ROOT}\/Makefiles\/Makefile.${QUIP_ARCH}\n/' Makefile.lammps
    sed -i '4s/^/\n/' Makefile.lammps
    sed -i '4s/^/F95=ifort\n/' Makefile.lammps
    sed -i '4s/^/QUIP_ARCH=linux_x86_64_ifort_icc_serial\n/' Makefile.lammps
    sed -i '4s/^/QUIP_ROOT=..\/..\/lib\/quip\n/' Makefile.lammps
    sed -i '4s/^/\n/' Makefile.lammps

    cp Makefile.lammps ../../src/USER-QUIP

    export F95=ifort
    export QUIP_ARCH=linux_x86_64_ifort_icc_serial
    export QUIP_ROOT=`pwd`

    #in a practice build directory run make config, answer questions, and save in Makefile.inc_quip
    #or just modify the present version in ../../..

    mkdir -p build/$QUIP_ARCH
    cp ../../../Makefile.inc_quip build/$QUIP_ARCH/Makefile.inc

    MY_OPTS="$KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits"
    sed -i "s/-vec-report0 -unroll -xP/$MY_OPTS -diag-disable=7712/" arch/Makefile.$QUIP_ARCH
    sed -i "s/COPTIM = -O3/COPTIM = -O3 $MY_OPTS -diag-disable=7712/" arch/Makefile.$QUIP_ARCH

    #make config
    make libquip
    make quippy   # python wrapper See README.md https://github.com/libAtoms/QUIP

    ml unload python
   #ml unload netcdf

 cd ../..


fi

if [[ $liblist =~ "meam" ]]; then
 cd lib/meam

    echo "Working on meam"
    make -f Makefile.ifort F90="ifort $KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits"

    sed -e "s@/opt/intel/fce/10.0.023/lib@${IFC_LIB} ${IFC_RPATH}@"  Makefile.lammps.ifort | \
    sed -e "s/-lompstub/${OMP_STUBS_LIB}/"                          >Makefile.lammps

    #no Makefile.lammps required
 cd ../..
fi

if [[ $liblist =~ "poems" ]]; then
 cd lib/poems
    echo "Working on poems"
    make -j 4 -f Makefile.icc CC="icc $KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits"

    #no Makefile.lammps required
 cd ../..
fi


if [[ $liblist =~ "qmmm" ]]; then
 cd lib/qmmm

    ml espresso/5.4.0
    export QETOPDIR=$TACC_ESPRESSO_DIR

    echo "Working on qmmm using expresso/5.4.0"
    PWD=`pwd`

   #make -f Makefile.gfortran
    make -f Makefile.ifort MPICXX=mpicxx \
                           MPILIBS="-qopenmp  -lz  -lifcore  -lmpi -lmpiif" \
            MPICXXFLAGS=" $MY_OPTS -DOMPI_SKIP_MPICXX=1 -O2 -Wall -g -fPIC -I../../src -I$QETOPDIR/COUPLE/include"

    module unload espresso/5.4.0

    cat >Makefile.lammps <<EOF
    qmmm_SYSINC      = -I../../lib/qmmm
    qmmm_SYSLIB      = -lqmmm
    qmmm_SYSPATH     = -L../../lib/qmmm
EOF
    cp Makefile.lammps  ../../src/USER-QMMM

 cd ../..
fi

if [[ $liblist =~ "reax" ]]; then
echo 'WARNING:  USER-REAX should not be turned on!!!!'
echo "          USER-lib list: $liblist"
echo "          This may cause problems in the lammps USER-REAX build."
##  Virtual space consumes 1.6GB of space (2.2GB total per task),
##  and TACC monitor kill jobs.
##  Users can add this library by building lammps from /work/apps/lammps directory.
## cd lib/reax
##    echo "Working on reax"
##    make -j 4 -f Makefile.ifort F90="ifort $MY_OPTS " \
##                           F90FLAGS="-O -fPIC -diag-disable 8290"
##
##    sed -e "s/-lompstub/${OMP_STUBS_LIB}/"  Makefile.lammps.ifort | \
##    sed -e 's@PATH.*@PATH = -L'$IFC_LIB'@' >Makefile.lammps

## cd ../..

fi

if [[ $liblist =~ "voronoi" ]]; then
 cd lib/voronoi

   echo "Working on voronoi"
   PWD=`pwd`
   cat >Makefile.lammps << EOF
   voronoi_SYSINC   = -I$PWD/include/voro++
   voronoi_SYSLIB   = -lvoro++
   voronoi_SYSPATH  = -L$PWD/lib
EOF
   cp Makefile.lammps ../../src/VORONOI

    make -j 4 PREFIX=`pwd` \
     CFLAGS="-Wall -ansi -pedantic -O3 -fPIC $KNSX_OPTS -fp-model fast=2 -qno-offload -qoverride-limits" \
     CXX="icpc "
    make install PREFIX=`pwd`

    ln -s ../voronoi/src ../voronoi/includelink
    ln -s ../voronoi/src ../voronoi/liblink
 cd ../..
fi


if [[ $liblist =~ "gpu" ]]; then
echo keeping_shell_happy
# cd lib/gpu
# module   load cuda/$CUDA_VER
#
#    echo "Working on gpu"
#
#    mkdir -p obj
#
#     make -j 12 -f Makefile.fermi all CUDA_HOME=$TACC_CUDA_DIR EXTRAMAKE=Makefile.lammps.standard CUDA_ARCH=-arch=$SM \
#                            CUDR_CPP="mpicxx -DMPI_GERYON -DUCL_NO_EXIT -L $TACC_CUDA_LIB/stubs -I$TACC_CUDA_DIR/include"
#
#   # sed -e 's@gpu_SYSPATH.*@gpu_SYSPATH = -L'$TACC_CUDA_LIB'@' Makefile.lammps.standard > Makefile.lammps
#     sed -e 's@gpu_SYSPATH.*@gpu_SYSPATH = -L'"$TACC_CUDA_LIB -L$TACC_CUDA_LIB/stubs"'@' Makefile.lammps.standard > Makefile.lammps
#
# module unload cuda/$CUDA_VER
# cd ../..
fi


# LIBS  ^ ################################################################################
   

# BUILD v ################################################################################

# Now make the program:
cd src
KNL_OPTS="-xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits"
KNSX_OPTS="-xCORE-AVX2 -axCORE-AVX512,MIC-AVX512 -diag-disable=cpu-dispatch -fp-model fast=2 -qno-offload -qoverride-limits"

make yes-standard

if [[ ! $liblist =~ "gpu"      ]]; then make no-gpu       ; fi
if [[ ! $liblist =~ "kokkos"   ]]; then make no-kokkos    ; fi
if [[ ! $liblist =~ "python"   ]]; then make no-python    ; fi

                  #NO linalg does not appear in packages
                  #NO user-phonon libs downloaded

                  ##  Virtual space consumes 1.6GB of space (2.2GB total per task),
                  ##  and TACC monitor kill jobs.
                  ##  Users can add this library by building lammps from /work/apps/lammps directory.

                  ## molfile requires VMD and this is 0.18 version -- don't install

if [[ ! $liblist =~ "reax"     ]]; then make no-REAX; make no-USER-REAXC; fi
if [[ ! $liblist =~ "molfile"  ]]; then make no-user-molfile ; fi   #???

if [[ ! $liblist =~ "atc"      ]]; then make no-user-atc     ; fi
if [[ ! $liblist =~ "awpmd"    ]]; then make no-user-awpmd   ; fi
if [[ ! $liblist =~ "colvars"  ]]; then make no-user-colvars ; fi
if [[ ! $liblist =~ "compress" ]]; then make no-compress     ; fi    #not user-- but lib
if [[ ! $liblist =~ "h5md"     ]]; then make no-user-h5md    ; fi
if [[ ! $liblist =~ "kim"      ]]; then make no-user-kim     ; fi
if [[ ! $liblist =~ "meam"     ]]; then make no-meam         ; fi    #not user-- but lib
if [[ ! $liblist =~ "mscg"     ]]; then make no-mscg         ; fi    #not user-- but lib
if [[ ! $liblist =~ "poems"    ]]; then make no-poems        ; fi    #not user-- but lib
if [[ ! $liblist =~ "qmmm"     ]]; then make no-user-qmmm    ; fi
if [[ ! $liblist =~ "quip"     ]]; then make no-user-quip    ; fi
if [[ ! $liblist =~ "smd"      ]]; then make no-user-smd     ; fi
if [[ ! $liblist =~ "vtk"      ]]; then make no-user-vtk     ; fi
if [[ ! $liblist =~ "voronoi"  ]]; then make no-voronoi      ; fi    #not user-- but lib

make package-status

#  FINALLY:   Let there be light -- make lammmps

   echo make -j 10 stampede2  # 2>&1 | tee make_stampede2.log
        make -j 10 stampede2  # 2>&1 | tee make_stampede2.log
        mv lmp_stampede2 _lmp_stampede2

echo "Finished Making _lmp_stampede2"

make clean-stampede2

make yes-user-omp
make yes-user-intel

   echo make         stampede2_knl      # |& tee make_stampede2_knl.log
        make -j 10   stampede2_knl      # |& tee make_stampede2_knl.log
        mv lmp_stampede2_knl  _lmp_stampede2_knl

echo "Finished Making _lmp_stampede2_knl"

#
#make yes-gpu
#
#        module load cuda/$CUDA_VER
#
#        make -j 12 tacc CUDA_HOME=$TACC_CUDA_DIR
#        mv lmp_tacc _lmp_tacc_gpu
#
#        module unload cuda/$CUDA_VER
#
#make no-gpu
#echo "Finished Making _lmp_tacc_gpu"
#
#
#make clean-tacc

# Make the shared lib, for python, etc.
#      make makeshlib                     # creates Makefile.shlib
#      make SHLIBFLAGS=-shared -f Makefile.shlib tacc    # build for whatever machine target you wish

cd ..

%endif # BUILD_PACKAGE |

# BUILD ^ ################################################################################



%install

  echo "Installing the package?:    %{BUILD_PACKAGE}"
  echo "Installing the modulefile?: %{BUILD_MODULEFILE}"
 

# INSTALL LAMMPS V

  %if %{?BUILD_PACKAGE}

    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
   #mkdir -p $RPM_BUILD_ROOT/%{}

    
     #cleanup tools and lib directories
    
     rm -rf ./lib/cuda
     rm -rf ./lib/kokkos
     rm -rf ./lib/qmmm
     rm -rf ./lib/linalg
    
     find lib -name \*\*.o   -exec rm {} \;
     find lib -name \*\*.c   -exec rm {} \;
     find lib -name \*\*.cpp -exec rm {} \;
     find lib -name \*\*.h   -exec rm {} \;
     find lib -name \*\*.f   -exec rm {} \;
     find lib -name \*\*.f90 -exec rm {} \;
     find lib -name \*\*.cu  -exec rm {} \;
     find lib -name \*\*.blk -exec rm {} \;
    
     rm -rf lib/voro/examples
     rm -rf lib/voro/man
     rm -rf lib/voro/html
     rm -rf lib/kim/EXAMPLES
     rm -rf lib/kim/DOCS
     rm -rf lib/kim/TESTS
    
     find tools -name \*\*.o   -exec rm {} \;
     find tools -name \*\*.c   -exec rm {} \;
     find tools -name \*\*.cpp -exec rm {} \;
     find tools -name \*\*.h   -exec rm {} \;
     find tools -name \*\*.f   -exec rm {} \;
     find tools -name \*\*.f90 -exec rm {} \;
    
    
    
     mkdir                      $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
     cp src/_lmp_stampede2      $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_stampede2
     cp src/_lmp_stampede2_knl  $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_stampede2_knl
    #cp src/_lmp_tacc_gpu       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_tacc_gpu
    #cp src/_lmp_tacc_omp       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_tacc_omp
    #cp src/_lmp_tacc_mic       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_tacc_mic
    
     rm -rf src/Obj_shlib_tacc
     rm -rf src/Obj_tacc
     mv  src/_lmp_* .               #Keep them around if build directory saved.
    
     cp -pR lib             $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
     cp -pR potentials      $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials
     cp -pR python          $RPM_BUILD_ROOT/%{INSTALL_DIR}/python
     cp -pR tools           $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools
     cp -pR bench           $RPM_BUILD_ROOT/%{INSTALL_DIR}/bench
    #cp -pR doc             $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
     cp -pR examples        $RPM_BUILD_ROOT/%{INSTALL_DIR}/examples
     cp -pR src             $RPM_BUILD_ROOT/%{INSTALL_DIR}/src  
    
    chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*


  %endif #BUILD_PACKAGE

# INSTALL LAMMPS^



#### INSTALL MODULEFILE V

%if %{?BUILD_MODULEFILE}

    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
    touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The LAMMPS modulefile defines the following environment variables:
TACC_LAMMPS_DIR/BIN/BENCH/EXAM/LIB/POT/PYTH/SRC/TOOLS
for the location of the LAMMPS home, binaries,
benchmarks, examples, libraries, 
potentials, python scripts, source, and tools, respectively.

*Note* 
--BENCH/DOC/EXAM/SRC files are now kept in the
--/work/apps/lammps/production_src/%{version} directory.  Also, the
--source files for the package libraries and tools can be found in
--this directory. 
Some time after the production installation, a software development
kit will be available for modifying and building lammps in your own 
directory.  A tar file and readme file will be installed in the 
/work/apps/lammps/sdk/%{version} directory.  If you don't find
it, submit a ticket to find out when it will appear.


The modulefile also appends TACC_LAMMPS_BIN & TACC_LAMMPS_TOOLS to PATH.

TO RUN THE KNL VERSION OF LAMMPS: 
This version runs fast with a limited set of potentials.
This version will not run on the SKYLAKE (SKX) nodes.

Include the following lines in your job script:

       use: 68 MPI tasks per node, e.g. -N 1 -n 68 ; -N 2 -n 136; etc.
       module load lammps
       export OMP_NUM_THREADS=2
       ibrun lmp_stampede2_knl -pk intel 0 -sf intel <options>    < my_lammps_script.in
  or
       export OMP_NUM_THREADS=2
       ibrun lmp_stampede2_knl -pk intel 0 -sf intel <options> -in  my_lammps_script.in

See the Intel website for additional information on Phi (mix) execution:
https://software.intel.com/en-us/articles/recipe-lammps-for-intel-xeon-phi-processors

TO RUN THE SKX/KNL VERSION OF LAMMPS use the lmp_stampede2 executable.
This version is compiled for the SKYLAKE and KNL nodes.
The USER-INTEL style (package) in not available in this verion.

       use an appropriate number of tasks per node for your model:

       module load lammps
       ibrun lmp_stampede2  <options>  <   my_lammps_script.in
 or
       ibrun lmp_stampede2  <options> -in  my_lammps_script.in

See the LAMMPS website for additional info: http://lammps.sandia.gov/
Uses openkim-api-v%{kimver} and voro++-%{vorover}

These USER styles (packages) were not built: kokkos, molfile, python, quip, reax, smd vtk 

*REMOVED*
Library REAX/C was not compiled with this version, because the default Virtual 
space of the library consumes 1.6GB/task (for a total of 2.2GB per task), and
the TACC monitor kills jobs that use over 2.0GB/task (32GB for 16 tasks).
Users can build lammps from the %{version} version in /work/apps/lammps directory
and add this library with appropriate data arrays sized for their needs.
Read the LAMMPS_%{version}_README file.

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
  local sdk_dir="%{sdk_dir}"
--local src_dir="%{production_src_dir}"

setenv("TACC_LAMMPS_DIR"       ,lmp_dir)
setenv("TACC_LAMMPS_BIN"       ,pathJoin(lmp_dir,"bin"))
setenv("TACC_LAMMPS_LIB"       ,pathJoin(lmp_dir,"lib"))
setenv("TACC_LAMMPS_POT"       ,pathJoin(lmp_dir,"potentials"))
setenv("TACC_LAMMPS_PYTH"      ,pathJoin(lmp_dir,"python"))
setenv("TACC_LAMMPS_TOOLS"     ,pathJoin(lmp_dir,"tools"))

setenv("TACC_LAMMPS_BENCH"     ,pathJoin(lmp_dir,"bench"))
--setenv("TACC_LAMMPS_DOC"       ,pathJoin(lmp_dir,"doc"))
setenv("TACC_LAMMPS_EXAM"      ,pathJoin(lmp_dir,"examples"))
setenv("TACC_LAMMPS_SRC"       ,pathJoin(lmp_dir,"src"))
setenv("TACC_LAMMPS_SDK"       ,sdk_dir)


append_path("PATH",pathJoin(lmp_dir,"bin"))
append_path("PATH",pathJoin(lmp_dir,"tools"))

prepend_path("PYTHONPATH", pathJoin(lmp_dir,"python"))

EOF


cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for lammps
##
 
set     ModulesVersion      "%{version}"
EOF


%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua



%endif # BUILD_MODULEFILE |

#MODULEFILE ^




%if %{?BUILD_PACKAGE}
%files package
   %defattr(775,root,install)
   %{INSTALL_DIR}
%endif # BUILD_PACKAGE |

%if %{?BUILD_MODULEFILE}
%files modulefile 
   %defattr(775,root,install)
   %{MODULE_DIR}
%endif # BUILD_MODULEFILE |


#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT
