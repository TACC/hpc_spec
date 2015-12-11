#
# siesta-3.2.spec, v3.2, 2013-04-05 11:59:00 carlos@tacc.utexas.edu
#
# See http://www.icmab.es/siesta/

Summary:    Spanish Initiative for Electronic Simulations with Thousands of Atoms
Name:       tacc-siesta
Version:    3.2
Release:    1
License:    Limited academic use (http://www.icmab.es/siesta/Licenses)
Vendor:     Fundacion General de la Universidad Autonoma de Madrid
Group:      Applications/Chemistry
Source:     siesta-%{version}.tar.gz
Packager:   TACC - carlos@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

# TACC BUILD NOTES
# custom arch.make added to /Src/Sys directory before repackaging
# NOT NEEDED in 3.2 - fixed Makefile added to /Util/STM/ol-stm before repackaging


#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug_package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
%include compiler-defines.inc
# MPI Family Definitions
%include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: Spanish Initiative for Electronic Simulations with Thousands of Atoms
Group:   Applications/Chemistry

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Siesta (Spanish Initiative for Electronic Simulations with Thousands of Atoms) 
is both a method and its computer program implementation, to perform electronic 
structure calculations and ab initio molecular dynamics simulations of 
molecules and solids.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/siesta/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep -n siesta-%{version}.tar.gz

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/<name>-<version>
%setup -n siesta-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
# Use mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mount -t tmpfs tmpfs %{INSTALL_DIR}

# Start with a clean environment
#if [ -f "$BASH_ENV" ]; then
#  . $BASH_ENV
#  module purge
#  clearMT
#  export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
#fi

module purge
module load TACC
# Load correct compiler
unset MODULEPATH
%include compiler-load.inc
# Load correct mpi stack
%include mpi-load.inc

#-----------------------------
# Build parallel version
#-----------------------------

# Prepare the build directory 
cd ./Obj
sh ../Src/obj_setup.sh
cp ../Src/Sys/ls5_intel_mkl.make ./arch.make

# Build siesta
make
mkdir %{INSTALL_DIR}/bin
cp siesta %{INSTALL_DIR}/bin

# Build transiesta
make clean
make transiesta 
cp transiesta %{INSTALL_DIR}/bin

# Build atm
cd ../Pseudo/atom
make
cp atm %{INSTALL_DIR}/bin

# Build Utilities
cd ../../Util
sh ./build_all.sh
cp ./COOP/dm_creator %{INSTALL_DIR}/bin
cp ./COOP/mprop %{INSTALL_DIR}/bin
cp ./TBTrans/tbtrans %{INSTALL_DIR}/bin
cp ./Denchar/Src/denchar %{INSTALL_DIR}/bin
cp ./STM/ol-stm/Src/stm %{INSTALL_DIR}/bin
cp ./STM/simple-stm/plstm %{INSTALL_DIR}/bin
cp ./Gen-basis/gen-basis %{INSTALL_DIR}/bin
cp ./Gen-basis/ioncat %{INSTALL_DIR}/bin
cp ./Gen-basis/ionplot.sh %{INSTALL_DIR}/bin

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

 mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
 cp -r ./Examples %{INSTALL_DIR}
 cp -r ./Tutorials %{INSTALL_DIR}
 cp -r ./Docs %{INSTALL_DIR}

#  Kluge, the make install, installs in /tmp/carlos
cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount                                   %{INSTALL_DIR}


# ADD ALL MODULE STUFF HERE
# TACC module

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message = [[
This module loads Siesta built with Intel 16 and Cray MPT 7.2.4.
This module makes available the following executables:

siesta
transiesta

as well as the following utilities:

tbtrans
denchar
dm_creator
mprop
stm
plstm
gen-basis
ioncat

In order to run siesta please create a link to the binary inside the execution
directory, and make sure your submission script contains the lines:

module load siesta
ibrun ./siesta < input.fdf
 
Version 3.2
]]


local err_message = [[
You do not have access to this software!

Licenses for academic use are free. As long as you agree to the
terms and conditions of the academic license for Siesta, which 
can be found at http://www.icmab.es/siesta, you can use the
software freely in TACC systems.

Please send an email to carlos@tacc.utexas.edu with a request
to be added to the SIESTA user group including your name, 
an academic email address, and a statement saying that you agree 
to follow the academic licensing conditions for Siesta.
]]

local group = "G-802412"
local grps  = capture("groups")
local found = false
local isRoot = tonumber(capture("id -u")) == 0
for g in grps:split("[ \n]") do
   if (g == group or isRoot)  then
      found = true
      break
   end
end

whatis("Siesta")
whatis("Version: 3.2")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Molecular Dynamics, Application")
whatis("Description: Spanish Initiative for Electronic Simulations with Thousands of Atoms")
whatis("URL: http://www.icmab.es/siesta/")

help(help_message,"\n")

if (found) then
   setenv("TACC_SIESTA_DIR","/opt/apps/intel13/mvapich2_1_9/siesta/3.2")
   setenv("TACC_SIESTA_BIN","/opt/apps/intel13/mvapich2_1_9/siesta/3.2/bin")
   prepend_path("PATH","/opt/apps/intel13/mvapich2_1_9/siesta/3.2/bin")
else
   LmodError(err_message,"\n")
end

EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}

# Define files permisions, user and group
%defattr(-,root,install)
%{INSTALL_DIR}/Tutorials
%{INSTALL_DIR}/Docs
%{INSTALL_DIR}/Examples
%{MODULE_DIR}

# These files must be group-protected for licensing reasons
%attr(750,root,G-802412) %{INSTALL_DIR}/bin
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/siesta
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/transiesta
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/tbtrans
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/denchar
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/dm_creator
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/mprop
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/stm
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/plstm
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/gen-basis
%attr(750,root,G-802412) %{INSTALL_DIR}/bin/ioncat

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the source files from /tmp/BUILD
rm -rf /tmp/BUILD/%{name}-%{version}

# Remove the installation files now that the RPM has been generated
rm -rf /var/tmp/%{name}-%{version}-buildroot

rm -rf $RPM_BUILD_ROOT
