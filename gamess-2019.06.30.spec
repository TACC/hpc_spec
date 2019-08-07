# build rpm

# rpmbuild -bb --define 'is_intel18 1' --define 'is_impi 1' --define 'mpiV 18_5' gamess-2019.06.30.spec 2>&1 | tee gamess-2019.06.30_i18_2a.log

# r=/admin/build/admin/rpms/frontera/RPMS/x86_64
#rpm -hiv --nodeps    $r/tacc-gamess-intel18-impi18_0-package-2019.06.30-2.el7.x86_64.rpm
#rpm -hiv --nodeps $r/tacc-gamess-intel18-impi18_0-modulefile-2019.06.30-2.el7.x86_64.rpm

# rpmbuild -bb --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_4' gamess-2019.06.30.spec 2>&1 | tee gamess-2019.06.30_i19_#a.log
# r=/admin/build/admin/rpms/frontera/RPMS/x86_64
#rpm -hiv --nodeps $r/tacc-gamess-intel19-impi19_0-package-2019.06.30-1.el7.x86_64.rpm
#rpm -hiv --nodeps $r/tacc-gamess-intel19-impi19_0-modulefile-2019.06.30-1.el7.x86_64.rpm


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
%define SYS frontera
%define use_relocate %{?relocate}%{!?relocate:0}
%define USE_RELOCATE %( if [[ ${RELOCATE:=0} == 0 ]]; then echo "0"; else echo "1"; fi )


# Give the package a base name and cap name for module env var
%define pkg_base_name gamess
%define MODULE_VAR    GAMESS

# Create some macros (spec file variables)
%define major_version 2019
%define minor_version 06
%define micro_version 30

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


Release:   2%{?dist}
License:   GPL
Vendor:    Ames Lab
Group:     applications/chemistry
Packager:  TACC - milfeld@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar

%define override_vec_flags %{nil}
%define maxcpus 56

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%undefine __brp_python_bytecompile
%undefine py_auto_byte_compile
%global _python_bytecompile_errors_terminate_build 0


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

  export  GMS_PATH=`pwd`
  export  GMS_BUILD=`pwd`

  MAXCPUS=%{maxcpus}

  cd TACC_FILES

  cp                  comp_%{SYS}    ../comp
  cp          install.info_%{SYS}    ../install.info.template
  cp              Makefile_%{SYS}    ../Makefile.template
  cp                rungms_%{SYS}    ../rungms

  cd ..

  sed -i  s'/^set MAXCPUS=.*/set MAXCPUS='$MAXCPUS'/'  ddi/compddi

  sed -i s'@^\s*setenv\s*GMS_PATH\s*$@setenv GMS_PATH $GMS_PATH@' install.info.template
  sed -i s'@^\s*setenv\s*GMS_BUILD_DIR\s*$@setenv GMS_BUILD_DIR $GMS_BUILD@' install.info.template
  cp install.info.template install.info

  sed -i s'@^\s*GMS_PATH\s*=\s*$@GMS_PATH = ${GMS_BUILD}@' Makefile.template
  sed -i s'@^\s*GMS_BUILD_PATH\s*=\s*$@GMS_BUILD_PATH = ${GMS_BUILD}@' Makefile.template
  cp Makefile.template Makefile

  #                       #Prepare activation executable
  sed -e "s/^\*UNX/    /" tools/actvte.code > actvte.f

%endif # BUILD_PACKAGE |


%if %{?BUILD_PACKAGE}
%build

   export  GMS_PATH=`pwd`
   export  GMS_BUILD=`pwd`

   OVERRIDE_VEC_FLAGS=%{override_vec_flags}

             # I really don't want to see the details of modules loading compiler and mpi!

   set +x
   %include system-load.inc
   %include compiler-load.inc
   %include mpi-load.inc
   set -x

   ifort -o tools/actvte.x actvte.f

   [[ ${OVERRIDE_VEC_FLAGS:+hasvalue}  == hasvalue ]] && export TACC_VEC_FLAGS="$OVERRIDE_VEC_FLAGS"

   export TACC_GMS_EXTRAOPTS="-mcmodel=large $TACC_VEC_FLAGS "

   make ddi
   make modules
   make -j 4

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

                              # This puts everything in INSTALL_DIR 
                              # into the RPM_BUILD_ROOT/INSTALL_DIR dir

                              # we are in %%{_topdir}/BUILD = /admin/build/rpms
                              # we are in %%{_builddir}/%%{pkg_basename}-%%{version}   where things are made

  #                       #Move files to rpm build directories
  
  cp -p         gms-files.csh    $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp gamess.*                    $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -p TACC_FILES/rungms_%{SYS} $RPM_BUILD_ROOT/%{INSTALL_DIR}/rungms

  cp -pr              auxdata    $RPM_BUILD_ROOT/%{INSTALL_DIR}
  rm -rf                         $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata/QUANPOL/RXNFLD3840.DAT

  cp -pr                tools    $RPM_BUILD_ROOT/%{INSTALL_DIR}

  cp                    *.DOC    $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc

  cp -pr                  bin    $RPM_BUILD_ROOT/%{INSTALL_DIR}

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

  chmod 755                      $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
  chmod 755                      $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/*

 #cp -r tests $RPM_BUILD_ROOT/%{INSTALL_DIR}
                
  
%endif # BUILD_PACKAGE |


%if %{?BUILD_MODULEFILE}

  rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR} #Delete the module installation directory.
  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  %if %{?USE_RELOCATE} || %{?use_relocate}
     touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  %endif

echo "gms_dir=%{INSTALL_DIR}"  
echo "intel_lib_dir=$TACC_INTEL_LIB"
                              # Write out the modulefile

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message=[[
The %{MODULE_VAR} modulefile defines the following environment variables:
TACC_%{MODULE_VAR}_DIR/BIN/DOC/DATA/TOL for the location of the Gamess home
directory and the gamess.00.x file, script files, documentation, the aux data 
directory, and tools, respectively.
The modulefile also defines GMSPATH (Gamess dir) and VERNO (00) for use in rungms.
Both GMSPATH and the bin directory are included in the PATH variable.

To run GAMESS, include the following lines in your job script.

       module load gamess

       rungms my_molecule 
    or
       rungms my_molecule NCPUS

where my_molecule is the input file name. The input file must have an .inp suffix.
But it is not necessary to include the suffix in the name used on the rungms command.

e.g. for an h2.inp input file you can run gamess with

      rungms h2.inp  or rungms h2

Note: rungms uses a special mpirun launcher, mpiexec.hydra, to launch gamess.00.x, 
so you do not need to use ibrun.

NCPUS is the number of COMPUTING service processes that will be used, and
NCPUS additional       DATA      service processes will be launched.
NCPUS should normally be one-half of the number of cores on a node (28).

If NCPUS is not supplied rungms will use one-half of the number of tasks
requested (with the -n option) for COMPUTING service processes and
one-half the number of tasks for   DATA      service processes.
(So always use an even number of tasks, and never requests more than 56
tasks per node.)

If using NCPUS, make sure that NCPUS/N >= 28,
where N is the number of nodes (N=1,2,3,4, etc.)

***** IMPORTANT *****
Rungms will not allow you to run more than 56 services per node 
(28 compute and 28 data).

This version of gamess was compiled with %{} compiler flag.

Version %{version}

]]

help(help_message,"\n")

whatis("Name:    %{pkg_base_name}")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Quantum, Application")
whatis("URL: http://www.msg.ameslab.gov/GAMESS/")
whatis("Description: General ab initio quantum chemistry package")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local gms_dir = "%{INSTALL_DIR}"

family("GAMESS")

-- TACC Variables
setenv("TACC_%{MODULE_VAR}_DIR",  gms_dir)
setenv("TACC_%{MODULE_VAR}_BIN",  gms_dir)
setenv("TACC_%{MODULE_VAR}_DOC",  pathJoin(gms_dir,"doc")     )
setenv("TACC_%{MODULE_VAR}_TOL",  pathJoin(gms_dir,"tools")   )
setenv("TACC_%{MODULE_VAR}_DAT",  pathJoin(gms_dir,"auxdata") )

--
-- GMS Variables and PATH append
--

setenv("VERNO",                 "00"      )
setenv("GMSPATH",               gms_dir   )
prepend_path("PATH",            gms_dir   )
prepend_path("PATH",            pathJoin(gms_dir,"bin")   )

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
