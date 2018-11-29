#
# Spec file for DDT
#
Summary: DDT is a parallel, symbolic debugger.
Name: ddt
Version: 18.1.3
Release: 2
License: Commercial
Group: tools/debugging
Source0: ddt_18.1.3.tar.gz
URL: https://developer.arm.com/products/software-development-tools/hpc/downloads/download-arm-forge
Distribution: SuSE Linux
Vendor: Allinea
Packager: TACC - cazes@tacc.utexas.edu
%include rpm-dir.inc
%define _unpack_name %{name}_%{version}
%define _system_config_file system.config

%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

# %define licenses ddt-license
# BuildRoot: /tmp/%{name}-%{version}-buildroot
%description

The Distributed Debugging Tool is a comprehensive graphical debugger for scalar,
multi-threaded and large-scale parallel applications that are written in C, C++ and
Fortran.

%package -n tacc-%{name}
Summary: Module file for %{name}
Group: tools/debugging
%description -n tacc-%{name}
Module file for %{name}

%prep
# rm -rf  $RPM_BUILD_ROOT/%INSTALL_DIR
mkdir -p $RPM_BUILD_ROOT/%INSTALL_DIR
pwd

%setup -n %{_unpack_name} 

%build
#SUSE handles this differently. sigh.
rm -rf  $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
ls -ld $RPM_BUILD_ROOT/%{INSTALL_DIR}


cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}
###
### Edit config.ddt file to reflect installation directory
###
cp $RPM_BUILD_ROOT/%{INSTALL_DIR}/%{_system_config_file} $RPM_BUILD_ROOT/%{INSTALL_DIR}/%{_system_config_file}.orig

sed -i -e 's@INSTALL_DIR@%{INSTALL_DIR}@' $RPM_BUILD_ROOT/%{INSTALL_DIR}/%{_system_config_file}

#
#
chmod -R a+rX $RPM_BUILD_ROOT/%INSTALL_DIR

# rm -rf  $RPM_BUILD_ROOT/%MODULE_DIR
mkdir -p $RPM_BUILD_ROOT/%MODULE_DIR
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

--  modulefile for DDT 

local help_message = [[

For detailed instructions, go to:
   https://portal.tacc.utexas.edu/software/ddt

0.  Login to Lonestar with X11 enabled:
        ssh -Y ls5.tacc.utexas.edu

1.  Load the ddt module:
        module load ddt

2.  Start ddt
        ddt ./<host_exe> <args>

3.  Set your mpi type via the "Change" button in the MPI pane in the 
    "DDT - Run" window.  Choose "MPICH 2" if it is not already selected
    from the "MPI/UPC Implementation" dropdown menu.

4.  Set the number of tasks to the TOTAL number of MPI tasks in the 
    "Number of Processes" window in the MPI section.

5.  Set the number of nodes via the "Parameters" button in the 
    run on.  This is analagous to using "-N #" in a slurm batch script.

6.  Set your project via the "Parameters" button in the 
    "Queue Submission Parameters" pane.

7.  Submit your job using the "Submit" at the bottom of the 
    "DDT - Run" window.

8.  A "Job Submitted" window should appear and show all of the jobs you 
    have in the queue, including a job named "ddt".  Once the batch 
    job begins, the DDT Debugging window will appear.

]]

help(help_message,"\n")

whatis("Version: %{version}")
whatis("Category: utility, runtime support")
whatis("Keywords: System, Utility")
whatis("URL: http://content.allinea.com/downloads/userguide.pdf")
whatis("Description: Parallel, graphical, symbolic debugger")

local home = os.getenv("HOME")

setenv("DDTROOT","%{INSTALL_DIR}")
setenv("DDTPATH","%{INSTALL_DIR}/bin")
setenv("TACC_DDT_DIR","%{INSTALL_DIR}")
setenv("TACC_DDT_BIN","%{INSTALL_DIR}/bin")
setenv("ALLINEA_TOOLS_CONFIG_DIR",pathJoin(home,".allinea"))
setenv("ALLINEA_ALLOW_CRAY_DMALLOC_PRELOAD","1")
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib/64")


EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
## version file for ddt
##
 
set     ModulesVersion      "%{version}"
EOF

%files -n tacc-%{name}
%defattr(-,root,root)
%{INSTALL_DIR}
%{MODULE_DIR}

%post


%clean
# rm -rf $RPM_BUILD_ROOT
