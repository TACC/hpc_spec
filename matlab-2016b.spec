# $Id: matlab.spec, v2016b, 2017/03/07 siliu $ 
Summary: Matlab
Name: Matlab
Version: 2016b
Release: 1
License: Mathworks License
Vendor: Mathworks
Group: Matlab
Source: %{name}-%{version}.tar.gz
Packager:  siliu@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps/
%define MODULES modulefiles

# Note: this is a binary distribution and there is nothing to compile!
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}


%description
MATLAB is a high-level language and interactive environment that enables you to perform computationally intensive tasks faster than with traditional programming languages such as C, C++, and Fortran.

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%build

%install

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[
MATLAB is a high-level language and interactive environment that enables you to  
perform computationally intensive tasks faster than with traditional programming languages
such as C, C++, and Fortran.
 
Unless you are supplying your own MATLAB license file,  
you are using a license owned by University of Texas at Austin.

The UT license is for ACADEMIC USE ONLY!

Version 2016b
]]
)

whatis("Name: MATLAB")
whatis("Version: 2016b")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab 2016b from MathWorks")

prepend_path("PATH", "/home1/apps/matlab/2016b/bin")

append_path("LD_LIBRARY_PATH", "/home1/apps/matlab/2016b/bin/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/matlab/2016b/runtime/glnxa64")
append_path("LD_LIBRARY_PATH", "/home1/apps/matlab/2016b/sys/java/jre/glnxa64/jre/lib/amd64/server/")

setenv ("TACC_MATLAB_DIR", "/work/apps/matlab/2016b")

--Set MKLROOT, BLAS_VERSION, and LAPACK_VERSION for matlab
local mklroot=os.getenv("MKLROOT")

if mklroot then
    setenv("BLAS_VERSION", pathJoin(mklroot,"lib/intel64/libmkl_rt.so") )
    setenv("LAPACK_VERSION", pathJoin(mklroot,"lib/intel64/libmkl_rt.so") )
    setenv("MKL_INTERFACE_LAYER","ILP64")
end

local UserWork=os.getenv("WORK") 
--setenv ("MATLAB_PREFDIR", pathJoin(UserWork, "/mypref") )

--License file
local UserHome=os.getenv("HOME")
append_path("LM_LICENSE_FILE", pathJoin(UserHome,".tacc_matlab_license") )

EOF

%files
%defattr(-,root,install)
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
