#
# $Id: boost.spec 7993 2015-02-23 11:13:08Z agomez $
#

Summary: boost

%define major_version 1
%define minor_version 55
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

Name: boost
Version: %{pkg_version}
#Intel 13/14
#Release: 5 
#Intel 15
Release: 1 
License: GPLv2
Group: System Environment/Base
Source0: boost_%{major_version}_%{minor_version}_%{micro_version}.tar.gz
#Source1: icu4c-54_1-src.tgz
Source1: icu4c-49_1_2-src.tgz
Packager: TACC - agomez@tacc.utexas.edu

%define debug_package %{nil}
%include rpm-dir.inc
%include compiler-defines.inc

# This is a hack to prevent mpi-defines.inc to complain if mpi is not set.
%define  mpi_fam none
%include mpi-defines.inc

# TACC %defines

%define APPS /opt/apps
%define MODULES modulefiles


%define PNAME               %{name}
%define BOOST_BASE_DIR      %{APPS}/%{comp_fam_ver}/%{PNAME}/%{pkg_version}
%define MODULE_DIR          %{APPS}/%{comp_fam_ver}/%{MODULES}/%{PNAME}
%define RPM_NAME            %{PNAME}-%{comp_fam_ver}
%define BOOST_TYPE          (Serial Version)
%define MODULE_VAR          BOOST

%define INSTALL_DIR         %{BOOST_BASE_DIR}/x86_64
%define MIC_INSTALL_DIR     %{BOOST_BASE_DIR}/k1om

%package -n %{RPM_NAME}

Summary: Boost is a set of libraries which extend the functionality of C++.
Group: System Environment/Base

%description
%description -n %{RPM_NAME}
Boost provides free peer-reviewed portable C++ source libraries.

We emphasize libraries that work well with the C++ Standard
Library. Boost libraries are intended to be widely useful, and usable
across a broad spectrum of applications. The Boost license encourages
both commercial and non-commercial use.

We aim to establish "existing practice" and provide reference
implementations so that Boost libraries are suitable for eventual
standardization. Ten Boost libraries are already included in the C++
Standards Committee's Library Technical Report (TR1) and the C++11 Standard.
More Boost libraries are proposed for standardization in C++17.

# '
%prep
module purge
##
## SETUP (The -n is needed here because boost untars to
## a directory with a different name than the tar file.)
##

%setup  -n boost_%{major_version}_%{minor_version}_%{micro_version}  %{name}-%{version}
# The second call untars the second source, in a subdirectory
# of the first. 
# -b <n> means unpack the nth source *before* changing directories.  
# -a <n> means unpack the nth source *after* changing to the top-level build directory. 
# -T prevents the 'default' source file from re-unpacking.  If you don't have this, the
#    default source will unpack twice... a weird RPMism.
# -D prevents the top-level directory from being deleted before we can get there!
%setup  -n boost_%{major_version}_%{minor_version}_%{micro_version}  -T -D -a 1

%build

%install

%include compiler-load.inc

ICU_MODE=Linux

%if "%{comp_fam}" == "intel"
    CONFIGURE_FLAGS=--with-toolset=intel-linux
    ICU_MODE=Linux/ICC
%endif

archA=()

if [ "%{comp_mic_support}" = 1 ]; then
    archA+=("k1om")
fi

archA+=("x86_64")

for ARCH in "${archA[@]}"; do
    INSTALL_DIR="%{BOOST_BASE_DIR}/$ARCH"
    rm -rf $RPM_BUILD_ROOT/${INSTALL_DIR}
    mkdir -p $RPM_BUILD_ROOT/${INSTALL_DIR} 
    
    rm -rf bin.v2/
    if [ "$ARCH" = "k1om" ]; then
        CONFIGURE_FLAGS=--with-toolset=intel-linux CFLAGS="-mmic" CXXFLAGS="-mmic"
    else
        CONFIGURE_FLAGS=--with-toolset=intel-linux
    fi

    %if "%{comp_fam}" == "gcc"
        CONFIGURE_FLAGS=--with-toolset=gcc
    %endif

#    tacctmpfs -mount ${INSTALL_DIR}

    WD=`pwd`

    %if "%{comp_fam}" == "intel"
        TOOLSET="toolset=intel"
	%if "%{comp_fam_ver}" == "intel15"
            export LD_LIBRARY_PATH=/opt/apps/intel/composer_xe_2015.1.133/compiler/lib/intel64
            source /opt/apps/intel/composer_xe_2015.1.133/bin/compilervars.sh intel64
    	    #export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/apps/gcc/4.9.1/lib/
	%endif
	%if "%{comp_fam_ver}" == "intel14"
            export LD_LIBRARY_PATH=/opt/apps/intel/13/composer_xe_2013.2.146/compiler/lib/intel64
            source /opt/apps/intel/13/composer_xe_2013.2.146/bin/compilervars.sh intel64
	%endif
    %else
        TOOLSET="toolset=gcc"
    %endif

    if [ "$ARCH" = "k1om" ]; then   
        ./bootstrap.sh --prefix=${INSTALL_DIR} ${CONFIGURE_FLAGS} --libdir=/opt/mpss/3.3/sysroots/k1om-mpss-linux/lib64/ 
        LIBS="--with-atomic --with-chrono --with-date_time --with-exception --with-filesystem --with-graph --with-graph_parallel --with-locale --with-log --with-math --with-program_options --with-random --with-signals --with-system --with-test --with-serialization --with-timer --with-wave"
        FLAGS='cxxflags="-mmic" cflags="-mmic" linkflags="-mmic"'
        EXTRA='--disable-icu address-model=64 install'
    else
        #ICU
        FLAGS=" "
        cd icu/source
        ./runConfigureICU  $ICU_MODE --prefix=${INSTALL_DIR}
        make -j 4
        make install

        #Now boost
        cd $WD
        ./bootstrap.sh --prefix=${INSTALL_DIR} ${CONFIGURE_FLAGS}
        EXTRA="address-model=64 install"
        LIBS="--without-python --without-mpi"
    fi

    ./b2 -j 8 --prefix=${INSTALL_DIR} ${FLAGS} ${TOOLSET} ${LIBS} ${EXTRA}

    mkdir -p              $RPM_BUILD_ROOT/${INSTALL_DIR}
    cp -r ${INSTALL_DIR}/ $RPM_BUILD_ROOT/${INSTALL_DIR}/..

    #tacctmpfs -umount ${INSTALL_DIR}
done

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_msg=[[
The boost module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, and TACC_%{MODULE_VAR}_INC for the
location of the boost distribution. Finally, it also modifies
LD_LIBRARY_PATH to add the corresponding folder.

The following Boost libraries are NOT installed:
        - MPI
	- Python

]]

local help_msg_version=[[
Version %{version}
]]

%if "%{comp_mic_support}" == "1"
--help(help_msg, help_mic_msg, help_msg_version)
help(help_msg, help_mic_msg, help_msg_version)
%else
--help(help_msg)
help(help_msg)
%endif

whatis("Name: boost")
whatis("Version: %{version}")
whatis("Category: %{group}")
whatis("Keywords: System, Library, C++")
whatis("URL: http://www.boost.org")
whatis("Description: Boost provides free peer-reviewed portable C++ source libraries %{BOOST_TYPE}.")

local boost_dir     =  "%{INSTALL_DIR}"
local boost_micdir  =  "%{MIC_INSTALL_DIR}"

setenv("TACC_%{MODULE_VAR}_DIR", boost_dir)
setenv("TACC_%{MODULE_VAR}_LIB", pathJoin(boost_dir,"lib"))
setenv("TACC_%{MODULE_VAR}_INC", pathJoin(boost_dir,"include"))
prepend_path("LD_LIBRARY_PATH", pathJoin(boost_dir, "lib"))

%if "%{comp_mic_support}" == "1"
    setenv("MIC_TACC_%{MODULE_VAR}_DIR", boost_micdir)
    setenv("MIC_TACC_%{MODULE_VAR}_LIB", pathJoin(boost_micdir,"lib"))
    setenv("MIC_TACC_%{MODULE_VAR}_INC", pathJoin(boost_micdir,"include"))
    prepend_path("MIC_LD_LIBRARY_PATH", pathJoin(boost_micdir, "lib"))
    add_property("arch","mic")
%endif
EOF


#--------------
# Version file. 
#--------------
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module1.0##################################################
##
## version file for %{name}-%{version}
##

set ModulesVersion "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua


%files -n %{RPM_NAME}
%defattr(-,root,root,-)

%{INSTALL_DIR}

#Only include the mic version if we actually created it
%if "%{comp_mic_support}" == "1"
    %{MIC_INSTALL_DIR}
%endif

%{MODULE_DIR}

%post


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Feb 23 2015 Antonio Gomez <agomez@tacc.utexas.edu> 1.55.0-1
- Initial Wrangler installation
