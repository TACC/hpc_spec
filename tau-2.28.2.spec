## export NO_PACKAGE  # for no package compile

## rpmbuild -bb --clean --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_5' tau-2.28.2spec 2>&1 | tee tau-2.28.2_ic+im_905_r1_a.log
# r=/admin/build/admin/rpms/frontera/RPMS/x86_64
# rpm -hiv --nodeps    $r/tacc-tau-intel19-impi19_0-package-2.28.2-1.el7.x86_64.rpm
# rpm -hiv --nodeps $r/tacc-tau-intel19-impi19_0-modulefile-2.28.2-1.el7.x86_64.rpm

## rpmbuild -bb --clean --define 'is_intel19 1' --define 'is_impi 1' --define 'mpiV 19_5' tau-2.28.spec 2>&1 | tee tau-2.28_intel19_r1_a.log
# r=/admin/build/admin/rpms/frontera/RPMS/x86_64
# rpm -hiv --nodeps $r/tacc-tau-intel19-impi19_0-package-2.28-1.el7.x86_64.rpm
# rpm -hiv --nodeps $r/tacc-tau-intel19-impi19_0-modulefile-2.28-1.el7.x86_64.rpm
#

#  rpm -e   
#  rpm -e   


# Give the package a base name
%define pkg_base_name tau
%define MODULE_VAR    TAU


# Create some macros (spec file variables)
%define major_version 2
%define minor_version 28
%define micro_version 2

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc

%include name-defines-noreloc.inc

Summary:   Spec file for TAU
Name:      %{pkg_name}
Version:   %{pkg_version}
Release:   1%{?dist}
License:   University of Oregon, ZAM, and LANL
Vendor:    Department of Computer Science, Oregon 
Group:     Development/Languages
Source:    %{pkg_base_name}-%{pkg_version}.tgz
Packager:  milfeld@tacc.utexas.edu
URL:       http://www.cs.uoregon.edu/research/tau/

# Needs release value in this include
#include name-defines-noreloc.inc

# Don't strip archives
#https://fedoraproject.org/wiki/Packaging/Guidelines
#http://rpm.org/wiki/Docs#UserDocumentation
# this is suppose to work.
# or %define __spec_install_post /usr/lib/rpm/brp-compress \
#                                /usr/lib/rpm/brp-strip-comment-note \
#                                /usr/lib/rpm/brp-strip %{nil}
#http://www.redhat.com/archives/rpm-list/2001-November/msg00257.html
# rpm --eval %__spec_install_post   (to see defaults)
# The true at the end probably turns them "off":
%define __spec_install_post /usr/lib/rpm/brp-strip-comment-note /bin/true
%define __spec_install_post /usr/lib/rpm/brp-compress /bin/true
%define __spec_install_post /usr/lib/rpm/brp-strip /bin/true


# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

  %define TAU_tag       "-tag=whatever"
  %define TAU_tag       %{nil}

  %define PDT_name      pdtoolkit
  %define PDT_version   3.25
  %define PDT_dir       %{APPS}/%{comp_fam_ver}/%{PDT_name}/%{PDT_version}

  %define TAU_metrics   GET_TIME_OF_DAY:PAPI_TOT_CYC:PAPI_L2_LDM

 #%define TAU_makefile     Makefile.tau-intelmpi-icpc-papi-ompt-mpi-pdt-openmp
 #%define TAU_makefile_omp Makefile.tau-intelomp-icpc-papi-ompt-pdt-openmp
 #                                                                          # intel mpi openmp
  %define TAU_makefile     Makefile.tau-icpc-papi-ompt-tr4-mpi-pdt-openmp
  
#                                               Configure Options
  %define  PREFIX     "-prefix=%{INSTALL_DIR}"
  %define  PDT        "-pdt=%{PDT_dir}"
  #define  ARCH       "-arch=x86_64"

##############

%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
TAU is the Tuning Analysis Utility Framework. It is used to provide extensive
feedback from profiling, which is then used for analysis and optimization.

%package %{MODULEFILE}
Summary: The package MODULE
Group: System Environment/Base
%description modulefile
TAU is the Tuning Analysis Utility Framework. It is used to provide extensive
feedback from profiling, which is then used for analysis and optimization.

%description
TAU is the Tuning Analysis Utility Framework. It is used to provide extensive
feedback from profiling, which is then used for analysis and optimization.

##############

%define verbose
%prep
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

  %if %{?BUILD_PACKAGE}
%setup -n %{pkg_base_name}-%{pkg_version}
  %endif # BUILD_PACKAGE |

  %if %{?BUILD_PACKAGE}
%build
     set +x
     %include system-load.inc
     %include compiler-load.inc
     %include mpi-load.inc
     set -x


     mkdir -p             %{INSTALL_DIR}
     mount -t tmpfs tmpfs %{INSTALL_DIR}

     module load cmake

     module load papi
     %define PAPI_version        ${TACC_PAPI_DIR##*/}
     %define PAPI_dir             $TACC_PAPI_DIR
     %define PAPI_events          $TACC_PAPI_DIR/share/papi/papi_events.csv
     %define PAPI_avail           $TACC_PAPI_DIR/bin/papi_avail
     %define PAPI_component_avail $TACC_PAPI_DIR/bin/papi_component_avail
     %define PAPI                 "-papi=%PAPI_dir"

    #%define TAG       "-tag=whatever"
     %define TAG       %{nil} 

     ./configure %{TAG} %{PREFIX} -c++=mpicxx -cc=mpicc -fortran=mpif90 \
                 %{PDT} %{PAPI}   -ompt=download \
                 -bfd=download -iowrapper -unwind=download -ompt=download
     make clean install -j 10

     %define TAG       %{nil} 

     ./configure %{TAG} %{PREFIX} -c++=icpc   -cc=icc   -fortran=ifort \
                 %{PDT} %{PAPI}   -ompt=download \
                 -bfd=download -iowrapper -unwind=download -ompt=download
     make clean install -j 10

  %endif  #BUILD_PACKAGE |

%install
  %if %{?BUILD_PACKAGE}
#mkdir -p /root/rpmbuild/BUILDROOT/tacc-tau-intel19-impi19_0-2.28-1.el7.x86_64//opt/apps/intel19/impi19_0/tau/2.28
    mkdir -p                  $RPM_BUILD_ROOT/%{INSTALL_DIR}
    cp    -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
    mkdir -p                  $RPM_BUILD_ROOT/%{INSTALL_DIR}/docs
    cp    -rp docs            $RPM_BUILD_ROOT/%{INSTALL_DIR}
    umount                                    %{INSTALL_DIR}
   #rm -rf                                    %{INSTALL_DIR}

  %endif #BUILD_PACKAGE |

###  MODULE
  %if %{?BUILD_MODULEFILE}

    #%include system-load.inc
    #%include compiler-load.inc
    #%include mpi-load.inc

    #module load papi
    #%define PAPI_VER        %( echo ${TACC_PAPI_DIR##*/} )
    #%define PAPI_TOPDIR     %{TACC_PAPI_DIR}
    #%define PAPI_EVENTS     %( echo ${TACC_PAPI_DIR}/share/papi/papi_events.csv )
    %define PAPI_VER        5.7.0
    %define PAPI_TOPDIR     /opt/apps/papi/5.7.0
    %define PAPI_EVENTS     /opt/apps/papi/5.7.0/share/papi/papi_events.csv 

    rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'

-- This module file sets up the environment variables and path for TAU.

local help_message = [[
The tau module defines the following standard environment variables:
TACC_TAU_DIR and TAU, TACC_TAU_BIN, TACC_TAU_LIB, and TACC_TAU_DOC 
TACC_TAU_EXM, TACC_TAU_TOL for the location of the TAU distribution, 
binaries, libraries, documents, examples and tools, respectively.  

It also defines defaults: 
   TAU_PROFILE=1, 
   TAU_MAKEFILE=%{TAU_makefile},
   TAU_METRICS=%{TAU_metrics}.

TAU_MAKEFILE sets the tools (pdt), compilers (intel) and parallel 
paradigm (serial, or mpi and/or openmp) to be used in the instrumentation.

For TAU %{pkg_version} it is only necessary to load up the TAU
%{pkg_version} environment. Advanced users may need to load up
papi/%{PAPI_VER} and pdtoolkit/%{PDT_version} for library and command access.
For normal usage use the defaults: just load up tau, recompile, and run.
See the User Guide and Reference pdf files in the $TACC_TAU_DOC directory. 
Man pages are available for commands (e.g. paraprof, tauf90, etc.),
and the application program interface. 

Load command:

    module load tau

    or

    module load tau/%{pkg_version}

Java is used in the TAU gui, paraprof, and is available in the default
environment.

The TAU makefile is used by the Tau compiler wrappers shown below. 
The full path to this makefile is specified in the TAU_MAKEFILE 
environement variable. It has been set for you.

The makefile is: %{TAU_makefile}, 
and has component names that describe features of the build:

    Intel Compilers (icpc)
    MPI             (mpi)
    OMP             (openmp)
    OpenMP Tool     (ompt)   openmp events
    PAPI            (papi)   now included by default
    PDtoolkit       (pdt)    now included by default

The default TAU Makefile works for pure MPI, pure OpenMP,
and hybrid applications.  For pure OpenMP applications set

     export TAU_SET_NODE=0   #bash shell 

Otherwise you will get a warning to set the variable, and no data.

For advanced users there may be other TAU Makefiles in 

    $TACC_TAU_LIB

which support advanced features.  Most users have no need for these.
See component names.

To compile your code with TAU, use one of the TAU compiler wrappers:

   tau_f90.sh
   tau_cc.sh
   tau_cxx.sh

for constructing an instrumented code (instead of mpif90, mpicc, etc.).

E.g.  tau_f90.sh mpihello.f90, tau_cc.sh mpihello.c, etc.

These may also be used in makefiles, using macro definitions:

E.g.  F90=tau_f90.sh, CC=tau_cc.sh, Cxx=tau_cxx.sh.

-- To enable callpath information collection set TAU_CALLPATH to 1.
-- To enable trace collection set the environmental variable TAU_TRACE to 1.

Version %{pkg_version}

]]

help(help_message,"\n")

whatis("Name: Tuning Analysis Utilities ")
whatis("Version: %{pkg_version}")
whatis("Category: library, profiling and optimization")
whatis("System: Profiling, Tools")
whatis("URL: http://www.cs.uoregon.edu/research/tau/home.php")
whatis("Description: Framework for Application profiling and optimization")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

--#
--# Create environment variables.
--#
local             tau_dir        =  "%{INSTALL_DIR}"
local             tau_bin        =  "%{INSTALL_DIR}/x86_64/bin"
local             tau_lib        =  "%{INSTALL_DIR}/x86_64/lib"

prepend_path(    "PATH"           , tau_bin                 )
prepend_path(    "LD_LIBRARY_PATH", tau_lib                 )
prepend_path(    "MANPATH"        , pathJoin(tau_dir,"man") )

prepend_path(    "LD_LIBRARY_PATH", "%{PAPI_TOPDIR}/lib"    )
prepend_path(    "MANPATH"        , "%{PAPI_TOPDIR}/man"    )

setenv(           "TACC_TAU_DIR",            tau_dir        )
setenv(           "TACC_TAU_BIN",            tau_bin        )
setenv(           "TACC_TAU_LIB",            tau_lib        )
setenv(           "TACC_TAU_INC",   pathJoin(tau_dir,"include"))
setenv(           "TACC_TAU_DOC",   pathJoin(tau_dir,"docs"))
setenv(           "TACC_TAU_EXM",   pathJoin(tau_dir,"examples"))
setenv(           "TACC_TAU_TOL",   pathJoin(tau_dir,"tools"))
setenv(           "TACC_TAU_MAN",   pathJoin(tau_dir,"man"))
setenv(                "TAU",                tau_lib        )
setenv(           "TAU_MAKEFILE", pathJoin(tau_lib,"%{TAU_makefile}") )
setenv("PAPI_PERFMON_EVENT_FILE",   "%{PAPI_EVENTS}"        )
setenv(            "TAU_METRICS",   "%{TAU_metrics}"        )
setenv(            "TAU_PROFILE",            "1"            )
setenv(            "LIBGL_ALWAYS_INDIRECT",  "1"            )

-- setenv(              "TAU_TRACE",            "0"            )
-- setenv(           "TAU_CALLPATH",            "0"            )

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF


    # Check the syntax of the generated lua modulefile
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

  %endif  # BUILD_MODULEFILE |
#### END MODULE

%if %{?BUILD_PACKAGE}
%files package
   #defattr(-,root,install)
   %defattr(755,root,install)
   %{INSTALL_DIR}
%endif #BUILD_PACKAGE |

%if %{?BUILD_MODULEFILE}
%files modulefile
   %defattr(-,root,install,)
   %{MODULE_DIR}
%endif #BUILD_MODULEFILE |


%clean
rm -rf $RPM_BUILD_ROOT

#rm -rf $RPM_BUILD_DIR/%{name}-%{version}
# http://www.rpm.org/max-rpm/s1-rpm-inside-scripts.html
#http://wiki.mandriva.com/en/Mandriva_RPM_HOWTO
