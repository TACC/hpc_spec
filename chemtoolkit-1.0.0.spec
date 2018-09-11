################################################################
#
#    CHEMTOOLKIT SPEC FILE
#
#    MACHINE       :   TACC STAMPEDE2
#    VERSION       :   1.0.0
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   09-07-2018
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
# rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1' --define 'mpiV 17_0' chemtoolkit-1.0.0.spec   | tee log_chemtoolkit-1.0.0
#

%define pkg_base_name chemtoolkit
%define MODULE_VAR    CHEMTOOLKIT

%define major_version 1
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

################################################################

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc

################################################################

Summary:   Chemtoolkit is a collection of computational chemistry tools
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   1%{?dist}
License:   Open source
Vendor:    Various authors
Group:     applications/chemistry
URL:       https://www.tacc.utexas.edu/
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Packager:  TACC Albert Lu - alu@tacc.utexas.edu

%define    buildroot   /var/tmp/%{name}-%{version}-buildroot
%define    hoomd_src     %{pkg_base_name}-%{pkg_version}

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

################################################################

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
CHEMTOOLKIT package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
CHEMTOOLKIT modulefile.

# Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
Chemtoolkit is a collection of computational chemistry tools.

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

  module load intel/17.0.4
  module load python3/3.6.3

  mkdir -p chemtoolkit/lib/python3.6/site-packages
  chemtoolkit_dir=`pwd`/chemtoolkit

  export PYTHONPATH=${chemtoolkit_dir}/lib/python3.6/site-packages/:$PYTHONPATH

  # BIOPYTHON

  cd biopython
  python3 setup.py build
  python3 setup.py install --prefix=${chemtoolkit_dir}
  cd ..

  # PARMED

  cd ParmEd
  python3 setup.py install --prefix=${chemtoolkit_dir}
  cd ..

  # PYTABLES

  ml hdf5/1.8.16
  export HDF5_DIR=$TACC_HDF5_DIR
  export CC=gcc
  export CXX=g++

  cd PyTables
  python3 setup.py build --hdf5=$TACC_HDF5_DIR
  python3 setup.py install --prefix=${chemtoolkit_dir}
  cd ..

  # NETWORKX

  cd networkx
  python3 setup.py build
  python3 setup.py install --prefix=${chemtoolkit_dir}
  cd ..

  # MDTRAJ

  cd mdtraj
  export CC=icc
  export CXX=icpc
  python3 setup.py install --disable-openmp  --prefix=${chemtoolkit_dir}
  cd ..

  # PYTRAJ and CPPTRAJ

  unset CC
  unset CXX
  unset FC

  cd pytraj/cpptraj
  PWD=`pwd`
  ./configure gnu -shared --with-netcdf=/opt/apps/intel17/netcdf/4.3.3.1/x86_64 -mkl  -openmp --prefix=${PWD}

  make libcpptraj
  make install
  source ./cpptraj.sh
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`
  cd ..
  python3 setup.py install --prefix=${chemtoolkit_dir}
  cd ..

  # NGLVIEW

  cd nglview
  python3 setup.py build
  python3 setup.py install --prefix=${chemtoolkit_dir}
  cd ..

  #npm install
  #jupyter nbextension enable widgetsnbextension --py —user
  #jupyter nbextension enable nglview --py --user

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

# INSTALL CHEMTOOLKIT

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  # install chemtoolkit
  cp -r chemtoolkit/*      $RPM_BUILD_ROOT/%{INSTALL_DIR}/
  cp pytraj/cpptraj/bin/*  $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  cp pytraj/cpptraj/lib/*  $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib
  ln $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/cpptraj.OMP $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/cpptraj

  chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*

%endif # BUILD_PACKAGE

################################################################

%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua <<EOF
local help_message = [[
Chemtoolkit is a collection of computational chemistry tools 
installed on Stampede2, which currently includes the following 
applications:

  - Biopython  (master as of 09-06-2018) 
  - MDTraj     (1.9.0)
  - NGLView    (1.0.0)
  - ParmEd     (2.5.0)
  - Pytraj     (2.0.3)

The package was built with intel/17.0.4 and python3/3.6.3.
For more information about using specific tools, please check the 
official website:
  
  - Biopython   https://biopython.org/
  - MDTraj      http://mdtraj.org/1.9.0/
  - NGLView     http://nglviewer.org/nglview/latest/
  - ParmEd      http://parmed.github.io/ParmEd/html/index.html
  - Pytraj      https://amber-md.github.io/pytraj/latest/index.html 

Version %{version}
]]

help(help_message,"\n")

whatis("Name: ChemToolKit")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Molecular Dynamics, Application")
whatis("URL: ")
whatis("Description: Computational chemistry tools")

local chemtoolkit_dir="%{INSTALL_DIR}/chemtoolkit"

load("hdf5/1.8.16")

setenv("TACC_CHEMTOOLKIT_DIR"    ,chemtoolkit_dir)
setenv("TACC_CHEMTOOLKIT_LIB"    ,pathJoin(chemtoolkit_dir,"lib"))
prepend_path("PATH"              ,pathJoin(chemtoolkit_dir,"bin"))
prepend_path("LD_LIBRARY_PATH"   ,pathJoin(chemtoolkit_dir,"lib"))
prepend_path("LD_LIBRARY_PATH"   ,pathJoin(chemtoolkit_dir,"lib/python3/site-packages"))
prepend_path("PYTHONPATH"        ,pathJoin(chemtoolkit_dir,"lib"))
prepend_path("PYTHONPATH"        ,pathJoin(chemtoolkit_dir,"lib/python3/site-packages"))
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} <<EOF
#%Module3.1.1#################################################
##
## version file for CHEMTOOLKIT
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
