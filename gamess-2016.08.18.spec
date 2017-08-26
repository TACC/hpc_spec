# build rpm

# rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1' gamess-2016.08.18.spec 2>&1 | tee gamess-2016.08.18.log
# rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1' gamess-2016.08.18-x.spec 2>&1 | tee gamess-2016.08.18-x.log
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

# Give the package a base name and cap name for module env var
%define pkg_base_name gamess
%define MODULE_VAR    GAMESS

# Create some macros (spec file variables)
%define major_version 2016
%define minor_version 08
%define micro_version 18

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc


 %include name-defines.inc
#%include name-defines-noreloc.inc


Summary:   Spec file for gamess
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot


Release:   1%{?dist}
License:   GPL
Vendor:    Ames Lab
Group:     applications/chemistry
Packager:  TACC - milfeld@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: GAMESS QM Application 
Group:   applications/chemistry
%description package
Quantum Chemistry Application

%package %{MODULEFILE}
Summary: GAMESS QM Application 
Group:     applications/chemistry
%description modulefile
Modulefile includes gamess bin in directory PATH; defines GMSPATH, and TACC_GAMESS_DIR/BIN/DOC/DATA
  

%description
GAMESS can compute SCF wavefunctions ranging from RHF, ROHF, UHF, GVB, and MCSCF. Correlation corrections to these SCF wavefunctions include Configuration Interaction, second order Perturbation Theory, and Coupled-Cluster approaches, as well as the Density Functional Theory approximation. Nuclear gradients are available, for automatic geometry optimization, transition state searches, or reaction path following. Computation of the energy hessian permits prediction of vibrational frequencies, with IR or Raman intensities. Solvent effects may be modeled by the discrete Effective Fragment Potentials, or continuum models such as the Polarizable Continuum Model. Numerous relativistic computations are available, including third order Douglas-Kroll scalar corrections, and various spin-orbit coupling options. The Fragment Molecular Orbital method permits use of many of these sophisticated treatments to be used on very large systems, by dividing the computation into small fragments.

#This one is queryable with rpm -qi <rpm-name>

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"


# do %%dump to get all the variable names then exit (but exit didn't work, did others, prep,...


%define verbose
%prep


%if %{?BUILD_PACKAGE}
%setup -n %{pkg_base_name}-%{pkg_version}

  export  GMS_PATH=`pwd`
  export  GMS_BUILD=`pwd`

  cd TACC_FILES

  cp                  lked_${SYS}    ../lked
  cp                  comp_${SYS}    ../comp
  cp                rungms_${SYS}    ../machines/unix/rungms
  cp               compall_${SYS}    ../compall
  cp               compddi_${SYS}    ../ddi/compddi
  cp     Makefile.template_${SYS}    ../Makefile.template
  cp install.info.template_${SYS}    ../install.info.template

  cd ..

  sed -i s'@^\s*GMS_PATH\s*=\s*$@GMS_PATH = ${GMS_BUILD}@' Makefile.template
  sed -i s'@^\s*GMS_BUILD_PATH\s*=\s*$@GMS_BUILD_PATH = ${GMS_BUILD}@' Makefile.template
  cp Makefile.template Makefile

  #                       #Prepare activation executable
  sed -e "s/^\*UNX/    /" tools/actvte.code > actvte.f

%endif # BUILD_PACKAGE |


%if %{?BUILD_PACKAGE}
%build
             # I really don't want to see the details of modules loading compiler and mpi!
   set +x
   %include system-load.inc
   %include compiler-load.inc
   %include mpi-load.inc
   set -x

   ifort -o tools/actvte.x actvte.f
   make -j 4

%endif # BUILD_PACKAGE |


%install

%if %{?BUILD_PACKAGE}
  rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR} # Delete the package installation directory.
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  echo "TACC_OPT %{TACC_OPT}"
                              # This puts everything in INSTALL_DIR 
                              #into the RPM_BUILD_ROOT/INSTALL_DIR dir

                              # we are in %%{_topdir}/BUILD = /admin/build/rpms
                              # we are in %%{_builddir}/%%{pkg_basename}-%%{version}   where things are made

                
  cp -r bin $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r doc $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
%endif # BUILD_PACKAGE |


%if %{?BUILD_MODULEFILE}

  rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR} #Delete the module installation directory.
  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
                              # Write out the modulefile

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message=[[
The %{MODULE_VAR} modulefile defines the following environment variables:
TACC_%{MODULE_VAR}_DIR/DOC/BIN/DATA for the location of the Gamess home,
documentation, binaries and aux data directories, respectively.
The modulefile defines GMSPATH (Gamess dir) used in rungms.

To run GAMESS, include the following lines in your job script.

       module load gamess
       rungms my_molecule or
       rungms my_molecule NCPUS

where my_molecule is the input file name. The input file must have an .inp suffix.
But it is not necessary to include the suffix in the name used on the rungms command.
The rungms command will run the appropriate knl or sky version of the GAMESS executable.

e.g. for an h2.inp input file you can run gamess with

      rungms h2.inp  or rungms h2

(rungms uses a special mpirun command, mpiexec.hydra, to launch gamess, so you do not
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
local intel_lib_dir = os.getenv("TACC_INTEL_LIB")
--
-- TACC Variables

whatis("Name: %{pkg_base_name}")
whatis("Version: %{pkg_version}%{dbg}")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local gms_dir           = "%{INSTALL_DIR}"

family("APP")

setenv("TACC_%{MODULE_VAR}_DIR",  gms_dir)
setenv("TACC_%{MODULE_VAR}_BIN",  pathJoin(gms_dir,"bin" ) )
setenv("TACC_%{MODULE_VAR}_DOC",  pathJoin(gms_dir,"doc" ) )
setenv("TACC_%{MODULE_VAR}_DATA", pathJoin(gms_dir,"auxdata") )

--
-- GMS Variables and PATH append
--

setenv( "VERNO",           "00"                   )
setenv("GMSPATH",          gms_dir                )
prepend_path("PATH",       pathJoin(gms_dir,"bin"))
prepend_path("LD_LIBRARY_PATH",     intel_lib_dir)
--prepend_path("LD_LIBRARY_PATH", "/opt/intel/compilers_and_libraries_2017.4.196/linux/compiler/lib/intel64_lin/")

EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{pkg_basename}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

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

%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc

############ Do Not Remove #############

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT
