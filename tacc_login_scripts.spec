#
# $Id: tacc_login_scripts.spec 1934 2013-10-12 14:10:48Z karl $

Summary:   Standard TACC Login scripts for our friendly Linux Clusters.
Name:      tacc_login_scripts
Version:   2.1
Release:   44%{?dist}
License:   Proprietary
Group:     System Environment/Base
Source0:   %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-buildroot
Packager:  TACC - mclay@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc

%define PROFILE_D_PATH /etc/profile.d

%package -n %{name}-login
Summary: Standard TACC Login scripts for our friendly Linux Clusters.
Group: System Environment/Base

%package -n %{name}-compute
Summary: Standard TACC Login scripts for our friendly Linux Clusters (Compute Nodes).
Group: System Environment/Base

%description
%description -n %{name}-login
These are the scripts for login nodes

%description -n %{name}-compute
These are the scripts for login nodes

%prep
%setup -q

%build

rm -rf   $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc 
mkdir -p $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc/zsh


PROFILE_D_FILES="
               profile.d/00_shell_startup.CSH
               profile.d/00_shell_startup.SH
               profile.d/work_archive.csh
               profile.d/work_archive.sh
               profile.d/z00_tacc_login.csh
               profile.d/z00_tacc_login.sh
               profile.d/z01_lmod.csh
               profile.d/z01_lmod.sh
               profile.d/z84_tacc_system_vars.csh
               profile.d/z84_tacc_system_vars.sh
               profile.d/z85_idev.sh
               profile.d/z85_idev.csh
               profile.d/z88_taccinfo.sh
               profile.d/z88_taccinfo.csh
               profile.d/z89_tacctips.sh
               profile.d/z89_tacctips.csh
               profile.d/z90_compute_modules.csh
               profile.d/z90_compute_modules.sh
               profile.d/z90_login_modules.csh
               profile.d/z90_login_modules.sh
"

%install

rm -rf $RPM_BUILD_ROOT/usr/local/bin       	   $RPM_BUILD_ROOT/usr/local/etc/
mkdir -p                                   	   $RPM_BUILD_ROOT/usr/local/bin
find fsMounted workdir | cpio -pduv --owner=build: $RPM_BUILD_ROOT/usr/local/bin/

OLD_TACC_STARTUP_FILES="
       etc/cshrc
       etc/login
       etc/profile
"

mkdir -p                                                 $RPM_BUILD_ROOT/usr/local/etc/
find archive | cpio -pduv --owner=build:                 $RPM_BUILD_ROOT/usr/local/etc/
find $OLD_TACC_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/usr/local

find ./profile.d $PROFILE_D_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT%{PROFILE_D_PATH}/..

#
#  The new shells all look in /etc/tacc/ for their startup scripts
#

SHELL_STARTUP_FILES="
         bash_logout
         bashrc
         profile
         csh.login
         csh.cshrc
         csh.logout
         tacc_functions
         ksh.kshrc
"

find $SHELL_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/etc/tacc

ZSH_STARTUP_FILES="
         zsh/zlogin
         zsh/zlogout
         zsh/zprofile
         zsh/zshenv
         zsh/zshrc
"

find $ZSH_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/etc/tacc


###%build

#Get hostname of build computer:
myhost=$(uname -n)
myhost=${myhost%.tacc.utexas.edu}
first=${myhost%%.*}
SYSHOST=${myhost#*.}
#MODULEPATH="/opt/apps/teragrid/modulefiles /opt/apps/modulefiles /opt/modulefiles"
MODULEPATH="/opt/apps/xsede/modulefiles /opt/apps/modulefiles /opt/modulefiles"

SYSTEM_DIRS="work scratch"
ALIAS_DIRS="work scratch stockyard"

if   [ $SYSHOST = stampede ]; then
  :
elif [ $SYSHOST = ls4 ]; then
  SYSTEM_DIRS="work scratch"
  ALIAS_DIRS="work scratch"
  MODULEPATH="/opt/apps/teragrid/modulefiles /opt/apps/modulefiles /opt/modulefiles"
elif [ $SYSHOST = maverick -o $SYSHOST = wrangler ]; then
  SYSTEM_DIRS="work"
  ALIAS_DIRS="work stockyard"
elif [ $SYSHOST = hikari ]; then
  SYSTEM_DIRS="work"
  ALIAS_DIRS="work stockyard"
  MODULEPATH="/opt/apps/modulefiles /opt/modulefiles"
fi

for i in $RPM_BUILD_ROOT/etc/profile.d/{z*,work_archive}.{sh,csh}; do
  mv ${i} ${i}.tmp
  sed -e "s|@system_dir_create_list@|$ALIAS_DIRS|g"  \
      -e "s|@system_dir_list@|$SYSTEM_DIRS|g"        \
          ${i}.tmp > ${i}
  rm ${i}.tmp
done



for i in $RPM_BUILD_ROOT/etc/profile.d/z01_lmod.{sh,csh}; do
  mv ${i} ${i}.tmp
  sed -e "s|@modulepath@|$MODULEPATH|g" ${i}.tmp > ${i}
  rm ${i}.tmp
done



%files -n %{name}-compute
%defattr(755,root,root,)
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/work_archive.csh
%{PROFILE_D_PATH}/work_archive.sh
%{PROFILE_D_PATH}/z00_tacc_login.csh
%{PROFILE_D_PATH}/z00_tacc_login.sh
%{PROFILE_D_PATH}/z01_lmod.csh
%{PROFILE_D_PATH}/z01_lmod.sh
%{PROFILE_D_PATH}/z84_tacc_system_vars.csh
%{PROFILE_D_PATH}/z84_tacc_system_vars.sh
%{PROFILE_D_PATH}/z85_idev.csh
%{PROFILE_D_PATH}/z85_idev.sh
%{PROFILE_D_PATH}/z90_compute_modules.csh
%{PROFILE_D_PATH}/z90_compute_modules.sh
/etc/tacc/bash_logout
/etc/tacc/bashrc
/etc/tacc/profile
/etc/tacc/csh.login
/etc/tacc/csh.cshrc
/etc/tacc/csh.logout
/etc/tacc/ksh.kshrc
/etc/tacc/tacc_functions
/etc/tacc/zsh
/usr/local/bin/workdir
/usr/local/bin/fsMounted
/usr/local/etc/archive
/usr/local/etc/cshrc
/usr/local/etc/login
/usr/local/etc/profile

%files -n %{name}-login
%defattr(755,root,root,)
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/work_archive.csh
%{PROFILE_D_PATH}/work_archive.sh
%{PROFILE_D_PATH}/z00_tacc_login.csh
%{PROFILE_D_PATH}/z00_tacc_login.sh
%{PROFILE_D_PATH}/z01_lmod.csh
%{PROFILE_D_PATH}/z01_lmod.sh
%{PROFILE_D_PATH}/z84_tacc_system_vars.csh
%{PROFILE_D_PATH}/z84_tacc_system_vars.sh
%{PROFILE_D_PATH}/z88_taccinfo.sh
%{PROFILE_D_PATH}/z88_taccinfo.csh
%{PROFILE_D_PATH}/z89_tacctips.sh
%{PROFILE_D_PATH}/z89_tacctips.csh
%{PROFILE_D_PATH}/z90_login_modules.csh
%{PROFILE_D_PATH}/z90_login_modules.sh
/etc/tacc/bash_logout
/etc/tacc/bashrc
/etc/tacc/profile
/etc/tacc/csh.login
/etc/tacc/csh.cshrc
/etc/tacc/csh.logout
/etc/tacc/ksh.kshrc
/etc/tacc/tacc_functions
/etc/tacc/zsh
/usr/local/bin/workdir
/usr/local/bin/fsMounted
/usr/local/etc/archive
/usr/local/etc/cshrc
/usr/local/etc/login
/usr/local/etc/profile

%clean
rm -rf $RPM_BUILD_ROOT
