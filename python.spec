Summary:    Python is a high-level general-purpose programming language.

%include python-defines.inc

Name:       tacc-python%{python_major_version}
Version:    %{python_module_version}
Release:    1%{?dist}
License:    GPLv2
Vendor:     Python Software Foundation
Group:      Applications
Packager:   TACC - rtevans@tacc.utexas.edu


%global _python_bytecompile_errors_terminate_build 0

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc

#------------------------------------------------
# Either Python package w/o mpi4py or just mpi4py 
# will be built based on if mpiV is defined
#------------------------------------------------
%if %{defined mpiV}
    %include mpi-defines.inc
%endif	

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/python%{python_major_version}/%{version}
%define MODULE_DIR %{APPS}/%{comp_fam_ver}/%{MODULES}/python%{python_major_version}
%define PACKAGE_NAME %{name}-%{comp_fam_ver}

%if %{defined mpiV}
    %define INSTALL_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/python%{python_major_version}/%{version}
    %define MODULE_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/python%{python_major_version}
    %define PACKAGE_NAME tacc-mpi4py-%{comp_fam_ver}-%{mpi_fam_ver}-python%{python_major_version}
%endif

%package -n %{PACKAGE_NAME}

Summary: Python built for TACC systems
Group:   Programming Language

%description

%description -n %{PACKAGE_NAME}
This is intended to be a core Python
interpreter for TACC systems.

%prep

%build

%install

export BASH_ENV=/etc/tacc/tacc_functions
%include system-load.inc
%include compiler-load.inc

export PATH=%{INSTALL_DIR}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR}/lib64:%{INSTALL_DIR}/lib:$LD_LIBRARY_PATH
export PIP=%{INSTALL_DIR}/bin/pip%{python_major_version}
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
    %include compiler-load.inc   
    export LD_LIBRARY_PATH=${MKL_LIB}:${OMP_LIB}:${LD_LIBRARY_PATH}
%endif

############################################################
# Build core python here
############################################################

if [ ! -f "%{INSTALL_DIR}/bin/python%{python_major_version}" ]; then
    if ! mountpoint -q %{INSTALL_DIR} ; then	
        mkdir -p %{INSTALL_DIR}
        mount -t tmpfs tmpfs %{INSTALL_DIR}
    fi
    echo `which strip`
    if [ ! -f "%{_topdir}/BUILD/Python-%{version}.tgz" ]; then
     	wget http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
    fi	
    rm -rf %{_topdir}/SOURCES/Python-%{version}
    tar -xzf %{_topdir}/BUILD/Python-%{version}.tgz -C %{_topdir}/SOURCES
    cd %{_topdir}/SOURCES/Python-%{version}
    export LD_LIBRARY_PATH=`pwd`:$LD_LIBRARY_PATH
    ls

    %if "%{comp_fam_name}" == "Intel"
    ./configure --prefix=%{INSTALL_DIR} CC=icc CXX=icpc LD=xild AR=xiar LIBS='-lpthread -limf -lirc -lssp' CXXFLAGS="-std=c++11" CFLAGS="-Wformat -Wformat-security -D_FORTIFY_SOURCE=2 -fstack-protector -fwrapv -fpic -O3" LDFLAGS="-Xlinker -export-dynamic" CPPFLAGS="" CPP="icc -E" --with-system-ffi --with-cxx-main=icpc --enable-shared --with-pth --without-gcc --with-libm=-limf --with-threads --with-lto --enable-optimizations --with-computed-gotos --with-ensurepip --enable-unicode=ucs4    
    %endif
    %if "%{comp_fam_name}" == "GNU"
    ./configure --prefix=%{INSTALL_DIR} CC=gcc CXX=g++ LD=ld AR=ar LIBS='-lpthread' CFLAGS="-Wp,-D_FORTIFY_SOURCE=2 -fexceptions --param=ssp-buffer-size=4 -grecord-gcc-switches -fwrapv -fpic -O2" LDFLAGS="-fpic -Xlinker -export-dynamic" --with-system-ffi --enable-shared --with-pth --with-threads --with-ensurepip --with-computed-gotos --with-lto --enable-unicode=ucs4
    %endif

    make -j 24
    make sharedinstall
    make -i install
fi

############################################################
# core python modules
############################################################
if [ ! -f "%{INSTALL_DIR}/bin/pip%{python_major_version}" ]; then
    wget https://bootstrap.pypa.io/get-pip.py
    %{INSTALL_DIR}/bin/python%{python_major_version} get-pip.py
fi
${PIP} install --upgrade pip
${PIP} install --trusted-host pypi.python.org certifi
${PIP} install nose
${PIP} install pytest
${PIP} install virtualenv
${PIP} install virtualenvwrapper    
${PIP} install sympy
${PIP} install brewer2mpl
%if "%{python_major_version}" == "2"
${PIP} install futures
%endif

${PIP} install simpy    
${PIP} install jsonpickle
${PIP} install meld3

${PIP} install paramiko

${PIP} install pybind11
${PIP} install --upgrade pip
${PIP} install --upgrade setuptools
#############################################################
# scipy stack: use INSTALL_DIR . 
# We need to know which pip modules are compiler specific.  
# numpy scipy matplotlib jupyter pandas sympy
############################################################

CFLAGS="-O2" ${PIP} install --no-binary :all: Cython	

### Numpy
if ! $(%{INSTALL_DIR}/bin/python%{python_major_version} -c "import numpy"); then
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/numpy-1.18.1.tar.gz" ]; then	
	wget https://github.com/numpy/numpy/releases/download/v1.18.1/numpy-1.18.1.tar.gz
    fi	   
    
    rm -rf %{_topdir}/SOURCES/numpy-1.18.1 	   
    tar -xzvf %{_topdir}/SOURCES/numpy-1.18.1.tar.gz -C %{_topdir}/SOURCES	
    cd %{_topdir}/SOURCES/numpy-1.18.1

    echo "[mkl]
library_dirs = ${MKL_LIB}:${OMP_LIB}
include_dirs = ${MKL_INC}
mkl_libs = mkl_rt
lapack_libs = " > site.cfg

    %if "%{comp_fam_name}" == "Intel"
    sed -i 's/-O3/-O3 %{TACC_OPT}/' numpy/distutils/intelccompiler.py
    sed -i 's/-m64/-g/' numpy/distutils/intelccompiler.py
    sed -i 's/-O1/-O1 %{TACC_OPT} -fPIC/' numpy/distutils/fcompiler/intel.py    
    sed -i 's/check_output(version_cmd)/check_output(version_cmd, stderr=subprocess.STDOUT)/' numpy/distutils/ccompiler.py

    %{INSTALL_DIR}/bin/python%{python_major_version} setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
    %endif
    %if "%{comp_fam_name}" == "GNU"
    %{INSTALL_DIR}/bin/python%{python_major_version} setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
    %endif
fi

### Scipy
pip uninstall scipy
if ! $(%{INSTALL_DIR}/bin/python%{python_major_version} -c "import scipy"); then
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/scipy-1.2.3.tar.gz" ]; then	
	wget -O scipy-1.2.3.tar.gz https://github.com/scipy/scipy/releases/download/v1.2.3/scipy-1.2.3.tar.gz
    fi	   

    rm -rf %{_topdir}/SOURCES/scipy-1.2.3
    tar -xzvf scipy-1.2.3.tar.gz -C %{_topdir}/SOURCES	 
    cd %{_topdir}/SOURCES/scipy-1.2.3

    %if "%{comp_fam_name}" == "Intel"
    %{INSTALL_DIR}/bin/python%{python_major_version} setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
    %endif
    %if "%{comp_fam_name}" == "GNU"
    %{INSTALL_DIR}/bin/python%{python_major_version} setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
    %endif
fi

${PIP} install wheel
${PIP} install --no-binary :all: pycairo
${PIP} install --no-binary :all: PyGObject
${PIP} install --no-binary :all: matplotlib
${PIP} install --no-binary :all: cffi	
CFLAGS="-O2" ${PIP} install --no-binary :all: pandas
${PIP} install --no-binary :all: psutil
${PIP} install --no-binary :all: numexpr
${PIP} install --no-binary :all: rpyc	
${PIP} install jupyter	
${PIP} install --no-binary :all: mako
CFLAGS="-O2" ${PIP} install --no-binary :all: lxml
${PIP} install --no-binary :all: pystuck
${PIP} install --no-binary :all: PyMySQL
${PIP} install --no-binary :all: psycopg2
%if "%{python_major_version}" == "2"
     ${PIP} install --no-binary :all: mercurial
%endif
#CFLAGS="-O0" ${PIP} install --no-binary :all: yt
${PIP} install --no-binary :all: theano
${PIP} install --no-binary :all: ply
${PIP} install --no-binary :all: PyYAML
#CFLAGS="-O2" ${PIP} install --no-binary :all: scikit_learn

if module load hdf5; then
    HDF5_DIR=$TACC_HDF5_DIR ${PIP} install --no-binary :all: h5py
    ${PIP} install --no-binary :all: tables 
fi
#############################################################
# mpi4py: use INSTALL_DIR_MPI
############################################################
%if %{defined mpiV}
  if ! mountpoint -q %{INSTALL_DIR_MPI} ; then	
    mkdir -p %{INSTALL_DIR_MPI}
    mount -t tmpfs tmpfs %{INSTALL_DIR_MPI}
  fi
  module load python%{python_major_version}/%{version}	
  module load %{mpi_module}   
  ${PIP} install --no-binary :all: --prefix=%{INSTALL_DIR_MPI} mpi4py

  if module load phdf5; then
      export PYTHONPATH=%{INSTALL_DIR_MPI}/lib/python%{python_major_version}.%{python_minor_version}/site-packages
      CC="mpicc" HDF5_MPI="ON" HDF5_DIR=$TACC_HDF5_DIR ${PIP} install --no-binary=h5py --no-deps --prefix=%{INSTALL_DIR_MPI} --ignore-installed h5py
      #${PIP} install tables
  fi
%endif

find %{INSTALL_DIR} -name '*.py' | xargs sed -i '1s|/usr/bin/python|%{INSTALL_DIR}/bin/python%{python_major_version}|'
find %{INSTALL_DIR} -name '*.py' | xargs sed -i '1s|/usr/local/bin/python|%{INSTALL_DIR}/bin/python%{python_major_version}|'

#----------------------------------------------------------
# Copy into rpm directory
#----------------------------------------------------------
# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.

#----------------------------------------------------------
# UNMOUNT THE TEMP FILESYSTEM
#----------------------------------------------------------

%if %{undefined mpiV}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
    if mountpoint -q %{INSTALL_DIR} ; then	
	umount %{INSTALL_DIR}
    fi
%endif

%if %{defined mpiV}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
    cp -r %{INSTALL_DIR_MPI}/ $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}/..
    if mountpoint -q %{INSTALL_DIR_MPI} ; then	
	umount %{INSTALL_DIR_MPI}
    fi
%endif


#----------------------------------------------------------
# Create the module file for the Python installation 
#----------------------------------------------------------
%if %{undefined mpiV}
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{APPS}/%{comp_fam_ver}/python%{python_label}/modulefiles
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << EOF
help(
[[
This is the Python%{python_major_version} package built on %(date +'%B %d, %Y').

You can install your own modules (choose one method):
        1. python%{python_major_version} setup.py install --user
        2. python%{python_major_version} setup.py install --home=<dir>
        3. pip%{python_major_version} install --user module-name

Version %{version}
]]
)

whatis("Name: Python%{python_major_version}")
whatis("Version: %{version}")
whatis("Version-notes: Compiler:%{comp_fam_ver}")
whatis("Category: Applications, Scientific, Graphics")
whatis("Keywords: Applications, Scientific, Graphics, Scripting Language")
whatis("URL: http://www.python.org/")
whatis("Description: scientific scripting package")

--
-- Create environment variables.
--
local python_dir   = "%{INSTALL_DIR}"
local python_bin   = "%{INSTALL_DIR}/bin"
local python_inc   = "%{INSTALL_DIR}/include"
local python_lib   = "%{INSTALL_DIR}/lib"
local python_man   = "%{INSTALL_DIR}/share/man:%{INSTALL_DIR}/man"

%if "%{comp_fam_name}" == "GNU"
local mkl_lib      = "${MKL_LIB}"
local omp_lib      = "${OMP_LIB}"
%endif

setenv("TACC_PYTHON_DIR", python_dir)
setenv("TACC_PYTHON_BIN", python_bin)
setenv("TACC_PYTHON_INC", python_inc)
setenv("TACC_PYTHON_LIB", python_lib)
setenv("TACC_PYTHON_MAN", python_man)
setenv("TACC_PYTHON_VER", "%{python_major_version}.%{python_minor_version}")

prepend_path("PATH", python_bin)
prepend_path("MANPATH", python_man)
prepend_path("LD_LIBRARY_PATH", python_lib)
prepend_path("MODULEPATH", "%{APPS}/%{comp_fam_ver}/python%{python_label}/modulefiles")

%if "%{comp_fam_name}" == "GNU"
prepend_path("LD_LIBRARY_PATH", mkl_lib)
prepend_path("LD_LIBRARY_PATH", omp_lib)
%endif

prepend_path("PATH",       "%{INSTALL_DIR}/bin")
family("python")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for Python %{python_major_version} Compiler version %{version}
##
set ModulesVersion "%version"
EOF

%endif

#----------------------------------------------------------
# Create the module file for the mpi4py installation 
#----------------------------------------------------------
%if %{defined mpiV}

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}
mkdir -p $RPM_BUILD_ROOT/%{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/python%{python_label}/modulefiles

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua << 'EOF'
inherit()
whatis("Version-notes: Compiler:%{comp_fam_ver}. MPI:%{mpi_fam_ver}")
prepend_path("PYTHONPATH", "%{INSTALL_DIR_MPI}/lib/python%{python_major_version}.%{python_minor_version}/site-packages")
prepend_path("MODULEPATH", "%{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/python%{python_label}/modulefiles")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for Python %{python_major_version} MPI version %{version}
##
set ModulesVersion "%version"
EOF
%endif

#----------------------------------------------------------
# Lua syntax check 
#----------------------------------------------------------
if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
   echo "testing module file syntax"
   export PATH=$PATH:%{INSTALL_DIR}/bin/
   %if %{undefined mpiV}
       $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
   %endif
   %if %{defined mpiV}
       $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua
   %endif
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{PACKAGE_NAME}
%defattr(-,root,install)

%if %{undefined mpiV}
    %{INSTALL_DIR}
    %{MODULE_DIR}
    %{APPS}/%{comp_fam_ver}/python%{python_label}/modulefiles
%endif

%if %{defined mpiV}
    %{INSTALL_DIR_MPI}
    %{MODULE_DIR_MPI}
    %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/python%{python_label}/modulefiles
%endif

%post -n %{PACKAGE_NAME}

%clean


