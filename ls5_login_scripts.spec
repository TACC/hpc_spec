
%define name_prefix tacc-comp
%define base_name ls5_login_scripts

Summary:   Standard LS5 TACC Login scripts
Name:      %{name_prefix}-%{base_name}
Version:   1.0
Release:   3
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
               profile.d/zzz00_lmod.sh
               profile.d/zzz84_tacc.sh
               profile.d/zzz90_login_modules.sh
"

#rm -rf $RPM_BUILD_ROOT/usr/local/bin          $RPM_BUILD_ROOT/usr/local/etc/
#mkdir -p                                      $RPM_BUILD_ROOT/usr/local/bin
#find fsMounted workdir | cpio -pduv --owner=build: $RPM_BUILD_ROOT/usr/local/bin/


find ./profile.d $PROFILE_D_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT%{PROFILE_D_PATH}/..
#rm $RPM_BUILD_ROOT%{PROFILE_D_PATH}/record_module_use.*.fini

#
#  The new shells all look in /etc/tacc/ for their startup scripts
#

#SHELL_STARTUP_FILES="
#         bash_logout
#         bashrc
#         profile
#         csh.login
#         csh.cshrc
#         csh.logout
#         tacc_functions
#         ksh.kshrc
#"

SHELL_STARTUP_FILES="
         bash.bashrc
         profile
         tacc_functions
"

find $SHELL_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/etc/tacc

#ZSH_STARTUP_FILES="
#         zsh/zlogin
#         zsh/zlogout
#         zsh/zprofile
#         zsh/zshenv
#         zsh/zshrc
#"
#
#find $ZSH_STARTUP_FILES | cpio -pduv --owner=build: $RPM_BUILD_ROOT/etc/tacc


###%build

MPATH="/opt/apps/modulefiles /opt/cray/modulefiles /opt/cray/ari/modulefiles  /opt/cray/craype/default/modulefiles /opt/modulefiles"

#MODULEPATH="/opt/apps/xsede/modulefiles /opt/apps/modulefiles /opt/modulefiles"

for i in $RPM_BUILD_ROOT/etc/profile.d/zzz00_lmod.sh; do
  mv ${i} ${i}.tmp
  sed -e "s|@modulepath@|$MPATH|g" ${i}.tmp > ${i}
  rm ${i}.tmp
done



%files -n %{name}-compute
%defattr(755,root,root,)
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/zzz00_lmod.sh
%{PROFILE_D_PATH}/zzz84_tacc.sh
%{PROFILE_D_PATH}/zzz90_login_modules.sh
/etc/tacc/bash.bashrc
/etc/tacc/profile
/etc/tacc/tacc_functions

%files -n %{name}-login
%defattr(755,root,root,)
%{PROFILE_D_PATH}/00_shell_startup.SH
%{PROFILE_D_PATH}/zzz00_lmod.sh
%{PROFILE_D_PATH}/zzz84_tacc.sh
%{PROFILE_D_PATH}/zzz90_login_modules.sh
/etc/tacc/bash.bashrc
/etc/tacc/profile
/etc/tacc/tacc_functions

%clean
rm -rf $RPM_BUILD_ROOT
