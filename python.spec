Summary:    Python is a high-level general-purpose programming language.
Name:       tacc-python 
Version:    2.7.13
Release:    2%{?dist}
License:    GPLv2
Vendor:     Python Software Foundation
Group:      Applications
Packager:   TACC - rtevans@tacc.utexas.edu

#------------------------------------------------
# Either Python package or mpi4py will be built 
# based on this switch
#------------------------------------------------
%define build_mpi4py     1
%global _python_bytecompile_errors_terminate_build 0
#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%if "%{build_mpi4py}" == "0"
    %define mpi_fam     none
    %define mpi_label   none
%endif

%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc	

%define PNAME python
%define MODULE_VAR TACC_PYTHON

%define INSTALL_DIR_COMP %{APPS}/%{comp_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR_COMP %{APPS}/%{comp_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{comp_fam_ver}

%if "%{build_mpi4py}" == "1"
    %define INSTALL_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
    %define MODULE_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
    %define PACKAGE_NAME tacc-mpi4py-%{comp_fam_ver}-%{mpi_fam_ver}-%{PNAME}
%endif

%package -n %{PACKAGE_NAME}
Summary: Python built for TACC systems
Group:   Programming Language

%description
%description -n %{PACKAGE_NAME}
This is intended to be a core Python
interpreter for TACC systems.

%prep

rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}

%if "%{build_mpi4py}" == "0"
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
%endif
%if "%{build_mpi4py}" == "1"
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
%endif

%build

%install
export BASH_ENV=/etc/tacc/tacc_functions
%include system-load.inc
%include compiler-load.inc

# Set up src directory
export SRC_DIR=/tmp/src
mkdir -p ${SRC_DIR}
cd %{_topdir}/SOURCES

export PATH=%{INSTALL_DIR_COMP}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR_COMP}/lib64:%{INSTALL_DIR_COMP}/lib:$LD_LIBRARY_PATH
export PYTHONPATH=%{INSTALL_DIR_COMP}/lib:$PYTHONPATH

############################################################
# System Specific
############################################################
%if "%{comp_fam_name}" == "Intel"
    #export ISAFLAGS=TACC_OPT #"-xCORE-AVX2 -axCOMMON-AVX512"
    export MKL_INC=$TACC_MKL_INC
    export MKL_LIB=$TACC_MKL_LIB
    export OMP_LIB=$ICC_LIB
%endif
%if "%{comp_fam_name}" == "GNU"
    #export ISAFLAGSTACC_OPT #="-march=native"
    ml intel
    export MKL_INC=$TACC_MKL_INC
    export MKL_LIB=$TACC_MKL_LIB
    export OMP_LIB=$ICC_LIB
    ml gcc
    export LD_LIBRARY_PATH=$MKL_LIB:$OMP_LIB:$LD_LIBRARY_PATH
%endif

echo $LD_LIBRARY_PATH | sed -e "s/:/\n/g" 
############################################################
# Build core python here
############################################################

if [ ! -f "%{INSTALL_DIR_COMP}/bin/python" ]; then
    if ! mountpoint -q %{INSTALL_DIR_COMP} ; then	
        mkdir -p %{INSTALL_DIR_COMP}
        mount -t tmpfs tmpfs %{INSTALL_DIR_COMP}
    fi

    if [ ! -f "%{_topdir}/SOURCES/Python-%{version}.tgz" ]; then
     	wget http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
    fi	
    rm -rf ${SRC_DIR}/Python-%{version}
    tar -xzf %{_topdir}/SOURCES/Python-%{version}.tgz -C ${SRC_DIR}
    cd ${SRC_DIR}/Python-%{version}
    export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH
    ls
    %if "%{comp_fam_name}" == "Intel"
    ./configure --prefix=%{INSTALL_DIR_COMP} CC=icc CXX=icpc LD=xild AR=xiar LIBS='-lpthread -limf -lirc' CFLAGS="-O3 -fp-model strict -fp-model source -ipo -prec-div -prec-sqrt -xhost" LDFLAGS="-ipo -Xlinker -export-dynamic" CPPFLAGS="" CPP="icc -E" --with-system-ffi --with-cxx-main=icpc --enable-shared --with-pth --without-gcc --with-libm=-limf --with-threads --with-lto --enable-optimizations --with-computed-gotos --with-ensurepip    
    %endif
    %if "%{comp_fam_name}" == "GNU"
    #./configure --prefix=%{INSTALL_DIR_COMP} CFLAGS="-flto -ffat-lto-objects -fuse-linker-plugin %{TACC_OPT}" LDFLAGS="-flto -ffat-lto-objects -fuse-linker-plugin -rdynamic" --with-system-ffi --enable-shared --with-pth --with-threads --with-lto --enable-optimizations --with-computed-gotos --with-ensurepip    
    ./configure --prefix=%{INSTALL_DIR_COMP} --with-system-ffi --enable-shared --with-lto --with-pth --with-threads --with-computed-gotos --with-ensurepip    
    %endif

    make -j 28
    make sharedinstall
    make -i install
fi
############################################################
# core python modules
############################################################
if [ ! -f "%{INSTALL_DIR_COMP}/bin/pip" ]; then
    wget https://bootstrap.pypa.io/get-pip.py
    %{INSTALL_DIR_COMP}/bin/python get-pip.py
fi
%{INSTALL_DIR_COMP}/bin/pip install --trusted-host pypi.python.org certifi
%{INSTALL_DIR_COMP}/bin/pip install nose
%{INSTALL_DIR_COMP}/bin/pip install virtualenv
%{INSTALL_DIR_COMP}/bin/pip install virtualenvwrapper    
%{INSTALL_DIR_COMP}/bin/pip install sympy
%{INSTALL_DIR_COMP}/bin/pip install brewer2mpl
%{INSTALL_DIR_COMP}/bin/pip install futures
%{INSTALL_DIR_COMP}/bin/pip install simpy    
%{INSTALL_DIR_COMP}/bin/pip install jsonpickle
%{INSTALL_DIR_COMP}/bin/pip install meld3
%{INSTALL_DIR_COMP}/bin/pip install supervisor
%{INSTALL_DIR_COMP}/bin/pip install paramiko
%{INSTALL_DIR_COMP}/bin/pip install readline
%{INSTALL_DIR_COMP}/bin/pip install egenix-mx-base


#############################################################
# scipy stack: use INSTALL_DIR_COMP . 
# We need to know which pip modules are compiler specific.  
# numpy scipy matplotlib jupyter pandas sympy nose
############################################################

### Numpy
if ! $(%{INSTALL_DIR_COMP}/bin/python -c "import numpy"); then
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/numpy-1.12.1.tar.gz" ]; then	
	wget https://github.com/numpy/numpy/releases/download/v1.12.1/numpy-1.12.1.tar.gz
    fi	   
    
    rm -rf ${SRC_DIR}/numpy-1.12.1 	   
    tar -xzvf %{_topdir}/SOURCES/numpy-1.12.1.tar.gz -C ${SRC_DIR}	
    cd ${SRC_DIR}/numpy-1.12.1

    sed -i 's/-openmp/-fopenmp -xhost/' numpy/distutils/intelccompiler.py
    sed -i 's/-openmp/-fopenmp -xhost/' numpy/distutils/fcompiler/intel.py

    %if "%{comp_fam_name}" == "Intel"
    echo "[mkl]
library_dirs = $MKL_LIB:$OMP_LIB
include_dirs = $MKL_INC
mkl_libs = mkl_rt
lapack_libs = " > site.cfg
    %{INSTALL_DIR_COMP}/bin/python setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
    %endif

    %if "%{comp_fam_name}" == "GNU"	
    echo "[mkl]
library_dirs = $MKL_LIB
include_dirs = $MKL_INC
mkl_libs    = mkl_rt
lapack_libs = " > site.cfg
    export CFLAGS="-m64 -Wl,--no-as-needed"    
    export CXXFLAGS="-m64 -Wl,--no-as-needed"
    export LDFLAGS="-ldl -lm"
    export FFLAGS="-m64"

    %{INSTALL_DIR_COMP}/bin/python setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
    %endif
fi

### Scipy
if ! $(%{INSTALL_DIR_COMP}/bin/python -c "import scipy"); then
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/scipy-0.19.0.tar.gz" ]; then	
	wget -O scipy-0.19.0.tar.gz https://github.com/scipy/scipy/releases/download/v0.19.0/scipy-0.19.0.tar.gz
    fi	   

    rm -rf ${SRC_DIR}/scipy-0.19.0
    tar -xzvf scipy-0.19.0.tar.gz -C ${SRC_DIR} 
    cd ${SRC_DIR}/scipy-0.19.0
    %if "%{comp_fam_name}" == "Intel"
    %{INSTALL_DIR_COMP}/bin/python setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
    %endif

    %if "%{comp_fam_name}" == "GNU"	
    %{INSTALL_DIR_COMP}/bin/python setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
    %endif
fi

#%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: scipy
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: matplotlib	
CFLAGS="-O2" %{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: cython	
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: cffi	
#%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: pandas
%{INSTALL_DIR_COMP}/bin/pip install pandas
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: psutil
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: numexpr
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: rpyc	
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: ipython
%{INSTALL_DIR_COMP}/bin/pip install jupyter	
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: mako


#Antonio: Removed this temporarily
CFLAGS="-O2" %{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: lxml
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: pystuck
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: fortran-magic
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: MySQL
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: psycopg2
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: mercurial

#Antonio: Removed the next three temporarily
CFLAGS="-O2" %{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: yt
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: theano
%{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: scikit_learn

if module load phdf5; then
    CC="mpicc -ip-no-inlining" HDF5_MPI="ON" HDF5_DIR=$TACC_HDF5_DIR pip install --no-binary=h5py --no-deps --ignore-installed h5py --user
    #%{INSTALL_DIR_COMP}/bin/pip install h5py
    %{INSTALL_DIR_COMP}/bin/pip install tables
fi
#############################################################
# mpi4py: use INSTALL_DIR_MPI
############################################################
%if "%{build_mpi4py}" == "1"
  if ! mountpoint -q %{INSTALL_DIR_MPI} ; then	
    mkdir -p %{INSTALL_DIR_MPI}
    mount -t tmpfs tmpfs %{INSTALL_DIR_MPI}
  fi
  module load %{PNAME}/%{version}	
  module load %{mpi_module}   
  %{INSTALL_DIR_COMP}/bin/pip install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_MPI}" mpi4py
%endif

#----------------------------------------------------------
# Copy into rpm directory
#----------------------------------------------------------
# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.

#----------------------------------------------------------
# UNMOUNT THE TEMP FILESYSTEM
#----------------------------------------------------------
%if "%{build_mpi4py}" == "0"
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
    cp -r %{INSTALL_DIR_COMP}/ $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}/..
%endif

%if "%{build_mpi4py}" == "1"
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
    cp -r %{INSTALL_DIR_MPI}/ $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}/..
%endif

if mountpoint -q %{INSTALL_DIR_COMP} ; then	
    umount %{INSTALL_DIR_COMP}
fi

if mountpoint -q %{INSTALL_DIR_MPI} ; then	
    umount %{INSTALL_DIR_MPI}
fi

#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
%if "%{build_mpi4py}" == "0"
#------- Serial Module
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}/%{version}.lua << 'EOF'
help(
[[
This is the Python package built on %(date +'%B %d, %Y').

You can install your own modules (choose one method):
        1. python setup.py install --user
        2. python setup.py install --home=<dir>
        3. pip install --user module-name

Version %{version}
]]
)

whatis("Name: Python")
whatis("Version: %{version}")
whatis("Version-notes: Compiler:%{comp_fam_ver}")
whatis("Category: Applications, Scientific, Graphics")
whatis("Keywords: Applications, Scientific, Graphics, Scripting Language")
whatis("URL: http://www.python.org/")
whatis("Description: scientific scripting package")

--
-- Create environment variables.
--
local python_dir   = "%{INSTALL_DIR_COMP}"
local python_bin   = "%{INSTALL_DIR_COMP}/bin"
local python_inc   = "%{INSTALL_DIR_COMP}/include"
local python_lib   = "%{INSTALL_DIR_COMP}/lib"
local python_man   = "%{INSTALL_DIR_COMP}/share/man:%{INSTALL_DIR_COMP}/man"

%if "%{comp_fam_name}" == "GNU"
local mkl_lib      = "$MKL_LIB"
local omp_lib      = "$OMP_LIB"
%endif

setenv("TACC_PYTHON_DIR", python_dir)
setenv("TACC_PYTHON_BIN", python_bin)
setenv("TACC_PYTHON_INC", python_inc)
setenv("TACC_PYTHON_LIB", python_lib)
setenv("TACC_PYTHON_MAN", python_man)

prepend_path("PATH", python_bin)
prepend_path("MANPATH", python_man)
prepend_path("LD_LIBRARY_PATH", python_lib)

%if "%{comp_fam_name}" == "GNU"
prepend_path("LD_LIBRARY_PATH", mkl_lib)
prepend_path("LD_LIBRARY_PATH", omp_lib)
%endif

prepend_path("PATH",       "%{INSTALL_DIR_COMP}/bin")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for Python Compiler version %{version}
##
set ModulesVersion "%version"
EOF
%endif

%if "%{build_mpi4py}" == "1"
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua << 'EOF'
inherit()
whatis("Version-notes: Compiler:%{comp_fam_ver}. MPI:%{mpi_fam_ver}")
prepend_path("PATH",       "%{INSTALL_DIR_MPI}/lib/python2.7/site-packages/mpi4py/bin")
prepend_path("PYTHONPATH", "%{INSTALL_DIR_MPI}/lib/python2.7/site-packages")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for Python MPI version %{version}
##
set ModulesVersion "%version"
EOF
%endif

#----------------------------------------------------------
# Lua syntax check 
#----------------------------------------------------------
if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
   echo "testing module file syntax"
   export PATH=$PATH:%{INSTALL_DIR_COMP}/bin/
   $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}/%{version}.lua
   %if "%{build_mpi4py}" == "1"
   	$RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua
   %endif
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{PACKAGE_NAME}
%defattr(-,root,install)

%if "%{build_mpi4py}" == "0"
    %{INSTALL_DIR_COMP}
    %{MODULE_DIR_COMP}
%endif

%if "%{build_mpi4py}" == "1"
    %{INSTALL_DIR_MPI}
    %{MODULE_DIR_MPI}
%endif

%post -n %{PACKAGE_NAME}

%clean


