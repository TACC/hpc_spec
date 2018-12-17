# $Id: adcirc.spec, 52.00, 2018/12/12 siliu $ 

Summary: Adcirc spec file

%define mpi_fam none


# Give the package a base name
%define pkg_base_name adcirc
%define MODULE_VAR    ADCIRC

# Create some macros (spec file variables)
%define major_version 52
%define minor_version 00

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc
%include compiler-defines.inc
%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
#%include name-defines.inc
%include name-defines-noreloc.inc
########################################
############ Do Not Remove #############
########################################

############ Do Not Change #############
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot
########################################

Release:   5
License:   GPL
Group:     Applications/Geoscience
URL:       https://adcirc.org
Packager:  TACC - siliu@tacc.utexas.edu

%description
ADCIRC is a system of computer programs for solving time dependent, free surface circulation and transport problems in two and three dimensions. These programs utilize the finite element method in space allowing the use of highly flexible, unstructured grids.

%prep
#Nothing necessary here

%build
#Nothing necessary here

%install

#-----------------
# Modules Section 
#-----------------

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT//%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

local help_msg=[[
ADCIRC is a system of computer programs for solving time dependent, free surface circulation and transport problems in two and three dimensions.
These programs utilize the finite element method in space allowing the use of highly flexible, unstructured grids.
Typical ADCIRC applications have included:
    prediction of storm surge and flooding
    modeling tides and wind driven circulation
    larval transport studies
    near shore marine operations
    dredging feasibility and material disposal studies

The %{MODULE_VAR} module file defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_BIN for
the location of the %{name} distribution and excutables,respectively.
It also appends the path to the executables
to the PATH environment variable.

The excutables of %{MODULE_VAR} in this version include:
        adcirc  adcprep  padcirc  padcswan

Version %{pkg_version}
]]

help(help_msg)

whatis("ADCIRC: adcirc is a system of computer programs for solving time dependent, free surface circulation and transport problems in two and three dimensions. ")
whatis("Version: %{pkg_version}%{dbg}")
whatis("Category: application, geoscience")
whatis("URL: https://adcirc.org/")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local adcirc_dir           = "/work/projects/wma_apps/lonestar5/adcirc/52.00"

family("adcirc")
prepend_path(    "PATH",               "/work/projects/wma_apps/lonestar5/adcirc/52.00/bin")
setenv( "TACC_%{MODULE_VAR}_DIR",                adcirc_dir)
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(adcirc_dir, "bin"))
EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"


EOF

#--------------
#  Version file. 
#--------------

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{name}-%{version}
##
 
set     ModulesVersion      "%{version}"
EOF

%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files
%defattr(755,root,root,-)
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

