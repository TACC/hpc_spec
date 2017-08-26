# build rpm

# rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1' amask-1.0.spec 2>&1 | tee amask-1.0.log
# rpmbuild -bb --define 'is_intel17 1' --define 'is_impi 1' amask-1.0.spec 2>&1 | tee amask-1.0-x.log
#
# Build only PACKAGE or MODULE -- set variable.  E.g. NO_PACKAGE=1 rpmbuild -bb ... only build modulefile
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM


# install rpm in /opt/apps # install r= RPMS/x86-64 directory
# rpm -hiv --relocate /tmprpm=/opt/apps $r/tacc-amask-package...
# rpm -hiv --relocate /tmpmod=/opt/apps  $r/tacc-amask-modulefile...

# remove rpm
# rpm -e tacc-amask-package......el7.centos.x86_64
# rpm -e tacc-amask-modulefile...el7.centos.x86_64
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#

# Give the package a base name and cap name for module env var
%define pkg_base_name amask
%define MODULE_VAR    AMASK

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 0
%define micro_version 0

%define pkg_version %{major_version}.%{minor_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
%include compiler-defines.inc
%include mpi-defines.inc


 %include name-defines.inc
#%include name-defines-noreloc.inc


Summary:   Spec file for amask
Name:      %{pkg_name}
Version:   %{pkg_version}
BuildRoot: /var/tmp/%{pkg_name}-%{pkg_version}-buildroot


Release:   2%{?dist}
License:   GPL
Group:     Development/Tools
URL:       http://www.gnu.org/software/bar
Packager:  TACC - milfeld@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Affinity Mask Tool
Group: Development/Tools
%description package
AMASK is a tool for evaluating process masks.

%package %{MODULEFILE}
Summary: Module forAffinity Mask Tool
Group: Lmod/Modulefiles
%description modulefile
Modulefile includes amask bin directory PATH, and defines TACC_AMASK_DIR/BIN/LIB
  

%description
AMASK is a tool for evaluating process masks.
The longer-winded description of the package that will 
end in up inside the rpm and is queryable if installed via:

#This one is queryable with rpm -qi <rpm-name>

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"


# do %%dump to get all the variable names then exit (but exit didn't work, did others, prep,...


%define verbose
%prep


%if %{?BUILD_PACKAGE}
%setup -n %{pkg_base_name}-%{pkg_version}
  echo `pwd` >/tmp/whereami0
  env        >/tmp/env0
  ls -ld     >/tmp/ls0
  cd ..
  ls -la %{pkg_base_name}-%{pkg_version}
  rm -rf %{pkg_base_name}-%{pkg_version}
  git clone https://github.com/tacc/amask.git
  mv amask %{pkg_base_name}-%{pkg_version}

%endif # BUILD_PACKAGE |


%if %{?BUILD_PACKAGE}
%build
             # I really don't want to see the details of modules loading compiler and mpi!
   set +x
   %include system-load.inc
   %include compiler-load.inc
   %include mpi-load.inc
   set -x

   make

%endif # BUILD_PACKAGE |


%install

%if %{?BUILD_PACKAGE}
  rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR} # Delete the package installation directory.
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary

  echo "TACC_OPT %{TACC_OPT}"
                              # This puts everything in INSTALL_DIR 
                              #into the RPM_BUILD_ROOT/INSTALL_DIR dir

                              # we are in %%{_topdir}/BUILD = /admin/build/rpms
                              # we are in %%{_builddir}/%%{pkg_basename}-%%{version}   where things are made

                
  cp -r bin $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r lib $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r doc $RPM_BUILD_ROOT/%{INSTALL_DIR}
  
%endif # BUILD_PACKAGE |


%if %{?BUILD_MODULEFILE}

  rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR} #Delete the module installation directory.
  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  
                              # Write out the modulefile

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message=[[

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_BIN, and 
TACC_%{MODULE_VAR}_DOC for the location of the %{MODULE_VAR} distribution, libraries,
executables, and documents respectively.

Execute amask_omp, amask_mpi, or amask_hybrid (found in the $TACC_AMASK_BIN
directory) in a parallel environment to display the masks that
the processes will have (process = OMP thread or MPI task here). E.g.

STAND-ALONE BINARIES

      export OMP_NUM_THREADS=16
      export OMP_PROC_BIN=close
      $TACC_AMASK_BIN/amask_omp
      ./my_omp_application

      ibrun $TACC_AMASK_BIN/amask_mpi
      ibrun ./my_mpi_application

      export OMP_NUM_THREADS=4
      export OMP_PROC_BIN=spread
      ibrun $TACC_AMASK_BIN/amask_hybrid
      ibrun ./my_hybrid_application

Application code can be instrumented to report the masks within an application.
The C/C++ functions are argumentless, and have the same names as the stand-alone
executables.  Similarly, for the corresponding Fortran subroutines.  E.g.

INSTRUMENTATION FUNCTIONS   ( compile with $TACC_AMASK_LIB/amask.a)

  ...
  #pragma omp parallel     // Pure OpenMP code
  amask_omp();
  ...

  ...
  MPI_Init(NULL,NULL);    // Pure MPI code
    amask_mpi();
  ...
  MPI_Finalize();


  ...
  MPI_Init(NULL,NULL);    // Hybrid code
  ...
     #pragma omp parallel
     amask_hybrid();
  ...
  MPI_Finalize();
  ...

A full description of the options can be found in the pdf file located
in $TACC_AMASK_DOC.  The syntax and usage can be found by executing any
one of the stand-alone executables with the -u (usage) and -h (help) options.


]]

help(help_message)

whatis("Name: %{pkg_base_name}")
whatis("Version: %{pkg_version}%{dbg}")
%if "%{is_debug}" == "1"
setenv("TACC_%{MODULE_VAR}_DEBUG","1")
%endif

-- Create environment variables.
local APP_dir           = "%{INSTALL_DIR}"

family("APP")
prepend_path(    "PATH",                pathJoin(APP_dir, "bin"))
prepend_path(    "LD_LIBRARY_PATH",     pathJoin(APP_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_DIR",                APP_dir)
setenv( "TACC_%{MODULE_VAR}_LIB",       pathJoin(APP_dir, "lib"))
setenv( "TACC_%{MODULE_VAR}_BIN",       pathJoin(APP_dir, "bin"))
setenv( "TACC_%{MODULE_VAR}_DOC",       pathJoin(APP_dir, "doc"))
EOF
  
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{pkg_basename}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

%endif # BUILD_MODULEFILE |


%if %{?BUILD_PACKAGE}
%files package

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

%endif # BUILD_PACKAGE |


%if %{?BUILD_MODULEFILE}
%files modulefile 

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

%endif # BUILD_MODULEFILE |

## Fix Modulefile During Post Install ##

%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc

############ Do Not Remove #############

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT
