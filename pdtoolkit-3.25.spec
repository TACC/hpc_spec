
## rpmbuild -bb --define 'is_intel18 1'  pdtoolkit-3.25.spec 2>&1 | tee pdtoolkit-3.25_intel18_r1_a.log
## rpmbuild -bb --define 'is_gcc63 1'    pdtoolkit-3.25.spec 2>&1 | tee pdtoolkit-3.25-gcc63_r1.log
#
#                     r=/admin/rpms/RPMS/x86_64
#  rpm -hiv --nodeps $r/tacc-pdtoolkit-intel18-package-3.25-1.x86_64.rpm
#  rpm -hiv --nodeps $r/tacc-pdtoolkit-intel18-modulefile-3.25-1.x86_64.rpm

# Give the package a base name
%define pkg_base_name pdtoolkit
%define MODULE_VAR    PDTOOLKIT

# Create some macros (spec file variables)
%define major_version 3
%define minor_version 25
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

%include rpm-dir.inc
%include compiler-defines.inc

%include name-defines-noreloc.inc


Summary:   Spec file for PDToolkit
Name:      %{pkg_name}
Version:   %{pkg_version}
Release:   1%{?dist}
License:   University of Oregon, ZAM, and LANL
Vendor:    Department of Computer Science, Oregon 
Group:     Development/Languages
Source:    %{pkg_base_name}-%{pkg_version}.tar
Packager:  TACC - milfeld@tacc.utexas.edu
URL:       http://www.cs.uoregon.edu/research/tau/


# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}

#------------------------------------------------
# Other DEFINITIONS
#------------------------------------------------
%define system linux

#The are now come from name-defines-noreloc.inc
#INSTALL_DIR/MODULE_DIR
#define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
#define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}

%define PREFIX  -prefix=%{INSTALL_DIR}


%package %{PACKAGE}
Summary: RPM  for PDToolkit
Group: Development/Languages
%description package
PDTOOLKIT package is a dependency for some of the TAU tools like the parser.
This package needs to be installed ahead of TAU.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...

%description
PDTOOLKIT package is a dependency for some of the TAU tools like the parser.
This package needs to be installed ahead of TAU.



%prep
  rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{pkg_base_name}-%{pkg_version}

%build
  %if %{?BUILD_PACKAGE}

    %include compiler-load.inc

    mkdir -p             %{INSTALL_DIR}
    mount -t tmpfs tmpfs %{INSTALL_DIR}


    #./configure -icpc  %{PREFIX}
     ./configure        %{PREFIX}

    #export LD_DEBUG=files
    make

  %endif # BUILD_PACKAGE |


%install

  %if %{?BUILD_PACKAGE}

    %include compiler-load.inc
    make install

    mkdir -p                  $RPM_BUILD_ROOT/%{INSTALL_DIR}
    cp    -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
    umount                                    %{INSTALL_DIR}
    rm    -rf %{INSTALL_DIR}

  %endif # BUILD_PACKAGE | 

#----------MODULE ----------------
  %if %{?BUILD_MODULEFILE}

    # Module file for PDtoolkit (in Lua)
    rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

    touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary

cat >    $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}  << 'EOF'

-- This module file sets up the environment variables & path for PDTtoolkit.

local help_message = [[

The pdtoolkit module defines the following environment variables:
TACC_PDTOOLKIT_DIR, TACC_PDTOOLKIT_BIN, TACC_PDTOOLKIT_LIB and 
TACC_PDTOOLKIT_INC for the location of the PDToolkit distribution,
binaries, libraries and include files.

Version %{pkg_version}

]]

help(help_message,"\n")

whatis("Name: PDT, Program Database Toolkit ")
whatis("Version: %{pkg_version}")
whatis("Category: library, profiling and optimization")
whatis("System: Profiling, Tools")
whatis("URL: http://www.cs.uoregon.edu/research/tau/home.php")
whatis("Description: Instruments code for TAU profiling and tracing")

%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif
--#
--# Create environment variables.
--#
family("pdtoolkit")
local         pdtoolkit_dir       = "%{INSTALL_DIR}"
local         pdtoolkit_bin       = "%{INSTALL_DIR}/x86_64/bin"
local         pdtoolkit_lib       = "%{INSTALL_DIR}/x86_64/lib"
local         pdtoolkit_inc       = "%{INSTALL_DIR}/x86_64/include"

prepend_path( "PATH"              , pdtoolkit_bin )
prepend_path( "LD_LIBRARY_PATH"   , pdtoolkit_lib )

setenv(       "TACC_PDTOOLKIT_DIR", pdtoolkit_dir )
setenv(       "TACC_PDTOOLKIT_BIN", pdtoolkit_bin )
setenv(       "TACC_PDTOOLKIT_LIB", pdtoolkit_lib )
setenv(       "TACC_PDTOOLKIT_INC", pdtoolkit_inc )

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF

    #        RPM_BUILD_ROOT not removed on Target, but removed on line name
    ### -sf $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} $RPM_BUILD_ROOT/%{MODULE_DIR}/.version
    #ln -sf                 %{MODULE_DIR}/.version.%{version} $RPM_BUILD_ROOT/%{MODULE_DIR}/.version

    # Check the syntax of the generated lua modulefile
    # changed from                                               {version}.lua
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}

%endif  # BUILD_MODULEFILE |

%if %{?BUILD_PACKAGE}

%files package
   %defattr(755,root,install)
   %{INSTALL_DIR}

%endif # BUILD_PACKAGE


%if %{?BUILD_MODULEFILE}

%files modulefile
  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

%endif # BUILD_MODULEFILE |



%clean
rm -rf $RPM_BUILD_ROOT
rm -rf /var/tmp/%{name}-%{version}-buildroot
rm -rf $RPM_BUILD_DIR/%{name}-%{version}
# http://www.rpm.org/max-rpm/s1-rpm-inside-scripts.html
