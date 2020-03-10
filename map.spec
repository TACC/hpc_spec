#
# Spec file for DDT
#
# Give the package a base name
%define pkg_base_name ddt
%define MODULE_VAR    ddt

# Create some macros (spec file variables)
%define major_version 19
%define minor_version 0
%define micro_version 5

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

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
# Name: ddt
# Version: 18.1.3
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}_%{pkg_version}-buildroot
Summary: DDT is a parallel, symbolic debugger.
########################################

Release: 1%{?dist}
License: Commercial
Vendor: Allinea
URL: http://www.allinea.com
Packager: TACC - cazes@tacc.utexas.edu
Source:    %{pkg_base_name}_%{pkg_version}.tar.gz
#  define _unpack_name ddt_7.0.3
%define _system_config_file system.config


# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: DDT is a parallel, symbolic debugger.
Group: tools/debugging
%description package
The Distributed Debugging Tool is a comprehensive graphical debugger for scalar, multi-threaded and large-scale parallel applications that are written in C, C++ and Fortran.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
The Distributed Debugging Tool is a comprehensive graphical debugger for scalar, multi-threaded and large-scale parallel applications that are written in C, C++ and Fortran.

%description 
The Distributed Debugging Tool is a comprehensive graphical debugger for scalar, multi-threaded and large-scale parallel applications that are written in C, C++ and Fortran.

%define HOME1 /home1/apps
%define OPT /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{HOME1}/%{pkg_base_name}/%{version}
%define MODULE_DIR  %{OPT}/%{MODULES}/%{pkg_base_name}

# %define licenses ddt-license
# BuildRoot: /tmp/%{name}-%{version}-buildroot

%prep

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

#  %setup -n ddt_%{version}
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
  ###
  ### Edit config.ddt file to reflect installation directory
  ###
  cp $RPM_BUILD_ROOT/%{INSTALL_DIR}/%{_system_config_file} $RPM_BUILD_ROOT/%{INSTALL_DIR}/%{_system_config_file}.orig

  sed -i -e 's@INSTALL_DIR@%{INSTALL_DIR}@' $RPM_BUILD_ROOT/%{INSTALL_DIR}/%{_system_config_file}

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

--  modulefile for DDT 

local help_message = [[

For detailed instructions, go to:
   https://portal.tacc.utexas.edu/software/ddt

0.  Login to Frontera with X11 enabled:
        ssh -Y frontera.tacc.utexas.edu

1.  Load the ddt module:
        module load ddt

2.  Start ddt
        ddt ./<host_exe> <args>

3.  Set your mpi type via the "Change" button in the MPI pane in the 
    "DDT - Run" window.  Choose the appropriate MPI version from the 
    "MPI/UPC Implementation" "DDT - Run" window.  (The default is set
    to "Intel MPI".)

4.  Set the number of tasks to the TOTAL number of MPI tasks in the 
    "Number of processes" window in the MPI section.

5.  Set the number of nodes to the number of nodes you would like to 
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
setenv("ALLINEA_TOOLS_CONFIG_DIR",pathJoin(home,".allinea_%{version}"))
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
## version file for ddt
##
 
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

