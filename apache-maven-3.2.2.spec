Summary: apache-maven-3.2.2-paths
 
#
#
#

Name: apache-maven
Version: 3.2.2
Release: 1
License: GPL 
Vendor: Apache
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
Setting Apache Maven 3.2.2 run time environment 

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
##
## SETUP
##
##setup -n %{name}-%{version}
 
##
## BUILD
##
%build
cd $RPM_BUILD_ROOT/%{INSTALL_DIR}
wget http://mirror.olnevhost.net/pub/apache/maven/binaries/apache-maven-3.2.2-bin.tar.gz
tar xvf apache-maven-3.2.2-bin.tar.gz
mv apache-maven-3.2.2/* .
rmdir apache-maven-3.2.2
rm apache-maven-3.2.2-bin.tar.gz

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
Setting Apache Maven 3.2.2 environment variables
]]
)



--
-- Create environment variables.
--
-- set variable

local m2_home="%{INSTALL_DIR}"

-- bin or executable

--  LD_LIBRARY_PATH
setenv("M2_HOME", m2_home)

prepend_path("PATH", pathJoin(m2_home,"bin"))


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
%{INSTALL_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
