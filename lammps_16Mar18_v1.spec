################################################################
#
#    LAMMPS SPEC FILE
#
#    MACHINE       :   TACC STAMPEDE2
#    VERSION       :   16 MAR 2018
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   04-19-2018
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

%define pkg_base_name lammps
%define MODULE_VAR    LAMMPS 

%define major_version 16Mar18
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
  %include system-load.inc
  %include compiler-load.inc
  %include mpi-load.inc
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
    ifort createAtoms.f -ocreateAtoms
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
    echo "Working on micell2d ..."
    ifort micelle2d.f -o micelle2d

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
  liblist="atc awpmd colvars compress linalg meam poems python voronoi"

  # Include all packages which don't need external libraries
  # Remove the packges that's not in the liblist

  cd src
  
  make yes-all
  make no-ext
  make no-gpu
  make no-reax
  make no-kokkos
  make no-latte

  if [[ ! $liblist =~ "atc"      ]]; then make no-user-atc     ; fi
  if [[ ! $liblist =~ "awpmd"    ]]; then make no-user-awpmd   ; fi
  if [[ ! $liblist =~ "colvars"  ]]; then make no-user-colvars ; fi
  if [[ ! $liblist =~ "compress" ]]; then make no-compress     ; fi
  if [[ ! $liblist =~ "meam"     ]]; then make no-meam         ; fi
  if [[ ! $liblist =~ "poems"    ]]; then make no-poems        ; fi
  if [[ ! $liblist =~ "python"   ]]; then make no-python       ; fi

  # External libraries required
  if [[ $liblist =~ "voronoi"   ]]; then make yes-voronoi      ; fi

  make package-status

  cd ..
  
  # FC flags (KNL-SKX fat binary)
  KNSX_FOPTS="-O2 -qopenmp -xCOMMON-AVX512 -axMIC-AVX512 -diag-disable=cpu-dispatch -fp-model fast=2 -qno-offload -qoverride-limits -fno-alias -ansi-alias -no-prec-div"
  # CC flags (KNL-SKX fat binary)
  KNSX_OPTS="$KNSX_FOPTS -restrict"

  # atc

  if [[ $liblist =~ "atc" ]]; then

    echo "Working on atc ..."
    cd lib/atc

    make -j 4 -f Makefile.icc \
    CC="mpiicpc"  LINK="mpiicpc" \
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
    CC="mpiicpc" \
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
        
    make -j 4 -f Makefile.mpi \
    CXX="mpiicpc " \
    CXXFLAGS="-g -fPIC $KNSX_OPTS -funroll-loops"

    cat > Makefile.lammps <<EOF
      colvars_SYSINC =  -I../../colvars
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

  # linalg (needed by atc and awpmd)

  if [[ $liblist =~ "linalg" ]]; then

    echo "Working on linalg ..."
    cd lib/linalg

    make -f Makefile.mpi FC="mpiifort" FFLAGS="$KNSX_FOPTS" FFLAGS0="$KNSX_FOPTS"

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

  # python

  if [[ $liblist =~ python ]]; then

    echo "Working on python ..."
    cd lib/python

    module load python

    # Must make Makefile.lammps lammps 
    cat > Makefile.lammps <<EOF

      python_SYSINC  = -I$(python-config --include)   
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
    
    make -j 4 -f Makefile.icc CC="mpiicpc" LINK="mpiicpc" \
    CCFLAGS="-g -fPIC $KNSX_OPTS -diag-disable 869,981,1572"

    #no Makefile.lammps required
    cd ../..
  fi

  # voronoi

  if [[ $liblist =~ "voronoi" ]]; then

    echo "Working on voronoi ..."

    # voronoi library source code
    cd lib/voronoi/src/voro++-%{vorover}

    make -j 4 CXX="mpiicpc" CFLAGS="-g -fPIC $KNSX_OPTS -ansi -pedantic"

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

  cd src

  # Make lammmps (use src/MAKE/MACHINES/Makefile.stampede)

  echo make -j 10 stampede  # 2>&1 | tee make_stampede.log
  make -j 10 stampede #2>&1 | tee make_stampede.log
  echo "Finished Making lmp_stampede"

  cd ..

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"
 
# INSTALL LAMMPS

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  
  # cleanup lib directories
  rm -rf lib/gpu lib/h5md lib/kokkos lib/latte lib/molfile
  rm -rf lib/mscg lib/netcdf lib/qmmm lib/qmmm lib/quip 
  rm -rf lib/reax lib/smd lib/vtk

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
  find lib -name \*\*.h   -exec rm {} \;
  find lib -name \*\*.f   -exec rm {} \;
  find lib -name \*\*.f90 -exec rm {} \;
  find lib -name \*\*.cu  -exec rm {} \;
  find lib -name \*\*.blk -exec rm {} \;

  find tools -name \*\*.o   -exec rm {} \;
  find tools -name \*\*.c   -exec rm {} \;
  find tools -name \*\*.cpp -exec rm {} \;
  find tools -name \*\*.h   -exec rm {} \;
  find tools -name \*\*.f   -exec rm {} \;
  find tools -name \*\*.f90 -exec rm {} \;

  # cleanup obj files

  rm -rf src/Obj_stampede

  # clean doc files
  rm -rf doc/html  
  rm -rf doc/Makefile
  rm -rf doc/src
  rm -rf doc/utils

  mkdir                  $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  cp src/lmp_stampede    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/lmp_stampede
  cp -pR lib             $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  cp -pR potentials      $RPM_BUILD_ROOT/%{INSTALL_DIR}/potentials
  cp -pR python          $RPM_BUILD_ROOT/%{INSTALL_DIR}/python
  cp -pR tools           $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools
  cp -pR bench           $RPM_BUILD_ROOT/%{INSTALL_DIR}/bench
  cp -pR doc             $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
  cp -pR examples        $RPM_BUILD_ROOT/%{INSTALL_DIR}/examples
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

      * TO RUN LAMMPS

      Set the number of nodes (N) and MPI tasks (n) in the job script.

      module load intel/17.0.4
      module load impi/17.0.3
      module load lammps/%{major_version}

      export OMP_NUM_THREADS=2  (or any other reasonable number)

      ibrun lmp_stampede -pk intel 0 -sf intel [options] -in lammps_input > log_file
      
      * ENVIRONMENT VARIABLES 
      
      The LAMMPS modulefile defines the following environment 
      variables (with the prefix "TACC_LAMMPS_"):

      TACC_LAMMPS_DIR/BIN/BENCH/EXAM/LIB/POT/PYTH/SRC/TOOLS

      for the location of the LAMMPS home, binaries, benchmarks, examples, 
      libraries, potentials, python scripts, source, and tools, respectively.
      The modulefile also appends TACC_LAMMPS_BIN & TACC_LAMMPS_TOOLS to PATH.

      Folder "examples" is now kept in the
      /work/apps/lammps/production_src/16Mar18 directory

      Not all the tools are compiled and included in the TOOLS directory.

      * PACKAGES

      The following packages were not installed:

      GPU, KIM, KOKKOS, LATTE, MSCG, REAX,
      USER-H5MD, USER-MOLFILE, USER-NETCDF, USER-QMMM, USER-QUIP,
      USER-SMD, USER-VTK

      Library REAX was not compiled with this version, because the default virtual 
      space of the library consumes 1.6GB/task (for a total of 2.2GB per task), and
      the TACC monitor kills jobs that use over 2.0GB/task (32GB for 16 tasks).

      Information of external libraries:
      voronoi: voro++-%{vorover}
      
      * REFERENCE
      
      See the LAMMPS website for additional info: http://lammps.sandia.gov/

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
    setenv("TACC_LAMMPS_PYTH"      ,pathJoin(lmp_dir,"python"))
    setenv("TACC_LAMMPS_TOOLS"     ,pathJoin(lmp_dir,"tools"))

    setenv("TACC_LAMMPS_BENCH"     ,pathJoin(lmp_dir,"bench"))
    setenv("TACC_LAMMPS_DOC"       ,pathJoin(lmp_dir,"doc"))
    setenv("TACC_LAMMPS_EXAM"      ,pathJoin(lmp_example_dir,"examples"))
    setenv("TACC_LAMMPS_SRC"       ,pathJoin(lmp_dir,"src"))

    append_path("PATH",pathJoin(lmp_dir,"bin"))
    append_path("PATH",pathJoin(lmp_dir,"tools"))

    prepend_path("PYTHONPATH", pathJoin(lmp_dir,"python"))

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
rm -rf $RPM_BUILD_ROOT

################################################################
