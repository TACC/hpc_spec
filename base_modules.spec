
%define name_prefix tacc-comp
%define base_name base-modules

Summary:   TACC Baseline Environment Modules
Name:      %{name_prefix}-%{base_name}
Version:   2.0
Release:   20
License:   GPL
Group:     System Environment/Base
Packager:  mclay@tacc.utexas.edu 
Buildroot: /tmp/rpm/%{base_name}-%{version}-buildroot

%include rpm-dir.inc

%define __spec_install_post /usr/lib/rpm/brp-compress
%define __spec_install_post /usr/lib/rpm/brp-strip


%description 

Modules are really cool.  We like things that are cool. 

%define INSTALL_MODULES   /opt/apps/modulefiles

%prep

%build

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_MODULES}/

cat >  $RPM_BUILD_ROOT/%{INSTALL_MODULES}/TACC <<'EOF'

proc ModulesHelp { } {
puts stderr "The TACC modulefile defines the default paths and environment"
puts stderr "variables needed to use the local software and utilities"
puts stderr "available, placing them after the vendor-supplied"
puts stderr "paths in PATH and MANPATH.:"
}

proc inMPath { path } {
    global env
    if { ! [file exists $path] } {
       return 0
    }
    if {[info exists env(MODULEPATH)]} {
       set separator ":"
       foreach dir [split $env(MODULEPATH) $separator] {
         if { $dir == $path } {
           return 1
         }
       }
    } 
    return 0
}

setenv ESWRAP_LOGIN login0

if [module-info mode load] {
     if { ! [inMPath /opt/modulefiles] } {
        module use   /opt/modulefiles
     }
     if { ! [inMPath /opt/cray/ari/modulefiles] } {
        module use   /opt/cray/ari/modulefiles
     }
     if { [file exists /opt/cray/ari/modulefiles/switch] } {
        module load switch
     }

     #if { [file exists /opt/modulefiles/Base-opts] } {
     #   module load Base-opts
     #}

     if { ! [inMPath /opt/cray/craype/default/modulefiles] } {
        module use   /opt/cray/craype/default/modulefiles
     }
     module load craype-network-aries PrgEnv-intel cray-mpich craype-haswell

     #if { [file exists /opt/modulefiles/slurm] } {
     #   module load slurm
     #}
}

if [ module-info mode remove ] {
     module del slurm craype-haswell cray-libsci cray-mpich PrgEnv-intel craype-network-aries 
     #module del Base-opts switch
     module del switch
}
EOF


mkdir  $RPM_BUILD_ROOT/%{INSTALL_MODULES}/.base
cat >  $RPM_BUILD_ROOT/%{INSTALL_MODULES}/.base/PrgEnv-base.lua <<EOF
local name = myModuleName():gsub("PrgEnv%%-","")
local mpath = pathJoin("/opt/apps",name,myModuleVersion())
inherit()
prepend_path("MODULEPATH",mpath)
family("MPI_COMPILER")
EOF

for pe in PrgEnv-gnu PrgEnv-intel PrgEnv-cray; do
   mkdir -p $RPM_BUILD_ROOT/%{INSTALL_MODULES}/$pe
   for v in 5.2.40.lua; do
      ln -s ../.base/PrgEnv-base.lua $RPM_BUILD_ROOT/%{INSTALL_MODULES}/$pe/$v
   done
done


%files
%defattr(-,root,root,)

%{INSTALL_MODULES}

%post
%clean
rm -rf $RPM_BUILD_ROOT
