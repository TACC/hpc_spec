#
# $Id%
#
%define name_prefix tacc
%define base_name base-modules

Summary:   TACC Baseline Environment Modules
Name:      %{name_prefix}-%{base_name}
Version:   2.0
Release:   21
License:   GPL
Group:     System Environment/Base
Packager:  mclay@tacc.utexas.edu 
Buildroot: /tmp/rpm/%{base_name}-%{version}-buildroot

%include rpm-dir.inc

%define __spec_install_post /usr/lib/rpm/brp-compress
%define __spec_install_post /usr/lib/rpm/brp-strip


%description 

Modules are really cool.  We like things that are cool. 

%define INSTALL_MODULES   /opt/apps/cray_world/modulefiles

%prep

%build

%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_MODULES}/

cat >  $RPM_BUILD_ROOT/%{INSTALL_MODULES}/TACC <<'EOF'

#%Module1.0#####################################################################
#
# $Id$
#############################################################################

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
     ### WCP 2015-12-01 Don't load Base-opts if you want typical compute module env
     #if { [file exists /opt/modulefiles/Base-opts] } {
     #   module load Base-opts
     #}

     if { ! [inMPath /opt/cray/craype/default/modulefiles] } {
        module use   /opt/cray/craype/default/modulefiles
     }
     module load craype-network-aries PrgEnv-intel cray-mpich craype-haswell

     ### WCP 2015-12-01 Don't load cray slurm -- see tacc slurm below
     #if { [file exists /opt/modulefiles/slurm] } {
     #   module load slurm
     #}
}

if [ module-info mode remove ] {
     #module del slurm craype-haswell cray-mpich PrgEnv-intel craype-network-aries 
     module del craype-haswell cray-mpich PrgEnv-intel craype-network-aries 
     #module del Base-opts switch
     module del switch
}

### WCP 2015-12-01 Add tacc slurm information instead.
set base_dir "/opt/slurm/15.08.0"
prepend-path PATH            "$base_dir/bin"
prepend-path LD_LIBRARY_PATH "$base_dir/lib"
prepend-path MANPATH         "$base_dir/share/man"
prepend-path MANPATH         "/usr/share/man"
prepend-path PERL5LIB        "$base_dir/lib/perl5/site_perl/5.10.0/x86_64-linux-thread-multi"
setenv SINFO_FORMAT          {%20P %5a %.10l %16F}
setenv SQUEUE_FORMAT         {%.18i %.9P %.9j %.8u %.2t %.10M %.6D %R}
setenv SQUEUE_SORT           {-t,e,S}

setenv TACC_SLURM_DIR        "$base_dir"
setenv TACC_SLURM_INC        "$base_dir/include"
setenv TACC_SLURM_LIB        "$base_dir/lib"
setenv TACC_SLURM_BIN        "$base_dir/bin"

# "Wimmy Wham Wham Wozzle!" -- Slurms MacKenzie

EOF


%files
%defattr(-,root,root,)

%{INSTALL_MODULES}

%post
%clean
rm -rf $RPM_BUILD_ROOT