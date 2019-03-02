################################################################
#
#    HOOMD SPEC FILE
#
#    MACHINE       :   TACC STAMPEDE2
#    VERSION       :   2.4.2
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   02-05-2019
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
# rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1' --define 'mpiV 17_0' hoomd_2018.8.17.spec  | tee log_hoomd.2018.8.17
# ./build_rpm.sh -i18 -j18_2 -l hoomd_2.4.2.spec

%define pkg_base_name hoomd
%define MODULE_VAR    HOOMD

%define major_version 2
%define minor_version 4
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

################################################################

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
#%include name-defines-noreloc.inc
%include name-defines.inc

################################################################

Summary:   HOOMD-blue is a general-purpose particle simulation toolkit.
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   2%{?dist}
License:   Open Source Software License Copyright 2009-2018
Vendor:    University of Michigan
Group:     applications/chemistry
URL:       http://glotzerlab.engin.umich.edu/hoomd-blue/
Source:    %{pkg_base_name}-v%{pkg_version}.tar.gz
Packager:  TACC Albert Lu - alu@tacc.utexas.edu

%define    buildroot   /var/tmp/%{name}-%{version}-buildroot
%define    hoomd_src     %{pkg_base_name}-v%{pkg_version}

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

################################################################

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
HOOMD-Blue package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
HOOMD-Blue modulefile.

# Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
HOOMD-blue is a general-purpose particle simulation toolkit. 
It scales from a single CPU core to thousands of GPUs.

################################################################

%prep

%if %{?BUILD_PACKAGE}

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -q -n %{pkg_base_name}-v%{pkg_version}

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

  module load python3/3.7.0
  module load cmake
  module load autotools  

  export SOFTWARE_ROOT=`pwd`/hoomd-blue

  mkdir -p hoomd/lib/python3

  cd hoomd-blue

  mkdir build
  cd build

  # "-xCORE-AVX2 -axCORE-AVX512,MIC-AVX512"
  # will cause TEST-262 FAIL
  # test_polyhedron.cc
  # overlap_sphero_octahedron_no_rot: FAIL
  # overlap_octahedron_no_rot: FAIL

  cmake ../ -DCMAKE_INSTALL_PREFIX=../../hoomd/lib/python3 \
            -DCMAKE_CXX_COMPILER="mpicxx" \
            -DCMAKE_C_COMPILER="mpicc"  \
            -DCMAKE_CXX_FLAGS="-mkl -L${ICC_BIN}/../../tbb/lib/intel64/gcc4.7 -ltbbmalloc" \
            -DCMAKE_C_FLAGS="-mkl -L${ICC_BIN}/../../tbb/lib/intel64/gcc4.7 -ltbbmalloc" \
            -DENABLE_CUDA=OFF \
            -DENABLE_MPI=ON \
            -DPYTHON_EXECUTABLE="${TACC_PYTHON3_BIN}/python3" \
            -DENABLE_TBB=ON \
            -DCOPY_HEADERS=ON \
            -DBUILD_CGCMM=ON \
            -DBUILD_HPMC=ON \
            -DBUILD_MD=ON \
            -DBUILD_METAL=ON

  # TEST-221: test_boxMC.py-cpu hang
  # cmake ../ -DCMAKE_INSTALL_PREFIX=../../hoomd/lib/python3 \
  #          -DCMAKE_CXX_COMPILER="/opt/apps/intel18/impi/18.0.2/bin/mpicxx" \
  #          -DCMAKE_C_COMPILER="/opt/apps/intel18/impi/18.0.2/bin/mpicc"  \
  #          -DCMAKE_CXX_FLAGS="-mkl -L${ICC_BIN}/../../tbb/lib/intel64/gcc4.7 -ltbbmalloc" \
  #          -DCMAKE_C_FLAGS="-mkl -L${ICC_BIN}/../../tbb/lib/intel64/gcc4.7 -ltbbmalloc" \
  #          -DENABLE_CUDA=OFF -DENABLE_MPI=ON -DPYTHON_EXECUTABLE="/opt/apps/intel18/python3/3.7.0/bin/python3" \
  #          -DENABLE_TBB=ON -DCOPY_HEADERS=ON 

 make -j10 VERBOSE=1
 make install

 cd ../../

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

# INSTALL HOOMD

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  # install hoomd
  mkdir -p               $RPM_BUILD_ROOT/%{INSTALL_DIR}/hoomd
  cp -r hoomd/lib        $RPM_BUILD_ROOT/%{INSTALL_DIR}/hoomd

  chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*

%endif # BUILD_PACKAGE

################################################################

%if %{?BUILD_MODULEFILE}

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua <<EOF
local help_message = [[
HOOMD-blue is a general-purpose particle simulation toolkit. 
It scales from a single CPU core to thousands of GPUs.

You define particle initial conditions and interactions in a 
high-level python script. Then tell HOOMD-blue how you want to 
execute the job and it takes care of the rest. Python job 
scripts give you unlimited flexibility to create custom 
initialization routines, control simulation parameters, 
and perform in situ analysis.

For more information about using HOOMD-Blue package, please check
the website:

  https://hoomd-blue.readthedocs.io/en/stable/

* REFERENCE
      
  HOOMD-Blue website: http://glotzerlab.engin.umich.edu/hoomd-blue/

Version %{version}
]]

help(help_message,"\n")

whatis("Name: HOOMD-Blue")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Molecular Dynamics, Application")
whatis("URL:  http://glotzerlab.engin.umich.edu/hoomd-blue/")
whatis("Description: General-purpose particle simulation toolkit")

local hoomd_dir="%{INSTALL_DIR}/hoomd"

setenv("TACC_HOOMD_DIR"              ,hoomd_dir)
setenv("TACC_HOOMD_LIB"              ,pathJoin(hoomd_dir,"lib"))
prepend_path("PYTHONPATH",            pathJoin(hoomd_dir,"lib/python3"))
depends_on("python3/3.7.0")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} <<EOF
#%Module3.1.1#################################################
##
## version file for HOOMD
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
