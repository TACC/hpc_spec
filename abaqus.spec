#
# Stephen Lien Harrell
# 2020-05-15
#
# Change version here
%define major_version 2019

# Give the package a base name
%define pkg_base_name abaqus
%define MODULE_VAR    ABAQUS


%define pkg_version %{major_version}

Summary: Abaqus spec file
Release: 2%{?dist}
License: Abaqus License
Vendor: Simulia
Group: Utility
Source: %{name}-%{version}.tar.gz
Packager:  TACC - sharrell@tacc.utexas.edu

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}



%package %{PACKAGE}
Summary: Abaqus package RPM
Group: Applications
%description package
Abaqus is a software suite for finite element analysis and computer-aided engineering.

%package %{MODULEFILE}
Summary: Abaqus modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
Abaqus is a software suite for finite element analysis and computer-aided engineering.

%description
Abaqus is a software suite for finite element analysis and computer-aided engineering.

%define HOME1 /home1/apps
%define OPT /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{HOME1}/%{pkg_base_name}/%{version}
%define MODULE_DIR  %{OPT}/%{MODULES}/%{pkg_base_name}

%define ABAQUS_GROUP G-813612

%define BUILD_ROOT ${RPM_BUILD_ROOT}
# Make sure only certain users can access this

#---------------------------------------
%prep
#---------------------------------------
export BASH_ENV=/etc/tacc/tacc_functions
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


mkdir -p  $RPM_BUILD_ROOT/%{INSTALL_DIR}

# This is an 
#
#rm -rf /tmp/DSY*
#cd /tmp
#for f in /tmp/2020.AM_SIM_Abaqus_Extend.AllOS*.tar; do tar xfv "$f"; done
#
#rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}/*
#export RPM_BUILD_ROOT=$RPM_BUILD_ROOT
#RPM_BUILD_ROOT=$RPM_BUILD_ROOT echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
#<UserIntentions mediaName=\"CODE\linux_a64\SIMULIA_EstPrd.media\" mediaVersion=\"422\">
#  <SetVariable item=\"flex\" name=\"serverType_radioButton\" value=\"true\"/>
#  <SetVariable name=\"flexServer1\" value=\"27000@license02.tacc.utexas.edu\"/>
#  <SetVariable name=\"flexServer2\" value=\"\"/>
#  <SetVariable name=\"flexServer3\" value=\"\"/>
#  <SetVariable name=\"commandsDir\" value=\"${RPM_BUILD_ROOT}/%{INSTALL_DIR}/commands\"/>
#  <SetVariable name=\"pluginsDir\" value=\"${RPM_BUILD_ROOT}/%{INSTALL_DIR}/plugins\"/>
#  <SetVariable item=\"solverAbaqus\" name=\"checkSolverInterfaces\" value=\"true\"/>
#  <SetVariable item=\"solverMscNastran\" name=\"checkSolverInterfaces\" value=\"false\"/>
#  <SetVariable item=\"solverAnsys\" name=\"checkSolverInterfaces\" value=\"false\"/>
#  <SetVariable item=\"solverFemfat\" name=\"checkSolverInterfaces\" value=\"false\"/>
#  <SetVariable item=\"interfaceAnsa\" name=\"checkSolverInterfaces\" value=\"false\"/>
#  <SetVariable name=\"workingDir\" value=\"/tmp\"/>
#  <SetVariable name=\"solverCcmpDir\" value=\"\"/>
#  <SetVariable name=\"solverCcmpPodkey\" value=\"\"/>
#  <SetVariable name=\"solverFluentDir\" value=\"\"/>
#  <SetVariable name=\"DSYWelcomePanel\"/>
#  <SetVariable name=\"TARGET_PATH\" value=\"${RPM_BUILD_ROOT}/%{INSTALL_DIR}\"/>
#  <!--Abaqus/Standard Solver-->
#  <SetVariable item=\"CODE\linux_a64\SIMAQSL_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus/Explicit Solver-->
#  <SetVariable item=\"CODE\linux_a64\SIMAQXL_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Cosimulation Services-->
#  <SetVariable item=\"CODE\linux_a64\SIMCSS_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus ODB API Services-->
#  <SetVariable item=\"CODE\linux_a64\SIMODB_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus CAE-->
#  <SetVariable item=\"CODE\linux_a64\SIMCAE_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus Samples-->
#  <SetVariable item=\"CODE\linux_a64\SIMSAMP_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Tosca Structure-->
#  <SetVariable item=\"CODE\linux_a64\SIMTOSE_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Tosca Fluid-->
#  <SetVariable item=\"CODE\linux_a64\SIMTOFE_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe-->
#  <SetVariable item=\"CODE\linux_a64\SIMFESD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2019 ODBs-->
#  <SetVariable item=\"CODE\linux_a64\SIMFS19_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2018 ODBs-->
#  <SetVariable item=\"CODE\linux_a64\SIMFS18_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2017 ODBs-->
#  <SetVariable item=\"CODE\linux_a64\SIMFS17_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2016 ODBs-->
#  <SetVariable item=\"CODE\linux_a64\SIMFS16_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe materials and surface finish specifications-->
#  <SetVariable item=\"CODE\linux_a64\SIMFSMD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Material database server for fe-safe-->
#  <SetVariable item=\"CODE\linux_a64\SIMFSMS_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial and sample data-->
#  <SetVariable item=\"CODE\linux_a64\SIMFSTD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for Abaqus-->
#  <SetVariable item=\"CODE\linux_a64\SIMFSAD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for I-DEAS-->
#  <SetVariable item=\"CODE\linux_a64\SIMFSID_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for Ansys-->
#  <SetVariable item=\"CODE\linux_a64\SIMFSRD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for NASTRAN-->
#  <SetVariable item=\"CODE\linux_a64\SIMFSND_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus/CFD Solver-->
#  <SetVariable item=\"CODE\linux_a64\SIMAQF_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <SetVariable name=\"FinishPanel\"/>
#</UserIntentions>
#" > config_options
#
#/tmp/AM_SIM_Abaqus_Extend.AllOS/4/SIMULIA_EstablishedProducts/Linux64/1/StartTUI.sh --silent ./config_options
#
#RPM_BUILD_ROOT=$RPM_BUILD_ROOT echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
#<UserIntentions mediaName=\"CAA\linux_a64\SIMULIA_EstPrd.media\" mediaVersion=\"422\">
#  <SetVariable name=\"DSYWelcomePanel\"/>
#  <SetVariable name=\"TARGET_PATH\" value=\"${RPM_BUILD_ROOT}/%{INSTALL_DIR}/\"/>
#  <!--Abaqus/Standard Solver-->
#  <SetVariable item=\"CAA\linux_a64\SIMAQSL_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus/Explicit Solver-->
#  <SetVariable item=\"CAA\linux_a64\SIMAQXL_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Cosimulation Services-->
#  <SetVariable item=\"CAA\linux_a64\SIMCSS_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus ODB API Services-->
#  <SetVariable item=\"CAA\linux_a64\SIMODB_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus CAE-->
#  <SetVariable item=\"CAA\linux_a64\SIMCAE_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus Samples-->
#  <SetVariable item=\"CAA\linux_a64\SIMSAMP_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Tosca Structure-->
#  <SetVariable item=\"CAA\linux_a64\SIMTOSE_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Tosca Fluid-->
#  <SetVariable item=\"CAA\linux_a64\SIMTOFE_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe-->
#  <SetVariable item=\"CAA\linux_a64\SIMFESD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2019 ODBs-->
#  <SetVariable item=\"CAA\linux_a64\SIMFS19_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2018 ODBs-->
#  <SetVariable item=\"CAA\linux_a64\SIMFS18_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2017 ODBs-->
#  <SetVariable item=\"CAA\linux_a64\SIMFS17_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe interface to Abaqus 2016 ODBs-->
#  <SetVariable item=\"CAA\linux_a64\SIMFS16_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe materials and surface finish specifications-->
#  <SetVariable item=\"CAA\linux_a64\SIMFSMD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Material database server for fe-safe-->
#  <SetVariable item=\"CAA\linux_a64\SIMFSMS_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial and sample data-->
#  <SetVariable item=\"CAA\linux_a64\SIMFSTD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for Abaqus-->
#  <SetVariable item=\"CAA\linux_a64\SIMFSAD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for I-DEAS-->
#  <SetVariable item=\"CAA\linux_a64\SIMFSID_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for Ansys-->
#  <SetVariable item=\"CAA\linux_a64\SIMFSRD_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--fe-safe tutorial models for NASTRAN-->
#  <SetVariable item=\"CAA\linux_a64\SIMFSND_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <!--Abaqus/CFD Solver-->
#  <SetVariable item=\"CAA\linux_a64\SIMAQF_TP.prd\" name=\"SelectProduct\" value=\"true\"/>
#  <SetVariable name=\"FinishPanel\"/>
#</UserIntentions>
#" > config_options2
#
#/tmp/AM_SIM_Abaqus_Extend.AllOS/4/SIMULIA_EstablishedProducts_CAA_API/Linux64/1/StartTUI.sh --silent ./config_options2
#

mv * $RPM_BUILD_ROOT/%{INSTALL_DIR}


mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/tacc_test

echo '#!/bin/bash
#SBATCH -J testAbaqusJob
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH -n 4
#SBATCH -o myMPI.o%j
#SBATCH -p normal

ml abaqus/2020
# ml abaqus/2019

# Set this to the correct environment file
# for the test we will use some reasonable defaults
cp $TACC_ABAQUS_DIR/tacc_test/abaqus_v6.env ./
abaqus_environment_file=abaqus_v6.env

# Figure out what nodes this job should run on
node_list=$(scontrol show hostname $cores_per_node | sort | uniq)

# This assumes that there will be an even number of tasks across
# each node, if you have configured your job to run with different
# numbers of tasks on each node, you will need to change the task
# calculations below and create a modified mp_host_list.
cores_per_node=$(echo $SLURM_TASKS_PER_NODE | grep -oP '\''^[^0-9]*\K[0-9]+'\'')

# Make node list and count the number of nodes
core_count=0
mp_host_list="["

for i in  ${node_list} ; do
    mp_host_list="${mp_host_list}['$i', ${cores_per_node}],"
    number_of_nodes=$((number_of_nodes + 1))
done

echo $mp_host_list

# Calculate the amount of coress per node and multiply it by the amount
# of nodes we are running on
core_count=$(($number_of_nodes*$cores_per_node))
echo "Running on nodes: $cores_per_node"
echo "Running on $cores_per_node cores per node for a total of $core_count processes"

mp_host_list=`echo ${mp_host_list} | sed -e "s/,$//"`
mp_host_list="${mp_host_list}]"

echo "mp_host_list=${mp_host_list}"  >> $abaqus_environment_file

unset SLURM_GTIDS

# Copy test input files to scratch directory
cp $TACC_ABAQUS_DIR/tacc_test/knee_bolster* ./


$TACC_ABAQUS_BIN/abaqus job=test_abaqus_job cpus=$core_count \
    input=./knee_bolster.inp -verbose 3 mp_mode=mpi \
    standard_parallel=all interactive scratch="."

sed -i "/mp_host_list/d" $abaqus_environment_file' > $RPM_BUILD_ROOT/%{INSTALL_DIR}/tacc_test/abaqus.slm

echo 'ask_delete=OFF

# Set this for your output files, you can also specify this in your
# job script
#scratch="path-to-the location where the files should be written"

mp_mode=MPI
run_mode=INTERACTIVE
memory="50 gb"
abaquslm_license_file="27000@license02.tacc.utexas.edu"

#  ABAQUS jobs will keep checking for licensing tokens till the
# time the required number of tokens become available or the jobs
# time-out of the queue. In order to save SUs in the event the
# tokens are not available for usage, the users should have this
# line here. "5" in the line "lmhanglimit=5" means that ABAQUS
# will only wait for a license token for 5 minutes.
lmhanglimit=5' >  $RPM_BUILD_ROOT/%{INSTALL_DIR}/tacc_test/abaqus_v6.env


# Download and add test so the documentation works out of the box
wget "https://abaqus-docs.mit.edu/2017/English/SIMAINPRefResources/knee_bolster.inp" --directory-prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}/tacc_test
wget "https://abaqus-docs.mit.edu/2017/English/SIMAINPRefResources/knee_bolster_ef1.inp" --directory-prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}/tacc_test
wget "https://abaqus-docs.mit.edu/2017/English/SIMAINPRefResources/knee_bolster_ef2.inp" --directory-prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}/tacc_test
wget "https://abaqus-docs.mit.edu/2017/English/SIMAINPRefResources/knee_bolster_ef3.inp" --directory-prefix=$RPM_BUILD_ROOT/%{INSTALL_DIR}/tacc_test

rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/commands/*
ln -s %{INSTALL_DIR}/linux_a64/code/bin/ABQLauncher  $RPM_BUILD_ROOT/%{INSTALL_DIR}/commands/abq%{major_version}
ln -s %{INSTALL_DIR}/commands/abq%{major_version} $RPM_BUILD_ROOT/%{INSTALL_DIR}/commands/abaqus
chgrp -R G-813612 $RPM_BUILD_ROOT/%{INSTALL_DIR}
chmod -R g+rX $RPM_BUILD_ROOT/%{INSTALL_DIR}
chmod -R o-wrx $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm -rf /tmp/AM_SIM_Abaqus_Extend.AllOS
rm -rf /tmp/DSY*

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------




# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge


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
  
  
# Write out the modulefile associated with the application

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message=[[
The TACC ABAQUS module appends the path to the abaqus executables
to the PATH environment variable.  Also TACC_ABAQUS_DIR, and
TACC_ABAQUS_BIN are set to ABAQUS home and command directories.

In order to use ABAQUS on TACC resources, UT Austin users will
need to submit a ticket requesting to be added to the "ABAQUS"
group at https://portal.tacc.utexas.edu/tacc-consulting

Information on running ABAQUS and using other license servers 
can be found at:
https://portal.tacc.utexas.edu/software/abaqus

This is the ABAQUS %{major_version} release.

Version %{version}
]]


whatis("Version: %{pkg_version}")
whatis("Category: application, engineering")
whatis("Keywords: finite element analysis, computer-aided engineering")
whatis("URL: https://www.3ds.com/")
whatis("Description: Abaqus is a software suite for finite element analysis and computer-aided engineering.")
help(help_message,"\n")


local group = "%{ABAQUS_GROUP}"
found = userInGroup(group)


local err_message = [[
You do not have access to ABAQUS!

In order to use ABAQUS on TACC resources, UT Austin users will need to submit a ticket requesting to be added to the "ABAQUS" group.

Information on running ABAQUS can be found at:
https://portal.tacc.utexas.edu/software/abaqus
]]


if (found) then
local abaqus_dir="%{INSTALL_DIR}"

prepend_path(    "PATH",                pathJoin(abaqus_dir, "commands"))
setenv( "TACC_%{MODULE_VAR}_DIR",       abaqus_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(abaqus_dir, "commands"))

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

  

# Check the syntax of the generated lua modulefile
%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-, root, %{ABAQUS_GROUP},)
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

