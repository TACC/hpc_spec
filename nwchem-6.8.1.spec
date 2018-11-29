#
#
# nwchem-6.8.1 SPEC
# 12/2015
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

Summary: NWCHEM

# Give the package a base name
%define pkg_base_name nwchem
%define MODULE_VAR    NWCHEM

# Create some macros (spec file variables)
%define major_version 6
%define minor_version 8
%define micro_version 1

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
#%define pkg_version %{major_version}.%{minor_version}
#%define pkg_version 6.8.1

### Toggle On/Off ###
%include rpm-dir.inc                  

%include compiler-defines.inc
%include mpi-defines.inc

#%include name-defines-noreloc.inc

########################################
### Construct name based on includes ###
########################################
%include name-defines.inc


########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1
License:   GPL
Group:     Applications/Chemistry
URL:       http://www.nwchem-sw.org/
Packager:  TACC - hliu@tacc.utexas.edu
#Source:    %{pkg_base_name}-%{pkg_version}.revision27746-src.2015-10-20.tar.gz
Source:    %{pkg_version}-release.compiled.tar.gz 
#Source0:   %{pkg_base_name}-%{pkg_version}.tar.bz2
#Source1:   libint-1.1.5.tar.gz
#Source2:   libxc-2.0.1.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Open Source High-Performance Computational Chemistry
Group: Applications/Chemistry
%description package
Open Source High-Performance Computational Chemistry
%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Open Source High-Performance Computational Chemistry
%description
Open Source High-Performance Computational Chemistry
#---------------------------------------
%prep
#---------------------------------------

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

%setup -n %{pkg_base_name}-%{pkg_version}

#---------------------------------------
%build
#---------------------------------------
%include compiler-load.inc
%include mpi-load.inc

export NWCHEM_TOP=$RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/
export NWCHEM_MODULES="all python"
export NWCHEM_TARGET="LINUX64"
export TARGET="LINUX64"

export ARMCI_NETWORK="MPI-PR"

#export MPI_LIB="-L$TACC_CRAY_XPMEM_LIB -L$TACC_CRAY_UGNI_LIB -L$TACC_CRAY_UDREG_LIB -L$TACC_CRAY_PMI_LIB -L$TACC_CRAY_DMAPP_LIB -L$TACC_CRAY_MPT_LIB"
#export MPI_INCLUDE="-I$TACC_CRAY_MPT_INC -I$TACC_CRAY_XPMEM_INC -I$TACC_CRAY_UGNI_INC -I$TACC_CRAY_UDREG_INC -I$TACC_CRAY_DMAPP_INC -I$TACC_CRAY_PMI_INC"
#export LIBMPI="-ldl -lmpichf90_intel -lmpich_intel -lrt -lugni -lpmi -ldl -lxpmem -lpthread -ludreg"
export USE_MPI="y"

export LARGE_FILES="TRUE"
export LIB_DEFINES="-DDFLT_TOT_MEM=16777216"
export USE_NOIO="TRUE"
export USE_NOFSCHECK="TRUE"
export MA_USE_ARMCI_MEM="1"

#export PYTHONHOME=/opt/apps/intel16/python/2.7.10
export PYTHONHOME=/opt/apps/intel18/python2/2.7.15/
export PYTHONVERSION=2.7
#export PYTHONHOME="/usr/"
#export PYTHONVERSION=2.7
export USE_PYTHON=y
export USE_PYTHONCONFIG=Y
module load python2/2.7.15

export USE_INTERNALBLAS=y

#mv $NWCHEM_TOP/src/config/makefile.h makefile.h.orig
#cp $NWCHEM_TOP/makefile.h.6.6.fat $NWCHEM_TOP/src/config/makefile.h

# apply official patches
function patch_me() {
        patches=(Tddft_mxvec20.patch Tools_lib64.patch Config_libs66.patch \
                 Cosmo_meminit.patch Sym_abelian.patch Xccvs98.patch Dplot_tolrho.patch \
                 Driver_smalleig.patch Ga_argv.patch Raman_displ.patch Ga_defs.patch \
                 Zgesvd.patch Cosmo_dftprint.patch Txs_gcc6.patch Gcc6_optfix.patch \
                 Util_gnumakefile.patch Util_getppn.patch Gcc6_macs_optfix.patch Notdir_fc.patch \
                 Xatom_vdw.patch Hfmke.patch)
        for ptch in ${patches[*]}; do
                if [ ! -e $NWCHEM_TOP/$ptch ]; then
                        wget -O $NWCHEM_TOP/${ptch}.gz "http://www.nwchem-sw.org/download.php?f=${ptch}.gz"
                        cd $NWCHEM_TOP/
                        gzip -d $ptch.gz
                        patch -p0 < $ptch
                fi
        done
}
#patch_me

cd $NWCHEM_TOP/src
#make nwchem_config
#make FC=ifort CC=icc


#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
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
  
  # Create some dummy directories and files for fun
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/data

  cp -r $RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/src/basis/libraries             $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
  cp -r $RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/src/data                        $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r $RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/src/nwpw/libraryps/pspw_default $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
  cp -r $RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/src/nwpw/libraryps/paw_default  $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
  cp -r $RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/src/nwpw/libraryps/TM           $RPM_BUILD_ROOT/%{INSTALL_DIR}/data
  cp -r $RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/src/nwpw/libraryps/HGH_LDA      $RPM_BUILD_ROOT/%{INSTALL_DIR}/data

  cp    $RPM_BUILD_DIR/%{pkg_base_name}-%{pkg_version}/bin/LINUX64/nwchem              $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin

  chmod -Rf u+rwX,g+rwX,o=rX                                                           $RPM_BUILD_ROOT/%{INSTALL_DIR}


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
local help_msg=[[

he default envs of the installed NWCHEM
NWCHEM_TOP  %{INSTALL_DIR}/
NWCHEM_NWPW_LIBRARY  %{INSTALL_DIR}/data/
NWCHEM_BASIS_LIBRARY %{INSTALL_DIR}/data/libraries/

To run NWChem, please include the following lines in
your job script, using the appropriate input file name:
module load nwchem
ibrun nwchem input.nw

You need to reset envs BY YOUR OWN if your calculation needs configuration
and input beyond the above defaults

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: NWCHEM")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif
whatis "Category: application, chemistry"
whatis "Keywords: Chemistry, Open Souece"
whatis "URL: http://www.nwchem-sw.org/"
whatis "NWChem aims to provide its users with computational chemistry tools that are scalable both in their ability to treat large scientific computational chemistry problems efficiently, and in their use of available parallel computing resources from high-performance parallel supercomputers to conventional workstation clusters."

-- Create environment variables.
local nwchem_dir="%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(nwchem_dir, "bin"))

setenv("NWCHEM_TOP",nwchem_dir)
setenv("TACC_NWCHEM_DIR",nwchem_dir)
setenv("TACC_NWCHEM_BIN",pathJoin(nwchem_dir,"bin"))
setenv("NWCHEM_NWPW_LIBRARY",pathJoin(nwchem_dir,"data/")..'/')
setenv("NWCHEM_BASIS_LIBRARY",pathJoin(nwchem_dir,"data/libraries/")..'/')

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

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

