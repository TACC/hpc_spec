#
# $Id: gsl.spec 496 2014-10-15 2:43:10Z chenk & agomez $
#
# Local TACC Spec file for GSL
#

Summary: GSL Library - TACC Build

%define major_version 1
%define minor_version 16
%define micro_version 0

%define debug_package %{nil}
%define dbg %{nil}

%define pkg_version %{major_version}.%{minor_version}


Name: gsl
Version: %{pkg_version}
#Intel 14
#Release: 2
#Intel 15
Release: 1
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/gsl/
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-buildroot
Packager: TACC - chenk@tacc.utexas.edu

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc

%define PNAME %{NAME}
%define RPM_NAME tacc_%{name}-%{comp_fam_ver}

#Define TWO different install directories
#INSTALL_DIR -> directory for the HOST files
#MIC_INSTALL_DIR ->directory for the MIC files
%define GSL_BASE_DIR    %{APPS}/%{comp_fam_ver}/%{name}/%{pkg_version}
%define INSTALL_DIR     %{GSL_BASE_DIR}/x86_64
%define MIC_INSTALL_DIR %{GSL_BASE_DIR}/k1om


%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define MODULE_VAR GSL

%include rpm-dir.inc

%package -n %{RPM_NAME}
Summary: The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers. 
Group: System Environment/Base

%description
%description -n %{RPM_NAME}

The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers. It is free software under the GNU General Public License.

The library provides a wide range of mathematical routines such as random number generators, special functions and least-squares fitting. There are over 1000 functions in total with an extensive test suite.

The complete range of subject areas covered by the library includes,

Complex Numbers	Roots of Polynomials
Special Functions	Vectors and Matrices
Permutations	Sorting
BLAS Support	Linear Algebra
Eigensystems	Fast Fourier Transforms
Quadrature	Random Numbers
Quasi-Random Sequences	Random Distributions
Statistics	Histograms
N-Tuples	Monte Carlo Integration
Simulated Annealing	Differential Equations
Interpolation	Numerical Differentiation
Chebyshev Approximation	Series Acceleration
Discrete Hankel Transforms	Root-Finding
Minimization	Least-Squares Fitting
Physical Constants	IEEE Floating-Point
Discrete Wavelet Transforms	Basis splines
Unlike the licenses of proprietary numerical libraries the license of GSL does not restrict scientific cooperation. It allows you to share your programs freely with others.

The current version is GSL-1.16. It was released on 19 July 2013. Details of recent changes can be found in the NEWS file. This is a stable release.

GSL can be found in the gsl subdirectory on your nearest GNU mirror http://ftpmirror.gnu.org/gsl/.

Main GNU ftp site: ftp://ftp.gnu.org/gnu/gsl/
For other ways to obtain GSL, please read How to get GNU Software

Installation instructions can be found in the included README and INSTALL files.

Precompiled binary packages are included in most GNU/Linux distributions.

A compiled version of GSL is available as part of Cygwin on Windows (but we recommend using GSL on a free operating system, such as GNU/Linux).


#---------------------------------------

%prep
module purge
#module load TACC
#Delete and recreate the installation directory.
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf $RPM_BUILD_ROOT/%{MIC_INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MIC_INSTALL_DIR}

#---------------------------------------

%setup -q -n %{name}-%{version}

#---------------------------------------

%build
#---------------------------------------

%install

#%include compiler-load.inc
module purge
module load intel

archA=()

if [ "%{comp_mic_support}" == 1 ]; then
  archA+=("k1om")
fi

archA+=("x86_64")

WD=`pwd`
#export ARCH=x86_64
#I need this to build GSL 
#export PATH=$HOME/linux-k1om-4.7/bin/:$PATH

for ARCH in "${archA[@]}"; do

  INSTALL_DIR="%{GSL_BASE_DIR}/$ARCH"
  rm -rf $RPM_BUILD_ROOT/$INSTALL_DIR
  mkdir -p $RPM_BUILD_ROOT/$INSTALL_DIR
  mkdir -p %{INSTALL_DIR}

  mount -t tmpfs tmpfs %{INSTALL_DIR}

  cd $WD
  unset CFLAGS
  unset CPPFLAGS
  export CONFIG_FLAGS=""
  #Different configure depending on the version HOST/MIC
  if [ "$INSTALL_DIR" = "%{MIC_INSTALL_DIR}" ]; then
    export CFLAGS="-std=gnu99 -O3 -mmic -mkl=sequential -vec-report1 -fno-alias -ip -funroll-all-loops -fimf-domain-exclusion=15 -g -DNDEBUG"
    export CPPFLAGS="-std=c++0x -O3 -mmic -mkl=sequential -vec-report1 -fno-alias -ip -funroll-all-loops -fimf-domain-exclusion=15 -g -DNDEBUG"
    export CONFIG_FLAGS="--host=x86_64-k1om-linux"
else
    export CFLAGS="-O3"
    export CPPFLAGS="-O3"
  fi

  ./configure $CONFIG_FLAGS --prefix=$INSTALL_DIR
  make clean
  make -j 12
  make install

  #When using the MIC, mount the folder with tacctmpfs.
  #Then, copy the files from the host to the mic.
  #I DON'T NEED IT HERE, BUT THIS SHOWS HOW TO DO THE TRICK
  #if [ "$INSTALL_DIR" = "%{MIC_INSTALL_DIR}" ]; then
  #  ssh mic0 tacctmpfs -m $INSTALL_DIR
  #  cd $INSTALL_DIR
  #  scp -r * mic0:`pwd`
  #fi
  
  #Now we have the content of INSTALL_DIR synchronized between the HOST and the MIC through tacctmpfs
  
  cp -r $INSTALL_DIR/ $RPM_BUILD_ROOT/$INSTALL_DIR/..

  #Unmount INSTALL_DIR on the MIC
  #if [ "$INSTALL_DIR" = "%{MIC_INSTALL_DIR}" ]; then
  #  ssh mic0 tacctmpfs -u $INSTALL_DIR
  #fi
  #Unmount INSTALL_DIR on the HOST
#  tmpfs -u $INSTALL_DIR
   umount %{INSTALL_DIR}
done

#-----------------
# Modules Section
#-----------------

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_msg=[[
The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively. 

Please compile the source code with the option:

	-I$TACC_%{MODULE_VAR}_INC/gsl -I$TACC_%{MODULE_VAR}_INC  

and add the following to the link step:

	-L$TACC_%{MODULE_VAR}_LIB -lgsl


The GSL module prepends to your PATH for access
to GSL utilities. It also modifies LD_LIBRARY_PATH
]]

local help_msg_mic=[[
-----------------------------
To build a MIC native code:
-----------------------------
The GSL module modifies MIC_LIBRARY_PATH.
It also defines MIC_TACC_%{MODULE_VAR},
MIC_TACC_%{MODULE_VAR}_INC, MIC_TACC_%{MODULE_VAR}_LIB, and MIC_TACC_%{MODULE_VAR}_BIN
for the location of MIC version files of the library.
Compile the source code with the option:
       
         -I$MIC_TACC_%{MODULE_VAR}_INC/gsl -I$MIC_TACC_%{MODULE_VAR}_INC

and add the following to the link step:
        
         -L$MIC_TACC_%{MODULE_VAR}_LIB -lgsl
]]

local help_msg_version = [[
Version %{pkg_version}%{dbg}
]]

%if "%{comp_mic_support}" == "1"
--help(help_msg,help_msg_mic,help_msg_version)
help(help_msg, help_msg_mic, help_msg_version)
%else
--help(help_msg,help_msg_version)
help(help_msg, help_msg_version)
%endif

whatis("Name: gsl")

whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: library, mathematics")
whatis("Keywords: Mathematics, Library")
whatis("Description: provides wide range of mathematical routines such as random number generators, special functions and least-squares fitting.")
whatis("URL: http://www.gnu.org/software/gsl/")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
setenv("MIC_TACC_%{MODULE_VAR}_DEBUG","1")
%endif


-- Create environment variables.
local gsl_dir		= "%{INSTALL_DIR}"

family("gsl")
prepend_path(    "PATH", 		pathJoin(gsl_dir, "bin"))
prepend_path(	 "LD_LIBRARY_PATH",	pathJoin(gsl_dir, "lib"))
setenv(	"TACC_%{MODULE_VAR}_DIR", 	gsl_dir)
setenv(	"TACC_%{MODULE_VAR}_INC",       pathJoin(gsl_dir, "include"))
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(gsl_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",	pathJoin(gsl_dir, "bin"))

%if "%{comp_mic_support}" == "1"

local gsl_micdir	= "%{MIC_INSTALL_DIR}"
prepend_path(  "MIC_LD_LIBRARY_PATH",   pathJoin(gsl_micdir, "lib"))
setenv( "MIC_TACC_%{MODULE_VAR}_DIR",   gsl_micdir)
setenv( "MIC_TACC_%{MODULE_VAR}_INC",   pathJoin(gsl_micdir, "include"))
setenv( "MIC_TACC_%{MODULE_VAR}_LIB",   pathJoin(gsl_micdir, "lib"))
setenv( "MIC_TACC_%{MODULE_VAR}_BIN",   pathJoin(gsl_micdir, "bin"))
add_property("arch","mic")
%endif

EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{RPM_NAME} 

%defattr(-,root,root,-)

%if "%{comp_mic_support}" == "1"
  %{MIC_INSTALL_DIR}
%endif

%{INSTALL_DIR}
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT
