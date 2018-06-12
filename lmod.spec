#
# $Id: lmod.spec 1934 2013-10-12 14:10:48Z karl $
#
%define name_prefix tacc
%define base_name lmod

Prefix:    /opt/apps
Summary:   lmod: Lua based Modules
Name:      %{name_prefix}-%{base_name}
Version:   7.7.32
Release:   1
License:   MIT
Vendor:    Robert McLay
Group:     System Environment/Base
Source:    Lmod-%{version}.tar.bz2
Packager:  TACC - mclay@tacc.utexas.edu
Buildroot: /var/tmp/%{base_name}-%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define APPS           /opt/apps
%define PKG_BASE       /opt/apps/%{base_name}
%define INSTALL_DIR    %{PKG_BASE}/%{version}
%define GENERIC_IDIR   %{PKG_BASE}/lmod
%define MODULES        tools/modulefiles
%define MODULE_DIR     %{APPS}/%{MODULES}/lmod
%define MODULE_DIR_ST  %{APPS}/%{MODULES}/settarg
%define ZSH_SITE_FUNC  /opt/apps/zsh/site-functions

%description

Lua Based Modules

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR} $RPM_BUILD_ROOT/%{ZSH_SITE_FUNC}

##
## SETUP
##

%setup -n Lmod-%{version}

##
## BUILD
##

%build

%install

myhost=$(hostname -f)
myhost=${myhost%.tacc.utexas.edu}
first=${myhost%%.*}
SYSHOST=${myhost#*.}

if [ "$SYSHOST" = "ls5" ]; then
EXTRA="--with-tmodPathRule=yes --with-syshost=ls5 --with-siteName=TACC --with-silentShellDebugging=yes"
CACHE_DIR="--with-spiderCacheDescript=cacheDescript.txt"

cat > cacheDescript.txt << EOF
/home1/moduleData/cacheDir/tacc:/home1/moduleData/cacheDir/tacc_cache_timestamp.txt
EOF
fi



# Lmod needs lua but should not require that a working module
# system be in place to install lmod.  So we search for lua
# the old fashion way

for i in /opt/apps/lua/lua/bin /usr/bin /usr/local/bin /opt/local/bin ; do
  if [ -x $i/lua ]; then
    luaPath=$i
    break
  fi
done
PATH=$luaPath:$PATH

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR} $RPM_BUILD_ROOT/%{ZSH_SITE_FUNC}

./configure --prefix=%{APPS} $CACHE_DIR --with-settarg=FULL $EXTRA
make DESTDIR=$RPM_BUILD_ROOT install
cp contrib/TACC/*.lua $RPM_BUILD_ROOT/%{INSTALL_DIR}/libexec
sed -e '/^scDescriptT = {/,/^}/d' < $RPM_BUILD_ROOT/%{INSTALL_DIR}/init/lmodrc.lua > $RPM_BUILD_ROOT/%{INSTALL_DIR}/init/lmodrc_cray_world.lua

rm $RPM_BUILD_ROOT/%{INSTALL_DIR}/../lmod

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
-- -*- lua -*-
help(
[[
This module is for Lmod.  Normal user will probably not need to
load this module.  It is only required if one is using the tools
that are part of Lmod.

Version %{version}
]])

local version = "%{version}"
whatis("Name: Lmod")
whatis("Version: " .. version)
whatis("Category: System Software")
whatis("Keywords: System, Utility, Tools")
whatis("Description: An environment module system")
whatis("URL: http://www.tacc.utexas.edu/tacc-projects/lmod")

prepend_path( "PATH",            "%{GENERIC_IDIR}/libexec" )
EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{base_name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR_ST}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR_ST}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR_ST}/%{version}.lua << 'EOF'
-- -*- lua -*-
help(
[[
The settarg module dynamically and automatically updates "$TARG" and a
host of other environment variables. These new environment variables
encapsulate the state of the modules loaded.

For example, if you have the settarg module and gcc/4.7.1 module loaded
then the following variables are defined in your environment:

TARG=OBJ/_x86_64_06_2d_gcc-4.7.1
TARG_COMPILER=gcc-4.7.1
TARG_COMPILER_FAMILY=gcc
TARG_MACH=x86_64_06_2d
TARG_SUMMARY=x86_64_06_2d_gcc-4.7.1

If you change your compiler to intel/13.1.0, these variables change to:

TARG=OBJ/_x86_64_06_2d_intel-13.1.0
TARG_COMPILER=intel-13.1.0
TARG_COMPILER_FAMILY=intel
TARG_MACH=x86_64_06_2d
TARG_SUMMARY=x86_64_06_2d_intel-13.1.0

If you then load mvapich2/1.9a2 module the following variables automatically
change to:

TARG=OBJ/_x86_64_06_2d_intel-13.1.0_mvapich2-1.9a2
TARG_COMPILER=intel-13.1.0
TARG_COMPILER_FAMILY=intel
TARG_MACH=x86_64_06_2d
TARG_MPI=mvapich2-1.9a2
TARG_MPI_FAMILY=mvapich2
TARG_SUMMARY=x86_64_06_2d_intel-13.1.0_mvapich2-1.9a2

You also get some TARG_* variables that always available, independent
of what modules you have loaded:

TARG_MACH=x86_64_06_2d
TARG_MACH_DESCRIPT=Intel(R) Xeon(R) CPU E5-2680 0 @ 2.70GHz
TARG_HOST=stampede
TARG_OS=Linux-2.6.32-358.el6.x86_64
TARG_OS_FAMILY=Linux

One way that these variables can be used is part of a build system where
the executables and object files are placed in $TARG.  You can also use
$TARG_COMPILER_FAMILY to know which compiler you are using so that you
can set the appropriate compiler flags.

Settarg can do more.  Please see the Lmod website for more details.

Version %{version}
]])

local version = "%{version}"
whatis("Name: Settarg")
whatis("Version: " .. version)
whatis("Category: System Software")
whatis("Keywords: System, Utility, Tools")
whatis("Description: A dynamic environment system based on Lmod")
whatis("URL: http://www.tacc.utexas.edu/tacc-projects/lmod")

prepend_path( "PATH", "%{GENERIC_IDIR}/settarg" )

local base        = "%{GENERIC_IDIR}/settarg"
local settarg_cmd = pathJoin(base, "settarg_cmd")

prepend_path("PATH",base)
pushenv("LMOD_SETTARG_CMD", settarg_cmd)
set_shell_function("settarg", 'eval $($LMOD_SETTARG_CMD -s sh "$@")',
		      'eval `$LMOD_SETTARG_CMD  -s csh $*`' )

set_shell_function("gettargdir",  'builtin echo $TARG', 'echo $TARG')

local respect = "true"
setenv("SETTARG_TAG1", "OBJ", respect )
setenv("SETTARG_TAG2", "_"  , respect )

if ((os.getenv("LMOD_FULL_SETTARG_SUPPORT") or "no"):lower() ~= "no") then
set_alias("cdt", "cd $TARG")
set_shell_function("targ",  'builtin echo $TARG', 'echo $TARG')
set_shell_function("dbg",   'settarg "$@" dbg',   'settarg $* dbg')
set_shell_function("empty", 'settarg "$@" empty', 'settarg $* empty')
set_shell_function("opt",   'settarg "$@" opt',   'settarg $* opt')
set_shell_function("mdbg",  'settarg "$@" mdbg',  'settarg $* mdbg')
end

local myShell = myShellName()
local cmd     = "eval `" .. settarg_cmd .. " -s " .. myShell .. " --destroy`"
execute{cmd=cmd, modeA = {"unload"}}
EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR_ST}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{base_name}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

%files
%defattr(-,root,root,)
%{INSTALL_DIR}
%{MODULE_DIR}
%{MODULE_DIR_ST}
%{ZSH_SITE_FUNC}

%post

cd %{PKG_BASE}

if [ -d %{base_name} ]; then
rm -f %{base_name}
fi
ln -s %{version} %{base_name}

%postun

cd %{PKG_BASE}

if [ -h %{base_name} ]; then
  lv=`readlink %{base_name}`
  if [ ! -d $lv ]; then
    rm %{base_name}
  fi
fi

%clean
rm -rf $RPM_BUILD_ROOT
