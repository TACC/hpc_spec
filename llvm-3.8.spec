# $Id: llvm-3.8.spec, 2013/07/02 10:18:32 willmore Exp $

Summary: LLVM, includes Clang 
Name: llvm
Version: 3.8
Release: 0
License: BSD
Group: Development/Libraries
Source0:%{name}-%{version}.tar.bz2
Packager:  cjansen@tacc.utexas.edu
Url: http://www.llvm.org

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME llvm
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_LLVM

%description
The LLVM Project is a collection of modular and reusable compiler and toolchain technologies. Despite its name, LLVM has little to do with traditional virtual machines, though it does provide helpful libraries that can be used to build them. The name "LLVM" itself is not an acronym; it is the full name of the project.

%prep
#rm_REMOVED_FOR_SAFETY-rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{PNAME}-%{version} #Unzips the zip and writes it to build directory

%build

#if [ -f "$BASH_ENV" ]; then #making sure bash exists
#  . $BASH_ENV
#  module purge
#  clearMT
#   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
#fi
#export CC=gcc
#./configure --prefix=%{INSTALL_DIR} #replace with cmake

mkdir build 
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} -DMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD=X86  -DBUILD_SHARED_LIBS=1 -DLLVM_ENABLE_RTTI=1 
#^^?Does it know which source to access automatically (.. not ../xxx.src)?
make --jobs=4

%install
cd build 
make install DESTDIR=$RPM_BUILD_ROOT


#-----------------
# Modules Section 
#-----------------

#rm_REMOVED_FOR_SAFETY -rf    $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p  $RPM_BUILD_ROOT/%{MODULE_DIR}
cat   >   $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines %{MODULE_VAR}_DIR, %{MODULE_VAR}_BIN, and %{MODULE_VAR}_LIB 

Version %{version}
]]
)

whatis("Name: LLVM")
whatis("Version: %{version}")
whatis("Category: compiler")
whatis("Keywords: Compiler")
whatis("URL: http://www.llvm.org/")
whatis("Description: a collection of modular and reusable compiler and toolchain technologies.")

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
#rm_REMOVED_FOR_SAFETY-rf $RPM_BUILD_ROOT



