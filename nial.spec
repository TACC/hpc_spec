Summary: Test
 
#
#
#

Name: testsoftware
Version: 1.7.0
Release: 1
License: GPL 
Vendor: OpenJDK
Group: Application
Source: %{name}-%{version}.tar.gz
Packager: geek@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps/
%define MODULES modulefiles


%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}


%description
describe abt the software
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
Describe here what should be displayed to user
]]
)

--
-- Create environment variables.
--
-- set variable

local java_home = "/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.75.x86_64/jre"

-- bin or executable
local java_bin="/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.75.x86_64/bin"

--  LD_LIBRARY_PATH
setenv("JAVA_HOME", java_home)

prepend_path("PATH", java_bin)


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
