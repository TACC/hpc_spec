# $Id: openfoam.spec, 6.0, 2018/12/12 siliu $ 

Summary: OpenFoam spec file

# Give the package a base name
%define pkg_base_name openfoam
%define MODULE_VAR    OPENFOAM

# Create some macros (spec file variables)
%define major_version 6
%define minor_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
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


Release: 1
License: General Public Licence (GPL)
Vendor: OpenFOAM Foundation
Group: Utility/CFD
Source:  %{name}-%{version}.tar.gz
Packager: TACC - siliu@tacc.utexas.edu


%description
OpenFOAM is the leading free, open source software for computational fluid dynamics (CFD), owned by the OpenFOAM Foundation and distributed exclusively under the General Public Licence (GPL). The GPL gives users the freedom to modify and redistribute the software and a guarantee of continued free use, within the terms of the licence.

%prep
#Nothing necessary here

%build
#Nothing necessary here

%install

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[

The OpenFOAM (Open Field Operation and Manipulation) CFD Toolbox is a free, open source CFD software package.
This module is for OpenFOAM 6.0 compiled with Intel 18 and cray_mpich 7.7.

This OpenFOAM module defines a lot of environment variables from OpenFOAM bashrc file.
User may also source the following basrc file when necessary
/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/etc/bashrc

We suggest users set their own WM_PROJECT_USER_DIR and FOAM_RUN environment for their own OpenFOAM runs.
Typical settings could be:
export WM_PROJECT_USER_DIR=$WORK/OpenFOAM/personal
export FOAM_RUN=$WORK/OpenFOAM/personal/run

OpenFOAM user guide can be reached at
https://cfd.direct/openfoam/user-guide

For extra OpenFOAM support, please contact
https://cfd.direct/contact/

Version 6.0
]]
)

whatis("Name: OpenFOAM")
whatis("Version: 6.0")
whatis("Category: CFD")
whatis("Keywords: CFD, Tools")
whatis("URL: https://openfoam.org/")
whatis("Description: OpenFOAM 6.0")

setenv("FOAM_APP","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/applications")
setenv("FOAM_APPBIN","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/platforms/linux64IccDPInt32Opt/bin")
setenv("FOAM_ETC","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/etc");
setenv("FOAM_EXT_LIBBIN","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0/platforms/linux64IccDPInt32/lib")
setenv("FOAM_INST_DIR","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM")
setenv("FOAM_JOB_DIR","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/jobControl")
setenv("FOAM_LIBBIN","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0/platforms/linux64IccDPInt32/lib")
setenv("FOAM_MPI","7.7.3")
setenv("FOAM_SETTINGS","")
setenv("FOAM_SIGFPE","")
setenv("FOAM_SITE_APPBIN","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/site/6.0/platforms/linux64IccDPInt32Opt/bin")
setenv("FOAM_SITE_LIBBIN","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/site/6.0/platforms/linux64IccDPInt32Opt/lib")
setenv("FOAM_SOLVERS","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/applications/solvers")
setenv("FOAM_SRC","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/src")
setenv("FOAM_TUTORIALS","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/tutorials")
setenv("FOAM_UTILITIES","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/applications/utilities")

setenv("FOAMY_HEX_MESH","yes")

-- The following lines have been manually modified by Si Liu on Nov 20, 2017
-- Unless you really know what you are doing there

-- Si Liu extra tricks here 
append_path("LD_LIBRARY_PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/platforms/linux64IccDPInt32Opt/lib/dummy")
prepend_path("LD_LIBRARY_PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/platforms/linux64IccDPInt32Opt/lib/7.7.3")
prepend_path("LD_LIBRARY_PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0/platforms/linux64IccDPInt32/lib/7.7.3")
prepend_path("LD_LIBRARY_PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/platforms/linux64IccDPInt32Opt/lib")
prepend_path("LD_LIBRARY_PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0/platforms/linux64IccDPInt32/lib")

-- Extra MPI Settings:
setenv("MPI_ROOT",     "MPICH_HOME")
setenv("MPI_ARCH_PATH","MPICH_HOME")
setenv("MPI_BUFFER_SIZE","20000000")

-- The following lines(PATH) have been manually modified by Si Liu on Nov 21, 2017,
prepend_path("PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0/platforms/linux64Icc/cmake-3.2.1/bin")
prepend_path("PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/platforms/linux64IccDPInt32Opt/bin")
prepend_path("PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/bin")
prepend_path("PATH","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/wmake")

-- CGAL BOOST CMAKE
setenv("CMAKE_HOME"     ,"/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0/platforms/linux64Icc/cmake-3.2.1")
setenv("CMAKE_ROOT"     ,"/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0/platforms/linux64Icc/cmake-3.2.1")



-- Extra WM environment variables
setenv("WM_ARCH","linux64")
setenv("WM_ARCH_OPTION","64")
setenv("WM_CC","mpicc")
setenv("WM_CFLAGS","-O3 -m64 -fPIC")
setenv("WM_COMPILER","Icc")
setenv("WM_COMPILER_LIB_ARCH","64")
setenv("WM_COMPILE_OPTION","Opt")
setenv("WM_COMPILER_TYPE","system")
setenv("WM_CXX","mpicxx")
setenv("WM_CXXFLAGS","-O3 -m64 -fPIC -std=c++0x")
setenv("WM_DIR","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/wmake")
setenv("WM_LABEL_OPTION","Int32")
setenv("WM_LABEL_SIZE","32")

setenv("WM_LDFLAGS","-m64")
setenv("WM_LINK_LANGUAGE","c++")
setenv("WM_MPLIB","cray_mpich")
setenv("WM_OPTIONS","linux64IccDPInt32Opt")
setenv("WM_OSTYPE","POSIX")
setenv("WM_PRECISION_OPTION","DP")
setenv("WM_PROJECT","OpenFOAM")
setenv("WM_PROJECT_DIR","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0")
setenv("WM_PROJECT_INST_DIR","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM")
setenv("WM_PROJECT_VERSION","6.0")
setenv("WM_THIRD_PARTY_DIR","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/ThirdParty-6.0")
-- The following lines have been manually modified by Si Liu on Nov 20, 2017.
setenv("WM_LINK_LANGUAGE", "c++")

-- The following lines have been manually modified by Si Liu on July 28, 2014.
setenv("TACC_OPENFOAM_DIR","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0")
setenv("TACC_OPENFOAM_LIB","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/platforms/linux64IccDPInt32Opt/lib")
setenv("TACC_OPENFOAM_BIN","/opt/apps/intel18/cray_mpich_7_7/OpenFOAM/OpenFOAM-6.0/platforms/linux64IccDPInt32Opt/bin")

EOF


#--------------
#  Version file. 
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files
%defattr(755,root,root,-)
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

