
# W. Cyrus Proctor
# 2015-11-20
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i --relocate /tmprpm=/opt/apps Bar-package-1.1-1.x86_64.rpm
# rpm -i --relocate /tmpmod=/opt/apps Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: A Nice little relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name TACC-largemem
%define MODULE_VAR    TACC-largemem

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
# hacked for reasonable name WCP 2015-12-01
Name:      tacc-tacc_env_base_modules-largemem
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   11%{?dist}
License:   GPL
Group:     Module Magic
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the long description for the package RPM...
Welcome to the TACC Module way!

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Welcome to the TACC Module way!

%description
Welcome to the TACC Module way!

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

# Setup modules
# Nothing to do!

# Insert necessary module commands
# None to have!

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================

  # Nothing to see here!

#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local helpMsg = [[
The %{MODULE_VAR} modulefile defines the default paths and environment
variables needed to use the local software and utilities
available, placing them after the vendor-supplied
paths in PATH and MANPATH.
]]

help(helpMsg)


--------------------------------------------------------------------------
-- Define TACC_SYSTEM and TACC_DOMAIN

local host    = capture("hostname -f"):gsub("\n","")
local syshost = host:gsub("%.tacc%.utexas%.edu",""):gsub("^[^.]*%.","")
local domain  = syshost

if (domain:find("^ls%d$") or domain:find("^nid"))then
   domain = "ls5"
end

if (mode() == "load") then
  -- Extract nid number if it exists
  local i,j, num = syshost:find("^nid(%d+)")
  if (i) then
     num = tonumber(num)
     -- Aries network (cray) computes are all nid numbers less than 2000 on LS5 
     if (num < 2000) then
        LmodMessage("\n=================================================================================")
        LmodMessage("WARNING:                                                                 :WARNING")
        LmodMessage("WARNING:        You have loaded the \"TACC-largemem\" module.              :WARNING")
        LmodMessage("WARNING:                                                                 :WARNING")
        LmodMessage("WARNING: This module is intended for compiling and running on Lonestar 5 :WARNING")
        LmodMessage("WARNING:               large memory compute nodes only.                  :WARNING")
        LmodMessage("WARNING:                                                                 :WARNING")
        LmodMessage("WARNING:     You are currently not on a large memory compute node.       :WARNING")
        LmodMessage("WARNING:                                                                 :WARNING")
        LmodMessage("WARNING:           Please use \"module load TACC\" instead.                :WARNING")
        LmodMessage("WARNING:                                                                 :WARNING")
        LmodMessage("WARNING:                         Navigate to:                            :WARNING")
        LmodMessage("WARNING:     https://portal.tacc.utexas.edu/user-guides/lonestar5        :WARNING")
        LmodMessage("WARNING:                      for more information.                      :WARNING")
        LmodMessage("WARNING:                                                                 :WARNING")
        LmodMessage("WARNING:                This message is worth repeating.                 :WARNING")
        LmodMessage("WARNING:                                                                 :WARNING")
        LmodMessage("=================================================================================\n")
     end
  -- else
  --   LmodMessage("\n========================================================================")
  --   LmodMessage("                                                                        ")
  --   LmodMessage("            You have loaded the \"TACC-largemem\" module.                 ")
  --   LmodMessage("                                                                        ")
  --   LmodMessage("     This module is intended for compiling and running on Lonestar 5    ")
  --   LmodMessage("                   large memory compute nodes only.                     ")
  --   LmodMessage("                                                                        ")
  --   LmodMessage("========================================================================\n")
  end
end

setenv(         "TACC_SYSTEM",  domain)
setenv(         "TACC_DOMAIN",  domain)

if (os.getenv("USER") ~= "root") then
  append_path("PATH",  ".")
end

load("intel")
load("mvapich2-largemem")
load("git")
load("autotools")
load("python2")
load("cmake")

setenv("APPS","/opt/apps")
prepend_path("MANPATH","/usr/local/man:/usr/share/man:/usr/X11R6/man:/usr/kerberos/man:/usr/man")

-- Environment change - assume single threaded to fix silly MKL
if (mode() == "load" and os.getenv("OMP_NUM_THREADS") == nil) then
  setenv("OMP_NUM_THREADS","1")
end


-- Create slurm environment variables.
local base_dir           = "/opt/slurm/default"

prepend_path( "PATH"            , pathJoin( base_dir, "bin")      )
-- append_path("LD_LIBRARY_PATH" , pathJoin(base_dir, "lib")       )
prepend_path("MANPATH"         , pathJoin(base_dir, "share/man") )
prepend_path("MANPATH"         , "/usr/share/man"                )
prepend_path("PERL5LIB"        , pathJoin(base_dir,"lib/perl5/site_perl/5.10.0/x86_64-linux-thread-multi"))

setenv( "TACC_SLURM_DIR" ,                base_dir)
setenv( "TACC_SLURM_INC" ,       pathJoin(base_dir, "include"))
setenv( "TACC_SLURM_LIB" ,       pathJoin(base_dir, "lib"))
setenv( "TACC_SLURM_BIN" ,       pathJoin(base_dir, "bin"))
setenv( "TACC_SLURM_CONF",       "/etc/opt/slurm/slurm_LG.conf")
setenv( "TACC_SHOWQ_CONF",      "/opt/apps/tacc/bin/showq_LG.conf")
setenv( "SLURM_CONF"     ,       "/etc/opt/slurm/slurm_LG.conf")
setenv( "SQUEUE_FORMAT"  ,       "%.18i %.15P %.8j %.8u %.2t %.10M %.6D %R")

-- "Wimmy Wham Wham Wozzle!" -- Slurms MacKenzie

-- prepend_path{ "PATH", "/opt/apps/tacc/bin", priority=10 }

family("TACC")


EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
  ####%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile 
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT

