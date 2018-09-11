################################################################
#
#    KIMAPI SPEC FILE
#
#    MACHINE       :   TACC STAMPEDE2
#    VERSION       :   1.9.6
#    AUTHOR        :   Albert Lu
#    LAST MODIFIED :   07-05-2018
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
# rpmbuild -bb --define 'is_gcc71 1' --define 'is_impi 1' kim_1.9.5.spec | tee log_kim_1.9.5
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

Release:   1%{?dist}
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
  %include system-load.inc
  %include compiler-load.inc
  %include mpi-load.inc
  set -x

  mkdir installed-kim-api
  cd installed-kim-api

  kim_build_dir=`pwd`

  cd ../%{kim_src}
  kim_src_dir=`pwd`

  ml gcc/7.1.0
  ml impi/17.0.3

  ./configure --prefix=${kim_build_dir} --compiler-suite="GCC"  CXX="mpicxx" CC="mpicc" FC="mpif90"
  
  make
  make install

  cd ../kim_env_collection/models
  ${kim_build_dir}/bin/kim-api-v1-build-config --makefile-kim-config > ./Makefile.KIM_Config
  kim_model_dir=`pwd`

  cp -r ../../kim-api-v%{pkg_version}/examples/models/ex_* .

  for i in ex_*; do echo $i | sed 's/.txz//' >> models.txt; done

  cd ../model_drivers
  ${kim_build_dir}/bin/kim-api-v1-build-config --makefile-kim-config > ./Makefile.KIM_Config
  kim_driver_dir=`pwd`

  cp -r ../../kim-api-v%{pkg_version}/examples/model_drivers/ex_* .

  for i in ex_*; do echo $i | sed 's/.txz//' >> drivers.txt; done

  export KIM_API_MODELS_DIR=${kim_model_dir}
  export KIM_API_MODEL_DRIVERS_DIR=${kim_driver_dir}

  # Install drivers

  while read  mo; do
  
    echo $mo
    tar -xf "${mo}.txz"
    cd "${mo}"
    make
    rm -rf *.o *.cpp *.hpp RE* LIC*
    cd ..
    rm "${mo}.txz"

  done < drivers.txt

  # Install models

  cd ../models

  while read  mo; do
  
    echo $mo
    tar -xf "${mo}.txz"
    cd "${mo}"
    make
    rm -rf *.o RE* LIC*
    cd ..
    rm "${mo}.txz"

  done < models.txt

  cd ${kim_src_dir}

  ./configure --prefix="/opt/apps/%{INSTALL_SUFFIX}/kim-api" --compiler-suite="GCC"  CXX="mpicxx" CC="mpicc" FC="mpif90"
  
  make


%endif # BUILD_PACKAGE 

################################################################

%install

echo "Installing the package?:    %{BUILD_PACKAGE}"
echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

cd %{kim_src}

kim_src_dir=`pwd`

# INSTALL KIM API

%if %{?BUILD_PACKAGE}

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  mkdir                  $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api
  mkdir                  $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin
  mkdir -p               $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/etc/bash_completion.d
  mkdir -p               $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/include/kim-api-v1
  mkdir -p               $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  mkdir -p               $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/libexec/kim-api-v1
  mkdir                  $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/models
  mkdir                  $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/model_drivers

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

  cp ./Makefile.KIM_Config                                         ../kim_env_collection/models
  cp ./Makefile.KIM_Config                                         ../kim_env_collection/model_drivers
  cp ./Makefile.KIM_Config                                         $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  cp ./Makefile.Version                                            $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  cp -r $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/bin                 $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  cp -r $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/include/kim-api-v1  $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1/include
  cp -r ./build_system                                             $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1
  cp -r $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/libexec             $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim-api/lib/kim-api-v1

  cd ..

  find kim_env_collection -name \*\*\*.a -exec rm {} \;
  find kim_env_collection -name \*\*\*.hpp -exec rm {} \;
  find kim_env_collection -name \*\*\*.cpp -exec rm {} \;

  cp -r kim_env_collection   $RPM_BUILD_ROOT/%{INSTALL_DIR}/kim_env_collection

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

    LAMMPS (version 16Mar18) installed on Stampede2 was compiled with the 
    KIM package.

    For more information about using KIM package in LAMMPS, please see
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
    local model_dir="%{INSTALL_DIR}/kim_env_collection/models"
    local driver_dir="%{INSTALL_DIR}/kim_env_collection/drivers"    

    setenv("TACC_KIM_DIR"              ,kim_dir)
    setenv("TACC_KIM_API"              ,pathJoin(kim_dir,"kim-api"))
    setenv("TACC_KIM_MODEL"            ,model_dir)
    setenv("TACC_KIM_DRIVER"           ,driver_dir)

    setenv("KIM_API_MODELS_DIR"        ,model_dir)
    setenv("KIM_API_MODEL_DRIVERS_DIR" ,driver_dir)

    append_path("PATH",pathJoin(kim_dir,"kim-api/bin"))
    append_path("LD_LIBRARY_PATH","/opt/apps/gcc/7.1.0/lib64")
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

  cd %{INSTALL_DIR}/kim_env_collection/models

  while read  mo; do

    cd "${mo}"
    ln -s *dynamic-load.so libkim-api-model-v1.so
    cd ..

  done < models.txt

  cd ../model_drivers

  while read  mo; do

    cd "${mo}"
    ln -s *dynamic-load.so libkim-api-model-driver-v1.so
    cd ..

  done < drivers.txt 

  cd ../..

# ----------------------------------------

# Files for LAMMPS

PWD=`pwd`

cat > Makefile.KIM_DIR <<EOF
KIM_INSTALL_DIR=${PWD}/kim-api

.DUMMY: print_dir

print_dir:
	@printf \$(KIM_INSTALL_DIR)
EOF

cat > Makefile.KIM_Config <<EOF
include ${PWD}/kim-api/lib/kim-api-v1/Makefile.KIM_Config
EOF
# -----------------------------------------

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
