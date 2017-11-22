# $Id: matlab.spec, v2017a, 2017/03/20 siliu $ 

Summary: Matlab
Name: matlab
Version: 2017b
Release: 1
License: Mathworks License
Vendor: Mathworks
Group: Matlab
Source:  %{name}-%{version}.tar.gz
Packager: siliu@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%define PKG_BASE    %{APPS}/%{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_TIPS

%description
MATLAB is a high-level language and interactive environment 
that enables you to perform computationally intensive tasks faster 
than with traditional programming languages such as C, C++, and Fortran.

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
MATLAB is a high-level language and interactive environment 
that enables you to perform computationally intensive tasks faster 
than with traditional programming languages such as C, C++, and Fortran.

Unless you are supplying your own MATLAB license file,
you are using a license owned by University of Texas at Austin.

The UT license is for ACADEMIC USE ONLY!

Version 2017b
]]
)

whatis("Name: MATLAB")
whatis("Version: 2017b")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab 2017b from MathWorks")

append_path("PATH", "/opt/apps/matlab/2017b/bin")

append_path("LD_LIBRARY_PATH", "/opt/apps/matlab/2017b/bin/glnxa64")
append_path("LD_LIBRARY_PATH", "/opt/apps/matlab/2017b/runtime/glnxa64")
append_path("LD_LIBRARY_PATH", "/opt/apps/matlab/2017b/sys/java/jre/glnxa64/jre/lib/amd64/server")

setenv ("TACC_MATLAB_DIR", "/opt/apps/matlab/2017b")
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

