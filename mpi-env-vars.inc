%if "%{mpi_fam}" != "none"
   CC=mpicc
   CXX=mpicxx
   FC=mpif90
   F77=mpif77
   F90=$FC
%endif

