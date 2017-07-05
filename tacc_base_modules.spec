Summary: TACC base module

# Give the package a base name
%define pkg_base_name tacc
%define MODULE_VAR    TACC
%define pkg_name      tacc_base_modules

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
Name:      tacc-base_modules
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   4%{?dist}
License:   GPL
Group:     Module Magic
Packager:  TACC - mclay@tacc.utexas.edu

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}
%define MODULES        modulefiles
%define APPS           /opt/apps
%define MODULE_DIR     %{APPS}/%{MODULES}/
%define MODULE_VAR     TACC

%package -n %{pkg_name}
Summary: The package RPM
Group: Development/Tools

%description 
%description -n %{pkg_name}
Tacc base module package

#---------------------------------------
%prep
#---------------------------------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/TACC.lua << 'EOF'
local helpMsg = [[
The %{MODULE_VAR} modulefile defines the default paths and environment
variables needed to use the local software and utilities
available, placing them after the vendor-supplied
paths in PATH and MANPATH.
]]

help(helpMsg)


if (os.getenv("USER") ~= "root") then
  append_path("PATH",  ".")
end

load("intel")
load("impi")
load("git")
load("autotools")
load("python")
load("cmake")
try_load("xalt")

prepend_path("MANPATH","/usr/local/man:/usr/share/man:/usr/X11R6/man:/usr/kerberos/man:/usr/man")

-- Environment change - assume single threaded to fix silly MKL
if (mode() == "load" and os.getenv("OMP_NUM_THREADS") == nil) then
  setenv("OMP_NUM_THREADS","1")
end

--prepend_path{ "PATH", "/opt/apps/tacc/bin", priority=10 }

EOF
  


%files -n %{pkg_name}
%defattr(-,root,install,)
# RPM modulefile contains files within these directories
%{MODULE_DIR}/TACC.lua

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

