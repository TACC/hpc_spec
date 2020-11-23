#
# Amit Ruhela
# 2020-09-20 Add name-defines-noreloc.inc
# 2020-09-20 Need to investigate relocation -- use /opt/apps for now
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
# rpm -qilp tacc-pgi-package-20.7.0-1.el7.x86_64.rpm
# rpm -qilp tacc-pgi-modulefile-20.7.0-1.el7.x86_64.rpm
# rpm –hiv --relocate /tmprpm=/opt/apps tacc-pgi-package-20.7.0-1.el7.x86_64.rpm
# rpm –hiv --relocate /tmpmod=/opt/apps tacc-pgi-modulefile-20.7.0-1.el7.x86_64.rpm
# rpm -e tacc-pgi-package-20.7.0-1.el7.x86_64.rpm tacc-pgi-modulefile-20.7.0-1.el7.x86_64.rpm

Summary: A Nice little non-relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name pgi
%define MODULE_VAR    PGI

# Create some macros (spec file variables)
%define major_version 20
%define minor_version 7
%define micro_version 0

%define year 2020
%define pgversion %{major_version}.%{minor_version}
%define moduleversion  %{pkg_base_name}%{major_version}

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pgi_ver pgi%{pgversion}

%global __os_install_post %{nil}

%define APPS /opt/apps
%define PKG_BASE %{APPS}/%{pkg_base_name}/%{pkg_version}

### Toggle On/Off ###
%include rpm-dir.inc
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines.inc
#%include name-defines-noreloc.inc

%define lib_dir linuxpower/%{major_version}.%{minor_version}
%{echo: INSTALL_DIR = %{INSTALL_DIR} }

%define lib_dir Linux_ppc64le/%{major_version}.%{minor_version}                                                              


########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   2%{?dist}
License:   Community
Group:     Development/Tools
URL:       https://www.pgroup.com/products/community.htm
Packager:  TACC - aruhela@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

#--------------------------------------- '
%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the package RPM...
The PGI Compiler Collection includes PGI C, C++, Fortran, OpenMP, and OpenACC.
PGI C and C++ optimize ANSI C11 and GNU-compatible C++17 compilers. Both
compilers implement OpenMP 4.5 pragma-based parallel programming for multicore
CPUs, and OpenACC 2.6 pragma-based parallel programming for CPUs and NVIDIA
GPUs. PGI Fortran supports the industry standard ISO_C_BINDING, which allows
for easy argument passing and procedure invocation between Fortran, C, and C++.

#--------------------------------------- '
%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the modulefile RPM...
The PGI Compiler Collection includes PGI C, C++, Fortran, OpenMP, and OpenACC.
PGI C and C++ optimize ANSI C11 and GNU-compatible C++17 compilers. Both
compilers implement OpenMP 4.5 pragma-based parallel programming for multicore
CPUs, and OpenACC 2.6 pragma-based parallel programming for CPUs and NVIDIA
GPUs. PGI Fortran supports the industry standard ISO_C_BINDING, which allows
for easy argument passing and procedure invocation between Fortran, C, and C++.

#--------------------------------------- '
%description
The PGI Compiler Collection includes PGI C, C++, Fortran, OpenMP, and OpenACC.
PGI C and C++ optimize ANSI C11 and GNU-compatible C++17 compilers. Both
compilers implement OpenMP 4.5 pragma-based parallel programming for multicore
CPUs, and OpenACC 2.6 pragma-based parallel programming for CPUs and NVIDIA
GPUs. PGI Fortran supports the industry standard ISO_C_BINDING, which allows
for easy argument passing and procedure invocation between Fortran, C, and C++.

#--------------------------------------- '
%prep
#---------------------------------------
echo "RPM_BUILD_ROOT=$RPM_BUILD_ROOT"                                     
                                                                              

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"
echo "pgi_install = %{pgi_install}"                                    
echo "MODULE_PREFIX = %{MODULE_PREFIX}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  mount -t tmpfs tmpfs %{INSTALL_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================
export LMOD_SH_DBG_ON=1
##################################################
export pgi=`pwd`
##################################################

export PATH=${pgi_install}/${lib_dir}/bin:${PATH}
export LD_LIBRARY_PATH=${pgi_install}/${lib_dir}/lib:${LD_LIBRARY_PATH}

export pgi_major=%{major_version}
export pgi_minor=%{minor_version}
export pgi_patch=%{micro_version}

export pgi_version=${pgi_major}.${pgi_minor}.${pgi_patch}

cd ${pgi}

printf "\n\n************************************************************\n"
printf "Installing PGI\n"
printf "************************************************************\n\n"

#wget https://www.pgroup.com/support/download_community.php?file=pgi-community-linux-x64

#cp /root/rpmbuild/SOURCES/pgi/20.7/nvhpc_2020_207_Linux_ppc64le_cuda_multi.tar.gz
#tar xpzf nvhpc_2020_207_Linux_ppc64le_cuda_multi.tar.gz
set -x
cd /root/rpmbuild/SOURCES/pgi/20.7/nvhpc_2020_207_Linux_ppc64le_cuda_multi

export NVHPC_SILENT=true
export NVHPC_INSTALL_DIR=%{INSTALL_DIR}
export NVHPC_INSTALL_TYPE=single
export NVHPC_DEFAULT_CUDA=11.0

./install

cd  %{INSTALL_DIR}
rm -rf modulefiles

cd %{INSTALL_DIR}/%{lib_dir}
ls
rm -rf ../%{year}
rm -rf REDIST
rm -rf profilers
rm -rf math_libs
echo -e "\nThe directory contents are:"
ls
ls ..
cd  %{INSTALL_DIR}/..

if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/
set +x

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message = [[
The PGI Compiler Collection %{pkg_version} includes PGI C, C++, Fortran, OpenMP,
and OpenACC. PGI C and C++ optimize ANSI C11 and GNU-compatible C++17 compilers.
Both compilers implement OpenMP 4.5 pragma-based parallel programming for
multicore CPUs, and OpenACC 2.6 pragma-based parallel programming for CPUs and
NVIDIA GPUs. PGI Fortran supports the industry standard ISO_C_BINDING, which
allows for easy argument passing and procedure invocation between Fortran, C,
and C++.


This module loads PGI Compiler variables.
The command directory is added to PATH.
The library directory is added to LD_LIBRARY_PATH.
The include directory is added to INCLUDE.
The man     directory is added to MANPATH.

Also Defined:
TACC_%{MODULE_VAR}_DIR   = %{MODULE_VAR} base             directory
TACC_%{MODULE_VAR}_BIN   = %{MODULE_VAR} binary           directory
TACC_%{MODULE_VAR}_LIB   = %{MODULE_VAR} library          directory
TACC_%{MODULE_VAR}_INC   = %{MODULE_VAR} include          directory

Note: The $TACC_VEC_FLAGS environment variable is provided as a convenience
during your compliation step. This variable specifies instruction sets
appropriate to build and run on any compute node).
                        

The PGI module also defines the following environment variables:
TACC_PGI_DIR, TACC_PGI_LIB, TACC_PGI_INC and
TACC_PGI_BIN for the location of the PGI distribution,
libraries, include files, and tools respectively.

Version %{pkg_version}
]]

help(help_message,"\n")

whatis("Name: PGI Compilers")
whatis("Version: %{pkg_version}")
whatis("Category: compiler")
whatis("Keywords: System, compiler")
whatis("URL: https://www.pgroup.com")

-- Create environment variables
local nvcudadir = "/opt/apps/%{INSTALL_SUFFIX}/%{lib_dir}/cuda"
local nvcompdir = "/opt/apps/%{INSTALL_SUFFIX}/%{lib_dir}/compilers"
local nvcommdir = "/opt/apps/%{INSTALL_SUFFIX}/%{lib_dir}/comm_libs"

prepend_path( "PATH"                     , pathJoin(nvcudadir,"bin"       ))
prepend_path( "PATH"                     , pathJoin(nvcompdir,"bin"       ))
prepend_path( "PATH"                     , pathJoin(nvprofdir,"bin"       ))

prepend_path( "LD_LIBRARY_PATH"          , pathJoin(nvcudadir,"lib64"       )               )
prepend_path( "LD_LIBRARY_PATH"          , pathJoin(nvcompdir,"lib"                 ))
prepend_path( "LD_LIBRARY_PATH"          , pathJoin(nvmathdir,"lib"                 ))
prepend_path( "MANPATH"                  , pathJoin(nvcompdir,"man" )               )


prepend_path( "CPATH"                    , pathJoin(nvcudadir,"include"                         ))
prepend_path( "CPATH"                    , pathJoin(nvcompdir,"include"                         ))
prepend_path( "CPATH"                    , pathJoin(nvmathdir,"include"                         ))
prepend_path( "CPATH"                    , pathJoin(nvcompdir,"include_acc"                     ))
prepend_path( "CPATH"                    , pathJoin(nvcompdir,"include_omp"                     ))
prepend_path( "CPATH"                    , pathJoin(nvcompdir,"include-gcc70"                   ))
prepend_path( "MODULEPATH"               , "/opt/apps/pgi%{major_version}/modulefiles"   )

setenv(       "PGI"                      , "/opt/apps/%{INSTALL_SUFFIX}"  )
setenv(       "NVHPC"                    , nvcompdir                      )
setenv(       "%{MODULE_VAR}_LIB"        , pathJoin(nvcompdir,"lib"       ))
setenv(       "OPAL_PREFIX"              , pathJoin(nvcommdir,"openmpi/openmpi-3.1.5"       ))

setenv(       "TACC_%{MODULE_VAR}_DIR"   , nvcompdir                      )
setenv(       "TACC_%{MODULE_VAR}_BIN"   , pathJoin(nvcompdir,"bin"       ))
setenv(       "TACC_%{MODULE_VAR}_LIB"   , pathJoin(nvcompdir,"lib"       ))
setenv(       "TACC_%{MODULE_VAR}_INC"   , pathJoin(nvcompdir,"include"   ))                                                                           

if (os.getenv("TACC_SYSTEM") == "longhorn") then
  setenv( "TACC_VEC_FLAGS" ,      "-i8 -m64 -mcmodel=medium -Mdalign -Mllalign -O2 -fastsse -Mipa=fast  -Mvect=simd:256" )
end

family("compiler")
EOF


cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
echo "PKG_BASE = %{PKG_BASE} INSTALL_DIR = %{INSTALL_DIR} pgi_ver = %{pgi_ver}"
%{PKG_BASE}/%{lib_dir}/compilers/bin/makelocalrc -x %{PKG_BASE}/%{lib_dir}/compilers/bin

%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT


