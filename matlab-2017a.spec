# $Id: matlab.spec, v 2017a, 2017/08/01 siliu $ 
 
Summary: Matlab

Name: matlab
Version: 2017a
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

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%description
MATLAB is a high-level language and interactive environment that enables you to perform computationally intensive tasks faster than with traditional programming languages such as C, C++, and Fortran.

%prep
##rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
##mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
 
## SETUP
##setup -n %{name}-%{version}
 
## BUILD
%build

#INSTALL
%install

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help(
[[
MATLAB interpreter and compiler MATLAB is a high-level language
and interactive environment that enables you to perform computationally
intensive tasks faster than with traditional programming languages
such as C, C++, and Fortran.
 
UT Austin students, researchers and faculty have access to UT Austin license. 
Please contact the TACC help desk with your department/college information.

All other students, researchers and faculty: Matlab usage on TACC systems
follows a Bring-Your-Own-License format. To use Matlab on TACC resources
you must have a matlab license server with a floating network license.
Furthermore the license server has to be accessible from the compute nodes
on TACC systems. You can test this with:
telnet hostname port_number

The TACC helpdesk staff can provide ip-ranges to your license admin to
add exceptions in your firewall rules for license checkout.

Version 2017a
]]
)

whatis("Name: MATLAB")
whatis("Version: 2017a")
whatis("Category: library, mathematics")
whatis("Keywords: Library, Mathematics, Tools")
whatis("URL: http://www.mathworks.com/")
whatis("Description: Matlab 2017a from MathWorks")

prepend_path("PATH", "/work/apps/matlab/2017a/bin")

prepend_path("LD_LIBRARY_PATH", "/work/apps/matlab/2017a/bin/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/work/apps/matlab/2017a/runtime/glnxa64")
prepend_path("LD_LIBRARY_PATH", "/work/apps/matlab/2017a/sys/java/jre/glnxa64/jre/lib/amd64/server/")

setenv ("TACC_MATLAB_DIR", "/work/apps/matlab/2017a")
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
 
set     ModulesVersion      "%{version}"
EOF

%files
%defattr(-,root,install)
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
