%define name_prefix tacc
%define base_name ls5_login_scripts

Summary:   Standard LS5 TACC Login scripts
Name:      %{name_prefix}-%{base_name}
Version:   1.0
Release:   26
License:   Proprietary
Group:     System Environment/Base
Source0:   %{base_name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{base_name}-%{version}-buildroot
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
%setup -q -n %{base_name}-%{version}

%build

rm -rf   $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc 
mkdir -p $RPM_BUILD_ROOT%{PROFILE_D_PATH}  $RPM_BUILD_ROOT/etc/tacc/zsh



%install

PROFILE_D_FILES="
               profile.d/00_shell_startup.SH
               profile.d/00_shell_startup.CSH
               profile.d/work_archive.sh
               profile.d/work_archive.csh
               profile.d/zzz00_lmod.csh
               profile.d/zzz00_lmod.sh
               profile.d/zzz85_idev.sh
               profile.d/zzz85_idev.csh
               profile.d/zzz87_tacc_login.csh
               profile.d/zzz87_tacc_login.sh
               profile.d/zzz88_taccinfo.csh
               profile.d/zzz88_taccinfo.sh
               profile.d/zzz89_tacc_tips.csh
               profile.d/zzz89_tacc_tips.sh
               profile.d/zzz90_compute_modules.csh
               profile.d/zzz90_compute_modules.sh
               profile.d/zzz90_login_modules.csh
               profile.d/zzz90_login_modules.sh
"

find taccinfo fsMounted workdir archive | cpio -pduv --owner=build: $RPM_BUILD_ROOT/etc/tacc


find ./profile.d $PROFILE_D_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT%{PROFILE_D_PATH}/..

SHELL_STARTUP_FILES="
         bash.bashrc
         profile
         tacc_functions
         csh.login
         csh.cshrc
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


MPATH_TACC="/opt/apps/modulefiles /opt/apps/tools/modulefiles"
MPATH_CRAY="/opt/apps/cray_world/modulefiles /opt/cray/modulefiles /opt/cray/ari/modulefiles /opt/cray/craype/default/modulefiles /opt/modulefiles /opt/apps/tools/modulefiles"

for i in $RPM_BUILD_ROOT/etc/profile.d/zzz00_lmod.{csh,sh}; do
  mv ${i} ${i}.tmp
  sed -e "s|@modulepath_tacc@|$MPATH_TACC|g" \
      -e "s|@modulepath_cray@|$MPATH_CRAY|g" \
    ${i}.tmp > ${i}
  rm ${i}.tmp
done

myhost=$(uname -n)
myhost=${myhost%.tacc.utexas.edu}
first=${myhost%%.*}
SYSHOST=${myhost#*.}

SYSTEM_DIRS="work scratch opt/apps"
ALIAS_DIRS="work scratch stockyard"

for i in $RPM_BUILD_ROOT/etc/profile.d/{z*,work_archive}.{sh,csh}; do
  mv ${i} ${i}.tmp
  sed -e "s|@system_dir_create_list@|$ALIAS_DIRS|g"  \
      -e "s|@system_dir_list@|$SYSTEM_DIRS|g"        \
          ${i}.tmp > ${i}
  rm ${i}.tmp
done


%files -n %{name}-compute
%defattr(755,root,root,)
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/work_archive.csh
%{PROFILE_D_PATH}/work_archive.sh
%{PROFILE_D_PATH}/zzz00_lmod.csh
%{PROFILE_D_PATH}/zzz00_lmod.sh
%{PROFILE_D_PATH}/zzz85_idev.csh
%{PROFILE_D_PATH}/zzz85_idev.sh
%{PROFILE_D_PATH}/zzz87_tacc_login.csh
%{PROFILE_D_PATH}/zzz87_tacc_login.sh
%{PROFILE_D_PATH}/zzz90_compute_modules.csh
%{PROFILE_D_PATH}/zzz90_compute_modules.sh
/etc/tacc/bash.bashrc
/etc/tacc/profile
/etc/tacc/csh.cshrc
/etc/tacc/csh.login
/etc/tacc/tacc_functions
/etc/tacc/archive
/etc/tacc/fsMounted
/etc/tacc/taccinfo
/etc/tacc/workdir
/etc/tacc/zsh/zlogin
/etc/tacc/zsh/zlogout
/etc/tacc/zsh/zprofile
/etc/tacc/zsh/zshenv
/etc/tacc/zsh/zshrc


%files -n %{name}-login
%defattr(755,root,root,)
%{PROFILE_D_PATH}/00_shell_startup.CSH
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/work_archive.csh
%{PROFILE_D_PATH}/work_archive.sh
%{PROFILE_D_PATH}/zzz00_lmod.csh
%{PROFILE_D_PATH}/zzz00_lmod.sh
%{PROFILE_D_PATH}/zzz87_tacc_login.csh
%{PROFILE_D_PATH}/zzz87_tacc_login.sh
%{PROFILE_D_PATH}/zzz88_taccinfo.csh
%{PROFILE_D_PATH}/zzz88_taccinfo.sh
%{PROFILE_D_PATH}/zzz89_tacc_tips.csh
%{PROFILE_D_PATH}/zzz89_tacc_tips.sh
%{PROFILE_D_PATH}/zzz90_login_modules.sh
%{PROFILE_D_PATH}/zzz90_login_modules.csh
/etc/tacc/bash.bashrc
/etc/tacc/profile
/etc/tacc/csh.cshrc
/etc/tacc/csh.login
/etc/tacc/tacc_functions
/etc/tacc/archive
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
