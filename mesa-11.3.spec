Summary: Mesa, include Intel OpenSWR
Name: swr
Version: 11.3
Release: 0
License: BSD
Group: X11/Libraries
Source0:%{name}-%{version}.tar.bz2
Packager:  cjansen@tacc.utexas.edu
Url: github.org/OpenSWR/openswr-mesa

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME %{name}
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_SWR
%define LLVM_INSTALL_PATH %{APPS}/llvm/3.8

%description

%prep
# rm_REMOVED_FOR_SAFETY   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%setup -n %{PNAME}-%{version}

%build
./autogen.sh --with-gallium-drivers=swrast,swr --disable-dri --disable-egl --enable-xlib-glx --with-llvm-prefix=%{LLVM_INSTALL_PATH} --prefix=%{INSTALL_DIR}

make -j4


%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p  $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin


cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/mesa << 'EOF'
#!/bin/bash
LD_LIBRARY_PATH=%{LLVM_INSTALL_PATH}/lib:%{INSTALL_DIR}/lib:$LD_LIBRARY_PATH GALLIUM_DRIVER=llvmpipe $*
EOF

cat > $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/swr << 'EOF'
#!/bin/bash
LD_LIBRARY_PATH=%{LLVM_INSTALL_PATH}/lib:%{INSTALL_DIR}/lib:$LD_LIBRARY_PATH GALLIUM_DRIVER=swr $*
EOF





#-----------------
# Modules Section 
#-----------------

# rm_REMOVED_FOR_SAFETY -rf    $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p  $RPM_BUILD_ROOT/%{MODULE_DIR}
cat   >   $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines %{MODULE_VAR}_DIR, %{MODULE_VAR}_BIN, and %{MODULE_VAR}_LIB 

Version %{version}
]]
)


whatis("Name:OpenSWR")
whatis("Version: %{version}")
whatis("Category: X11")
whatis("Keywords: OpenSWR Intel Mesa")
whatis("URL: http://github.org/OpenSWR/openswr-mesa")
whatis("Description: OpenSWR Mesa implementation from Intel")

prepend_path("PATH",        "%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
setenv("%{MODULE_VAR}_LIB", "%{INSTALL_DIR}/lib")

EOF

#--------------
#  Version file. 
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
#rm_REMOVED_FOR_SAFETY -rf $RPM_BUILD_ROOT



