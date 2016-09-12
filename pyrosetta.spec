#
# R. Todd Evans
# 2016-08-12
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

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name pyrosetta
%define MODULE_VAR    PYROSETTA

%define maintainer_email rtevans@tacc.utexas.edu
%define rpm_group G-814534

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 6
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
#%include name-defines-noreloc.inc
#%include name-defines-hidden.inc
#%include name-defines-hidden-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   http://depts.washington.edu/ventures/UW_Technology/Express_Licenses/rosetta.php
Group:     Development/Tools
URL:       https://www.rosettacommons.org
Packager:  TACC - %{maintainer_email}
Source:    rosetta_src_%{pkg_version}_bundle.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

%description
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

###%setup -n %{pkg_base_name}-%{pkg_version}

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
module purge

# Insert further module commands

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

#if ! mountpoint -q %{INSTALL_DIR} ; then
#   mkdir -p %{INSTALL_DIR}
#   mount -t tmpfs tmpfs %{INSTALL_DIR}
#fi	      
  
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

cd %{INSTALL_DIR}
 
export rosetta=`pwd`
export rosetta_major=%{major_version}
export rosetta_minor=%{minor_version}
export rosetta_version=${rosetta_major}.${rosetta_minor}

cd ${rosetta}
# Untar
if [ ! -d "${rosetta}/rosetta_src_${rosetta_version}_bundle" ]; then
   mkdir -p ${rosetta}/rosetta_src_${rosetta_version}_bundle
   tar xvf %{_sourcedir}/rosetta_src_${rosetta_version}_bundle.tgz -C ${rosetta}/rosetta_src_${rosetta_version}_bundle --strip-components=1
fi

if [ ! -e "${rosetta}/PyRosetta.Develop.64/BuildPyRosetta.sh" ]; then
   ${rosetta}/rosetta_src_${rosetta_version}_bundle/tools/PyRosetta.develop/DeployPyRosetta.py -j6
   cp ${rosetta}/PyRosetta.Develop.64/BuildPyRosetta.sh ${rosetta}/rosetta_src_${rosetta_version}_bundle/main/source
fi

cd ${rosetta}/rosetta_src_${rosetta_version}_bundle/main/source
sed -i 's/python2.7/python2.6/' external/scons-local/scons.py
sed -i 's/python2.7/python2.6/' update_options.sh
sed -i 's/python2.7/python2.6/' update_ResidueType_enum_files.sh
./BuildPyRosetta.sh --monolith -j6

cd %{INSTALL_DIR}/rosetta_src_${rosetta_version}_bundle/main/source/build/PyRosetta/linux/monolith/release
rm -f database
ln -s %{INSTALL_DIR}/rosetta_src_${rosetta_version}_bundle/main/database database

echo "Almost completed"
cd $RPM_BUILD_ROOT 

cp -rp %{INSTALL_DIR}/PyRosetta.Develop.64/bin $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -rp %{INSTALL_DIR}/PyRosetta.Develop.64/lib $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -rp %{INSTALL_DIR}/rosetta_src_${rosetta_version}_bundle/main/source/build $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -rp %{INSTALL_DIR}/rosetta_src_${rosetta_version}_bundle/main/database $RPM_BUILD_ROOT/%{INSTALL_DIR}

#umount %{INSTALL_DIR}
  
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

%define kern_ver() %(uname -r | cut -d . -f -2)

  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_msg=[[
The Rosetta software suite includes algorithms for computational modeling and
analysis of protein structures. It has enabled notable scientific advances in
computational biology, including de novo protein design, enzyme design, ligand
docking, and structure prediction of biological macromolecules and
macromolecular complexes.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN, and TACC_%{MODULE_VAR}_DATABASE
for the location of the %{MODULE_VAR} distribution, binaries, and database
respectively.

NOTE: %{MODULE_VAR} is hard-coded to attempt to write temporary files within
the designated database location. This action will fail if the user sets
-database=$TACC_%{MODULE_VAR}_DATABASE. Instead, copy the database from
TACC_%{MODULE_VAR}_DATABASE to a writable location via something like:

cp -r $TACC_%{MODULE_VAR}_DATABASE $WORK/rosetta_database

Then, to run:

$TACC_%{MODULE_VAR}_BIN/<rosetta-executable>.mpiomp.linuxiccrelease [options] -database=$WORK/rosetta_database

Version %{pkg_version}
]]

local err_message = [[
You do not have access to %{pkg_base_name} %{pkg_version}.


Users have to show their licenses and be confirmed by the %{pkg_base_name} team
that they are registered users under that license.  Send a copy of the license
to https://portal.tacc.utexas.edu/tacc-consulting.
]]

local group  = "%{rpm_group}"
local grps   = capture("groups")
local found  = false
local isRoot = tonumber(capture("id -u")) == 0
for g in grps:split("[ \n]") do
   if (g == group or isRoot)  then
      found = true
      break
    end
end


--help(help_msg)
help(help_msg)

whatis("Name: %{pkg_base_name}")
whatis("Version: %{pkg_version}")
whatis("Category: Scientific Application")
whatis("Keywords: Molecular Dynamics, Folding, Biology")
whatis("URL: http://www.rosettacommons.org/")
whatis("Description: The premier software suite for macromolecular modeling")

if (found) then
  -- Create environment variables.
  local base_dir           = "%{INSTALL_DIR}"
  local pyrosetta_lib      = "build/PyRosetta/linux/monolith/release"

  prepend_path( "PATH",                   pathJoin(base_dir, "bin"))
  prepend_path( "LD_LIBRARY_PATH",        pathJoin(base_dir, "lib"))
  prepend_path( "LD_LIBRARY_PATH",        pathJoin(base_dir, pyrosetta_lib))
  prepend_path( "PYTHONPATH",        pathJoin(base_dir, pyrosetta_lib))
  setenv( "TACC_%{MODULE_VAR}_DIR",                base_dir)
  setenv( "TACC_%{MODULE_VAR}_DATABASE",  pathJoin(base_dir, "database"))
  setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(base_dir, "bin"))
else
  LmodError(err_message,"\n")
end
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

  %defattr(750,root,%{rpm_group},)
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

