##rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1' lammps-17Nov16.spec | tee lammps.log.x
##rpmbuild -bb --define 'is_intel15 1' --define 'is_mvapich2 1' --define 'mpiV 2_1' lammps-10Feb15.spec|tee lmp.log

#LAMMPS

%define pkg_base_name lammps
%define MODULE_VAR    LAMMPS 

%define major_version 17Nov16
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

Release:   3%{?dist}
License:   GPL
Vendor:    Sandia
Group:     applications/chemistry
URL:       http://lammps.sandia.gov
Source:    %{pkg_base_name}-%{pkg_version}.tar
Packager:  TACC - milfeld@tacc.utexas.edu

%define   kimver   1.7.3
%define   vorover  0.4.6
%define   cudaver  7.5 
%define   cudasm   sm_35
%define   LMP_VER  knl

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

# Important macors
%define PNAME           lammps
%define INSTALL_DIR     %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR      %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
%define RPM_NAME        %{PNAME}-%{comp_fam_ver}-%{mpi_fam_ver}
%{echo: WITH MPI %PNAME-%{comp_fam_ver}-%{mpi_fam_ver}}
%{echo: WITH MPI %RPM_NAME}


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
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n %{pkg_base_name}-%{pkg_version}

  %endif # BUILD_PACKAGE |

  %if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
  %endif # BUILD_MODULEFILE |


%build
%if %{?BUILD_PACKAGE}

  unset MODULEPATH
  if [ -f "$BASH_ENV" ]; then
    . $BASH_ENV
    module purge
    clearMT
    MP="/opt/apps/tools/modulefiles:/opt/apps/modulefiles"

    if [ -z "$MODULEPATH" ]; then
     export MODULEPATH=$(/opt/apps/lmod/lmod/libexec/addto --append MODULEPATH ${MP//:/ })
    fi  
  fi

  module load %{comp_module}
  module load %{mpi_module}

# PREP  v ################################################################################

   OMP_STUBS_LIB=
    KIM_VER=%{kimver}
   VORO_VER=%{vorover}
   CUDA_VER=%{cudaver}
         SM=%{cudasm}
   INSTALL_DIR=%{INSTALL_DIR}

#          Use default IFC_LIB
  IFC_RPATH=-Wl,-rpath,$IFC_LIB

# Use our Makefile.%LMP_VER file!
   cp     Makefile.%LMP_VER   src/MAKE

#  PREP
#                          Create kim in real directory 
#                          Uses soname in very complex way.
   LMP_DIR=`pwd`

   mkdir -p %{INSTALL_DIR}/lib
   mount -t tmpfs tmpfs %{INSTALL_DIR}/lib

 cd         %{INSTALL_DIR}/lib
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
    cp voronoi.$$/install.py voronoi
    cp voronoi.$$/README voronoi/README_lammpsdistro
    echo "end:   untarring $LMP_DIR/voro++-0.4.6.tar.gz"

 cd ..


# PREP  ^ ################################################################################


# TOOLS v ################################################################################

# Make the tools

cd tools
echo Working on  binary2txt chain micelle2d data2xmovie -------------------------------

   #Changed to not print warning for main not returning int
   sed -i.bak 's/gcc -g -c/gcc -g -c -Wno-implicit-int/' Makefile
   make binary2txt chain micelle2d data2xmovie

   rm -rf *.o

########################## Other tools

if [ 1 = 2 ]; then

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

cd eff
echo Working on eff -------------------------------

   module load python
   python setup.py build_ext --inplace
   module unload python
   rm -rf build/temp*/*.o
   cd ..


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

 cd xmovie
 echo Working on xmovie -------------------------------

   rm -rf *.o
   make WARNS="-w" LIBS="-L/usr/lib64/ -lX11 -lXaw -lm -lXt -lXext -lXmu -lXpm"
   rm -rf *.o

   cd ..

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

# cd lib/atc
#    echo "Working on atc"
#
#    make -j 10 -f Makefile.icc \
#         CC="mpicxx"  LINK="mpicxx" \
#         CCFLAGS="-O3 -xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits -g -fPIC -I../../src -DMPICH_IGNORE_CXX_SEEK -diag-disable 858"
#        #CCFLAGS="-O -g -fPIC -I../../src -DMPICH_IGNORE_CXX_SEEK -diag-disable 858"
#
#    cp Makefile.lammps ../../src/USER-ATC
#
# cd ../..

# cd lib/awpmd
#    echo "Working on awpmd"
#
#    make -j 4 -f Makefile.mpicc CC="mpicxx " \
#     CCFLAGS="-O3 -xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits  -g -fPIC -Isystems/interact/TCP/ -Isystems/interact -Iivutils/include"
#    cp Makefile.lammps ../../src/USER-AWPMD
#
#
# cd ../..

# cd lib/colvars
#    echo "Working on colvars"
#
#    make -j 4 -f Makefile.g++ CXX="mpicxx " \
#        CXXFLAGS="-O2 -xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits -fstrict-aliasing -O2 -g -fPIC -funroll-loops -diag-disable 858"
#
#    cat >Makefile.lammps <<EOF
#       colvars_SYSINC =  -I../../colvars
#       colvars_SYSLIB =  -lcolvars
#       colvars_SYSPATH = -L../../lib/colvars
#EOF
#    cp Makefile.lammps  ../../src/USER-COLVARS
#
# cd ../..

 cd lib/compress

    echo "Working on compress"
    cp Makefile.lammps  ../../src/COMPRESS

 cd ../..


# cd lib/h5md
#    echo "Working on h5md"
#
#    ml hdf5
#    make
#
#    # Must make lammps at end, otherwise it is overwritten by make (above)
#    cat >Makefile.lammps <<EOF
#       h5md_SYSINC  = -I/opt/apps/intel17/hdf5/1.8.16/x86_64/include -I../../lib/h5md/include
#       h5md_SYSLIB  = -lhdf5 -lch5md
#       h5md_SYSPATH = -L/opt/apps/intel17/hdf5/1.8.16/x86_64/lib -L../../lib/h5md
#EOF
#    cp Makefile.lammps  ../../src/USER-H5MD
#
# cd ../..

 
if [ 1 = 1 ]; then   #DO KIM

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
    export INTEL_FIX="-xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits -free -cpp -Tf"
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

fi #END DO KIM

 cd lib/meam

    echo "Working on meam"
    make -f Makefile.ifort F90="ifort -xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits"

    sed -e "s@/opt/intel/fce/10.0.023/lib@${IFC_LIB} ${IFC_RPATH}@"  Makefile.lammps.ifort | \
    sed -e "s/-lompstub/${OMP_STUBS_LIB}/"                          >Makefile.lammps

    #no Makefile.lammps required
 cd ../..


 cd lib/poems
    echo "Working on poems"
    make -j 4 -f Makefile.icc CC="icc -xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits"

    #no Makefile.lammps required
 cd ../..

# cd lib/qmmm
#
#   echo "Working on qmmm"
#
# cd ../..

##  Virtual space consumes 1.6GB of space (2.2GB total per task),
##  and TACC monitor kill jobs.
##  Users can add this library by building lammps from /work/apps/lammps directory.

## cd lib/reax
##    echo "Working on reax"
##    make -j 4 -f Makefile.ifort F90=ifort  \
#          F90FLAGS="-xAVX -axCORE-AVX2 -diag-disable remark -O -fPIC -diag-disable 8290"
##
##    sed -e "s/-lompstub/${OMP_STUBS_LIB}/"  Makefile.lammps.ifort | \
##    sed -e 's@PATH.*@PATH = -L'$IFC_LIB'@' >Makefile.lammps
## cd ../..


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
     CFLAGS="-Wall -ansi -pedantic -O3 -fPIC -xMIC-AVX512 -fp-model fast=2 -qno-offload -qoverride-limits" \
     CXX="icpc "
    make install PREFIX=`pwd`

    ln -s ../voronoi/src ../voronoi/includelink
    ln -s ../voronoi/src ../voronoi/liblink
 cd ../..


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


# LIBS  ^ ################################################################################
   

# BUILD v ################################################################################

# Now make the program:
cd src

make yes-standard
make no-gpu
make no-kokkos
make no-python
make yes-user-omp yes-user-intel

                  ##  Virtual space consumes 1.6GB of space (2.2GB total per task),
                  ##  and TACC monitor kill jobs.
                  ##  Users can add this library by building lammps from /work/apps/lammps directory.
make no-REAX
make no-USER-REAXC

make package-status
##                    Removed from library, see note above.
##                    Users can add this library by building lammps from /work/apps/lammps directory.

   echo make -j 10 knl  # |& tee make_tacc.log
        make -j 10 knl  # |& tee make_tacc.log
        mv lmp_knl _lmp_knl

echo "Finished Making _lmp_tacc"

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

#make yes-user-omp
#
#        make -j 12 tacc OMP=-openmp
#        mv lmp_tacc _lmp_tacc_omp
#
#echo "Finished Making   _lmp_tacc_omp"


#make yes-USER-INTEL
#make package-status

#   echo make -j 4 tacc  # |& tee make_tacc.log
#        make -j 4 tacc  # |& tee make_tacc.log
#  echo make      tacc  # |& tee make_tacc.log
#       make      tacc  # |& tee make_tacc.log
#        mv lmp_tacc _lmp_tacc_mic

#echo "Finished Making _lmp_tacc_mic"



# Make the shared lib, for python, etc.
#      make makeshlib                     # creates Makefile.shlib
#      make SHLIBFLAGS=-shared -f Makefile.shlib tacc    # build for whatever machine target you wish

cd ..

%endif # BUILD_PACKAGE |

# BUILD ^ ################################################################################



%install

  %include system-load.inc
  module purge
 
  echo "Installing the package?:    %{BUILD_PACKAGE}"
  echo "Installing the modulefile?: %{BUILD_MODULEFILE}"
 

# INSTALL LAMMPS V

  %if %{?BUILD_PACKAGE}

    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

    
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
    
    
    
     mkdir                          $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
     cp src/_lmp_knl            $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_knl
    #cp src/_lmp_tacc_gpu       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_tacc_gpu
    #cp src/_lmp_tacc_omp       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_tacc_omp
    #cp src/_lmp_tacc_mic       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_tacc_mic
    
     rm -rf src/Obj_shlib_tacc
     rm -rf src/Obj_tacc
     mv  src/_lmp_* .               #Keep them around if build directory saved.
    
    #cp -pR bench           $RPM_BUILD_ROOT/%{INSTALL_DIR}/bench
    #cp -pR doc             $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
    #cp -pR examples        $RPM_BUILD_ROOT/%{INSTALL_DIR}/examples
     cp -pR lib             $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
     cp -pR potentials      $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials
     cp -pR python          $RPM_BUILD_ROOT/%{INSTALL_DIR}/python
     cp -pR tools           $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools
    #cp -pR src             $RPM_BUILD_ROOT/%{INSTALL_DIR}/src  
    
    chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*


  %endif #BUILD_PACKAGE

# INSTALL LAMMPS^


# INSTALL MODULEFILE V
%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  

## Module for lammps
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
The LAMMPS modulefile defines the following environment variables:
TACC_LAMMPS_DIR/BIN/BENCH/DOC/EXAM/LIB/POT/PYTH/SRC/TOOLS
for the location of the LAMMPS home, binaries,
benchmarks, documentation, examples, libraries, 
potentials, python scripts, source, and tools, respectively.

*Note* 
BENCH/DOC/EXAM/SRC files are now kept in the
/work/apps/lammps/distro_files/%{version} directory.  Also, the
source files for the package libraries and tools can be found in
this directory.

The modulefile also appends TACC_LAMMPS_BIN & TACC_LAMMPS_TOOLS to PATH.

To run the KNL version of LAMMPS, please include the following lines in 
your job script:

       use: 68 MPI tasks per node, e.g. -N 1 -n 68 ; -N 2 -n 136; etc.
       module load lammps
       export OMP_NUM_THREADS=2
       ibrun lmp_knl -pk intel 0 -sf intel <options>    < my_lammps_script.in
  or
       export OMP_NUM_THREADS=2
       ibrun lmp_knl -pk intel 0 -sf intel <options> -in  my_lammps_script.in

See the Intel website for additional information on Phi (mix) execution:
https://software.intel.com/en-us/articles/recipe-lammps-for-intel-xeon-phi-processors

See the LAMMPS website for additional info: http://lammps.sandia.gov/
Use openkim-api-v%{kimver} and voro++-%{vorover}

*REMOVED*
Library REAXC was not compiled with this version, because the default Virtual 
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
local distro_dir="/work/apps/lammps/distro_files/%{version}"

setenv("TACC_LAMMPS_DIR"       ,lmp_dir)
setenv("TACC_LAMMPS_BIN"       ,pathJoin(lmp_dir,"bin"))
setenv("TACC_LAMMPS_LIB"       ,pathJoin(lmp_dir,"lib"))
setenv("TACC_LAMMPS_POT"       ,pathJoin(lmp_dir,"potentials"))
setenv("TACC_LAMMPS_PYTH"      ,pathJoin(lmp_dir,"python"))
setenv("TACC_LAMMPS_TOOLS"     ,pathJoin(lmp_dir,"tools"))

setenv("TACC_LAMMPS_BENCH"     ,pathJoin(distro_dir,"bench"))
setenv("TACC_LAMMPS_DOC"       ,pathJoin(distro_dir,"doc"))
setenv("TACC_LAMMPS_EXAM"      ,pathJoin(distro_dir,"examples"))
setenv("TACC_LAMMPS_SRC"       ,pathJoin(distro_dir,"src"))


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
