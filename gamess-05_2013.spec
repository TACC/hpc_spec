#
# Spec file for GAMESS 201305

Summary:   GAMESS is a program for ab initio molecular quantum chemistry.
Name:      gamess
Version:   05_2013
Release:   1
License:   GPL
Vendor:    Ames Lab
Group:     applications/chemistry
Source:    gamess-05_2013.tar.gz
Packager:  TACC - (kent Xiao) milfeld@tacc.utexas.edu;xzhu216@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

#URL: http://www.msg.ameslab.gov/GAMESS/GAMESS.html
#     http://www.msg.ameslab.gov/gamess/versions.html

##define _unpackaged_files_terminate_build 0 


%define debug_package %{nil}
%include rpm-dir.inc

%define APPS /opt/apps
%define MODULES modulefiles

%include compiler-defines.inc
%include mpi-defines.inc

%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{MODULES}/%{name}


%package -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
Summary: Compute Node Version %{name}
Group: applications/chemistry
%description

%description -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
GAMESS can compute SCF wavefunctions ranging from RHF, ROHF, UHF, GVB, and MCSCF. Correlation corrections to these SCF wavefunctions include Configuration Interaction, second order Perturbation Theory, and Coupled-Cluster approaches, as well as the Density Functional Theory approximation. Nuclear gradients are available, for automatic geometry optimization, transition state searches, or reaction path following. Computation of the energy hessian permits prediction of vibrational frequencies, with IR or Raman intensities. Solvent effects may be modeled by the discrete Effective Fragment Potentials, or continuum models such as the Polarizable Continuum Model. Numerous relativistic computations are available, including third order Douglas-Kroll scalar corrections, and various spin-orbit coupling options. The Fragment Molecular Orbital method permits use of many of these sophisticated treatments to be used on very large systems, by dividing the computation into small fragments.
#

%prep

rm    -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p  $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-%{version}


%build

%include compiler-load.inc
%include mpi-load.inc

#module load mkl

export GMS_BUILD=`pwd`

#                       #Put files changed by TACC in place
cd TACC_FILES

%if "%{is_mvapich2}" == "1"
   cp lked_stampede             ../lked
   cp install.info_mv2          ../install.info.template
   cp Makefile                  ../Makefile.template
   cp rungms_stampede           ../machines/unix/rungms
   cp ibrun_gms                 ../machines/unix/ibrun_gms
%endif
%if "%{is_impi}" == "1"
   cp lked_stampede              ../lked
   cp install.info_impi          ../install.info.template
   cp Makefile                   ../Makefile.template
   cp rungms_stampede            ../machines/unix/rungms
   cp ibrun_gms                  ../machines/unix/ibrun_gms
%endif


cd $GMS_BUILD
#             Temporary workaround for gcc 4.9.1 TACC Install
#             ibcloog-isl.so.4: cannot open shared object file: No such file or directory
#             The next line can be removed after the fix.
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/apps/gcc/4.9.1/lib

sed -i s'@^\s*setenv\s*GMS_PATH\s*$@setenv GMS_PATH $GMS_BUILD@' install.info.template 
sed -i s'@^\s*setenv\s*GMS_BUILD_DIR\s*$@setenv GMS_BUILD_DIR $GMS_BUILD@' install.info.template 
cp install.info.template install.info

sed -i s'@^\s*GMS_PATH\s*=\s*$@GMS_PATH = ${GMS_BUILD}@' Makefile.template 
sed -i s'@^\s*GMS_BUILD_PATH\s*=\s*$@GMS_BUILD_PATH = ${GMS_BUILD}@' Makefile.template 
cp Makefile.template Makefile
 
#                       #Prepare activation executable
sed -e "s/^\*UNX/    /" tools/actvte.code > actvte.f
ifort -o tools/actvte.x actvte.f


#                       #Make the libraries for MPI
#cd ddi

#   ./compddi

#cd $GMS_BUILD

#                       #Compile and link
#   ./compall
#   ./lked
make -j 4

%install
mkdir -p       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
mkdir -p       $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata
##date> gamess.00.x

### Use rungms ###
#                       #Fix GAMESS HOME in rungms script

#sed -e 's@^setenv GMSPATH$@setenv GMSPATH /opt/apps/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}/%{version}@' machines/unix/rungms_template > machines/unix/rungms
#cp machines/unix/rungms_template  machines/unix/rungms

#                       #Move files to rpm build directories 
#                       #Uses special  ibrun for  gamess (ibrun_gms)

cp gamess.00.x                $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp gms-files.csh              $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp machines/unix/rungms       $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp machines/unix/ibrun_gms    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
cp -pr             auxdata    $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf                        $RPM_BUILD_ROOT/%{INSTALL_DIR}/auxdata/QUANPOL/RXNFLD3840.DAT
cp -pr               tools    $RPM_BUILD_ROOT/%{INSTALL_DIR}
#chmod -Rf u+rwX,g+rwX,o=rX    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
chmod a+rX                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/
chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/gamess.00.x
chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/gms-files.csh
chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/rungms
chmod a+rx                    $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin/ibrun_gms

###
### Install tests and documentation
###

mkdir -p    $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
cp *.DOC    $RPM_BUILD_ROOT/%{INSTALL_DIR}/doc
cp -r tests $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf    $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p    $RPM_BUILD_ROOT/%{MODULE_DIR}
cat >       $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
local help_message=[[
The GAMESS modulefile defines the following environment variables:
TACC_GAMESS_DIR/DOC/BIN/DATA for the location of the Gamess home,
documentation, binaries and aux data directories, respectively.
The modulefile defines GMSPATH (Gamess dir) used in rungms.

To run GAMESS, include the following lines in your job script.

       module load gamess
       rungms my_molecule or
       rungms my_molecule NCPUS

where my_molecule is the input file name. The input file must have an .inp suffix.
But it is not necessary to include the suffix in the name used on the rungms command. 
e.g. for an h2.inp input file you can run gamess with

      rungms h2.inp  or rungms h2

(rungms uses a special mpirun command, mpiexec.hydra, to launch gamess, so you do not 
need to use ibrun.) 

NCPUS is number of computing processes you want to use and the default value is the total 
tasks requested in the slurm job script. If you need to use the QUANPOL/RXNFLD3840.DAT 
data file please contact TACC. 

Version %{version}
]]

help(help_message,"\n")

whatis("Name: %{name}")
whatis("Version: %{version}")
whatis("Category: application, chemistry")
whatis("Keywords: Chemistry, Quantum, Application")
whatis("URL: http://www.msg.ameslab.gov/GAMESS/")
whatis("Description: General ab initio quantum chemistry package")

local gms_dir="%{INSTALL_DIR}" 
--
-- TACC Variables
--
setenv("TACC_GAMESS_DIR",  gms_dir)   
setenv("TACC_GAMESS_BIN",  pathJoin(gms_dir,"bin" ) )
setenv("TACC_GAMESS_DOC",  pathJoin(gms_dir,"doc" ) )
setenv("TACC_GAMESS_DATA", pathJoin(gms_dir,"auxdata") )
--
-- GMS Variables and PATH append 
--
setenv("GMSPATH",          gms_dir)
append_path("PATH",        pathJoin(gms_dir,"bin"))

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
##%Module1.0#################################################
##
## version file for GAMESS
## 
#
set     ModulesVersion      "%{version}"
EOF


%{SPEC_DIR}/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua

%files -n %{name}-%{comp_fam_ver}-%{mpi_fam_ver}
%defattr(-,root,install)
%{INSTALL_DIR}/bin
%{INSTALL_DIR}/auxdata
%{INSTALL_DIR}/tools
%{INSTALL_DIR}/tests
%{INSTALL_DIR}/doc
%{MODULE_DIR}

%post

%clean
rm -rf $RPM_BUILD_ROOT

#
# $Log$
#
