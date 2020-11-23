#
# $Id: tacc_login_scripts.spec 1934 2013-10-12 14:10:48Z karl $

Summary:   Standard TACC Login scripts for our friendly Linux Clusters.
Name:      tacc_login_scripts
Version:   2.14
Release:   1%{?dist}
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
These are the scripts for compute nodes

%prep
%setup -q

%build

%install

PROFILE_D_FILES="
               profile.d/00_shell_startup.CSH
               profile.d/00_shell_startup.SH
               profile.d/z00_tacc_login.csh
               profile.d/z00_tacc_login.sh
               profile.d/z01_lmod.csh
               profile.d/z01_lmod.sh
               profile.d/z84_tacc_system_vars.csh
               profile.d/z84_tacc_system_vars.sh
               profile.d/z85_idev.sh
               profile.d/z85_idev.csh
               profile.d/z87_tacc_login.csh
               profile.d/z87_tacc_login.sh
               profile.d/z88_fs_taccinfo.sh
               profile.d/z88_fs_taccinfo.csh
               profile.d/z89_tacctips.sh
               profile.d/z89_tacctips.csh
               profile.d/z90_compute_modules.csh
               profile.d/z90_compute_modules.sh
               profile.d/z90_login_modules.csh
               profile.d/z90_login_modules.sh
"

SCRIPT_FILES="
               scripts/archive
               scripts/check_changedir.pl
               scripts/fsMounted
               scripts/available_fs
               scripts/workdir
"
rm -rf   $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc 
mkdir -p $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc/zsh

rm -rf $RPM_BUILD_ROOT/usr/local/bin       	   $RPM_BUILD_ROOT/usr/local/etc/
mkdir -p                                   	   $RPM_BUILD_ROOT/usr/local/bin
mkdir -p                                           $RPM_BUILD_ROOT/usr/local/etc/
find $SCRIPT_FILES | cpio -pduv --owner=build:     $RPM_BUILD_ROOT
mv    $RPM_BUILD_ROOT/scripts/archive              $RPM_BUILD_ROOT/usr/local/etc/
mv    $RPM_BUILD_ROOT/scripts/*                    $RPM_BUILD_ROOT/usr/local/bin
rmdir $RPM_BUILD_ROOT/scripts

OLD_TACC_STARTUP_FILES="
       etc/cshrc
       etc/login
       etc/profile
"


find $OLD_TACC_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/usr/local

find ./profile.d $PROFILE_D_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT%{PROFILE_D_PATH}/..
find ./.version                   | cpio -pduv --owner=build: $RPM_BUILD_ROOT%{PROFILE_D_PATH}/

#
#  The new shells all look in /etc/tacc/ for their startup scripts
#

SHELL_STARTUP_FILES="
         startup/bash_logout
         startup/bashrc
         startup/profile
         startup/csh.login
         startup/csh.cshrc
         startup/csh.logout
         startup/tacc_functions
         startup/ksh.kshrc
"

find $SHELL_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/
mv $RPM_BUILD_ROOT/startup/* $RPM_BUILD_ROOT/etc/tacc/
rmdir $RPM_BUILD_ROOT/startup

ZSH_STARTUP_FILES="
         startup/zsh/zlogin
         startup/zsh/zlogout
         startup/zsh/zprofile
         startup/zsh/zshenv
         startup/zsh/zshrc
"

find $ZSH_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/
mv     $RPM_BUILD_ROOT/startup/zsh/*                $RPM_BUILD_ROOT/etc/tacc/zsh
rm -rf $RPM_BUILD_ROOT/startup


###%build

%files -n %{name}-compute
%defattr(755,root,root,)
%{PROFILE_D_PATH}/.version
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/z00_tacc_login.csh
%{PROFILE_D_PATH}/z00_tacc_login.sh
%{PROFILE_D_PATH}/z01_lmod.csh
%{PROFILE_D_PATH}/z01_lmod.sh
%{PROFILE_D_PATH}/z84_tacc_system_vars.csh
%{PROFILE_D_PATH}/z84_tacc_system_vars.sh
%{PROFILE_D_PATH}/z85_idev.csh
%{PROFILE_D_PATH}/z85_idev.sh
%{PROFILE_D_PATH}/z88_fs_taccinfo.csh
%{PROFILE_D_PATH}/z88_fs_taccinfo.sh
%{PROFILE_D_PATH}/z90_compute_modules.csh
%{PROFILE_D_PATH}/z90_compute_modules.sh
/etc/tacc/bash_logout
/etc/tacc/bashrc
/etc/tacc/csh.cshrc
/etc/tacc/csh.login
/etc/tacc/csh.logout
/etc/tacc/ksh.kshrc
/etc/tacc/profile
/etc/tacc/tacc_functions
/etc/tacc/zsh
/usr/local/bin/available_fs
/usr/local/bin/check_changedir.pl
/usr/local/bin/fsMounted
/usr/local/bin/workdir
/usr/local/etc/archive
/usr/local/etc/cshrc
/usr/local/etc/login
/usr/local/etc/profile

%files -n %{name}-login
%defattr(755,root,root,)
%{PROFILE_D_PATH}/.version
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/z00_tacc_login.csh
%{PROFILE_D_PATH}/z00_tacc_login.sh
%{PROFILE_D_PATH}/z01_lmod.csh
%{PROFILE_D_PATH}/z01_lmod.sh
%{PROFILE_D_PATH}/z84_tacc_system_vars.csh
%{PROFILE_D_PATH}/z84_tacc_system_vars.sh
%{PROFILE_D_PATH}/z88_fs_taccinfo.sh
%{PROFILE_D_PATH}/z88_fs_taccinfo.csh
%{PROFILE_D_PATH}/z89_tacctips.sh
%{PROFILE_D_PATH}/z89_tacctips.csh
%{PROFILE_D_PATH}/z90_login_modules.csh
%{PROFILE_D_PATH}/z90_login_modules.sh
/etc/tacc/bash_logout
/etc/tacc/bashrc
/etc/tacc/csh.cshrc
/etc/tacc/csh.login
/etc/tacc/csh.logout
/etc/tacc/ksh.kshrc
/etc/tacc/profile
/etc/tacc/tacc_functions
/etc/tacc/zsh
/usr/local/bin/available_fs
/usr/local/bin/check_changedir.pl
/usr/local/bin/fsMounted
/usr/local/bin/workdir
/usr/local/etc/archive
/usr/local/etc/cshrc
/usr/local/etc/login
/usr/local/etc/profile

%clean
rm -rf $RPM_BUILD_ROOT
