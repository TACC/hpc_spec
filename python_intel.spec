Summary:    Python is a high-level general-purpose programming language.
Name:       tacc-python 
Version:    2.7.10
Release:    2
License:    GPLv2
Vendor:     Python Software Foundation
Group:      Applications
Packager:   TACC - rtevans@tacc.utexas.edu
#Source:     %{name}-%{version}.tar.gz


#------------------------------------------------
# CONFIGURATION DEFINITIONS
#------------------------------------------------

%define build_python_version 1
%define build_comp_version 1
%define build_mpi_version 1
#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc
%include mpi-defines.inc


%define PNAME python
%define MODULE_VAR TACC_PYTHON

%define APPS /opt/apps

%define INSTALL_DIR_COMP %{APPS}/%{comp_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR_COMP %{APPS}/%{comp_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{comp_fam_ver}

%if "%{build_mpi_version}" == "1"
    %define INSTALL_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
    %define MODULE_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
    %define PACKAGE_NAME %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%endif

%package -n %{PACKAGE_NAME}
Summary: Python built with Intel Compilers
Group:   Programming Language

%description
%description -n %{PACKAGE_NAME}
This is intended to be the core Python
interpreter for the TACC systems.

%prep

%if "%{build_comp_version}" == "1"
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
%endif

%if "%{build_mpi_version}" == "1"
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
%endif

%build

%install

%include system-load.inc
#ml taccswitch
#source taccswitch
module load %{comp_module}
echo COMPILER LOAD: %{comp_module}

WD=`pwd`
export WD
# Set up src directory
export SRC_DIR=${WD}/src
mkdir -p ${SRC_DIR}
cd %{_topdir}/SOURCES
echo %{_topdir}/SOURCES

############################################################
# Install python here
############################################################
%if "%{build_python_version}" == "1"
     mkdir -p %{INSTALL_DIR_COMP}
     mount -t tmpfs tmpfs %{INSTALL_DIR_COMP}

     if [ ! -f "%{_topdir}/SOURCES/Python-%{version}.tgz" ]; then
	wget http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
     fi	
     rm -rf ${SRC_DIR}/Python-%{version}
     tar -xzf %{_topdir}/SOURCES/Python-%{version}.tgz -C ${SRC_DIR}
     cd ${SRC_DIR}/Python-%{version}

     ./configure --prefix=%{INSTALL_DIR_COMP} CC=icc CXX=icpc CFLAGS="-ipo -fPIC -mkl -O3 -fp-model strict -fomit-frame-pointer -axCORE-AVX2,CORE-AVX-I" CPPFLAGS="-ipo -fPIC -mkl -O3 -fp-model strict -fomit-frame-pointer -axCORE-AVX2,CORE-AVX-I" LDFLAGS="-ipo -fp-model strict -fomit-frame-pointer -axCORE-AVX2,CORE-AVX-I -lpthread -mkl" --with-system-ffi --with-cxx-main=icpc --enable-shared --with-pth
     make -j 16
     make sharedinstall
     make -i install
%endif

export PATH=%{INSTALL_DIR_COMP}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR_COMP}/lib64:%{INSTALL_DIR_COMP}/lib:$LD_LIBRARY_PATH
export PYTHONPATH=%{INSTALL_DIR_COMP}/lib/python2.7/site-packages:$PYTHONPATH

#############################################################
# setuptools and pip
############################################################
%if "%{build_python_version}" == "1"
     cd ${SRC_DIR}
     wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py
     python ez_setup.py --insecure
     easy_install certifi
     cd ${SRC_DIR}
     easy_install pip
%endif

############################################################
# compiler independent modules (pure python)
############################################################
%if "%{build_comp_version}" == "1"
    pip install nose
    pip install virtualenv
    pip install virtualenvwrapper    

    pip install sympy
    pip install brewer2mpl
    pip install futures
    pip install simpy

    pip install pystuck
    pip install jsonpickle
    pip install meld3
    pip install supervisor
    pip install paramiko

#############################################################
# scipy stack: use INSTALL_DIR_COMP . 
# We need to know which pip modules are compiler specific.  
# numpy scipy matplotlib ipython pandas sympy nose
############################################################

    ### Numpy
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/numpy-1.9.1.tar.gz" ]; then	
       wget http://sourceforge.net/projects/numpy/files/NumPy/1.9.1/numpy-1.9.1.tar.gz
    fi	   
   
    rm -rf ${SRC_DIR}/numpy-1.9.1 
    tar -xzvf %{_topdir}/SOURCES/numpy-1.9.1.tar.gz -C ${SRC_DIR}
    cd ${SRC_DIR}/numpy-1.9.1
    pwd

echo "[mkl]
library_dirs = ${MKLROOT}/lib/intel64
include_dirs = ${MKLROOT}/include
mkl_libs = mkl_rt
lapack_libs = " > site.cfg

    sed -i 's/-m64/-O3 -g -fp-model strict -fPIC -fomit-frame-pointer -openmp -axCORE-AVX2,CORE-AVX-I/' numpy/distutils/intelccompiler.py

    sed -i 's/-xhost/-axCORE-AVX2,CORE-AVX-I/' numpy/distutils/fcompiler/intel.py


    %{INSTALL_DIR_COMP}/bin/python setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install --prefix=%{INSTALL_DIR_COMP}

    echo $LD_LIBRARY_PATH

    ### Scipy Libraries
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/scipy-0.15.0.tar.gz" ]; then	
       wget http://sourceforge.net/projects/scipy/files/scipy/0.15.0/scipy-0.15.0.tar.gz
    fi	   

    rm -rf ${SRC_DIR}/scipy-0.15.0
    tar -xzvf scipy-0.15.0.tar.gz -C ${SRC_DIR} 
    cd ${SRC_DIR}/scipy-0.15.0

    %{INSTALL_DIR_COMP}/bin/python setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install --prefix=%{INSTALL_DIR_COMP}

    ### Matplotlib
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/matplotlib-1.5.0.tar.gz" ]; then		
       wget https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.5.0/matplotlib-1.5.0.tar.gz
    fi

    rm -rf ${SRC_DIR}/matplotlib-1.5.0
    tar -xzvf matplotlib-1.5.0.tar.gz -C ${SRC_DIR}
    cd ${SRC_DIR}/matplotlib-1.5.0

    # Need to modify minimum freetype from 2.4 -> 2.3.  matplotlib docs suggest this
    sed -i 's/min_version='\''2.4'\''/min_version='\''2.3'\''/' setupext.py
    # There is a bug in matplotlib for intel compilers - fix it here
    sed -i 's/defined(__INTEL_COMPILER)/defined(__BROKEN)/' extern/qhull/qhull_a.h
    python setup.py install --prefix=%{INSTALL_DIR_COMP}

    #Cython>=0.21 fails for Intel 13, so install Cython 0.20 instead
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" cython==0.20	

    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" pandas
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" psutil
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" numexpr
    ### 2015-11-18 WCP
    ### iPython 4.0.0 is not building correctly. Downgrade to 3.1.0 for now.
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" ipython[all]==3.1.0	
    #pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" fortran-magic
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" MySQL
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" psycopg2
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" mercurial
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" yt==3.1
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" theano

    module load hdf5
    export HDF5_DIR=$TACC_HDF5_DIR	
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$TACC_HDF5_LIB
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" h5py
    pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" tables
    CFLAGS="-O2" pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_COMP}" scikit_learn

%endif

#############################################################
# mpi4py: use INSTALL_DIR_MPI
############################################################

%if "%{build_mpi_version}" == "1"
	#If we are not building the interpreter we assume that it already exists and it is
	#installed, so we load it
	
	%if "%{build_python_version}" == "0"
		module load %{PNAME}/%{version}
	%endif

	mkdir -p %{INSTALL_DIR_MPI}
	mount -t tmpfs tmpfs %{INSTALL_DIR_MPI}
	module load %{mpi_module}   
	pip install --no-use-wheel --install-option="--prefix=%{INSTALL_DIR_MPI}" mpi4py==2.0.0
%endif

#----------------------------------------------------------
# Copy into rpm directory
#----------------------------------------------------------
# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.

#----------------------------------------------------------
# UNMOUNT THE TEMP FILESYSTEM
#----------------------------------------------------------

%if "%{build_comp_version}" == "1"
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
    cp -r %{INSTALL_DIR_COMP}/ $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}/..
    umount %{INSTALL_DIR_COMP}
%endif

%if "%{build_mpi_version}" == "1"
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
    cp -r %{INSTALL_DIR_MPI}/ $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}/..
    umount %{INSTALL_DIR_MPI}
%endif


#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
#------- Compiler version

%if "%{build_comp_version}" == "1"
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}/%{version}.lua << 'EOF'
help(
[[
This is the Python 2.7.9 package built on %(date +'%B %d, %Y').

You can install your own modules (choose one method):
        1. python setup.py install --user
        2. python setup.py install --home=<dir>
        3. pip install --user module-name

Please note: tables and h5py are there but you need to load the
hdf5 module to use these packages.
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

setenv("TACC_PYTHON_DIR", python_dir)
setenv("TACC_PYTHON_BIN", python_bin)
setenv("TACC_PYTHON_INC", python_inc)
setenv("TACC_PYTHON_LIB", python_lib)
setenv("TACC_PYTHON_MAN", python_man)

prepend_path("PATH", python_bin)
prepend_path("MANPATH", python_man)
prepend_path("LD_LIBRARY_PATH", python_lib)
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

#####------- MPI version
%if "%{build_mpi_version}" == "1"
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}

    cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua << 'EOF'
help(
[[
This is the Python 2.7.9 package built on %(date +'%B %d, %Y').

You can install your own modules (choose one method):
	1. python setup.py install --user
	2. python setup.py install --home=<dir>
	3. pip install --user module-name

Please note: tables and h5py are there but you need to load the
hdf5 module to use these packages.

Version %{version}
]]
)

whatis("Name: Python")
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

setenv("TACC_PYTHON_DIR", python_dir)
setenv("TACC_PYTHON_BIN", python_bin)
setenv("TACC_PYTHON_INC", python_inc)
setenv("TACC_PYTHON_LIB", python_lib)
setenv("TACC_PYTHON_MAN", python_man)

prepend_path("MANPATH", python_man)
prepend_path("LD_LIBRARY_PATH", python_lib)
prepend_path("PATH",       "%{INSTALL_DIR_COMP}/bin")
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
    %if "%{build_comp_version}" == "1"
	$RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR_COMP}/%{version}.lua
    %endif
    %if "%{build_mpi_version}" == "1"
 	$RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua
    %endif
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{PACKAGE_NAME}
%defattr(-,root,install)

%if "%{build_comp_version}" == "1"
	%{INSTALL_DIR_COMP}
	%{MODULE_DIR_COMP}
%endif

%if "%{build_mpi_version}" == "1"
	%{INSTALL_DIR_MPI}
	%{MODULE_DIR_MPI}
%endif

%post -n %{PACKAGE_NAME}

%clean


