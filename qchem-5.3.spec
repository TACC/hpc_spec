#
# Spec file for DDT
#
# Give the package a base name
%define pkg_base_name qchem
%define MODULE_VAR    qchem

# Create some macros (spec file variables)
%define major_version 5
%define minor_version 3
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
#%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc

############ Do Not Change #############
# Name: qchem
# Version: 5.3
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}_%{pkg_version}-buildroot
Summary: Q-Chem is a comprehensive ab initio quantum chemistry software for accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.
########################################

Release: 1%{?dist}
License: Commercial
Vendor: QChem
URL: https://www.q-chem.com/
Packager: TACC - huang@tacc.utexas.edu
Source:    %{pkg_base_name}_%{pkg_version}.tar


# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: Q-Chem is a comprehensive ab initio quantum chemistry software for accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.
Group: application/quantumn chemistry
%description package
Q-Chem is a comprehensive ab initio quantum chemistry software for accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Q-Chem is a comprehensive ab initio quantum chemistry software for accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.

%description 
Q-Chem is a comprehensive ab initio quantum chemistry software for accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.

%define HOME1 /home1/apps
%define OPT /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{HOME1}/%{pkg_base_name}/%{version}
%define MODULE_DIR  %{OPT}/%{MODULES}/%{pkg_base_name}

# BuildRoot: /tmp/%{name}-%{version}-buildroot

%prep

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}_%{pkg_version}
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


%build
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

# cp $RPM_SOURCE_DIR/%{licenses} ./License
   cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}


  chmod -R a+rX $RPM_BUILD_ROOT/%INSTALL_DIR

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  # rm -rf  $RPM_BUILD_ROOT/%MODULE_DIR
  mkdir -p $RPM_BUILD_ROOT/%MODULE_DIR
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message=[[
Q-Chem is a comprehensive ab initio quantum chemistry software for accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.

module load qchem
# qchem in ONLY available on SKX nodes. You can access it in queues skx-normal and skx-dev.

# Running a job on a single node with a single thread
qchem input output

# Running a job on a single node with 16 threads
qchem -nt 16 input output

Please note that qchem may not scale well by increasing thread number if your system/basis set is not large enough. You NEED to try various number of thread number to find out the optimal setting before your production runs. When your system size or basis set has been changed, the optimal setting needs to be tuned again.

QChem support running on multiple nodes for some functions.
https://www.q-chem.com/qchem-website/manual/qchem50_manual/sec-parallel.html

To run qchem on multiple nodes,

#SBATCH -J test # Job Name
#SBATCH -o test.o%j
#SBATCH -N 2    # Total number of nodes
#SBATCH -n 4    # Total number of mpi tasks
#SBATCH -p skx-normal # Queue (partition) name -- skx-normal, skx-dev, etc.
#SBATCH -t 24:00:00 # Run time (hh:mm:ss) - 24 hours

module load qchem
qchem -mpi -np 4 -nt 8 input output

# Please feel free to tune the number of tasks and the number of threads to find an optimal setting.

]]

help(help_message,"\n")

whatis("Name: QChem")
whatis("Version: 5.3")
whatis("Category: Apps/Quantum Chemistry")
whatis("Keywords: Quantum Chemistry")
whatis("Description: Q-Chem is a comprehensive ab initio quantum chemistry software for accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.")

-- Create environment variables.
local qchem_dir           = "/home1/apps/qchem/5.3"

family("qchem")

prepend_path(    "PATH",                pathJoin(qchem_dir, "bin"))
prepend_path(    "PATH",                pathJoin(qchem_dir, "exe"))

setenv("QC", "/home1/apps/qchem/5.3")
setenv("QCPLATFORM", "LINUX_Ix86_64")
setenv("QCRSH","ssh")
setenv("QCMPI","mpich3")
setenv("QCAUX","/home1/apps/qchem/5.3/qcaux")
setenv("QCPROG_S","/home1/apps/qchem/5.3/exe/qcprog.exe_s")
setenv("QCPROG","/home1/apps/qchem/5.3/exe/qcprog.exe")
setenv("QCLOCALSCR","/tmp")
setenv("QCSCRATCH","n")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
 
set     ModulesVersion      "%{version}"
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
# %files
%files package
#------------------------

  %defattr(-,root,root)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#---------------------------

  %defattr(-,root,root)
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


%clean
rm -rf $RPM_BUILD_ROOT

