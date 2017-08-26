Summary:    Python is a high-level general-purpose programming language.
Name:       tacc-python 
Version:    2.7.13
Release:    4%{?dist}
License:    GPLv2
Vendor:     Python Software Foundation
Group:      Applications
Packager:   TACC - rtevans@tacc.utexas.edu

#------------------------------------------------
# Either Python package or mpi4py will be built 
# based on this switch
#------------------------------------------------
%define build_mpi4py     0
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

export PATH=%{INSTALL_DIR_COMP}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR_COMP}/lib64:%{INSTALL_DIR_COMP}/lib:$LD_LIBRARY_PATH
export PIP=%{INSTALL_DIR_COMP}/bin/pip
############################################################
# System Specific Libraries
############################################################
%if "%{comp_fam_name}" == "Intel"
    export MKL_INC=${TACC_MKL_INC}
    export MKL_LIB=${TACC_MKL_LIB}
    export OMP_LIB=${ICC_LIB}
%endif
%if "%{comp_fam_name}" == "GNU"
    ml intel
    export MKL_INC=${TACC_MKL_INC}
    export MKL_LIB=${TACC_MKL_LIB}
    export OMP_LIB=${ICC_LIB}
    ml gcc
    export LD_LIBRARY_PATH=${MKL_LIB}:${OMP_LIB}:${LD_LIBRARY_PATH}
%endif

############################################################
# Build core python here
############################################################

if [ ! -f "%{INSTALL_DIR_COMP}/bin/%{PNAME}" ]; then
    if ! mountpoint -q %{INSTALL_DIR_COMP} ; then	
        mkdir -p %{INSTALL_DIR_COMP}
        mount -t tmpfs tmpfs %{INSTALL_DIR_COMP}
    fi

    if [ ! -f "%{_topdir}/SOURCES/Python-%{version}.tgz" ]; then
     	wget http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
    fi	
    rm -rf %{_topdir}/SOURCES/Python-%{version}
    tar -xzf %{_topdir}/SOURCES/Python-%{version}.tgz -C %{_topdir}/SOURCES
    cd %{_topdir}/SOURCES/Python-%{version}
    export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH
    ls

    %if "%{comp_fam_name}" == "Intel"
    #./configure --prefix=%{INSTALL_DIR_COMP} CC=icc CXX=icpc LD=xild AR=xiar LIBS='-lpthread -limf -lirc' CFLAGS="-O3 -fp-model strict -fp-model source -ipo -prec-div -prec-sqrt %{TACC_OPT}" LDFLAGS="-ipo -Xlinker -export-dynamic" CPPFLAGS="" CPP="icc -E" --with-system-ffi --with-cxx-main=icpc --enable-shared --with-pth --without-gcc --with-libm=-limf --with-threads --with-lto --enable-optimizations --with-computed-gotos --with-ensurepip --enable-unicode=ucs4    
    ./configure --prefix=%{INSTALL_DIR_COMP} CC=icc CXX=icpc LD=xild AR=xiar LIBS='-lpthread -limf -lirc -lssp' CFLAGS="-Wformat -Wformat-security -D_FORTIFY_SOURCE=2 -fstack-protector -fwrapv -fpic -O3" LDFLAGS="-Xlinker -export-dynamic" CPPFLAGS="" CPP="icc -E" --with-system-ffi --with-cxx-main=icpc --enable-shared --with-pth --without-gcc --with-libm=-limf --with-threads --with-lto --enable-optimizations --with-computed-gotos --with-ensurepip --enable-unicode=ucs4    
    %endif
    %if "%{comp_fam_name}" == "GNU"
    ./configure --prefix=%{INSTALL_DIR_COMP} CFLAGS="-flto -ffat-lto-objects -fuse-linker-plugin %{TACC_OPT}" LDFLAGS="-fPIC -flto -ffat-lto-objects -fuse-linker-plugin -rdynamic" --with-system-ffi --enable-shared --with-pth --with-threads --with-lto --with-computed-gotos --with-ensurepip --enable-unicode=ucs4          
    %endif

    make -j 1
    make sharedinstall
    make -i install
fi

############################################################
# core python modules
############################################################
if [ ! -f "%{INSTALL_DIR_COMP}/bin/pip" ]; then
    wget https://bootstrap.pypa.io/get-pip.py
    %{INSTALL_DIR_COMP}/bin/%{PNAME} get-pip.py
fi
${PIP} install --trusted-host pypi.python.org certifi
${PIP} install nose
${PIP} install virtualenv
${PIP} install virtualenvwrapper    
${PIP} install sympy
${PIP} install brewer2mpl
${PIP} install futures
${PIP} install simpy    
${PIP} install jsonpickle
${PIP} install meld3
${PIP} install supervisor
${PIP} install paramiko
${PIP} install readline
${PIP} install egenix-mx-base

#############################################################
# scipy stack: use INSTALL_DIR_COMP . 
# We need to know which pip modules are compiler specific.  
# numpy scipy matplotlib jupyter pandas sympy
############################################################

### Numpy
if ! $(%{INSTALL_DIR_COMP}/bin/%{PNAME} -c "import numpy"); then
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/numpy-1.12.1.tar.gz" ]; then	
	wget https://github.com/numpy/numpy/releases/download/v1.12.1/numpy-1.12.1.tar.gz
    fi	   
    
    rm -rf %{_topdir}/SOURCES/numpy-1.12.1 	   
    tar -xzvf %{_topdir}/SOURCES/numpy-1.12.1.tar.gz -C %{_topdir}/SOURCES	
    cd %{_topdir}/SOURCES/numpy-1.12.1

    sed -i 's/-openmp/-fopenmp '"%{TACC_OPT}"'/' numpy/distutils/intelccompiler.py
    sed -i 's/-openmp/-fopenmp '"%{TACC_OPT}"'/' numpy/distutils/fcompiler/intel.py
    echo "[mkl]
library_dirs = ${MKL_LIB}:${OMP_LIB}
include_dirs = ${MKL_INC}
mkl_libs = mkl_rt
lapack_libs = " > site.cfg

    %if "%{comp_fam_name}" == "Intel"
    %{INSTALL_DIR_COMP}/bin/%{PNAME} setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
    %endif
    %if "%{comp_fam_name}" == "GNU"
    %{INSTALL_DIR_COMP}/bin/%{PNAME} setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
    %endif
fi

### Scipy
if ! $(%{INSTALL_DIR_COMP}/bin/%{PNAME} -c "import scipy"); then
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/scipy-0.19.0.tar.gz" ]; then	
	wget -O scipy-0.19.0.tar.gz https://github.com/scipy/scipy/releases/download/v0.19.0/scipy-0.19.0.tar.gz
    fi	   

    rm -rf %{_topdir}/SOURCES/scipy-0.19.0
    tar -xzvf scipy-0.19.0.tar.gz -C %{_topdir}/SOURCES	 
    cd %{_topdir}/SOURCES/scipy-0.19.0

    %if "%{comp_fam_name}" == "Intel"
    %{INSTALL_DIR_COMP}/bin/%{PNAME} setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
    %endif
    %if "%{comp_fam_name}" == "GNU"
    %{INSTALL_DIR_COMP}/bin/%{PNAME} setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
    %endif
fi

### pycairo
if ! $(%{INSTALL_DIR_COMP}/bin/%{PNAME} -c "import cairo"); then
    if [ ! -f "%{_topdir}/SOURCES/pycairo-1.15.0.tar.gz" ]; then		
	wget -O pycairo-1.15.0.tar.gz https://github.com/pygobject/pycairo/releases/download/v1.15.0/pycairo-1.15.0.tar.gz
    fi
    rm -rf %{_topdir}/SOURCES/pycairo-1.15.0.tar.gz
    tar -xzvf pycairo-1.15.0.tar.gz -C %{_topdir}/SOURCES	 
    cd %{_topdir}/SOURCES/pycairo-1.15.0
    python setup.py install --prefix=%{INSTALL_DIR_COMP}
fi	   

### pygobject
if ! $(%{INSTALL_DIR_COMP}/bin/%{PNAME} -c "import gobject"); then
    if [ ! -f "%{_topdir}/SOURCES/" ]; then		
	wget -O pygobject-2.28.6.tar.xz http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.6.tar.xz
    fi
    rm -rf %{_topdir}/SOURCES/pygobject-2.28.6
    tar xvf pygobject-2.28.6.tar.xz -C %{_topdir}/SOURCES	 
    cd %{_topdir}/SOURCES/pygobject-2.28.6
    sed -i 's/case GI_INFO_TYPE_ERROR_DOMAIN:/ /' gi/pygi-info.c
    ./configure --prefix=%{INSTALL_DIR_COMP}; make; make install   
fi	   

### pygtk
if ! $(%{INSTALL_DIR_COMP}/bin/%{PNAME} -c "import pygtk"); then
    if [ ! -f "%{_topdir}/SOURCES/pygtk-2.24.0.tar.gz" ]; then		
	wget -O pygtk-2.24.0.tar.gz http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.gz
    fi
    rm -rf %{_topdir}/SOURCES/pygtk-2.24.0
    tar -xzvf pygtk-2.24.0.tar.gz -C %{_topdir}/SOURCES	 
    cd %{_topdir}/SOURCES/pygtk-2.24.0
    ./configure --prefix=%{INSTALL_DIR_COMP}; make; make install   
fi	   


${PIP} install --no-binary :all: matplotlib	
CFLAGS="-O2" ${PIP} install --no-binary :all: cython	
${PIP} install --no-binary :all: cffi	
CFLAGS="-O2" ${PIP} install --no-binary :all: pandas
${PIP} install --no-binary :all: psutil
${PIP} install --no-binary :all: numexpr
${PIP} install --no-binary :all: rpyc	
${PIP} install --no-binary :all: ipython
${PIP} install jupyter	
${PIP} install --no-binary :all: mako
CFLAGS="-O2" ${PIP} install --no-binary :all: lxml
${PIP} install --no-binary :all: pystuck
${PIP} install --no-binary :all: fortran-magic
${PIP} install --no-binary :all: MySQL
${PIP} install --no-binary :all: psycopg2
${PIP} install --no-binary :all: mercurial
#CFLAGS="-O0" ${PIP} install --no-binary :all: yt
${PIP} install --no-binary :all: theano
${PIP} install --no-binary :all: ply
CFLAGS="-O2" ${PIP} install --no-binary :all: scikit_learn

#if module load hdf5; then
#    ${PIP} install h5py
#    ${PIP} install tables
#fi
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
  ${PIP} install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_MPI}" mpi4py

  if module load phdf5; then
      export PYTHONPATH=%{INSTALL_DIR_MPI}/lib/python2.7/site-packages
      CC="mpicc -ip-no-inlining" HDF5_MPI="ON" HDF5_DIR=$TACC_HDF5_DIR ${PIP} install --no-binary=h5py --no-deps --install-option="--prefix=%{INSTALL_DIR_MPI}" --ignore-installed h5py
      ${PIP} install tables
  fi
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

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}/%{version}.lua << EOF
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
local mkl_lib      = "${MKL_LIB}"
local omp_lib      = "${OMP_LIB}"
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


