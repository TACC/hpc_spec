#
# Spec file for forge
#
# Give the package a base name
%define pkg_base_name forge
%define MODULE_VAR    forge

# Create some macros (spec file variables)
%define major_version 20
%define minor_version 0
%define micro_version 2

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
# Name: Forge
# Version: 20.0.2
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}_%{pkg_version}-buildroot
Summary: Forge contains ddt and map, parallel debugger and parallel profiler.
########################################

Release: 1%{?dist}
License: Commercial
Vendor: ARM
URL: http://www.arm.com
Packager: TACC - cazes@tacc.utexas.edu
Source:    %{pkg_base_name}_%{pkg_version}.tar.gz
#  define _unpack_name ddt_7.0.3
%define _system_config_file system.config


# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

%package %{PACKAGE}
Summary: Forge contains DDT and MAP
Group: tools/debugging
%description package
The Forge package contains DDT, a comprehensive graphical debugger for scalar, multi-threaded and large-scale parallel applications, and MAP, a parallel, lightweight profiler.  There are separate module files for ddt_skx, ddt_knl, and map_skx because they use different licenses.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
The Forge package contains DDT, a comprehensive graphical debugger for scalar, multi-threaded and large-scale parallel applications, and MAP, a parallel, lightweight profiler.

%description 
The Forge package contains DDT, a comprehensive graphical debugger for scalar, multi-threaded and large-scale parallel applications, and MAP, a parallel, lightweight profiler.

%define HOME1 /home1/apps
%define OPT /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{HOME1}/%{pkg_base_name}/%{version}
%define DDT_KNL_MODULE_DIR  %{OPT}/%{MODULES}/ddt_knl
%define DDT_SKX_MODULE_DIR  %{OPT}/%{MODULES}/ddt_skx
%define MAP_SKX_MODULE_DIR  %{OPT}/%{MODULES}/map_skx

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
  rm -rf $RPM_BUILD_ROOT/%{DDT_KNL_MODULE_DIR}
  rm -rf $RPM_BUILD_ROOT/%{DDT_SKX_MODULE_DIR}
  rm -rf $RPM_BUILD_ROOT/%{MAP_SKX_MODULE_DIR}
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

  rm -rf  $RPM_BUILD_ROOT/%DDT_KNL_MODULE_DIR
  rm -rf  $RPM_BUILD_ROOT/%DDT_SKX_MODULE_DIR
  rm -rf  $RPM_BUILD_ROOT/%MAP_SKX_MODULE_DIR
  mkdir -p $RPM_BUILD_ROOT/%DDT_KNL_MODULE_DIR
  mkdir -p $RPM_BUILD_ROOT/%DDT_SKX_MODULE_DIR
  mkdir -p $RPM_BUILD_ROOT/%MAP_SKX_MODULE_DIR
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{DDT_KNL_MODULE_DIR}/.tacc_module_canary
  touch $RPM_BUILD_ROOT/%{DDT_SKX_MODULE_DIR}/.tacc_module_canary
  touch $RPM_BUILD_ROOT/%{MAP_SKX_MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  cat > $RPM_BUILD_ROOT/%{DDT_KNL_MODULE_DIR}/%{version}.lua << 'EOF'

--  modulefile for DDT KNL

local help_message = [[

For detailed instructions, go to:
   https://portal.tacc.utexas.edu/software/ddt

0.  Login to Frontera with X11 enabled:
        ssh -Y stampede2.tacc.utexas.edu

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
    have in the queue, including a job named "forge".  Once the batch 
    job begins, the DDT Debugging window will appear.

]]

help(help_message,"\n")

whatis("Version: %{version}")
whatis("Category: utility, runtime support")
whatis("Keywords: System, Utility")
whatis("URL: https://static.docs.arm.com/101136/2002/userguide-forge.pdf ")
whatis("Description: Parallel, graphical, symbolic debugger")

local home = os.getenv("HOME")


setenv("DDTROOT","%{INSTALL_DIR}")
setenv("DDTPATH","%{INSTALL_DIR}/bin")
setenv("TACC_DDT_DIR","%{INSTALL_DIR}")
setenv("TACC_DDT_BIN","%{INSTALL_DIR}/bin")
setenv("ALLINEA_TOOLS_CONFIG_DIR",pathJoin(home,".forge_knl_%{version}"))
setenv("ALLINEA_LICENSE_DIR","%{INSTALL_DIR}/licenses/knl")
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

  cat > $RPM_BUILD_ROOT/%{DDT_SKX_MODULE_DIR}/%{version}.lua << 'EOF'

--  modulefile for DDT SKX

local help_message = [[

For detailed instructions, go to:
   https://portal.tacc.utexas.edu/software/ddt

0.  Login to Frontera with X11 enabled:
        ssh -Y stampede2.tacc.utexas.edu

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
    have in the queue, including a job named "forge".  Once the batch 
    job begins, the DDT Debugging window will appear.

]]

help(help_message,"\n")

whatis("Version: %{version}")
whatis("Category: utility, runtime support")
whatis("Keywords: System, Utility")
whatis("URL: https://static.docs.arm.com/101136/2002/userguide-forge.pdf ")
whatis("Description: Parallel, graphical, symbolic debugger")

local home = os.getenv("HOME")


setenv("DDTROOT","%{INSTALL_DIR}")
setenv("DDTPATH","%{INSTALL_DIR}/bin")
setenv("TACC_DDT_DIR","%{INSTALL_DIR}")
setenv("TACC_DDT_BIN","%{INSTALL_DIR}/bin")
setenv("ALLINEA_TOOLS_CONFIG_DIR",pathJoin(home,".forge_skx_%{version}"))
setenv("ALLINEA_LICENSE_DIR","%{INSTALL_DIR}/licenses/skx")
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF
  cat > $RPM_BUILD_ROOT/%{MAP_SKX_MODULE_DIR}/%{version}.lua << 'EOF'

--  modulefile for MAP SKX

local help_message = [[

-- For detailed instructions, go to:
--    https://portal.tacc.utexas.edu/software/ddt

0.  Login to Frontera with X11 enabled:
        ssh -Y stampede2.tacc.utexas.edu

1.  Load the map module:
        module load map

2.  Start map
        map ./<host_exe> <args>

3.  Set your mpi type via the "Change" button in the MPI pane in the 
    "MAP - Run" window.  Choose the appropriate MPI version from the 
    "MPI/UPC Implementation" "MAP - Run" window.  (The default is set
    to "Intel MPI".)

4.  Set the number of tasks to the TOTAL number of MPI tasks in the 
    "Number of processes" window in the MPI section.

5.  Set the number of nodes to the number of nodes you would like to 
    run on.  This is analagous to using "-N #" in a slurm batch script.

6.  Set your project via the "Parameters" button in the 
    "Queue Submission Parameters" pane.

7.  Submit your job using the "Submit" at the bottom of the 
    "MAP - Run" window.

8.  A "Job Submitted" window should appear and show all of the jobs you 
    have in the queue, including a job named "forge".  Once the batch 
    job begins, the MAP Profiling window will appear.

9.  You may stop the job at any point to analyze the data collected up 
    until that point.  Or, you may let the job finish and analyze the 
    complete results. 
]]

help(help_message,"\n")

whatis("Version: %{version}")
whatis("Category: utility, runtime support")
whatis("Keywords: System, Utility")
whatis("URL: https://static.docs.arm.com/101136/2002/userguide-forge.pdf ")
whatis("Description: Parallel, graphical, profiler")

local home = os.getenv("HOME")


setenv("MAPROOT","%{INSTALL_DIR}")
setenv("MAPPATH","%{INSTALL_DIR}/bin")
setenv("TACC_MAP_DIR","%{INSTALL_DIR}")
setenv("TACC_MAP_BIN","%{INSTALL_DIR}/bin")
setenv("ALLINEA_TOOLS_CONFIG_DIR",pathJoin(home,".forge_skx_%{version}"))
setenv("ALLINEA_LICENSE_DIR","%{INSTALL_DIR}/licenses/skx")
prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

cat > $RPM_BUILD_ROOT/%{DDT_KNL_MODULE_DIR}/.version.%{version} << 'EOF'
## version file for ddt
##
 
set     ModulesVersion      "%{version}"
EOF

cat > $RPM_BUILD_ROOT/%{DDT_SKX_MODULE_DIR}/.version.%{version} << 'EOF'
## version file for ddt
##
 
set     ModulesVersion      "%{version}"
EOF

cat > $RPM_BUILD_ROOT/%{MAP_SKX_MODULE_DIR}/.version.%{version} << 'EOF'
## version file for map
##
 
set     ModulesVersion      "%{version}"
EOF

#  # Check the syntax of the generated lua modulefile only if a visible module
#  %if %{?VISIBLE}
#    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{DDT_KNL_MODULE_DIR}/%{MODULE_FILENAME}
#    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{DDT_SKX_MODULE_DIR}/%{MODULE_FILENAME}
#    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MAP_SKX_MODULE_DIR}/%{MODULE_FILENAME}
#  %endif
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
  %{DDT_KNL_MODULE_DIR}
  %{DDT_SKX_MODULE_DIR}
  %{MAP_SKX_MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------

########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
#export PACKAGE_POST=1
#%include post-defines.inc
%post %{MODULEFILE}
#export MODULEFILE_POST=1
#%include post-defines.inc
#%preun %{PACKAGE}
#export PACKAGE_PREUN=1
#%include post-defines.inc
########################################
############ Do Not Remove #############
########################################


%clean
rm -rf $RPM_BUILD_ROOT

