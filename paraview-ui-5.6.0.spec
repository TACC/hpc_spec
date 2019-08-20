#
# Spec file for ParaView 5.6.0
#


Summary:   ParaView 5.6.0 local binary install
Packager:  gda@tacc.utexas.edu
License:   freely distributable
Vendor:    www.kitware.com
Group:     Visualization

Release:   0
Source:    ParaView-v5.6.0.tar.gz

# Give the package a base name
%define pkg_base_name paraview
%define MODULE_VAR    PARAVIEW

%define major_version 5
%define minor_version 6
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

%define is_intel19 1
%define is_cmpich 1

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
%include name-defines.inc

Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot

%define debug_package 	%{nil}
%define dbg		%{nil}


%package %{PACKAGE}
Summary: paraview 5.6.0 UI/X local binary install
Group: Visualization
%description package
ParaView is a free interactive parallel visualization and graphical analysis tool.

%package %{MODULEFILE}
Summary: paraview 5.6.0 UI/X modulefile
Group: Visualization
%description modulefile
ParaView is a free interactive parallel visualization and graphical analysis tool.

%description 
ParaView is a free interactive parallel visualization and graphical analysis tool.

%prep

echo "Building the modulefile?: %{BUILD_MODULEFILE}"
echo "Building the package?: %{BUILD_PACKAGE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n ParaView-v5.6.0

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

%include compiler-load.inc
%include mpi-load.inc

module use /admin/build/gda/rpminstall/modulefiles
module load python2 cmake qt5 ospray

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


  mkdir build
  cd build
  CC=icc CXX=icpc cmake .. \
    -DPARAVIEW_ENABLE_WEB=OFF \
    -DOSPRAY_INSTALL_DIR=$TACC_OSPRAY_DIR \
    -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT/%{INSTALL_DIR} \
    -DCMAKE_BUILD_TYPE=Release \
    -DPARAVIEW_QT_VERSION=5 \
    -DPARAVIEW_USE_MPI=OFF \
    -DVTK_USE_SYSTEM_HDF5=ON \
    -DPARAVIEW_ENABLE_PYTHON=ON \
    -DPARAVIEW_INSTALL_DEVELOPMENT_FILES=ON \
    -DPARAVIEW_USE_OSPRAY=ON 

  make pvCompileTools
  make -j 6

%endif # BUILD_PACKAGE


%install

# Setup modules
%include compiler-load.inc
%include mpi-load.inc


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

  cd build
make -j 6 install

cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/paraview-config << 'EOF1'
echo paraview-config is not available
EOF1

cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/paraview-config << 'EOF2'
echo paraview-config is not available
EOF2


find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name  QtTestingConfig.cmake -print
find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name  QtTestingConfig.cmake | xargs sed -i "s|$RPM_BUILD_ROOT||g"
find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name  vtkPython.cmake -print
find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name  vtkPython.cmake | xargs sed -i "s|$RPM_BUILD_ROOT||g"
find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name  VTKConfig.cmake -print
find $RPM_BUILD_ROOT/%{INSTALL_DIR} -name  VTKConfig.cmake | xargs sed -i "s|$RPM_BUILD_ROOT||g"
chmod a+x $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/paraview-config $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/paraview-config

cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/pv-parallel-startup << 'EOF1'
#! /bin/bash
module load paraview-osmesa
ibrun swr pvserver
EOF1

chmod a+rx $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/pv-parallel-startup

cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/default_servers.pvsc << 'EOF2'
<Servers>
  <Server name="auto" configuration="" resource="cs://localhost:11111">
    <CommandStartup>
      <Command exec="pv-parallel-startup" timeout="0" delay="5">
        <Arguments/>
      </Command>
    </CommandStartup>
  </Server>
</Servers>
EOF2

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
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.
]]

--help(help_msg)
help(help_msg)

whatis("Name: paraview")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

conflict("paraview")
prereq("python2", "qt5", "ospray", "swr")

-- Create environment variables.
local pv_dir           = "%{INSTALL_DIR}"

family("paraview")
prepend_path("PATH",               pathJoin(pv_dir, "bin"))
prepend_path("LD_LIBRARY_PATH",    pathJoin(pv_dir, "lib"))
prepend_path("MODULEPATH",         "%{MODULE_PREFIX}/modulefiles")
prepend_path("PYTHONPATH", 	   pathJoin(pv_dir, "lib/%{pkg_version}/site-packages"))
prepend_path("PYTHONPATH", 	   pathJoin(pv_dir, "lib/%{pkg_version}/site-packages/vtk"))

setenv( "TACC_%{MODULE_VAR}_DIR",       pv_dir)
setenv( "TACC_%{MODULE_VAR}_INC",       pathJoin(pv_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(pv_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_LIB64",     pathJoin(pv_dir, "lib64"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(pv_dir, "bin"))
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

