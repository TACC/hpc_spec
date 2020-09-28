# Quantum Espresso 6.5.SPEC
# 05/2017
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

Summary: Quantum Espresso

# Give the package a base name
%define pkg_base_name qe
%define MODULE_VAR    QE

# Create some macros (spec file variables)
%define major_version 6
%define minor_version 5
#%define micro_version 1  

#%define pkg_version %{major_version}.%{minor_version}.%{micro_version}
%define pkg_version %{major_version}.%{minor_version}

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
URL:       http://www.quantum-espresso.org
Packager:  TACC - hliu@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}-TACC-fat.tar.gz
#Source0:   %{pkg_base_name}-%{pkg_version}.tar.bz2
#Source1:   libint-1.1.5.tar.gz
#Source2:   libxc-2.0.1.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Quantum Espresso is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale.
Group: Applications/Chemistry
%description package
Quantum Espresso is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. 
It is based on density-functional theory, plane waves, and pseudopotentials.
%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Quantum Espresso is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. 
It is based on density-functional theory, plane waves, and pseudopotentials.
%description
Quantum Espresso is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. 
It is based on density-functional theory, plane waves, and pseudopotentials.
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

%setup -n %{pkg_base_name}-%{pkg_version}-TACC-fat

#---------------------------------------
%build
#---------------------------------------
%include compiler-load.inc
%include mpi-load.inc

export VERSION=6.5


wget --no-check-certificate http://elpa.mpcdf.mpg.de/html/Releases/2019.11.001/elpa-2019.11.001.tar.gz
tar xvf elpa-2019.11.001.tar.gz
cd elpa-2019.11.001

wget --no-check-certificate https://github.com/hfp/xconfigure/raw/master/configure-get.sh
chmod +x configure-get.sh
./configure-get.sh elpa

sed -i 's/mpiifort/mpif90/g' configure-elpa-hsw-omp.sh
sed -i 's/mpiicc/mpicc/g' configure-elpa-hsw-omp.sh
sed -i 's/mpiicpc/mpicxx/g' configure-elpa-hsw-omp.sh


./configure-elpa-hsw-omp.sh
make -j ; make install

cd ..

wget https://gitlab.com/QEF/q-e/-/archive/qe-6.5/q-e-qe-6.5.tar.gz
tar xvf q-e-qe-6.5.tar.gz
cd q-e-qe-6.5
wget --no-check-certificate https://github.com/hfp/xconfigure/raw/master/configure-get.sh
chmod +x configure-get.sh
./configure-get.sh qe
sed -i 's/mpiifort/mpif90/g' configure-qe-hsw-omp.sh
sed -i 's/mpiicc/mpicc/g' configure-qe-hsw-omp.sh
sed -i 's/mpiicpc/mpicxx/g' configure-qe-hsw-omp.sh

./configure-qe-hsw-omp.sh
make all



# Remove non active symbolic links in packages
#rm S3DE/iotk/iotk
#rm -rf Doc


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
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
#  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib

cp -r ./q-e-qe-6.5/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/
chmod -Rf u+rwX,g+rwX,o=rX  $RPM_BUILD_ROOT/%{INSTALL_DIR}

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


To run codes in quantum espresso, e.g. pw.x, include the following lines in
your job script, using the appropriate input file name:
module load qe/6.5
ibrun pw.x -input input.scf

IMPORTANT NOTES:

1. Run your jobs on $SCRATCH rather than $WORK. The $SCRATCH file system is better able to handle these kinds of loads.

2. Especially when running pw.x, set the keyword disk_io to low or none in input so that wavefunction
will not be written to file at each scf iteration step, but stored in memory.

3. When running ph.x, set the  reduced_io to .true. and run it and redirect its IO to $SCRATCH.
Do not run multiple ph.x jobs at given time.

Version %{version}
]]

--help(help_msg)
help(help_msg)

whatis("Name: Quantum Espresso")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif
whatis "Category: application, chemistry"
whatis "Keywords: Chemistry, Density Functional Theory, PLance Wave, Peudo potentials"
whatis "URL: http://www.quantum-espresso.org"
whatis "Description: Integrated suite of computer codes for electronic structure calculations and material modeling at the nanoscale."

-- Create environment variables.
local qe_dir="%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(qe_dir, "bin"))

setenv( "TACC_%{MODULE_VAR}_DIR",                qe_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(qe_dir, "bin"))
setenv("TACC_%{MODULE_VAR}_PSEUDO",pathJoin(qe_dir,"pseudo"))

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

