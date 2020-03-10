#
# W. Cyrus Proctor
# 2015-12-01 Add name-defines-noreloc.inc
# 2015-11-20 Need to investigate relocation -- use /opt/apps for now
# 2015-11-10 Update for LS5 Chroot Jail
# 2015-10-27
#
# Important Build-Time Environment Variables (see name-defines.inc)
# NO_PACKAGE=1    -> Do Not Build/Rebuild Package RPM
# NO_MODULEFILE=1 -> Do Not Build/Rebuild Modulefile RPM
#
# Important Install-Time Environment Variables (see post-defines.inc)
# VERBOSE=1       -> Print detailed information at install time
# RPM_DBPATH      -> Path To Non-Standard RPM Database Location
#
# Typical Command-Line Example:
# ./build_rpm.sh Bar.spec
# cd ../RPMS/x86_64
# rpm -i Bar-package-1.1-1.x86_64.rpm
# rpm -i Bar-modulefile-1.1-1.x86_64.rpm
# rpm -e Bar-package-1.1-1.x86_64 Bar-modulefile-1.1-1.x86_64

Summary: A Nice little non-relocatable skeleton spec file example.

# Give the package a base name
%define pkg_base_name wget
%define MODULE_VAR    WGET

# Create some macros (spec file variables)
%define major_version 1
%define minor_version 19
%define micro_version 5

%define pkg_version %{major_version}.%{minor_version}.%{micro_version}

### Toggle On/Off ###
%include rpm-dir.inc                  
#%include compiler-defines.inc
#%include mpi-defines.inc
########################################
### Construct name based on includes ###
########################################
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
Group:     Development/Tools
URL:       https://www.gnu.org/software/wget
Packager:  TACC - cproctor@tacc.utexas.edu
Source:    %{pkg_base_name}-%{pkg_version}.tar.gz

# Turn off debug package mode
%define debug_package %{nil}
%define dbg           %{nil}


%package %{PACKAGE}
Summary: The package RPM
Group: Development/Tools
%description package
This is the package RPM...
GNU Wget is a free software package for retrieving files using HTTP, HTTPS, FTP
and FTPS the most widely-used Internet protocols. It is a non-interactive
commandline tool, so it may easily be called from scripts, cron jobs, terminals
without X-Windows support, etc.

%package %{MODULEFILE}
Summary: The modulefile RPM
Group: Lmod/Modulefiles
%description modulefile
This is the modulefile RPM...
GNU Wget is a free software package for retrieving files using HTTP, HTTPS, FTP
and FTPS the most widely-used Internet protocols. It is a non-interactive
commandline tool, so it may easily be called from scripts, cron jobs, terminals
without X-Windows support, etc.

%description
GNU Wget is a free software package for retrieving files using HTTP, HTTPS, FTP
and FTPS the most widely-used Internet protocols. It is a non-interactive
commandline tool, so it may easily be called from scripts, cron jobs, terminals
without X-Windows support, etc.

#---------------------------------------
%prep
#---------------------------------------

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------
  # Delete the package installation directory.
  rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

# Setup modules
%include system-load.inc

# Insert necessary module commands
module purge
#module load TACC
#module load gcc/4.9.3

echo "Building the package?:    %{BUILD_PACKAGE}"
echo "Building the modulefile?: %{BUILD_MODULEFILE}"

#------------------------
%if %{?BUILD_PACKAGE}
#------------------------

  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
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

##################################################
export wget=`pwd`
export wget_install=%{INSTALL_DIR}
##################################################

ml purge
ml autotools
ml gcc/4.9.3

export nettle=${wget}
export nettle_install=%{INSTALL_DIR}
export nettle_version=3.1
export ncores=16


export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
export CFLAGS="-I/opt/apps/gcc/4.9.3/include"


cd "${nettle}"

wget https://ftp.gnu.org/gnu/nettle/nettle-"${nettle_version}".tar.gz
tar xvfz nettle-"${nettle_version}".tar.gz
cd nettle-"${nettle_version}"


./configure \
--prefix="${nettle_install}" \
--enable-shared=yes \
--enable-static=yes \
--enable-pic

make -j ${ncores}
make -j ${ncores} install

########################################################

ml purge
ml autotools
ml gcc/4.9.3

export libidn2=${wget}
export libidn2_install=%{INSTALL_DIR}
export libidn2_version=2.0.5
export ncores=16


export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
export CFLAGS="-I/opt/apps/gcc/4.9.3/include"


cd "${libidn2}"

wget https://ftp.gnu.org/gnu/libidn/libidn2-"${libidn2_version}".tar.gz
tar xvfz libidn2-"${libidn2_version}".tar.gz
cd libidn2-"${libidn2_version}"


./configure \
--prefix="${libidn2_install}" \
--enable-shared=yes \
--enable-static=yes \
--with-pic


make -j ${ncores}
make -j ${ncores} install

########################################################

ml purge
ml autotools
ml gcc/4.9.3

export unbound=${wget}
export unbound_install=%{INSTALL_DIR}
export unbound_version=1.7.1
export ncores=16


#export PATH=/opt/openssl/1.0.2o/usr/bin:$PATH
#export LD_LIBRARY_PATH=/opt/openssl/1.0.2o/usr/lib:$LD_LIBRARY_PATH
#export LDFLAGS="-Wl,-rpath=/opt/openssl/1.0.2o/usr/lib -L/opt/openssl/1.0.2o/usr/lib"
#export CFLAGS="-I/opt/openssl/1.0.2o/usr/include"


cd "${unbound}"
wget http://unbound.net/downloads/unbound-"${unbound_version}".tar.gz
tar xvfz unbound-"${unbound_version}".tar.gz
cd unbound-"${unbound_version}"


./configure \
--prefix="${unbound_install}" \
--enable-shared=yes \
--enable-static=yes \
--with-pic \
--with-ssl=/opt/openssl/1.0.2o/usr



make -j ${ncores}
make -j ${ncores} install

########################################################

ml purge
ml autotools
ml gcc/4.9.3

export libtasn1=${wget}
export libtasn1_install=%{INSTALL_DIR}
export libtasn1_version=4.13
export ncores=16


export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
export CFLAGS="-I/opt/apps/gcc/4.9.3/include"


cd "${libtasn1}"

wget https://ftp.gnu.org/gnu/libtasn1/libtasn1-"${libtasn1_version}".tar.gz
tar xvfz libtasn1-"${libtasn1_version}".tar.gz
cd libtasn1-"${libtasn1_version}"


./configure \
--prefix="${libtasn1_install}" \
--enable-shared=yes \
--enable-static=yes \
--with-pic



make -j ${ncores}
make -j ${ncores} install


########################################################

ml purge
ml autotools
ml gcc/4.9.3

export libunistring=${wget}
export libunistring_install=%{INSTALL_DIR}
export libunistring_version=0.9.9
export ncores=16


#export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
#export CFLAGS="-I/opt/apps/gcc/4.9.3/include"


cd "${libunistring}"

wget https://ftp.gnu.org/gnu/libunistring/libunistring-"${libunistring_version}".tar.gz
tar xvfz libunistring-"${libunistring_version}".tar.gz
cd libunistring-"${libunistring_version}"


./configure \
--prefix="${libunistring_install}" \
--enable-shared=yes \
--enable-static=yes \
--with-pic



make -j ${ncores}
make -j ${ncores} install

########################################################

ml purge
ml autotools
ml gcc/4.9.3

export libffi=${wget}
export libffi_install=%{INSTALL_DIR}
export libffi_version=3.2.1
export ncores=16


#export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
#export CFLAGS="-I/opt/apps/gcc/4.9.3/include"


cd "${libffi}"

wget ftp://sourceware.org/pub/libffi/libffi-"${libffi_version}".tar.gz
tar xvfz libffi-"${libffi_version}".tar.gz
cd libffi-"${libffi_version}"


./configure \
--prefix="${libffi_install}" \
--enable-shared=yes \
--enable-static=yes \
--with-pic



make -j ${ncores}
make -j ${ncores} install


########################################################

ml purge
ml autotools
ml gcc/4.9.3

export guile=${wget}
export guile_install=%{INSTALL_DIR}
export guile_version=2.2.3
export ncores=16

export PATH=${guile_install}/bin:${PATH}
export LD_LIBRARY_PATH=${guile_install}/lib64:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${guile_install}/lib:${LD_LIBRARY_PATH}
export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
export CFLAGS="-I${guile_install}/include -I/opt/apps/gcc/4.9.3/include"

export PKG_CONFIG_PATH=${guile_install}/lib64/pkgconfig:${PKG_CONFIG_PATH}
export PKG_CONFIG_PATH=${guile_install}/lib/pkgconfig:${PKG_CONFIG_PATH}



cd "${guile}"

wget https://ftp.gnu.org/gnu/guile/guile-"${guile_version}".tar.gz
tar xvfz guile-"${guile_version}".tar.gz
cd guile-"${guile_version}"


./configure \
--prefix="${guile_install}" \
--enable-shared=yes \
--enable-static=yes \
--with-pic



make -j ${ncores}
make -j 4 install


########################################################

ml purge
ml autotools
ml gcc/4.9.3
ml curl

export p11kit=${wget}
export p11kit_install=%{INSTALL_DIR}
export p11kit_version=0.23.12
export ncores=16

#export PATH=${tls_install}/bin:${PATH}
#export LD_LIBRARY_PATH=${tls_install}/lib:${LD_LIBRARY_PATH}

export PKG_CONFIG_PATH=${p11kit_install}/lib64/pkgconfig:${PKG_CONFIG_PATH}
export PKG_CONFIG_PATH=${p11kit_install}/lib/pkgconfig:${PKG_CONFIG_PATH}

#export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
#export CFLAGS="-I/opt/apps/gcc/4.9.3/include"


cd "${p11kit}"

curl -L --remote-name https://github.com/p11-glue/p11-kit/archive/${p11kit_version}.tar.gz
tar xvfz "${p11kit_version}".tar.gz
cd p11-kit-"${p11kit_version}"

./autogen.sh
./configure \
--prefix="${p11kit_install}" \
--enable-shared=yes \
--enable-static=no \
--with-pic \
--with-trust-paths=${p11kit_install}/etc/pki/trust



make -j ${ncores}
make -j ${ncores} install

########################################################

ml purge
ml autotools
ml gcc/4.9.3

export tls=${wget}
export tls_install=%{INSTALL_DIR}
export tls_version=3.5.18
export ncores=16

export PATH=${tls_install}/bin:${PATH}
export LD_LIBRARY_PATH=${tls_install}/lib64:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${tls_install}/lib:${LD_LIBRARY_PATH}

export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
export LDFLAGS="-Wl,-rpath=${tls_install}/lib -L${tls_install}/lib ${LDFLAGS}"
export CFLAGS="-I/opt/apps/gcc/4.9.3/include -I${tls_install}/include"

export PKG_CONFIG_PATH=${tls_install}/lib64/pkgconfig:${PKG_CONFIG_PATH}
export PKG_CONFIG_PATH=${tls_install}/lib/pkgconfig:${PKG_CONFIG_PATH}

cd "${tls}"

wget https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-"${tls_version}".tar.xz
tar xvfJ gnutls-"${tls_version}".tar.xz
cd gnutls-"${tls_version}"


./configure \
--prefix="${tls_install}" \
--enable-shared=yes \
--enable-static=no \
--with-pic \
--with-libcrypto-prefix=/opt/openssl/1.0.2o/usr \
--with-included-libtasn1 \
--with-included-unistring \
--enable-openssl-compatibility


make -j ${ncores}
make -j ${ncores} install


########################################################

ml purge
ml autotools
ml gcc/4.9.3

export gc=${wget}
export gc_install=%{INSTALL_DIR}
export gc_version=7.6.4
export ncores=16


#export LDFLAGS="-Wl,-rpath=/opt/apps/gcc/4.9.3/lib -L/opt/apps/gcc/4.9.3/lib"
#export CFLAGS="-I/opt/apps/gcc/4.9.3/include"


cd "${gc}"

wget http://www.hboehm.info/gc/gc_source/gc-"${gc_version}".tar.gz
tar xvfz gc-"${gc_version}".tar.gz
cd gc-"${gc_version}"
wget http://www.hboehm.info/gc/gc_source/libatomic_ops-7.6.2.tar.gz
tar xvfz libatomic_ops-7.6.2.tar.gz
ln -s libatomic_ops-7.6.2 libatomic_ops


./configure \
--prefix="${gc_install}" \
--enable-shared=yes \
--enable-static=yes \
--with-pic



make -j ${ncores}
make -j ${ncores} install


########################################################

ml purge
ml gcc/4.9.3

export wget=${wget}
export wget_install=%{INSTALL_DIR}
export wget_version=1.19.5
export ncores=8

cd "${wget}"
wget https://ftp.gnu.org/gnu/wget/wget-"${wget_version}".tar.gz
tar xvfz wget-"${wget_version}".tar.gz
cd wget-"${wget_version}"


export PATH=/opt/openssl/1.0.2o/usr/bin:${wget_install}/bin:$PATH
export LD_LIBRARY_PATH=/opt/openssl/1.0.2o/usr/lib:$LD_LIBRARY_PATH
export LDFLAGS="-Wl,-rpath=/opt/openssl/1.0.2o/usr/lib -L/opt/openssl/1.0.2o/usr/lib"
export LDFLAGS="-Wl,-rpath=${wget_install}/lib -L${wget_install}/lib ${LDFLAGS}"
export CFLAGS="-I/opt/openssl/1.0.2o/usr/include -I/opt/apps/gcc/4.9.3/include -I${wget_install}/include"

export PKG_CONFIG_PATH=${wget_install}/lib64/pkgconfig:${PKG_CONFIG_PATH}
export PKG_CONFIG_PATH=${wget_install}/lib/pkgconfig:${PKG_CONFIG_PATH}
export CC=gcc

./configure \
--prefix="${wget_install}" \
--with-ssl=openssl \
--with-libssl-prefix=/opt/openssl/1.0.2o/usr \
--with-openssl=yes \
--with-libgnutls-prefix="${wget_install}" \
--with-libidn="${wget_install}" \
--with-libunistring-prefix="${wget_install}" \

make -j ${ncores}
make -j ${ncores} install

########################################################


if [ ! -d $RPM_BUILD_ROOT/%{INSTALL_DIR} ]; then
  mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
fi

cp -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
umount %{INSTALL_DIR}/
  
  
#-----------------------  
%endif # BUILD_PACKAGE |
#-----------------------


#---------------------------
%if %{?BUILD_MODULEFILE}
#---------------------------

  mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
  
  #######################################
  ##### Create TACC Canary Files ########
  #######################################
  touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
  #######################################
  ########### Do Not Remove #############
  #######################################
  
# Write out the modulefile associated with the application
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{MODULE_FILENAME} << 'EOF'
local help_message = [[
GNU Wget is a free software package for retrieving files using HTTP, HTTPS, FTP
and FTPS the most widely-used Internet protocols. It is a non-interactive
commandline tool, so it may easily be called from scripts, cron jobs, terminals
without X-Windows support, etc.

Version %{pkg_version}
]]

help(help_message,"\n")

whatis("Name: GNU Wget")
whatis("Version: %{pkg_version}")
whatis("Category: System")
whatis("Keywords: System, wget")
whatis("URL: https://www.gnu.org/software/wget")

-- Create environment variables
local base         = "%{INSTALL_DIR}"
prepend_path( "PATH"            ,     pathJoin( base , "bin"   ) )
prepend_path( "LD_LIBRARY_PATH" ,     pathJoin( base , "lib64" ) )
prepend_path( "LD_LIBRARY_PATH" ,     pathJoin( base , "lib" ) )

family("wget")
EOF


cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{BASENAME}%{version}
##

set     ModulesVersion      "%{version}"
EOF
  
  # Check the syntax of the generated lua modulefile
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

