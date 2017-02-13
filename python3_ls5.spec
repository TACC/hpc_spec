Summary:    Python is a high-level general-purpose programming language.
Name:       tacc-python3 
Version:    3.5.2
Release:    1%{?dist}
License:    GPLv2
Vendor:     Python Software Foundation
Group:      Applications
Packager:   TACC - rtevans@tacc.utexas.edu
#Source:     %{name}-%{version}.tar.gz


#------------------------------------------------
# CONFIGURATION DEFINITIONS
#------------------------------------------------

%define build_interpreter 1
%define build_numpy       1
%define build_scipy       1
%define build_stack       1
#------------------------------------------------
# Either Python package or mpi4py will be built 
# based on this switch
#------------------------------------------------
%define build_mpi4py      0

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

%define PNAME python3
%define MODULE_VAR TACC_PYTHON

%define INSTALL_DIR_COMP %{APPS}/%{comp_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR_COMP %{APPS}/%{comp_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{comp_fam_ver}

%if "%{build_mpi4py}" == "1"
    %define INSTALL_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
    %define MODULE_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
    %define PACKAGE_NAME tacc-mpi4py-%{PNAME}-%{version}-%{comp_fam_ver}-%{mpi_fam_ver}    
%endif

%package -n %{PACKAGE_NAME}
Summary: Python built for TACC systems
Group:   Programming Language

%description
%description -n %{PACKAGE_NAME}
This is intended to be a core Python 3
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
export SRC_DIR=`pwd`/src
mkdir -p ${SRC_DIR}
cd %{_topdir}/SOURCES

export PATH=%{INSTALL_DIR_COMP}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR_COMP}/lib64:%{INSTALL_DIR_COMP}/lib:$LD_LIBRARY_PATH
export PYTHONPATH=%{INSTALL_DIR_COMP}/lib:$PYTHONPATH

%if "%{build_mpi4py}" == "0"
    if ! mountpoint -q %{INSTALL_DIR_COMP} ; then	
        mkdir -p %{INSTALL_DIR_COMP}
        mount -t tmpfs tmpfs %{INSTALL_DIR_COMP}
    fi
%endif
############################################################
# Build core python here
############################################################
%if "%{build_interpreter}" == "1"

if [ ! -f "%{INSTALL_DIR_COMP}/bin/python3" ]; then

    if [ ! -f "%{_topdir}/SOURCES/Python-%{version}.tgz" ]; then
     	wget http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
    fi	
    rm -rf ${SRC_DIR}/Python-%{version}
    tar -xzf %{_topdir}/SOURCES/Python-%{version}.tgz -C ${SRC_DIR}
    cd ${SRC_DIR}/Python-%{version}

    %if "%{comp_fam_name}" == "Intel"
    ./configure --prefix=%{INSTALL_DIR_COMP} CC=icc CXX=icpc LD=xild AR=xiar LIBS='-lpthread -limf -lirc' CFLAGS="-O3 -fp-model strict -fp-model source -axCORE-AVX2,CORE-AVX-I -fma -ipo -prec-div -prec-sqrt" LDFLAGS="-ipo -Xlinker -export-dynamic" CPPFLAGS="" CPP="icc -E" --with-system-ffi --enable-shared --with-pth --with-threads --without-gcc --with-libm=-limf --with-cxx-main=icpc
    %endif
    %if "%{comp_fam_name}" == "GNU"
    ./configure --prefix=%{INSTALL_DIR_COMP} CFLAGS="-march=ivybridge -mtune=haswell -flto -ffat-lto-objects" LDFLAGS="-Xlinker -export-dynamic -march=ivybridge -mtune=haswell -flto -ffat-lto-objects" --with-system-ffi --enable-shared --with-pth --with-threads
    %endif

    make -j 4
    make sharedinstall
    make -i install
    #############################################################
    # setuptools and pip
    ############################################################
    cd ${SRC_DIR}

    ############################################################
    # core python 3 modules
    ############################################################
#    wget https://bootstrap.pypa.io/get-pip.py
#    %{INSTALL_DIR_COMP}/bin/python get-pip.py
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org certifi
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org nose
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org virtualenv
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org virtualenvwrapper    
    
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org sympy
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org brewer2mpl
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org futures
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org simpy
    
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org jsonpickle
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org meld3
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org supervisor
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org paramiko
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org egenix-mx-base

fi
%endif

#############################################################
# scipy stack: use INSTALL_DIR_COMP . 
# We need to know which pip3 modules are compiler specific.  
# numpy scipy matplotlib jupyter pandas sympy nose
############################################################
%if "%{comp_fam_name}" == "GNU"	
    module load mkl
%endif

### Numpy
%if "%{build_numpy}" == "1"

    if ! $(%{INSTALL_DIR_COMP}/bin/python3 -c "import numpy"); then
	cd %{_topdir}/SOURCES	
	if [ ! -f "%{_topdir}/SOURCES/numpy-1.11.1.tar.gz" ]; then	
	    wget https://sourceforge.net/projects/numpy/files/NumPy/1.11.1/numpy-1.11.1.tar.gz
	fi	   
	
	rm -rf ${SRC_DIR}/numpy-1.11.1 	   
	tar -xzvf %{_topdir}/SOURCES/numpy-1.11.1.tar.gz -C ${SRC_DIR}	
	cd ${SRC_DIR}/numpy-1.11.1

	%if "%{comp_fam_name}" == "Intel"
	echo "[mkl]
library_dirs = ${MKLROOT}/lib/intel64
include_dirs = ${MKLROOT}/include
mkl_libs = mkl_rt
lapack_libs = " > site.cfg
	%{INSTALL_DIR_COMP}/bin/python3 setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
	%endif

	%if "%{comp_fam_name}" == "GNU"	
	echo "[mkl]
library_dirs = ${TACC_MKL_LIB}:${TACC_GCC_LIB64}
include_dirs = ${TACC_MKL_INC}
mkl_libs = mkl_def, mkl_intel_lp64, mkl_core, mkl_gnu_thread, mkl_avx, gomp
lapack_libs = mkl_def, mkl_intel_lp64, mkl_core, mkl_gnu_thread, mkl_avx, gomp" > site.cfg	
	%{INSTALL_DIR_COMP}/bin/python3 setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
	%endif
    fi
%endif

### Scipy Module
%if "%{build_scipy}" == "1"
    if ! $(%{INSTALL_DIR_COMP}/bin/python3 -c "import scipy"); then
	cd %{_topdir}/SOURCES	
	if [ ! -f "%{_topdir}/SOURCES/scipy-0.18.1.tar.gz" ]; then	
	    wget -O scipy-0.18.1.tar.gz https://github.com/scipy/scipy/releases/download/v0.18.1/scipy-0.18.1.tar.gz
	fi	   

	rm -rf ${SRC_DIR}/scipy-0.18.1
	tar -xzvf scipy-0.18.1.tar.gz -C ${SRC_DIR} 
	cd ${SRC_DIR}/scipy-0.18.1
	
	%if "%{comp_fam_name}" == "Intel"
	%{INSTALL_DIR_COMP}/bin/python3 setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install
	%endif
	
	%if "%{comp_fam_name}" == "GNU"	
        %{INSTALL_DIR_COMP}/bin/python3 setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install
	%endif
    fi
%endif

%if "%{build_stack}" == "1"
    ### Matplotlib
    if ! $(%{INSTALL_DIR_COMP}/bin/python3 -c "import matplotlib"); then
	%{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: pyparsing	
	%{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: cycler	
	%{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: pytz
	%{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: python-dateutil
	%{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: matplotlib
    fi

    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: cython	
# doesn't work on ls5 - no ffi    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: cffi	
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: pandas
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: psutil
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: numexpr
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: rpyc	
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: ipython
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org jupyter	
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: mako
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: lxml
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: pystuck
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: fortran-magic
#    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: MySQL
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: psycopg2
#    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: mercurial
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: yt
    %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: theano
    CFLAGS="-O2" %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: scikit_learn

    if module load hdf5; then
       export HDF5_DIR=$TACC_HDF5_DIR	
       export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$TACC_HDF5_LIB
       %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: nose
       %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: pkgconfig
       %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: h5py
       %{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: tables
    fi
%endif

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
	%{INSTALL_DIR_COMP}/bin/pip3 install --trusted-host pypi.python.org --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_MPI}" mpi4py
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
This is the Python 3 package built on %(date +'%B %d, %Y').

You can install your own modules (choose one method):
        1. python3 setup.py install --user
        2. python3 setup.py install --home=<dir>
        3. pip3 install --user module-name

Version %{version}
]]
)

whatis("Name: Python3")
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
local mkl_lib      = "/opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/mkl/lib/intel64"
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
#####------- MPI version

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}
cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua << 'EOF'
help(
[[
This is the Python 3 package built on %(date +'%B %d, %Y').

You can install your own modules (choose one method):
	1. python3 setup.py install --user
	2. python3 setup.py install --home=<dir>
	3. pip3 install --user module-name

Version %{version}
]]
)

whatis("Name: Python3")
whatis("Version: %{version}")
whatis("Version-notes: Compiler:%{comp_fam_ver}. MPI:%{mpi_fam_ver}")
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
local mkl_lib      = "/opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/mkl/lib/intel64"
%endif

setenv("TACC_PYTHON_DIR", python_dir)
setenv("TACC_PYTHON_BIN", python_bin)
setenv("TACC_PYTHON_INC", python_inc)
setenv("TACC_PYTHON_LIB", python_lib)
setenv("TACC_PYTHON_MAN", python_man)

prepend_path("MANPATH", python_man)
prepend_path("LD_LIBRARY_PATH", python_lib)

%if "%{comp_fam_name}" == "GNU"
prepend_path("LD_LIBRARY_PATH", mkl_lib)
%endif


prepend_path("PATH",       "%{INSTALL_DIR_COMP}/bin")
prepend_path("PYTHONPATH", "%{INSTALL_DIR_MPI}/lib/python3.5/site-packages")
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

