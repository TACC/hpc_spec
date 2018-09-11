################################################################
#
#    RDKIT SPEC FILE
#
#    MACHINE       :   TACC STAMPEDE2
#    VERSION       :   2018-03
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   08-31-2018
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
# rpmbuild -bb --define 'is_gcc71 1' --define 'is_impi 1' --define 'mpiV 18_2' rdkit-2018-03.spec | tee log_rdkit-2018-03
#

%define pkg_base_name rdkit
%define MODULE_VAR    RDKIT

%define major_version 2018
%define minor_version 03
%define micro_version 0

%define pkg_version %{major_version}_%{minor_version}

################################################################

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc

################################################################

Summary:   RDKit is an open source toolkit for cheminformatics
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   1%{?dist}
License:   Creative Commons Attribution-ShareAlike 4.0 License
Vendor:    http://www.rdkit.org/
Group:     applications/chemistry
URL:       http://www.rdkit.org/
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz
Packager:  TACC Albert Lu - alu@tacc.utexas.edu

%define    buildroot   /var/tmp/%{name}-%{version}-buildroot
%define    rdkit_src   %{pkg_base_name}-%{pkg_version}

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

################################################################

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
Rdkit package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Rdkit modulefile.

# Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
RDKit is an open source toolkit for cheminformatics

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

  ml gcc/7.1.0
  ml unload python/2.7.13
  ml python3

  py_3_dir=/opt/apps/gcc7_1/python3/3.6.1/
  py_3_bin=${py_3_dir}/bin/python3.6
  gcc_7_dir=/opt/apps/gcc/7.1.0/

  mkdir boost_1_61_0
  boost_dir=`pwd`/boost_1_61_0

  mkdir rdkit_install
  rdkit_install_dir=`pwd`/rdkit_install

  cd boost_1_61_0_src

  cd tools/build/src/tools/
  sed -e "s@include/python\$(version)@include/python\$(version)m@g" python.jam > tmp
  mv tmp python.jam
  cd ../../../../

  ./bootstrap.sh --prefix="../boost_1_61_0" --with-toolset=gcc --with-python=${py_3_bin} --with-python-version=3.6 --with-libraries=python,serialization
  ./b2 -j 10 --enable-unicode=ucs4 --prefix="../boost_1_61_0" cflags="-fPIC" cxxflags="-fPIC -std=c++11"  install

  rm ../boost_1_61_0/lib/*.a

  cd ../rdkit
  rd_dir=`pwd`

  export RDBASE=`pwd`
  export LD_LIBRARY_PATH=`pwd`/lib/:$LD_LIBRARY_PATH
  export PYTHONPATH=$RDBASE:$PYTHONPATH
  export PYTHON_INCLUDE_DIR=${py_3_dir}/include/python3.6m/
  export LD_LIBRARY_PATH=${boost_dir}/lib/:$LD_LIBRARY_PATH
  export EIGEN3_INCLUDE_DIR=${rd_dir}/External/eigen

  cd build

  ml cmake/3.10.2

  cmake ..  -DCMAKE_INSTALL_PREFIX="${rdkit_install_dir}" \
            -DRDK_INSTALL_INTREE=OFF \
            -DRDK_BUILD_INCHI_SUPPORT=ON \
            -DBoost_NO_SYSTEM_PATHS=ON \
            -DBoost_USE_STATIC_LIBS=OFF \
            -DCMAKE_CXX_STANDARD=11 \
            -DCMAKE_CXX_COMPILER="${gcc_7_dir}/bin/g++" \
            -DCMAKE_C_COMPILER="${gcc_7_dir}/bin/gcc" \
            -DCMAKE_CXX_FLAGS="-D_GLIBCXX_USE_CXX11_ABI=1 -fPIC" \
            -DPYTHON_LIBRARY="${py_3_dir}/lib/libpython3.so" \
            -DPYTHON_INCLUDE_DIR="${py_3_dir}/include/python3.6m/" \
            -DPYTHON_EXECUTABLE="${py_3_bin}" \
            -DBOOST_ROOT="${boost_dir}" \
            -DBOOST_LIBRARYDIR="${boost_dir}/lib/"

  make -j10 VERBOSE=1
  make install

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

rdkit_src_dir=`pwd`

# INSTALL RDKIT

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  cp -r boost_1_61_0         $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r rdkit_install        $RPM_BUILD_ROOT/%{INSTALL_DIR}/rdkit
  cp -r rdkit/External/eigen $RPM_BUILD_ROOT/%{INSTALL_DIR}

  chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*

%endif # BUILD_PACKAGE

################################################################

%if %{?BUILD_MODULEFILE}

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua <<EOF
local help_message = [[

RDKit is an open-source cheminformatics software written in C++.
Python (3.6) wrapper is generated using Boost.Python.

Compiler and external libraries:

  - GCC     (7.1)
  - Python3 (3.6.1)
  - Boost   (1.61.0)
  - Eigen3  (3.3.5)

The RDKit module defines a set of environment variables for the
locations of the RDKit home, libraries, include and more, with 
the prefix "TACC_RDKIT_". Use the "env" command to display the variables:

  $ env | grep "TACC_RDKIT"

For more information about using RDKit, visit the RDKit documentation website: 

http://www.rdkit.org/docs/index.html

Version %{version}
]]

help(help_message,"\n")

whatis("Name: RDKit")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Cheminformatics, Application")
whatis("URL:  http://www.rdkit.org/")
whatis("Description: Application Programming Interface for atomistic simulations")

local rdkit_dir="%{INSTALL_DIR}"

setenv("TACC_RDKIT_DIR"              ,pathJoin(rdkit_dir,"rdkit/"))
setenv("TACC_RDKIT_LIB"              ,pathJoin(rdkit_dir,"rdkit/lib/"))
setenv("TACC_RDKIT_INC"              ,pathJoin(rdkit_dir,"rdkit/include/"))
setenv("TACC_RDKIT_SHARE"            ,pathJoin(rdkit_dir,"rdkit/share/"))
setenv("RDBASE"                      ,pathJoin(rdkit_dir,"rdkit/"))
setenv("EIGEN3_INCLUDE_DIR"          ,pathJoin(rdkit_dir,"eigen/"))

prepend_path("PYTHONPATH",pathJoin(rdkit_dir,"rdkit/"))
prepend_path("PYTHONPATH",pathJoin(rdkit_dir,"rdkit/lib/"))
prepend_path("PYTHONPATH",pathJoin(rdkit_dir,"rdkit/lib/python3.6/site-packages/"))
prepend_path("LD_LIBRARY_PATH",pathJoin(rdkit_dir,"boost_1_61_0/lib"))
prepend_path("LD_LIBRARY_PATH",pathJoin(rdkit_dir,"rdkit/lib"))
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} <<EOF
#%Module3.1.1#################################################
##
## version file for RDKIT
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
