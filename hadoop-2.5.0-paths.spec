Summary: hadoop-paths
 
#
#
#

Name: hadoop-paths
Version: 2.5.0
Release: 1
License:  Apache License
Vendor: Apache
Group: Big data
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
Setting Hadoop run time environment

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
Setting hadoop environment variables
]]
)

--
-- Create environment variables.
--
-- set variable

local hadoop_cmd = "/usr/bin/hadoop"
local hadoop_streaming = "/usr/lib/hadoop-mapreduce/hadoop-streaming-2.5.0-cdh5.3.0.jar"
local yarn_conf_dir = "/etc/hadoop/conf"
local hadoop_bin = "/usr/lib/hadoop/bin"
local hadoop_libs = "/usr/lib/hadoop:/usr/lib/hadoop/lib:/usr/lib/hadoop-hdfs:/usr/lib/hadoop-mapreduce:/usr/lib/hadoop-yarn:/usr/lib/hadoop/client"

-- bin or executable

--  LD_LIBRARY_PATH

setenv("HADOOP_CMD", hadoop_cmd)
setenv("HADOOP_STREAMING", hadoop_streaming)
setenv("YARN_CONF_DIR",yarn_conf_dir)
setenv("HADOOP_HOME", hadoop_cmd)
setenv("HADOOP_BIN", hadoop_bin)
setenv("HADOOP_LIBS", hadoop_libs)

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
