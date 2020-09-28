# build rpm

# rpmbuild -bb --clean  --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_7' gamess-2019.09.30R2.spec   2>&1 | tee gamess-2019.09.30R2.r#_x.log

#r=/admin/build/admin/rpms/stampede2/RPMS/x86_64
#rpm -hiv --nodeps $r/tacc-gamess-intel19-impi19_0-package-2019.09.30R2-1.el7.x86_64.rpm
#rpm -hiv --nodeps $r/tacc-gamess-intel19-impi19_0-modulefile-2019.09.30R2-1.el7.x86_64.rpm


#
# Build only PACKAGE or MODULE -- set variable.  E.g. NO_PACKAGE=1 rpmbuild -bb ... only build modulefile
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM


# install rpm in /opt/apps # install r= RPMS/x86-64 directory
# rpm -hiv --relocate /tmprpm=/opt/apps $r/tacc-gamess-package...
# rpm -hiv --relocate /tmpmod=/opt/apps $r/tacc-gamess-modulefile...

# remove rpm
# rpm -e tacc-gamess-package......el7.centos.x86_64
# rpm -e tacc-gamess-modulefile...el7.centos.x86_64
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#

# define system; if macro relocate or env variable RELOCATE is 1, use relocation
%define SYS sp2
%define use_relocate %{?relocate}%{!?relocate:0}
%define USE_RELOCATE %( if [[ ${RELOCATE:=0} == 0 ]]; then echo "0"; else echo "1"; fi )


# Give the package a base name and cap name for module env var
%define pkg_base_name gamess
%define MODULE_VAR    GAMESS

# Create some macros (spec file variables)
%define major_version 2019
%define minor_version 09
%define micro_version 30R2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc


 %include name-defines.inc


%if %{?USE_RELOCATE} || %{?use_relocate}
   %include name-defines.inc
%else
   %include name-defines-noreloc.inc
%endif

Summary:   Spec file for gamess
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot


Release:   1%{?dist}
License:   GPL
Vendor:    Ames Lab
Group:     applications/chemistry
Packager:  TACC - milfeld@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%undefine __brp_python_bytecompile
%undefine   py_auto_byte_compile
%global _python_bytecompile_extra 0
# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


%package %{PACKAGE}
Summary: GAMESS QM Application 
Group:   applications/chemistry
%description package
Quantum Chemistry Application

%package %{MODULEFILE}
Summary: GAMESS QM Application 
Group:     applications/chemistry
%description modulefile
Modulefile includes gamess executable an rungms in directory PATH; defines GMSPATH, and TACC_GAMESS_DIR/BIN/DOC/DATA
  

%description
GAMESS can compute SCF wavefunctions ranging from RHF, ROHF, UHF, GVB, and MCSCF. Correlation corrections to these SCF wavefunctions include Configuration Interaction, second order Perturbation Theory, and Coupled-Cluster approaches, as well as the Density Functional Theory approximation. Nuclear gradients are available, for automatic geometry optimization, transition state searches, or reaction path following. Computation of the energy hessian permits prediction of vibrational frequencies, with IR or Raman intensities. Solvent effects may be modeled by the discrete Effective Fragment Potentials, or continuum models such as the Polarizable Continuum Model. Numerous relativistic computations are available, including third order Douglas-Kroll scalar corrections, and various spin-orbit coupling options. The Fragment Molecular Orbital method permits use of many of these sophisticated treatments to be used on very large systems, by dividing the computation into small fragments.

#This one is queryable with rpm -qi <rpm-name>

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

# do %%dump to get all the variable names then exit (but exit didn't work, did others, prep,...



%prep


%if %{?BUILD_PACKAGE}
%setup -n %{pkg_base_name}-%{pkg_version}

  export  SYSTEM=stampede2
  export  TACC_GMS_EXTRAOPTS="-mcmodel=large -xCORE-AVX2 -axCORE-AVX512,MIC-AVX512 -diag-disable=15009 "
  export  MAXCPUS=68

  export  GMS_PATH=`pwd`
  export  GMS_BUILD=`pwd`

  cd TACC_FILES
  cp -p               comp_${SYSTEM}_g19  ../comp
  cp -p       install.info_${SYSTEM}_g19  ../install.info.template
  cp -p             rungms_${SYSTEM}_g19  ../rungms
  cp -p           Makefile_${SYSTEM}_g19  ../Makefile
  cp -p        Makefile.in_${SYSTEM}_g19  ../Makefile.in
  cp -p           actvte.x_${SYSTEM}_g19  ../tools/actvte.x
  cp -p            compddi_${SYSTEM}_g19  ../ddi/compddi
  cp -p               lked_${SYSTEM}_g19  ../lked
  cd ..

  sed -i  s'/^set MAXCPUS=.*/set MAXCPUS='$MAXCPUS'/'                   ddi/compddi

  sed -i  s'@^\s*GMS_PATH\s*=.*$@GMS_PATH = '$GMS_PATH'@'               Makefile
  sed -i  s'@^\s*GMS_BUILD_PATH\s*=.*$@GMS_BUILD_PATH = '$GMS_BUILD'@'  Makefile


  sed -i 's@^\s*setenv\s*GMS_PATH.*$@setenv GMS_PATH '$GMS_PATH'@'            install.info.template
  sed -i 's@^\s*setenv\s*GMS_BUILD_DIR.*$@setenv GMS_BUILD_DIR '$GMS_BUILD'@' install.info.template
  echo "setenv TACC_GMS_EXTRAOPTS \"$TACC_GMS_EXTRAOPTS\""                  >>install.info.template

  cp install.info.template install.info

  #                       #Prepare activation executable
  #sed -e "s/^\*UNX/    /" tools/actvte.code > actvte.f

%endif # BUILD_PACKAGE |


%if %{?BUILD_PACKAGE}
%build

   export  GMS_PATH=`pwd`
   export  GMS_BUILD=`pwd`
             # I really don't want to see the details of modules loading compiler and mpi!
   set +x
   %include system-load.inc
   %include compiler-load.inc
   %include mpi-load.inc
   set -x

   #ifort -o tools/actvte.x actvte.f

   make ddi
   make modules
   make -j 12
   echo "FINISHED WITH BUILD"

%endif # BUILD_PACKAGE |


%if %{?BUILD_PACKAGE}
%install
%undefine py_auto_byte_compile
%undefine __brp_python_bytecompile

  rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR} # Delete the package installation directory.
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
  

%if %{?USE_RELOCATE} || %{?use_relocate}
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
%endif

  echo "TACC_OPT %{TACC_OPT}"
                              # This puts everything in INSTALL_DIR 
                              # into the RPM_BUILD_ROOT/INSTALL_DIR dir

                              # we are in %%{_topdir}/BUILD = /admin/build/rpms
                              # we are in %%{_builddir}/%%{pkg_basename}-%%{version}   where things are made

  #                       #Move files to rpm build directories
  
  cp -p         gms-files.csh    $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -p gamess.*                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -p rungms                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/rungms

  cp -pr              auxdata    $RPM_BUILD_ROOT/%{INSTALL_DIR}
  rm -rf                         $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata/QUANPOL/RXNFLD3840.DAT

  cp -pr                tools    $RPM_BUILD_ROOT/%{INSTALL_DIR}

  cp                    *.DOC    $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc

  chmod a+rX                     $RPM_BUILD_ROOT/%{INSTALL_DIR}
  chmod a+rx                     $RPM_BUILD_ROOT/%{INSTALL_DIR}/gms-files.csh
  chmod a+rx                     $RPM_BUILD_ROOT/%{INSTALL_DIR}/gamess.*
  chmod a+rx                     $RPM_BUILD_ROOT/%{INSTALL_DIR}/rungms

 # Extend user permissions to other and group, but remove w on other
  chmod -R g=u                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata
  chmod -R o=u                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata
  chmod -R o-w                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata

 # Extend user permissions to other and group, but remove w on other
  chmod -R g=u                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools
  chmod -R o=u                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools
  chmod -R o-w                   $RPM_BUILD_ROOT/%{INSTALL_DIR}/tools

  chmod a+rx                     $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
  chmod a+r                      $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc/*


 #cp -r tests $RPM_BUILD_ROOT/%{INSTALL_DIR}
                
  
%endif # BUILD_PACKAGE |


%if %{?BUILD_MODULEFILE}

  rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR} #Delete the module installation directory.
  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  %if %{?USE_RELOCATE} || %{?use_relocate}
     touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  %endif

echo "gms_dir=%{INSTALL_DIR}"  
                              # Write out the modulefile

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message=[[
The %{MODULE_VAR} modulefile defines the following environment variables:
TACC_%{MODULE_VAR}_DIR/BIN/DOC/DATA/TOOLS for the location of the Gamess home,
documentation, binaries and aux data directories, respectively.
The modulefile defines GMSPATH (Gamess dir) used in rungms.

To run GAMESS, include the following lines in your job script.

       module load gamess
       rungms my_molecule
     or
       rungms my_molecule NCPUS

where my_molecule is the input file name. The input file must have an .inp suffix.
But it is not necessary to include the suffix in the name used on the rungms command.

The gamess.00.x executable is a fat binary-- it is compiled to run on either the
KNL or SKX/CLX nodes. NCPUS is the number of GAMESS COMPUTION servers. 
GAMESS will automatically use an additional NCPUS (cores) for DATA servers.

***** IMPORTANT for execution ****************

SKX and CLX nodes:

Single node (max values): 
   NCPUS should be           = 1/2 number of cores on a node.
   The number of batch tasks =     number of cores on a node.

Multi node (max values): 
   NCPUS should be           = 1/2 number of Nodes x  number of cores per node.
   The number of batch tasks =     number of Nodes x  number of cores per node.

If NPCUS is set too high, rungms will automaticaly adjust it to the max value.

KNL nodes:
Due to the excessive use of Virtual Memory (VM) only NCPUS can only be 18
(18 COMPUTATION + 18 DATA servers).  On a node GAMESS doesn't scale well 
beyond 36 cores.  SKX/CLX nodes runs are more than 2x faster than KNL runs.
TACC staff is working on the VM problem, and will update gamess ASAP.

e.g. for an h2.inp input file you can run gamess with

      rungms h2.inp  or rungms h2

(rungms uses a special mpirun launcher, mpiexec.hydra, to launch gamess, so you do not
need to use ibrun.)

NCPUS is number of computing processes you want to use and the default value is the total
tasks requested in the slurm job script. (This should be half the number of cores on a node.
The other half of the cores will be used a data servers.)

If you need to use the QUANPOL/RXNFLD3840.DAT data file please contact TACC.
The virtual memory for the GAMESS knl version has been reduced, by eliminating the
space bloat of the Effective Fragment Potential (EFP) module.  
If you need to use this method, please contact TACC.

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

whatis("Name: %{pkg_base_name}")
whatis("Version: %{pkg_version}%{dbg}")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local gms_dir           = "%{INSTALL_DIR}"

family("GAMESS")

setenv("TACC_%{MODULE_VAR}_DIR",  gms_dir)
setenv("TACC_%{MODULE_VAR}_BIN",  gms_dir)
setenv("TACC_%{MODULE_VAR}_DOC",  pathJoin(gms_dir,"doc")     )
setenv("TACC_%{MODULE_VAR}_TOOLS",pathJoin(gms_dir,"tools")   )
setenv("TACC_%{MODULE_VAR}_DATA", pathJoin(gms_dir,"auxdata") )

--
-- GMS Variables and PATH append
--

setenv("VERNO",                 "00"      )
setenv("GMSPATH",               gms_dir   )
prepend_path("PATH",            gms_dir   )

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{pkg_basename}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
# %if %{?VISIBLE}
#   %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
# %endif

%endif # BUILD_MODULEFILE |


%if %{?BUILD_PACKAGE}
%files package
 
  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

%endif # BUILD_PACKAGE |


%if %{?BUILD_MODULEFILE}
%files modulefile 

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

%endif # BUILD_MODULEFILE |

## Fix Modulefile During Post Install ##

%if %{?USE_RELOCATE} || %{?use_relocate}

%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc

%endif

############ Do Not Remove #############

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT
