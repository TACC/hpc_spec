Summary: java64
 
#
#
#

Name: java64
Version: 1.8.0
Release: 2
License: GPL 
Vendor: Oracle
Group: Application
Source: %{name}-%{version}.tar.gz
Packager:  rhuang@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps/
%define MODULES modulefiles


%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}


%description
Setting jdk run time environment 

%prep
##rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
##mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
 
##
## SETUP
##
##setup -n %{name}-%{version}
 
##
## BUILD
##
%build

%install


rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The jdk64/1.8.0 modulefile defines the default paths and environment
variables needed to use the Java 1.8.0 software and utilities
available in /usr/java/latest,placing them before the vendor
-supplied
paths in PATH and MANPATH.:
]]
)

--
-- Create environment variables.
--
-- set variable

local java_home="/usr/java/latest/"
local jre_home="/usr/java/latest/jre"

-- bin or executable
local java_bindir="/usr/java/latest/bin"


--  LD_LIBRARY_PATH
setenv("JAVA_HOME", java_home)
setenv("JAVA_BINDIR",java_bindir)
setenv("JAVA_ROOT", java_home)
setenv("JDK_HOME", java_home)
setenv("SDK_HOME", java_home)
setenv("JRE_HOME", jre_home)

prepend_path("PATH", java_bindir)


EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%files
%defattr(-,root,install)
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
