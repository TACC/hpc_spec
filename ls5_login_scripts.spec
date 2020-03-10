%define name_prefix tacc
%define base_name ls5_login_scripts

Summary:   Standard LS5 TACC Login scripts
Name:      %{name_prefix}-%{base_name}
Version:   2.5
Release:   1
License:   Proprietary
Group:     System Environment/Base
Source0:   %{base_name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{base_name}-%{version}-buildroot
Packager:  TACC - mclay@tacc.utexas.edu, cproctor@tacc.utexas.edu

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
%setup -q -n %{base_name}-%{version}

%build

rm -rf   $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc 
mkdir -p $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc/zsh



%install

PROFILE_D_FILES="
               profile.d/00_shell_startup.SH
               profile.d/00_shell_startup.CSH
               profile.d/zzz00_lmod.csh
               profile.d/zzz00_lmod.sh
               profile.d/zzz85_idev.sh
               profile.d/zzz85_idev.csh
               profile.d/zzz87_tacc_login.csh
               profile.d/zzz87_tacc_login.sh
               profile.d/zzz88_fs_taccinfo.csh
               profile.d/zzz88_fs_taccinfo.sh
               profile.d/zzz89_tacc_tips.csh
               profile.d/zzz89_tacc_tips.sh
               profile.d/zzz90_compute_modules.csh
               profile.d/zzz90_compute_modules.sh
               profile.d/zzz90_login_modules.csh
               profile.d/zzz90_login_modules.sh
               profile.d/zzz91_tracker.csh
               profile.d/zzz91_tracker.sh
"
SCRIPT_FILES="
               scripts/archive
               scripts/check_changedir.pl
               scripts/fsMounted
               scripts/taccinfo
               scripts/workdir
"


find $SCRIPT_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/
mv $RPM_BUILD_ROOT/scripts/* $RPM_BUILD_ROOT/etc/tacc
rmdir $RPM_BUILD_ROOT/scripts

find ./profile.d $PROFILE_D_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT%{PROFILE_D_PATH}/..
find ./.version                   | cpio -pduv --owner=build: $RPM_BUILD_ROOT%{PROFILE_D_PATH}/

SHELL_STARTUP_FILES="
               startup/bash.bashrc
               startup/bash_logout
               startup/csh.login
               startup/csh.logout
               startup/csh.cshrc
               startup/profile
               startup/tacc_functions
"

find $SHELL_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/
mv $RPM_BUILD_ROOT/startup/* $RPM_BUILD_ROOT/etc/tacc
rmdir $RPM_BUILD_ROOT/startup

ZSH_STARTUP_FILES="
               startup/zsh/zlogin
               startup/zsh/zlogout
               startup/zsh/zprofile
               startup/zsh/zshenv
               startup/zsh/zshrc
"

find $ZSH_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/
mv $RPM_BUILD_ROOT/startup/zsh/* $RPM_BUILD_ROOT/etc/tacc/zsh
rm -rf $RPM_BUILD_ROOT/startup

%files -n %{name}-compute
%defattr(755,root,root,)
%{PROFILE_D_PATH}/.version
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/zzz00_lmod.csh
%{PROFILE_D_PATH}/zzz00_lmod.sh
%{PROFILE_D_PATH}/zzz85_idev.csh
%{PROFILE_D_PATH}/zzz85_idev.sh
%{PROFILE_D_PATH}/zzz87_tacc_login.csh
%{PROFILE_D_PATH}/zzz87_tacc_login.sh
%{PROFILE_D_PATH}/zzz88_fs_taccinfo.csh
%{PROFILE_D_PATH}/zzz88_fs_taccinfo.sh
%{PROFILE_D_PATH}/zzz90_compute_modules.csh
%{PROFILE_D_PATH}/zzz90_compute_modules.sh
%{PROFILE_D_PATH}/zzz91_tracker.sh
%{PROFILE_D_PATH}/zzz91_tracker.csh
/etc/tacc/bash.bashrc
/etc/tacc/bash_logout
/etc/tacc/profile
/etc/tacc/csh.cshrc
/etc/tacc/csh.login
/etc/tacc/csh.logout
/etc/tacc/tacc_functions
/etc/tacc/archive
/etc/tacc/check_changedir.pl
/etc/tacc/fsMounted
/etc/tacc/workdir
/etc/tacc/zsh/zlogin
/etc/tacc/zsh/zlogout
/etc/tacc/zsh/zprofile
/etc/tacc/zsh/zshenv
/etc/tacc/zsh/zshrc

%files -n %{name}-login
%defattr(755,root,root,)
%{PROFILE_D_PATH}/.version
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/zzz00_lmod.csh
%{PROFILE_D_PATH}/zzz00_lmod.sh
%{PROFILE_D_PATH}/zzz87_tacc_login.csh
%{PROFILE_D_PATH}/zzz87_tacc_login.sh
%{PROFILE_D_PATH}/zzz88_fs_taccinfo.csh
%{PROFILE_D_PATH}/zzz88_fs_taccinfo.sh
%{PROFILE_D_PATH}/zzz89_tacc_tips.csh
%{PROFILE_D_PATH}/zzz89_tacc_tips.sh
%{PROFILE_D_PATH}/zzz90_login_modules.sh
%{PROFILE_D_PATH}/zzz90_login_modules.csh
%{PROFILE_D_PATH}/zzz91_tracker.sh
%{PROFILE_D_PATH}/zzz91_tracker.csh
/etc/tacc/bash.bashrc
/etc/tacc/bash_logout
/etc/tacc/profile
/etc/tacc/csh.cshrc
/etc/tacc/csh.login
/etc/tacc/csh.logout
/etc/tacc/tacc_functions
/etc/tacc/archive
/etc/tacc/check_changedir.pl
/etc/tacc/fsMounted
/etc/tacc/taccinfo
/etc/tacc/workdir
/etc/tacc/zsh/zlogin
/etc/tacc/zsh/zlogout
/etc/tacc/zsh/zprofile
/etc/tacc/zsh/zshenv
/etc/tacc/zsh/zshrc

%clean
rm -rf $RPM_BUILD_ROOT
