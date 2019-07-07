#
# Si Liu
# 2019-06-13
#

# Give the package a base name
%define pkg_base_name matlab
%define MODULE_VAR    MATLAB

# Create some macros (spec file variables)
%define major_version 2019a

%define pkg_version %{major_version}

Summary: Matlab spec file
Release: 1%{?dist}
License: Mathworks License
Vendor: Mathworks
Group: Utility
Source: %{name}-%{version}.tar.gz
Packager:  TACC - siliu@tacc.utexas.edu

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
Summary: Matlab package RPM
Group: Applications
%description package
MATLAB is a high-level language and interactive environment that enables you to perform computationally intensive tasks faster than with traditional programming languages such as C, C++, and Fortran.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
MATLAB is a high-level language and interactive environment that enables you to perform computationally intensive tasks faster than with traditional programming languages such as C, C++, and Fortran.

%description
MATLAB is a high-level language and interactive environment that enables you to perform computationally intensive tasks faster than with traditional programming languages such as C, C++, and Fortran.



#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

# Insert necessary module commands
module purge

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
# mount -t tmpfs tmpfs %{INSTALL_DIR}
  
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

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[
MATLAB interpreter and compiler MATLAB is a high-level language
and interactive environment that enables you to perform computationally
intensive tasks faster than with traditional programming languages
such as C, C++, and Fortran.
 
Unless you are supplying your own MATLAB license file,
you are using a license owned by University of Texas at Austin.

The UT license is for ACADEMIC USE ONLY!

Version 2019a
]]
)

whatis("Name: MATLAB")
whatis("Version: 2019a")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab 2019a from MathWorks")

prepend_path("PATH", "/home1/apps/matlab/2019a/bin")

append_path("LD_LIBRARY_PATH", "/home1/apps/matlab/2019a/bin/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/matlab/2019a/runtime/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/matlab/2019a/sys/java/jre/glnxa64/jre/lib/amd64/server/")

setenv ("TACC_MATLAB_DIR", "/home1/apps/matlab/2019a")
setenv ("DVS_CACHE","off")

--Set MKLROOT, BLAS_VERSION, and LAPACK_VERSION for matlab
local mklroot=os.getenv("MKLROOT")

if mklroot then
  setenv("BLAS_VERSION", pathJoin(mklroot,"lib/intel64/libmkl_rt.so") )
  setenv("LAPACK_VERSION", pathJoin(mklroot,"lib/intel64/libmkl_rt.so") )
  setenv("MKL_INTERFACE_LAYER","ILP64")
end

--License file
local UserHome=os.getenv("HOME")
append_path("LM_LICENSE_FILE", pathJoin(UserHome,".tacc_matlab_license") )

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

