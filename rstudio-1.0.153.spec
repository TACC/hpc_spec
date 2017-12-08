Summary:    RStudio is a powerful and productive user interface for R
Name:       Rstudio-server
Version:    1.0.153 
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
%include compiler-defines.inc

%define PNAME Rstudio
%define MODULE_VAR TACC_RSTUDIO
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR %{APPS}/%{MODULES}/%{PNAME}
%define PACKAGE_NAME %{name}-%{version}

%package -n %{PACKAGE_NAME}
Summary: Rstudio server
Group:  Applications/Statistics

%description
%description -n %{PACKAGE_NAME} 
RStudio Server enables you to provide a browser
based interface to a version of R running on a
remote Linux server, bringing the power and
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
#mkdir -p             %{INSTALL_DIR}
#mount -t tmpfs tmpfs %{INSTALL_DIR}
tacctmpfs -m %{INSTALL_DIR}

echo "Once more into the breach...."

module purge
module load TACC
 
# Set up src directory
export WD=`pwd`
export SRC_DIR=${WD}/src
mkdir -p ${SRC_DIR}
cd ${SRC_DIR}

# get the rstudio rpm
wget "http://download2.rstudio.org/rstudio-server-rhel-1.0.153-x86_64.rpm"
# get the R-core rpm, does not matter which one
# since it is opened but never used. 
#wget "https://dl.fedoraproject.org/pub/epel/7/x86_64/r/R-core-3.3.3-1.el7.x86_64.rpm"
wget https://dl.fedoraproject.org/pub/epel/7/x86_64/r/R-core-3.4.1-1.el7.x86_64.rpm

# we also need libicu
wget "http://mirror.centos.org/centos/7/os/x86_64/Packages/libicu-50.1.2-15.el7.x86_64.rpm"

rpm2cpio rstudio-server-rhel-1.0.153-x86_64.rpm | cpio -idmv
rpm2cpio R-core-3.4.1-1.el7.x86_64.rpm | cpio -idmv
rpm2cpio libicu-50.1.2-15.el7.x86_64.rpm | cpio -idmv

# copy the binaries
cp -fr ./usr/lib/rstudio-server/* %{INSTALL_DIR}

# create a lib directory
mkdir %{INSTALL_DIR}/lib
# add missing shared libs to lib directory

# misc libraries
cp ./usr/lib64/R/lib/libR.so %{INSTALL_DIR}/lib/
cp ./usr/lib64/R/lib/libRblas.so %{INSTALL_DIR}/lib/
cp ./usr/lib64/R/lib/libRlapack.so %{INSTALL_DIR}/lib/
cp ./usr/lib64/libicu* %{INSTALL_DIR}/lib/

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
#umount  %{INSTALL_DIR}
tacctmpfs -u %{INSTALL_DIR}

#----------------------------------------------------------
# Create the module file
#----------------------------------------------------------
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
RStudio Server enables you to provide a browser based
interface to a version of R running on a remote Linux
server, bringing the power and productivity of the
RStudio IDE to server-based deployments of R.

Do not run rstudio on the login node, please use ssh port
forwarding. Or the sample job submission script here:
/share/doc/slurm/rstudio.slurm

Version %{version}
]]
)

whatis("Name: Rstudio")
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
local rstudio_man   = "%{INSTALL_DIR}/share/man:%{INSTALL_DIR}/man"

setenv("TACC_RSTUDIO_DIR", rstudio_dir)
setenv("TACC_RSTUDIO_BIN", rstudio_bin)
setenv("TACC_RSTUDIO_LIB", rstudio_lib)

append_path("PATH", rstudio_bin)
append_path("LD_LIBRARY_PATH", rstudio_lib)
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


