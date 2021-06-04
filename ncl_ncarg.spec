#
# Spec file for NCAR Graphics
# $Id: ncarg-6.3.0.spec
Summary: NCAR Languange and NCAR Graphics
Name: ncl_ncarg
Version: 6.6.2
Release: 1%{?dist}
License: http://www.ncl.ucar.edu/Download/NCL_binary_license.shtml
Group: applications/io
Source: ncl_ncarg-6.6.2-CentOS7.6_64bit_nodap_gnu485.tar.gz
URL: http://www.ncl.ucar.edu/Download/
Distribution: Centos 7
Vendor: Computational & Information Systems Laboratory, National Center for Atmospheric Research
Packager: TACC - cazes@tacc.utexas.edu
%include rpm-dir.inc

BuildRoot: /tmp/%{name}-%{version}-buildroot

%define APPS /opt/apps
%define MODULES modulefiles

%define comp_fam error

# Note: this is a binary distribution and there is nothing to compile!

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}


%description 
NCAR Command Language (NCL) is an interpreted language designed for
scientific data analysis and visualization
Includes NCAR Graphics functionality
Supports netcdf3/4, GRIB1/2, HDF-SDS, HDF4-EOS, binary, shapefiles, and 
ascii
* a library containing over two dozen Fortran/C utilities for drawing contours, 
  maps, vectors, streamlines, weather maps, surfaces, histograms, X/Y plots, annotations, and more
* an ANSI/ISO standard version of GKS, with both C and FORTRAN callable entries
* a math library containing a collection of C and Fortran interpolators and approximators
  for one-dimensional, two-dimensional, and three-dimensional data
* applications for displaying, editing, and manipulating graphical output
* map databases
* hundreds of FORTRAN and C examples
* demo programs
* compilation scripts

http://www.ncl.ucar.edu/index.shtml

%prep

rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# %setup expects it to untar into a directory called %{name}-%{version};
# otherwise you have to pass it the -n switch, which renames the
# directory. The important %setup switches are:
# -n <name>    (name of build directory)
# -c           (creates top-level build directory)
# -D           (don't delete top-level build directory)
# -T           (don't unpack Source0)
# -a <n>       (unpack Source number n, after cd'ing to build directory)
# -a <n>       (unpack Source number n, before cd'ing to build directory)
# -q           (unpack silently)

# This binary package unpacks to '.' by default.  We'll unpack to
# a subdirectory that we'll also create using the -c option
%setup -c -n %{name}-%{version}

%build

# "Build" just requires us to unzip, which is handled by setup,
# and then copy the files over to the INSTALL_DIR.  Should probably
# use the install program for this...
cp -r bin $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r include $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}

#
# Stuff for modules

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
--%Module1.0###################################################################
--#
--# This modulefile for package %{name} modifies the PATH and MANPATH so
--# that executables, man pages, libraries and include files associated
--# with %{name} can be accessed easily.
--#
--##############################################################################


local help_message = [[
The ncarg_ncl module file defines the following environment variables:
NCARG_ROOT, TACC_NCARG_ROOT, TACC_NCARG_BIN, TACC_NCARG_LIB, and 
TACC_NCARG_INC for the location of the NCARG distribution, binaries,
libraries, and include files, respectively.

To use the NCARG library, compile the source code with the option:

	-I$TACC_NCARG_INC 

and add the following options to the link step: 

	-L$TACC_NCARG_LIB -lncarg

(or another of the available libraries that is appropriate to your application) 

Version 6.3.0

]]

help(help_message,"\n")

whatis("ncarg: NCAR Graphics utilities")
whatis("Version: %{version}")
whatis("Category: utility, runtime support")
whatis("Keywords: Graphics, Utility")
whatis("Description: A library of graphics utilites from the Natl. Center for Atmospheric Research." )
whatis("URL: http://ngwww.ucar.edu/")


prepend_path("PATH","%{INSTALL_DIR}/bin")
prepend_path("MANPATH","%{INSTALL_DIR}/man")

setenv("NCARG_ROOT","%{INSTALL_DIR}")
setenv("TACC_NCARG_ROOT","%{INSTALL_DIR}")
setenv("TACC_NCARG_INC","%{INSTALL_DIR}/include")
setenv("TACC_NCARG_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_NCARG_BIN","%{INSTALL_DIR}/bin")

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
--#%Module1.0#################################################
--##
--## version file for the package
--##
 
set     ModulesVersion      "%{version}"
EOF



%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files 
%defattr(-,root,install)

%{INSTALL_DIR}
%{MODULE_DIR}

%post


%clean
rm -rf $RPM_BUILD_ROOT
