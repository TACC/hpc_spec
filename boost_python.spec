#
# Si Liu
# 2017-11-01
# 2019-03-03 WCP Clean up; add in Python
#

Summary: Boost spec file (www.boost.org)

# Give the package a base name
%define base          boost
%define pkg_base_name %{base}
%define MODULE_VAR    BOOST

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 69
%define micro_version 0

%define pkg_version     %{major_version}.%{minor_version}.%{micro_version}
%define pkg_und_version %{major_version}_%{minor_version}_%{micro_version}

%define icu_major_version 63
%define icu_minor_version  1

%define icu_version     %{icu_major_version}.%{icu_minor_version}
%define icu_und_version %{icu_major_version}_%{icu_minor_version}

%include rpm-dir.inc
### Toggle On/Off ######################
%include compiler-defines.inc
%if %{defined mpiV}
  %include mpi-defines.inc
%endif
%if %{defined pythonV}
  %include python-defines.inc
%endif
########################################
%if %{defined mpi_fam}
  %define base          boost
  %define pkg_base_name %{base}-mpi
  %define MODULE_VAR    BOOSTMPI
%endif
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

Release:   1%{?dist}
License:   GPL
Group:     Utility
URL:       http://www.boost.org
Packager:  TACC - siliu@tacc.utexas.edu
Source0:   %{base}_%{pkg_und_version}.tar.gz
Source1:   icu4c-%{icu_und_version}-src.tgz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: Boost RPM
Group: Development/System Environment
%description package
This is the long description for the package RPM...
Boost emphasizes libraries that work well with the C++ Standard
Library. Boost libraries are intended to be widely useful, and usable
across a broad spectrum of applications. The Boost license encourages
both commercial and non-commercial use.

Boost aims to establish "existing practice" and provide reference
implementations so that Boost libraries are suitable for eventual
standardization. Ten Boost libraries are already included in the C++
Standards Committee Library Technical Report (TR1) as a step toward
becoming part of a future C++ Standard. More Boost libraries are
proposed for the upcoming TR2.


%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the long description for the modulefile RPM...
Boost emphasizes libraries that work well with the C++ Standard
Library. Boost libraries are intended to be widely useful, and usable
across a broad spectrum of applications. The Boost license encourages
both commercial and non-commercial use.

Boost aims to establish "existing practice" and provide reference
implementations so that Boost libraries are suitable for eventual
standardization. Ten Boost libraries are already included in the C++
Standards Committee Library Technical Report (TR1) as a step toward
becoming part of a future C++ Standard. More Boost libraries are
proposed for the upcoming TR2.

%description
Boost emphasizes libraries that work well with the C++ Standard
Library. Boost libraries are intended to be widely useful, and usable
across a broad spectrum of applications. The Boost license encourages
both commercial and non-commercial use.

Boost aims to establish "existing practice" and provide reference
implementations so that Boost libraries are suitable for eventual
standardization. Ten Boost libraries are already included in the C++
Standards Committee Library Technical Report (TR1) as a step toward
becoming part of a future C++ Standard. More Boost libraries are
proposed for the upcoming TR2.


#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

###%##setup -n boost_%{pkg_und_version}
%setup -n %{base}_%{pkg_und_version} 
%setup -n %{base}_%{pkg_und_version} -T -D -a 1

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------
  #Delete the module installation directory.
  rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#---------------------------------------
%build
#---------------------------------------


#---------------------------------------
%install
#---------------------------------------

#########################################
########### Do Not Modify ###############
#########################################
# Setup modules
%include system-load.inc
module purge
# Load Compiler
%if %{defined comp_fam}
  %include compiler-load.inc
%endif
# Load MPI Library
%if %{defined mpi_fam}
  %include mpi-load.inc
%endif
# Load Python Library
%if %{defined python_fam}
  %include python-load.inc
  IFS=.; VER=(${TACC_PYTHON_VER##*-}); unset IFS
  export PYTHON_MAJOR_VERSION="${VER[0]}"
  export PYTHON_MINOR_VERSION="${VER[1]}"
  export PYTHON_EXEC=python"${PYTHON_MAJOR_VERSION}"
  export TACC_PYTHON_DIR=$(eval echo "\${TACC_PYTHON${PYTHON_MAJOR_VERSION}_DIR}")
%endif
#########################################
###### Add Additional Modules Here ######
#########################################
ml

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{PYTHON_INSTALL_DIR}
  mkdir -p %{INSTALL_DIR}
  mount -t tmpfs tmpfs %{INSTALL_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

  #========================================
  # Insert Build/Install Instructions Here
  #========================================

  # Everything except mpi and python
  export BOOST_LIBS="atomic,chrono,container,context,contract,coroutine,date_time,exception,fiber,filesystem,graph,graph_parallel,iostreams,locale,log,math,program_options,random,regex,serialization,stacktrace,system,test,thread,timer,type_erasure,wave"
  export INSTALL_LOC=%{INSTALL_DIR}
  export ICU_MODE=Linux
  export ncores=68

  %if "%{comp_fam}" == "intel"
    export CONFIGURE_FLAGS=--with-toolset=intel-linux
    export ICU_MODE=Linux/ICC
  %endif

  %if "%{comp_fam}" == "gcc"
    export CONFIGURE_FLAGS=--with-toolset=gcc
  %endif

  %if %{undefined mpi_fam}
    %if %{undefined python_fam}
      pushd icu/source
      CXXFLAGS="%{TACC_OPT}" CFLAGS="%{TACC_OPT}" ./runConfigureICU  ${ICU_MODE} --prefix=${INSTALL_LOC}
      make -j ${ncores}
      make install
      popd
      export EXTRA="-sICU_PATH=${INSTALL_LOC}"
      # Everything but python and mpi
      export BOOST_WHITELIST="${BOOST_LIBS}"
    %else
      # Just python
      export BOOST_WHITELIST="python"
      export INSTALL_LOC=%{PYTHON_INSTALL_DIR}
      export CONFIGURE_FLAGS="${CONFIGURE_FLAGS} --with-python=$(which ${PYTHON_EXEC}) \
                                                 --with-python-root=${TACC_PYTHON_DIR} \
                                                 --with-python-version=${TACC_PYTHON_VER}"
    %endif
  %else
    export CXX=mpicxx
    %if %{undefined python_fam}
      # Just mpi
      export BOOST_WHITELIST="mpi"
    %else
      # Both mpi and python
      export BOOST_WHITELIST="mpi,python"
      export INSTALL_LOC=%{PYTHON_INSTALL_DIR}
      export CONFIGURE_FLAGS="${CONFIGURE_FLAGS} --with-python=$(which ${PYTHON_EXEC}) \
                                                 --with-python-root=${TACC_PYTHON_DIR} \
                                                 --with-python-version=${TACC_PYTHON_VER}"
    %endif
  %endif

  export CONFIGURE_FLAGS="${CONFIGURE_FLAGS} --with-libraries=${BOOST_WHITELIST}"
  ./bootstrap.sh --prefix=${INSTALL_LOC} ${CONFIGURE_FLAGS}
  %if %{defined mpi_fam}
    echo "using mpi : $(which mpicxx) ;" >> ./project-config.jam
  %endif
  ./b2 -j ${ncores} --prefix=${INSTALL_LOC} ${EXTRA} cxxflags="%{TACC_OPT}" cflags="%{TACC_OPT}" linkflags="%{TACC_OPT}" variant=release -d+2 install
  
  mkdir -p              $RPM_BUILD_ROOT/%{INSTALL_DIR}
  cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
  umount %{INSTALL_DIR}



#---------------------- -
%endif # BUILD_PACKAGE |
#-----------------------

#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  mkdir -p $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}

  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################

# Modulefile Help Message
HELP_MSG=$(cat << EOM
%{MODULE_VAR} provides free peer-reviewed portable C++ source libraries.

The %{MODULE_VAR} module defines the following environment variables:
TACC_%{MODULE_VAR}_DIR, TACC_%{MODULE_VAR}_LIB, TACC_%{MODULE_VAR}_INC and
TACC_%{MODULE_VAR}_BIN for the location of the %{MODULE_VAR} distribution, libraries,
include files, and tools respectively.

To use the %{MODULE_VAR} library, compile your source code with the option:

     -I\$TACC_%{MODULE_VAR}_INC

and add the following options to the link step: 

     -L\$TACC_%{MODULE_VAR}_LIB -l<%{pkg_base_name} library of choice>

where one can substitute the appropriate %{pkg_base_name} libraries as needed.

Version %{version}
EOM
)

# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << EOF
help([["${HELP_MSG}"]])

whatis("Name: %{pkg_base_name}")
whatis("Version: %{version}")
whatis("Category: %{group}")
whatis("Keywords: System, Library, C++")
whatis("URL: http://www.boost.org")
whatis("Description: Boost provides free peer-reviewed portable C++ source libraries.")


setenv("TACC_%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}_LIB","%{INSTALL_DIR}/lib")
setenv("TACC_%{MODULE_VAR}_INC","%{INSTALL_DIR}/include")
setenv("TACC_%{MODULE_VAR}_BIN","%{INSTALL_DIR}/bin")
setenv("BOOST_ROOT","%{INSTALL_DIR}")

family("boost")

prepend_path("PATH", "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

EOF

# Write out the python-enabled modulefile associated with the application
%if %{?WITH_PYTHON}
cat > $RPM_BUILD_ROOT/%{PYTHON_MODULE_DIR}/%{MODULE_FILENAME} << EOF
inherit()
help([["${HELP_MSG}"]])
local python_boost_dir           = "%{PYTHON_INSTALL_DIR}"
setenv("TACC_%{MODULE_VAR}PYTHON_DIR","%{PYTHON_INSTALL_DIR}")
setenv("TACC_%{MODULE_VAR}PYTHON_LIB","%{PYTHON_INSTALL_DIR}/lib")
setenv("TACC_%{MODULE_VAR}PYTHON_INC","%{PYTHON_INSTALL_DIR}/include")
prepend_path("LD_LIBRARY_PATH","%{PYTHON_INSTALL_DIR}/lib")
EOF
%endif

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{pkg_base_name}%{version}
##
set     ModulesVersion      "%{version}"
EOF

  # Check the syntax of the generated lua modulefile only if a visible module
  %if %{?VISIBLE}
    %{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME}
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


#------------------------
%if %{?BUILD_PACKAGE}
%files package
#------------------------

  %defattr(-,root,install,)
  # RPM package contains files within these directories
  %{INSTALL_DIR}

  %if %{?WITH_PYTHON}
    %{PYTHON_INSTALL_DIR}
  %endif

#-----------------------
%endif # BUILD_PACKAGE |
#-----------------------
#---------------------------
%if %{?BUILD_MODULEFILE}
%files modulefile
#---------------------------

  %defattr(-,root,install,)
  # RPM modulefile contains files within these directories
  %{MODULE_DIR}

  %if %{?WITH_PYTHON}
    %{PYTHON_MODULE_DIR}
  %endif

#--------------------------
%endif # BUILD_MODULEFILE |
#--------------------------


########################################
## Fix Modulefile During Post Install ##
########################################
%post %{PACKAGE}
export PACKAGE_POST=1
%include post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include post-defines.inc
%preun %{PACKAGE}
export PACKAGE_PREUN=1
%include post-defines.inc
########################################
############ Do Not Remove #############
########################################

#---------------------------------------
%clean
#---------------------------------------
rm -rf $RPM_BUILD_ROOT
