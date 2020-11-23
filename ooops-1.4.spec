#
# W. Cyrus Proctor
# Antonio Gomez
# 2015-08-25
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

Summary: A Nice little relocatable skeleton spec file.

# Give the package a base name
%define pkg_base_name ooops
%define MODULE_VAR    OOOPS

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 4
%define micro_version 0

#%define pkg_version %{major_version}.%{minor_version}
%define pkg_version %{major_version}.%{minor_version}
### Toggle On/Off ###
%include rpm-dir.inc

#%include compiler-defines.inc
#%include mpi-defines.inc

#%include name-defines-noreloc.inc

########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc

########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   1%{?dist}
License:   GPL
URL:       https://github.com/TACC/ooops
Packager:  TACC - huang@tacc.utexas.edu
Source:    ooops-1.4.tgz
#Source1:   tcl8.5.9-linux-x86_64-threaded.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The OOOPS RPM
Group: Tools/Optimization
%description package
OOOPS, an innovative IO workload managing system that optimally throttles the IO 
workload from the users' side. 

%package %{MODULEFILE}
Summary: The OOOPS modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
OOOPS, an innovative IO workload managing system that optimally throttles the IO
workload from the users' side.

%description
OOOPS, an innovative IO workload managing system that optimally throttles the IO
workload from the users' side.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
#  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
#  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

%setup -n ooops-%{pkg_version}


#---------------------------------------
%build
#---------------------------------------

#---------------------------------------
%install
#---------------------------------------

# Setup modules
%include system-load.inc
module purge
#%include compiler-load.inc
#%include mpi-load.inc


# Insert necessary module commands
#module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

  cp -p bin/* $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
  cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}/
  cp -r conf $RPM_BUILD_ROOT/%{INSTALL_DIR}/
  cp -r test $RPM_BUILD_ROOT/%{INSTALL_DIR}/

  chmod -Rf u+rwX,g+rwX,o=rX                                  $RPM_BUILD_ROOT/%{INSTALL_DIR}


  # Copy everything from tarball over to the installation directory
#  cp * $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

#  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

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
Optimal Overloaded IO Protection System (OOOPS) is an easy to use tool that helps HPC users optimize heavy IO requests.

It will also help system administrator prevent IO overload caused by improper IO request.

Lei Huang (huang@tacc.utexas.edu)
Si Liu    (siliu@tacc.utexas.edu)

You can use command "set_io_param_batch" to adjust allowed maximum frequency of open/stat on all nodes of one running job.

Two ways to run set_io_param_batch:

Simple setting,
  set_io_param_batch jobid idx_fs [ low / medium / high / unlimit ]

  jobid     - The slurm job id
  idx_fs    - The index of file server. On Frontera, 0 represents /scratch1. 1 represents /work. 2 represents /home1. 3 represents /work2.

  Example, set_io_param_batch 12345 1 medium

More advanced setting,
  set_io_param_batch jobid idx_fs t_open freq_open t_stat freq_stat
  jobid     - The slurm job id
  idx_fs    - The index of file server. On Frontera, 0 represents /scratch1. 1 represents /work. 2 represents /home1. 3 represents /work2.
  t_open    - The estimated time to finish open(). Unit is microsecond.
  freq_open - The allowed max frequency of open() (times per second)
  t_stat    - The estimated time to finish stat(). Unit is microsecond.
  freq_stat - The allowed max frequency of stat() (times per second)

  Example to turn off the throttling on WORK.
  set_io_param_batch 12345 1 1000000 1000000 1000000 1000000

  Example to slow down open/stat on WORK a lot.
  set_io_param_batch 12345 1 1000 200 1000 500
  In this example, the number of open and stat can NOT be more frequent than 200 times and 500 times per second respectively.

If OOOPS finds intensive IO in your job, it will print out warning messages and create open/stat call report.
]]

--help(help_msg)
help(help_msg)

whatis("Name: OOOPS")
whatis("Version: 1.4")
whatis("Category: Tools/Optimization ")
whatis("Keywords: Tools, IO, Optimization")
whatis("Description: Optimal Overloaded IO Protection System (OOOPS) us an easy to use tool ")

-- Create environment variables.
local ooops_dir           = "%{INSTALL_DIR}"

family("ooops")
prepend_path( "PATH",                   pathJoin(ooops_dir, "bin"))
prepend_path( "LD_LIBRARY_PATH",        pathJoin(ooops_dir, "lib"))
append_path(  "LD_PRELOAD",             pathJoin(ooops_dir, "lib/ooops.so") )

setenv( "IO_LIMIT_CONFIG",              pathJoin(ooops_dir, "conf/config_frontera") )
setenv( "TACC_OOOPS_BIN", pathJoin(ooops_dir, "bin"))
setenv( "OOOPS_NCALL_REPORT_THRESHOLD", "60000")
setenv( "OOOPS_NCALL_PS_REPORT_THRESHOLD", "2")
setenv( "OOOPS_REPORT_T_INTERVAL", "30")


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

