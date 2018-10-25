################################################################
#
#    KIMAPI SPEC FILE
#
#    MACHINE       :   TACC LONESTAR 5
#    VERSION       :   1.9.6
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   10-12-2018
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
# ./build_rpm.sh -g73 -c7_7_3 kim_1.9.6_ls_v2.spec
# rpmbuild  -bb --define 'is_gcc73 1' --define 'compV 73' --define 'is_cmpich 1' --define 'mpiV 7_7_3' kim_1.9.6_ls_v2.spec
#

%define pkg_base_name kim
%define MODULE_VAR    KIM

%define major_version 1
%define minor_version 9
%define micro_version 6

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

################################################################

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc

################################################################

Summary:   The KIM API is an Application Programming Interface for atomistic simulations.
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   2%{?dist}
License:   CDDL-1.0
Vendor:    OpenKim.org
Group:     applications/chemistry
URL:       https://openkim.org
Source:    %{pkg_base_name}-api-v%{pkg_version}.tar.gz
Packager:  TACC Albert Lu - alu@tacc.utexas.edu

%define    buildroot   /var/tmp/%{name}-%{version}-buildroot
%define    kim_src     %{pkg_base_name}-api-v%{pkg_version}

# Turn off debug package mode
%define    debug_package %{nil}
%define    dbg           %{nil}

################################################################

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
OpenKIM API package.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
OpenKIM API modulefile.

# Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
The KIM API is an Application Programming Interface 
for atomistic simulations. The API provides a standard 
for exchanging information between atomistic simulation 
codes and interatomic models.

################################################################

%prep

%if %{?BUILD_PACKAGE}

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -q -n %{pkg_base_name}-api-v%{pkg_version}

%endif # BUILD_PACKAGE 

%if %{?BUILD_MODULEFILE}

  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%endif # BUILD_MODULEFILE 

################################################################

%build

%if %{?BUILD_PACKAGE}

set +x

unset MODULEPATH
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  MP="/opt/apps/tools/modulefiles:/opt/apps/modulefiles"

  if [ -z "$MODULEPATH" ]; then
    export MODULEPATH=$(/opt/apps/lmod/lmod/libexec/addto --append MODULEPATH ${MP//:/ })
  fi
fi

#module load %{comp_module}
#module load %{mpi_module}

set -x

  mkdir installed-kim-api
  cd installed-kim-api
  kim_build_dir=`pwd`

  cd ../%{kim_src}

  ml gcc
  ml cray_mpich

  ./configure --prefix="/opt/apps/%{INSTALL_SUFFIX}/kim-api" --compiler-suite="GCC"  CXX="mpicxx" CC="mpicc" FC="mpif90"
  #./configure --prefix=${kim_build_dir} --compiler-suite="GCC"  CXX="mpicxx" CC="mpicc" FC="mpif90"
  
  make

%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

cd %{kim_src}

kim_src_dir=`pwd`
#kim_install_dir=/work/05392/cylu/stampede2/rpmbuild/test/%{INSTALL_SUFFIX}/kim-api/lib/kim-api-v1/
kim_install_dir=/opt/apps/%{INSTALL_SUFFIX}/kim-api/lib/kim-api-v1/

# INSTALL KIM API

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  # install kim library
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/etc/bash_completion.d
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/include/kim-api-v1
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/libexec/kim-api-v1  
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/models
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/model_drivers

  cp ./src/utils/kim-api-v1-collections-management  $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin
  cp ./src/utils/kim-api-v1-build-config            $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin
  cp ./src/utils/kim-api-v1-activate                $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin
  cp ./src/utils/kim-api-v1-deactivate              $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin
  cp ./src/utils/kim-api-v1-collections-info        $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/libexec/kim-api-v1
  cp ./src/utils/kim-api-v1-descriptor-file-match   $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/libexec/kim-api-v1
  cp ./src/utils/kim-api-v1-simulator-model         $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/libexec/kim-api-v1

  cp ./completion/kim-api-v1-completion.bash   $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/etc/bash_completion.d
  cp ./src/*.h                                 $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/include/kim-api-v1
  cp ./src/*.mod                               $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/include/kim-api-v1
  cp ./src/*.dynamic-load.so                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/libkim-api-v1.so
  cp ./src/*.dynamic-load.so                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/
  cp ./src/*.dynamic-load.so                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/libkim-api-v1.so

  sed -e "s@${kim_src_dir}@${kim_install_dir}@" ./Makefile.KIM_Config > Makefile.KIM_Config_2

  cp ./Makefile.KIM_Config_2                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/Makefile.KIM_Config

  cp ./Makefile.Version                                            $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  cp -r $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin                 $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  cp -r $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/include/kim-api-v1  $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/include
  cp -r ./build_system                                             $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  cp -r $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/libexec             $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1

  cd ..

  chmod -Rf u+rwX,g+rwX,o=rX $RPM_BUILD_ROOT/%{INSTALL_DIR}/*

%endif # BUILD_PACKAGE

################################################################

%if %{?BUILD_MODULEFILE}

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
touch    $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua <<EOF
local help_message = [[
The KIM API is an Application Programming Interface for atomistic 
simulations. The API provides a standard for exchanging information 
between atomistic simulation codes (molecular dynamics, molecular 
statics, lattice dynamics, Monte Carlo, etc.) and interatomic models 
(potentials or force fields). 

It also includes a set of library routines for using the API with 
bindings for:

  FORTRAN 77, Fortran 90/95, Fortran 2003, C, C++

The KIM module defines a set of environment variables for the locations 
of the KIM home, binaries, library and more with the prefix "TACC_KIM_". 
Use the "env" command to display the variables:

  $ env | grep "TACC_KIM"

LAMMPS (version 16Mar18) installed on Lonestar5 was compiled with the 
KIM package.

For more information about using KIM package in LAMMPS, please check
the website:

  http://lammps.sandia.gov/doc/pair_kim.html

* REFERENCE
      
  OpenKIM website: https://openkim.org

  Version %{version}
]]

help(help_message,"\n")

whatis("Name: OpenKIM API")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Molecular Dynamics, Application")
whatis("URL:  https://openkim.org")
whatis("Description: Application Programming Interface for atomistic simulations")

local kim_dir="%{INSTALL_DIR}"

setenv("TACC_KIM_DIR"              ,kim_dir)
setenv("TACC_KIM_API"              ,pathJoin(kim_dir,"kim-api"))
setenv("TACC_KIM_BIN"              ,pathJoin(kim_dir,"kim-api/bin"))
setenv("TACC_KIM_LIB"              ,pathJoin(kim_dir,"kim-api/lib"))

append_path("PATH",pathJoin(kim_dir,"kim-api/bin"))
prepend_path("LD_LIBRARY_PATH","/opt/apps/gcc/7.3.0/lib64")
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} <<EOF
#%Module3.1.1#################################################
##
## version file for KIMAPI
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
