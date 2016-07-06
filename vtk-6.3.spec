#
# Spec file for vtk
#

Summary:  vtk 6.3 local binary install
Name:     vtk
Version:  6.3.0
Release:  0
License:  freely distributable
Vendor:   vtk.org
Group:    Visualization 
Packager:  gda@tacc.utexas.edu

%include rpm-dir.inc

%define VTK VTK-%{version}
%define VTK_SRC %{VTK}.tar.gz

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}
%define PACKAGE_NAME %{name}-%{comp_fam_ver}-%{mpi_fam_ver}

%package -n %{PACKAGE_NAME}
Summary: vtk %{version} local binary install
Group: Visualization

%description
%description -n %{PACKAGE_NAME}
VTK, the Visualization Toolkit, is a library of
visualization algorithms used by ParaView, VisIt,
EnVision and other fine visualization software

%prep

if test -e $RPM_BUILD_DIR/%{VTK} ; then
	rm -rf $RPM_BUILD_DIR/%{VTK}
fi
tar xzf $RPM_SOURCE_DIR/%{VTK_SRC}
cd $RPM_BUILD_DIR/%{VTK}
patch -p0 < $RPM_SOURCE_DIR/vtk-6.3-findmpi.patch
	
%build

cd $RPM_BUILD_DIR/%{VTK}
mkdir -p build 
cd build

module load cmake python qt/4.8

CC=icc CXX=icpc MPI_C_COMPILER=mpicc MPI_CXX_COMPILER=mpicxx cmake .. \
	-DVTK_Group_MPI=ON \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=/opt/apps/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version} \
	-DVTK_Group_Imaging=ON \
	-DVTK_Group_MPI=ON \
	-DVTK_Group_Qt=ON \
	-DVTK_Group_Rendering=ON \
	-DVTK_Group_StandAlone=ON \
	-DVTK_Group_Tk=OFF \
	-DVTK_Group_Views=ON \
	-DVTK_PYTHON_VERSION=2  \
	-DVTK_RENDERING_BACKEND=OpenGL2 \
	-DVTK_SMP_IMPLEMENTATION_TYPE=TBB \
	-DVTK_USE_LARGE_DATA=ON \
	-DVTK_WRAP_PYTHON=ON \
	-DTBB_INCLUDE_DIR=/opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/tbb/include \
	-DTBB_LIBRARY_DEBUG=/opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/tbb/lib/intel64_lin/gcc4.4/libtbb.so \
	-DTBB_LIBRARY_RELEASE=/opt/apps/intel/16.0.1.150/compilers_and_libraries_2016.1.150/linux/tbb/lib/intel64_lin/gcc4.4/libtbb.so  \
	-DPYTHON_EXECUTABLE=$TACC_PYTHON_DIR/bin/python2 \
	-DPYTHON_INCLUDE_DIR=$TACC_PYTHON_DIR/include/python2.7 \
	-DPYTHON_LIBRARY=$TACC_PYTHON_DIR/lib/libpython2.7.so

make -j 8 install

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r %{INSTALL_DIR}/* $RPM_BUILD_ROOT/%{INSTALL_DIR}

## Module for vtk-%{version}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version} << 'EOF'
#%Module1.0#####################################################################
##
## VTK library
##
proc ModulesHelp { } {
        puts stderr "\tVTK Library\n"
        puts stderr "\tThis module loads VTK library variables.\n"
	    puts stderr "\t{ The command directory is added to PATH.             } \n"
        puts stderr "\t{ The library directory is added to LD_LIBRARY_PATH.  } \n"
        puts stderr "\t{ The include directory is added to INCLUDE.          } \n"
        puts stderr "\t{ The python  directory is added to PYTHONPATH        } \n"
        puts stderr "\n\tVersion %{version}\n"

}

module-whatis   "VTK: Visualization Tool Kit"
module-whatis   "Version: %{version}"
module-whatis   "Category: library, visualization"
module-whatis   "Description: an open-source system for 3D computer graphics, image processing and visualization"
module-whatis   "URL: http://www.vtk.org"

conflict vtk

prereq qt/4.8
prereq python

prepend-path    PATH               %{INSTALL_DIR}/bin
prepend-path    LD_LIBRARY_PATH    %{INSTALL_DIR}/lib:%{INSTALL_DIR}/lib/site-packages/mpi4py:%{INSTALL_DIR}/lib/python2.7/site-packages/vtk
prepend-path    PYTHONPATH         %{INSTALL_DIR}/site-packages:%{INSTALL_DIR}/lib/python2.7/site-packages

setenv 		VTK_LOCATION	%{INSTALL_DIR}
setenv          TACC_VTK_DIR    %{INSTALL_DIR}
setenv          TACC_VTK_INC    %{INSTALL_DIR}/include
setenv          TACC_VTK_LIB    %{INSTALL_DIR}/lib

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0#################################################################
##
## version file for vtk %{version}
##

set     ModulesVersion     "%version"

EOF


%files -n %{PACKAGE_NAME}
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post -n %{PACKAGE_NAME}
%clean
rm -rf $RPM_BUILD_ROOT
