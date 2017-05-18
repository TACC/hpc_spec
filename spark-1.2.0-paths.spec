Summary: :spark-paths
 
#
#
#

Name: spark-paths
Version:1.2.0 
Release: 1
License: Apache License 2.0 
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
Setting spark run time environment

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
Setting spark environment variables
]]
)

--
-- Create environment variables.
--
-- set variable

local spark_home = "/usr/lib/spark"


-- bin or executable

local spark_submit_dir = "/opt/apps/intel15/mvapich2_2_1/big-data-r/3.1.3/r-library/SparkR"

--  LD_LIBRARY_PATH

setenv("SPARK_HOME",spark_home)
setevn("HADOOP_HOME","")

prepend_path("PATH", spark_submit_dir)

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
