Summary:    RStudioDesktop is a powerful and productive user interface for R
Name:       RstudioDesktop
Version:    1.1.423 
Release:    1 
License:    AGPL v3
Vendor:     RStudio, Inc
Group:      Applications
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - walling@tacc.utexas.edu

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include system-defines.inc
#%include compiler-defines.inc

%define PNAME RstudioDesktop
%define MODULE_VAR TACC_RSTUDIO
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{version}

%package -n %{PACKAGE_NAME}
Summary: RstudioDesktop
Group:  Applications/Statistics

%description
%description -n %{PACKAGE_NAME} 
RStudio Desktop brings the power and
productivity of the RStudio IDE to server-based
deployments of R.

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# %setup 

%build


%install

%include system-load.inc


# Create temporary directory for the install.  We need this to
mkdir -p             %{INSTALL_DIR}
mount -t tmpfs tmpfs %{INSTALL_DIR}
#tacctmpfs -m %{INSTALL_DIR}

echo "Once more into the breach...."

module purge
module load TACC
module swap intel intel/15.0.3
module load Rstats/3.4.0
 
# Set up src directory
export WD=`pwd`
export SRC_DIR=${WD}/src
mkdir -p ${SRC_DIR}
cd ${SRC_DIR}

# Dependencies

wget https://download1.rstudio.org/rstudio-1.1.423-x86_64.rpm

# Deps
wget https://rpmfind.net/linux/centos/7.4.1708/os/x86_64/Packages/glibc-2.17-196.el7.x86_64.rpm
wget https://rpmfind.net/linux/centos/7.4.1708/os/x86_64/Packages/libstdc++-4.8.5-16.el7.x86_64.rpm
wget https://rpmfind.net/linux/centos/7.4.1708/os/x86_64/Packages/gstreamer-tools-0.10.36-7.el7.x86_64.rpm
wget https://rpmfind.net/linux/centos/7.4.1708/os/x86_64/Packages/gstreamer-0.10.36-7.el7.x86_64.rpm
wget https://rpmfind.net/linux/centos/7.4.1708/os/x86_64/Packages/gstreamer-plugins-base-0.10.36-10.el7.x86_64.rpm
wget https://rpmfind.net/linux/centos/7.4.1708/os/x86_64/Packages/orc-0.4.26-1.el7.x86_64.rpm

rpm2cpio rstudio-1.1.423-x86_64.rpm | cpio -idmv
rpm2cpio glibc-2.17-196.el7.x86_64.rpm | cpio -idmv
rpm2cpio libstdc++-4.8.5-16.el7.x86_64.rpm | cpio -idmv
rpm2cpio gstreamer-tools-0.10.36-7.el7.x86_64.rpm | cpio -idmv
rpm2cpio gstreamer-0.10.36-7.el7.x86_64.rpm | cpio -idmv
rpm2cpio gstreamer-plugins-base-0.10.36-10.el7.x86_64.rpm | cpio -idmv
rpm2cpio orc-0.4.26-1.el7.x86_64.rpm | cpio -idmv

# copy the binaries
cp -fr ./usr/lib/rstudio/* %{INSTALL_DIR}

# create a lib directory
mkdir %{INSTALL_DIR}/lib
mkdir %{INSTALL_DIR}/lib64
#mkdir %{INSTALL_DIR}/bin

# add missing binaries and shared libs to lib directory

# misc libraries
cp ./usr/bin/* %{INSTALL_DIR}/bin/
cp -fr ./usr/lib64/* %{INSTALL_DIR}/lib64/
cp -fr ./usr/lib/* %{INSTALL_DIR}/lib/
#cp -fr ./lib/* %{INSTALL_DIR}/lib/
cp -fr ./lib64/*  %{INSTALL_DIR}/lib64/

#----------------------------------------------------------
# Copy into rpm directory
#----------------------------------------------------------
# Copy from tmpfs to RPM_BUILD_ROOT so that everything is in the right
# place for the rest of the RPM.  Then, unmount the tmpfs.

# test
mkdir -p                 $RPM_BUILD_ROOT/%{INSTALL_DIR}
# check with ls
echo "testing with an ls"
ls $RPM_BUILD_ROOT/%{INSTALL_DIR}

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..


#----------------------------------------------------------
# UNMOUNT THE TEMP FILESYSTEM
#----------------------------------------------------------
umount  %{INSTALL_DIR}
#tacctmpfs -u %{INSTALL_DIR}

#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}


cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
RStudio Desktop provides the leading R GUI to VNC desktop based interactive computing sessions.

Version %{version}
]]
)

whatis("Name: RstudioDesktop")
whatis("Version: %{version}")
whatis("Category: Applications, Statistics, Graphics")
whatis("Keywords: Applications, Statistics, Graphics, Scripting Language")
whatis("URL: https://www.rstudio.com/")
whatis("Description: Powerful IDE for R")

--
-- Create environment variables.
--
local rstudio_dir   = "%{INSTALL_DIR}"
local rstudio_bin   = "%{INSTALL_DIR}/bin"
local rstudio_inc   = "%{INSTALL_DIR}/include"
local rstudio_lib   = "%{INSTALL_DIR}/lib"
local rstudio_lib64 = "%{INSTALL_DIR}/lib64"
local rstudio_man   = "%{INSTALL_DIR}/share/man:%{INSTALL_DIR}/man"

setenv("TACC_RSTUDIO_DESKTOP_DIR", rstudio_dir)
setenv("TACC_RSTUDIO_DESKTOP_BIN", rstudio_bin)
setenv("TACC_RSTUDIO_DESKTOP_LIB", rstudio_lib)

prepend_path("PATH", rstudio_bin)
prepend_path("LD_LIBRARY_PATH", rstudio_lib)
prepend_path("LD_LIBRARY_PATH", rstudio_lib64)
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0####################################################################
##
## Version file for Rstudio version %{version}
##
set ModulesVersion "%version"
EOF

#----------------------------------------------------------
# Lua syntax check 
#----------------------------------------------------------
if [ -f $RPM_BUILD_DIR/SPECS/checkModuleSyntax ]; then
    $RPM_BUILD_DIR/SPECS/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
fi

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files -n %{PACKAGE_NAME} 
%defattr(-,root,install)
%{INSTALL_DIR}
%{MODULE_DIR}

%post -n %{PACKAGE_NAME} 

%clean

