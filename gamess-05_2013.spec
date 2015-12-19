#rpmbuild -bb --define 'is_intel16 1' --define 'is_cmpich 1' --define 'mpiV 7_2' gamess-05_2013.spec | tee gamess.log.1
#rpm -i --nodeps --relocate /tmpmod=/opt/apps $r/tacc-gamess-intel16-cray_mpich_7_2-modulefile-05_2013-1.x86_64.rpm
#rpm -i --nodeps --relocate /tmprpm=/opt/apps $r/tacc-gamess-intel16-cray_mpich_7_2-package-05_2013-1.x86_64.rpm
Summary: Summary:   GAMESS is a program for ab initio molecular quantum chemistry

%define pkg_base_name gamess
%define MODULE_VAR    gamess

%define major_version 05_2013
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}

%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc

%include name-defines.inc

Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

Release:   2
License:   GPL
Vendor:    Ames Lab 
Group:     applications/chemistry
URL:       http://www.msg.ameslab.gov/gamess
Source:    gamess-05_2013.tar.gz
Packager:  TACC - milfeld@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: application/chemistry
%description package
GAMESS can compute SCF wavefunctions ranging from RHF, ROHF, UHF, GVB, and MCSCF. 
Correlation corrections to these SCF wavefunctions include Configuration Interaction, 
second order Perturbation Theory, and Coupled-Cluster approaches, as well as the 
Density Functional Theory approximation. Nuclear gradients are available,  
for automatic geometry optimization, transition state searches, or reaction path following. 
Computation of the energy hessian permits prediction of vibrational frequencies, with IR  
or Raman intensities. Solvent effects may be modeled by the discrete Effective Fragment Potentials, 
or continuum models such as the Polarizable Continuum Model. Numerous relativistic  
computations are available, including third order Douglas-Kroll scalar corrections,  
and various spin-orbit coupling options. The Fragment Molecular Orbital method permits  
use of many of these sophisticated treatments to be used on very large systems, by dividing 
the computation into small fragments.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
GAMESS QM modulefile.

#Will be in rpm and is queryable if installed via: rpm -qi <rpm-name>
%description
GAMESS can compute SCF wavefunctions ranging from RHF, ROHF, UHF, GVB, and MCSCF. 
Correlation corrections to these SCF wavefunctions include Configuration Interaction, 
second order Perturbation Theory, and Coupled-Cluster approaches, as well as the 
Density Functional Theory approximation. Nuclear gradients are available,  
for automatic geometry optimization, transition state searches, or reaction path following. 
Computation of the energy hessian permits prediction of vibrational frequencies, with IR  
or Raman intensities. Solvent effects may be modeled by the discrete Effective Fragment Potentials, 
or continuum models such as the Polarizable Continuum Model. Numerous relativistic  
computations are available, including third order Douglas-Kroll scalar corrections,  
and various spin-orbit coupling options. The Fragment Molecular Orbital method permits  
use of many of these sophisticated treatments to be used on very large systems, by dividing 
the computation into small fragments.


%prep

%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n %{pkg_base_name}-%{pkg_version}
%endif # BUILD_PACKAGE |

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif # BUILD_MODULEFILE |


%build
%if %{?BUILD_PACKAGE}

  unset MODULEPATH
  if [ -f "$BASH_ENV" ]; then
    . $BASH_ENV
  set +xv
    module purge
  set -xv
    clearMT
    MP="/opt/apps/tools/modulefiles:/opt/apps/modulefiles"

    if [ -z "$MODULEPATH" ]; then
     export MODULEPATH=$(/opt/apps/lmod/lmod/libexec/addto --append MODULEPATH ${MP//:/ })
    fi  
  fi
set +xv
  module load %{comp_module}
  module load %{mpi_module}
set -xv

  echo "Installing the package?:    %{BUILD_PACKAGE}"
  echo "Installing the modulefile?: %{BUILD_MODULEFILE}"

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary


  export GMS_PATH=`pwd`
  export GMS_BUILD=`pwd`
  cd TACC_FILES

     cp lked_lonestar     ../lked
     cp install.info      ../install.info.template
     cp Makefile          ../Makefile.template
     cp rungms_tacc       ../machines/unix/rungms
     cp ibrun_gms         ../machines/unix/ibrun_gms
     cp compddi           ../ddi/compddi
     cp comp              ../comp

  #  IF using impi, uncomment out next line
  #  cp install.info_impi ../install.info.template


  cd $GMS_BUILD

  sed -i s'@^\s*setenv\s*GMS_PATH\s*$@setenv GMS_PATH $GMS_BUILD@' install.info.template
  sed -i s'@^\s*setenv\s*GMS_BUILD_DIR\s*$@setenv GMS_BUILD_DIR $GMS_BUILD@' install.info.template
  cp install.info.template install.info

  sed -i s'@^\s*GMS_PATH\s*=\s*$@GMS_PATH = ${GMS_BUILD}@' Makefile.template
  sed -i s'@^\s*GMS_BUILD_PATH\s*=\s*$@GMS_BUILD_PATH = ${GMS_BUILD}@' Makefile.template
  cp Makefile.template Makefile
 
  #                       #Prepare activation executable
  sed -e "s/^\*UNX/    /" tools/actvte.code > actvte.f
  ifort -o tools/actvte.x actvte.f


  make -j 8
 

%endif # BUILD_PACKAGE |


%install

  %include system-load.inc
  set +xv
  module purge
  set -xv
 
  echo "Installing the package?:    %{BUILD_PACKAGE}"
  echo "Installing the modulefile?: %{BUILD_MODULEFILE}"
 

%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    touch    $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
    

    #                       #Move files to rpm build directories
    #                       #Uses special  ibrun for  gamess (ibrun_gms)
    
    cp gamess.00.x                $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
    cp gms-files.csh              $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
    cp machines/unix/rungms       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
    cp machines/unix/ibrun_gms    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
    cp -pr             auxdata    $RPM_BUILD_ROOT/%{INSTALL_DIR}
    rm -rf                        $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata/QUANPOL/RXNFLD3840.DAT
    cp -pr               tools    $RPM_BUILD_ROOT/%{INSTALL_DIR}
    #chmod -Rf u+rwX,g+rwX,o=rX    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
    chmod a+rX                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
    chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/gamess.00.x
    chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/gms-files.csh
    chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/rungms
    chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/ibrun_gms
    
    ###
    ### Install tests and documentation
    ###
    
    mkdir -p    $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
    cp *.DOC    $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
    cp -r tests $RPM_BUILD_ROOT/%{INSTALL_DIR}

%endif #BUILD_PACKAGE


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
local help_message=[[
The GAMESS modulefile defines the following environment variables:
TACC_GAMESS_DIR/DOC/BIN/DATA for the location of the Gamess home,
documentation, binaries and aux data directories, respectively.
The modulefile defines GMSPATH (Gamess dir) used in rungms.

To run GAMESS, include the following lines in your job script.

       module load gamess
       rungms my_molecule or
       rungms my_molecule NCPUS

where my_molecule is the input file name. The input file must have an .inp suffix.
But it is not necessary to include the suffix in the name used on the rungms command.
e.g. for an h2.inp input file you can run gamess with

      rungms h2.inp  or rungms h2

(rungms uses a special mpirun command, mpiexec.hydra, to launch gamess, so you do not
need to use ibrun.)  Because gamess uses one DDI memory server for each MPI task, 
request only 1/2 the available cores on a node (e.g. 12/node on lonestar and 8/node
on stampede). rungms will automatically use the other cores for memory servers.

NCPUS is number of computing processes you want to use and the default value is the total
tasks requested in the slurm job script. If you need to use the QUANPOL/RXNFLD3840.DAT
data file please contact TACC.

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Quantum, Application")
whatis("URL: http://www.msg.ameslab.gov/GAMESS/")
whatis("Description: General ab initio quantum chemistry package")

local gms_dir="%{INSTALL_DIR}"
--
-- TACC Variables
--
setenv("TACC_GAMESS_DIR",  gms_dir)
setenv("TACC_GAMESS_BIN",  pathJoin(gms_dir,"bin" ) )
setenv("TACC_GAMESS_DOC",  pathJoin(gms_dir,"doc" ) )
setenv("TACC_GAMESS_DATA", pathJoin(gms_dir,"auxdata") )
--
-- GMS Variables and PATH append
--
setenv("GMSPATH",          gms_dir)
append_path("PATH",        pathJoin(gms_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile only if a visible module
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

