# -*-rpm-spec-*-
#
%if "%{mpi_fam}" != "none"
   CC=mpicc
   CXX=mpicxx
   FC=mpif90
   F77=mpif77
   F90=$FC
%endif


%if "%{mpi_fam}" == "impi"
   CC=mpiicc
   CXX=mpiicxx
   FC=mpiifort
   F77=mpiifort
   F90=$FC
%endif

      
