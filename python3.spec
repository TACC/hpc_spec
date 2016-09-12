Summary:    Python is a high-level general-purpose programming language.
Name:       tacc-python3 
Version:    3.5.1
Release:    2
License:    GPLv2
Vendor:     Python Software Foundation
Group:      Applications
Packager:   TACC - rtevans@tacc.utexas.edu
#Source:     %{name}-%{version}.tar.gz


#------------------------------------------------
# CONFIGURATION DEFINITIONS
#------------------------------------------------

%define build_new        0
%define build_numpy      0
%define build_scipy      0
%define build_matplotlib 0
%define build_mpi4py     1

%include mpi-defines.inc

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%include rpm-dir.inc
%include system-defines.inc
%include compiler-defines.inc

%define PNAME python3
%define MODULE_VAR TACC_PYTHON

%define INSTALL_DIR_COMP %{APPS}/%{comp_fam_ver}/%{PNAME}/%{version}
%define MODULE_DIR_COMP %{APPS}/%{comp_fam_ver}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{comp_fam_ver}

%if "%{build_mpi4py}" == "1"
    %define INSTALL_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{PNAME}/%{version}
    %define MODULE_DIR_MPI %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{PNAME}
    %define PACKAGE_NAME %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%endif

%package -n %{PACKAGE_NAME}
Summary: Python 3 built for TACC systems
Group:   Programming Language

%description
%description -n %{PACKAGE_NAME}
This is intended to be a core Python
interpreter for TACC systems.

%prep

%if "%{build_mpi4py}" == "0"
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_COMP}
%endif

%if "%{build_mpi4py}" == "1"
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR_MPI}
%endif

%build

%install
%include system-load.inc
%include compiler-load.inc

module purge
module load TACC
module load %{comp_module}

# Set up src directory
export SRC_DIR=`pwd`/src
mkdir -p ${SRC_DIR}
cd %{_topdir}/SOURCES

export PATH=%{INSTALL_DIR_COMP}/bin:$PATH
export LD_LIBRARY_PATH=%{INSTALL_DIR_COMP}/lib64:%{INSTALL_DIR_COMP}/lib:$LD_LIBRARY_PATH
export PYTHONPATH=%{INSTALL_DIR_COMP}/lib/python3.5/site-packages:$PYTHONPATH


%if "%{build_mpi4py}" == "0"

############################################################
# Install python here
############################################################
%if "%{build_new}" == "1"
    mkdir -p %{INSTALL_DIR_COMP}
    mount -t tmpfs tmpfs %{INSTALL_DIR_COMP}

    if [ ! -f "%{_topdir}/SOURCES/Python-%{version}.tgz" ]; then
     	wget http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
    fi	
     rm -rf ${SRC_DIR}/Python-%{version}
     tar -xzf %{_topdir}/SOURCES/Python-%{version}.tgz -C ${SRC_DIR}
     cd ${SRC_DIR}/Python-%{version}

     %if "%{comp_fam_name}" == "Intel"
     	 ./configure --prefix=%{INSTALL_DIR_COMP} CC=icc CXX=icpc CFLAGS="-ipo -fPIC -mkl -O3 -fp-model strict -fomit-frame-pointer -axCORE-AVX2,CORE-AVX-I -fma" CPPFLAGS="-ipo -fPIC -mkl -O3 -fp-model strict -fomit-frame-pointer -axCORE-AVX2,CORE-AVX-I -fma" LDFLAGS="-lpthread" --with-system-ffi --with-cxx-main=icpc --enable-shared --with-pth
     %endif
     %if "%{comp_fam_name}" == "GNU"
     	 ./configure --prefix=%{INSTALL_DIR_COMP} CFLAGS="-pthread -fPIC -fno-strict-aliasing -g -DNDEBUG -O3 -fwrapv -Wall -Wstrict-prototypes -march=ivybridge -mtune=haswell" CPPFLAGS="-pthread -fPIC -fno-strict-aliasing -g -DNDEBUG -O3 -fwrapv -Wall -Wstrict-prototypes -march=ivybridge -mtune=haswell" LDFLAGS="-lpthread" --with-system-ffi --enable-shared --with-pth
     %endif

     make -j 16
     make sharedinstall
     make -i install
     #############################################################
     # setuptools and pip
     ############################################################
     cd ${SRC_DIR}
%endif
############################################################
# compiler independent modules (pure python)
############################################################
    pip3 install --trusted-host pypi.python.org certifi
    pip3 install nose
    pip3 install virtualenv
    pip3 install virtualenvwrapper    

    pip3 install sympy
    pip3 install brewer2mpl
    pip3 install simpy

    pip3 install jsonpickle
    pip3 install meld3
    pip3 install paramiko

#############################################################
# scipy stack: use INSTALL_DIR_COMP . 
# We need to know which pip modules are compiler specific.  
# numpy scipy matplotlib jupyter pandas sympy nose
############################################################
%if "%{comp_fam_name}" == "GNU"	
    module load mkl
%endif

%if "%{build_numpy}" == "1"
    ### Numpy
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/numpy-1.11.0.tar.gz" ]; then	
       wget https://sourceforge.net/projects/numpy/files/NumPy/1.11.0/numpy-1.11.0.tar.gz
    fi	   
   
    rm -rf ${SRC_DIR}/numpy-1.11.0 	   
    tar -xzvf %{_topdir}/SOURCES/numpy-1.11.0.tar.gz -C ${SRC_DIR}	
    cd ${SRC_DIR}/numpy-1.11.0

    %if "%{comp_fam_name}" == "Intel"
echo "[mkl]
library_dirs = ${MKLROOT}/lib/intel64
include_dirs = ${MKLROOT}/include
mkl_libs = mkl_rt
lapack_libs = " > site.cfg
    sed -i 's/-xSSE4.2/-axCORE-AVX2,CORE-AVX-I -fma/' numpy/distutils/intelccompiler.py
    sed -i 's/-xSSE4.2/-axCORE-AVX2,CORE-AVX-I -O1 -fma/' numpy/distutils/fcompiler/intel.py
    %{INSTALL_DIR_COMP}/bin/python3 setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install --prefix=%{INSTALL_DIR_COMP}
    %endif

    %if "%{comp_fam_name}" == "GNU"	
echo "[mkl]
library_dirs = ${TACC_MKL_LIB}
include_dirs = ${TACC_MKL_INC}
mkl_libs = mkl_def, mkl_intel_lp64, mkl_core, mkl_gnu_thread, mkl_avx 
lapack_libs = mkl_def, mkl_intel_lp64, mkl_core, mkl_gnu_thread, mkl_avx" > site.cfg

    export LDFLAGS="-lm -lpthread -lgomp -shared"	    
    %{INSTALL_DIR_COMP}/bin/python3 setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install --prefix=%{INSTALL_DIR_COMP}
    %endif

%endif

%if "%{build_scipy}" == "1"
    export LDFLAGS="-lm -lpthread -lgomp -shared"	    
    ### Scipy Libraries
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/scipy-0.17.0.tar.gz" ]; then
       wget -O scipy-0.17.0.tar.gz https://github.com/scipy/scipy/releases/download/v0.17.0/scipy-0.17.0.tar.gz
    fi	   

    rm -rf ${SRC_DIR}/scipy-0.17.0
    tar -xzvf scipy-0.17.0.tar.gz -C ${SRC_DIR} 
    cd ${SRC_DIR}/scipy-0.17.0

    %if "%{comp_fam_name}" == "Intel"
    	%{INSTALL_DIR_COMP}/bin/python3 setup.py config --compiler=intelem --fcompiler=intelem build_clib --compiler=intelem --fcompiler=intelem build_ext --compiler=intelem --fcompiler=intelem install --prefix=%{INSTALL_DIR_COMP}
    %endif
    
    %if "%{comp_fam_name}" == "GNU"	
    #export LD_LIBRARY_PATH=/home1/02561/rtevans/OpenBLAS:$LD_LIBRARY_PATH
        %{INSTALL_DIR_COMP}/bin/python3 setup.py config --fcompiler=gfortran build_clib --fcompiler=gfortran build_ext --fcompiler=gfortran install --prefix=%{INSTALL_DIR_COMP}
    %endif

%endif

%if "%{build_matplotlib}" == "1"
    ### Matplotlib
    cd %{_topdir}/SOURCES	
    if [ ! -f "%{_topdir}/SOURCES/matplotlib-1.5.1.tar.gz" ]; then
	wget https://pypi.python.org/packages/source/m/matplotlib/matplotlib-1.5.1.tar.gz
    fi

    rm -rf ${SRC_DIR}/matplotlib-1.5.1
    tar -xzvf matplotlib-1.5.1.tar.gz -C ${SRC_DIR}
    cd ${SRC_DIR}/matplotlib-1.5.1
    python3 setup.py install --prefix=%{INSTALL_DIR_COMP}
%endif

    #Cython>=0.21 fails for Intel 13, so install Cython 0.20 instead
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" cython==0.20	
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" pandas
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" psutil
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" numexpr
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" rpyc	
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" ipython==3.1.0
    #pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" jupyter
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" pystuck
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" fortran-magic

    #pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" MySQL
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" psycopg2
    #pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" mercurial
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" yt==3.1
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" theano

    %if "%{comp_fam_name}" == "Intel"
    module load hdf5
    export HDF5_DIR=$TACC_HDF5_DIR	
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$TACC_HDF5_LIB
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" h5py
    pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" tables
    %endif
    CFLAGS="-O2" pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_COMP}" scikit_learn
%endif

#############################################################
# mpi4py: use INSTALL_DIR_MPI
############################################################

%if "%{build_mpi4py}" == "1"
	#If we are not building the interpreter we assume that it already exists and it is
	#installed, so we load it
	
	mkdir -p %{INSTALL_DIR_MPI}
	mount -t tmpfs tmpfs %{INSTALL_DIR_MPI}
	module load %{mpi_module}   
	pip3 install --no-binary :all: --install-option="--prefix=%{INSTALL_DIR_MPI}" mpi4py	
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
    umount %{INSTALL_DIR_MPI}
%endif

%if "%{build_new}" == "1"
    umount %{INSTALL_DIR_COMP}
%endif

#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
%if "%{build_mpi4py}" == "0"
#------- Compiler version

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

whatis("Name: Python 3")
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
always_load("mkl")
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

#####------- MPI version
%if "%{build_mpi4py}" == "1"

    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}

    cat >    $RPM_BUILD_ROOT/%{MODULE_DIR_MPI}/%{version}.lua << 'EOF'
help(
[[
This is the Python package built on %(date +'%B %d, %Y').

You can install your own modules (choose one method):
	1. python3 setup.py install --user
	2. python3 setup.py install --home=<dir>
	3. pip3 install --user module-name

Version %{version}
]]
)

whatis("Name: Python 3")
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
always_load("mkl")
%endif
setenv("TACC_PYTHON_DIR", python_dir)
setenv("TACC_PYTHON_BIN", python_bin)
setenv("TACC_PYTHON_INC", python_inc)
setenv("TACC_PYTHON_LIB", python_lib)
setenv("TACC_PYTHON_MAN", python_man)

prepend_path("MANPATH", python_man)
prepend_path("LD_LIBRARY_PATH", python_lib)
prepend_path("PATH",       "%{INSTALL_DIR_COMP}/bin")
prepend_path("PATH",       "%{INSTALL_DIR_MPI}/lib/python3.5/site-packages/mpi4py/bin")
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
%if "%{build_mpi4py}" == "0"
/usr/lib/rpm/brp-python-bytecompile %{INSTALL_DIR_COMP}/bin/python3
%endif

%if "%{build_mpi4py}" == "1"
/usr/lib/rpm/brp-python-bytecompile %{INSTALL_DIR_MPI}/bin/python3
%endif

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


