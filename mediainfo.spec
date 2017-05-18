Summary: mediainfo
 
#
#
#

Name: mediainfo
Version:8
Release: 0
License:BSD  
Vendor:Mediainfo
Group: Application
Source: %{name}-%{version}.tar.gz
Packager:  siva@tacc.utexas.edu
Buildroot: /var/tmp/%{name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps/
%define MODULES modulefiles


%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}


%description
Mediainfo is a convenient unified display of the most relevant technical and tag data for video and audio files.
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
MediaInfo is a convenient unified display of the most relevant technical and tag data for video and audio files.
]]
)

--
--





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
