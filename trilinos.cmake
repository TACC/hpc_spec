cmake -VV \
  -D BUILD_SHARED_LIBS:BOOL=ON \
  -D Trilinos_VERBOSE_CONFIGURE=OFF \
  -D CMAKE_VERBOSE_MAKEFILE=ON \
  -D Trilinos_ENABLE_ALL_PACKAGES:BOOL=OFF \
  -D Trilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=OFF \
  -D Trilinos_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_EXAMPLES:BOOL=ON \
  -D Trilinos_ENABLE_Export_Makefiles:BOOL=ON \
  -D Trilinos_ENABLE_Fortran:BOOL=ON \
  \
  -D CMAKE_INSTALL_PREFIX:PATH=${INSTALL_LOCATION} \
  -D CMAKE_BUILD_TYPE:STRING=RELEASE \
  -D CMAKE_C_FLAGS:STRING="${COPTFLAGS} -mkl" \
  -D CMAKE_CXX_FLAGS:STRING="${COPTFLAGS} -mkl -DMPICH_SKIP_MPICXX" \
  \
  -D BLAS_INCLUDE_DIRS:PATH="${TACC_MKL_INC}" \
  -D BLAS_LIBRARY_DIRS:PATH="${TACC_MKL_LIB}" \
  -D BLAS_LIBRARY_NAMES:STRING="mkl_intel_lp64;mkl_sequential;mkl_core;pthread" \
  -D LAPACK_INCLUDE_DIRS:PATH="${TACC_MKL_INC}" \
  -D LAPACK_LIBRARY_DIRS:PATH="${TACC_MKL_LIB}" \
  -D LAPACK_LIBRARY_NAMES:STRING="mkl_intel_lp64;mkl_sequential;mkl_core;pthread" \
  \
  -D TPL_ENABLE_MPI:BOOL=ON \
  -D MPI_EXEC:FILEPATH="/opt/apps/xalt/0.4.6/bin/ibrun" \
  -D TPL_ENABLE_GLM=OFF \
  -D TPL_ENABLE_Matio=OFF \
  \
  -D TPL_ENABLE_Boost:BOOL=ON \
  -D Boost_INCLUDE_DIRS:PATH=$TACC_BOOST_INC      \
  -D Boost_LIBRARY_DIRS:PATH=$TACC_BOOST_LIB      \
  -D TPL_ENABLE_BoostLib:BOOL=ON \
  -D BoostLib_INCLUDE_DIRS:PATH=$TACC_BOOST_INC      \
  -D BoostLib_LIBRARY_DIRS:PATH=$TACC_BOOST_LIB      \
  \
  -D TPL_ENABLE_HDF5:BOOL=ON \
  -D HDF5_INCLUDE_DIRS:PATH=$TACC_HDF5_INC    \
  -D HDF5_LIBRARY_DIRS:PATH=$TACC_HDF5_LIB    \
  -D TPL_ENABLE_Netcdf:BOOL=ON \
  -D Netcdf_INCLUDE_DIRS:PATH=$TACC_NETCDF_INC    \
  -D Netcdf_LIBRARY_DIRS:PATH=$TACC_NETCDF_LIB    \
  \
  -D Trilinos_ENABLE_ALL_OPTIONAL_PACKAGES:BOOL=ON \
  \
  -D Trilinos_ENABLE_Amesos:BOOL=ON \
  -D Amesos2_ENABLE_Basker:BOOL=ON \
  -D Trilinos_ENABLE_Anasazi:BOOL=ON \
  -D Trilinos_ENABLE_AztecOO:Bool=ON \
  -D Trilinos_ENABLE_Belos:BOOL=ON \
  -D Trilinos_ENABLE_Epetra:Bool=ON \
  -D Trilinos_ENABLE_EpetraExt:Bool=ON \
  -D                 Epetra_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_Ifpack:Bool=ON \
  -D Trilinos_ENABLE_Intrepid:BOOL=ON \
  -D                 Intrepid_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_ML:BOOL=ON \
  -D Trilinos_ENABLE_MOOCHO:BOOL=ON \
  -D Trilinos_ENABLE_MueLu:BOOL=ON \
  -D Trilinos_ENABLE_NOX=ON \
  -D                 NOX_ENABLE_TESTS:BOOL=ON \
  -D Trilinos_ENABLE_Pamgen:Bool=ON \
  -D Trilinos_ENABLE_Phalanx:BOOL=ON \
  -D Phalanx_EXPLICIT_TEMPLATE_INSTANTIATION=ON \
  -D Trilinos_ENABLE_Rythmos:BOOL=ON \
  -D Trilinos_ENABLE_Sacado:Bool=ON \
  -D Trilinos_ENABLE_SEACASIoss:BOOL=ON \
  -D Trilinos_ENABLE_SEACAS:BOOL=ON \
  -D Trilinos_ENABLE_SEACASBlot:BOOL=ON \
  -D Trilinos_ENABLE_Shards:BOOL=ON \
  -D Trilinos_ENABLE_ShyLU:BOOL=OFF \
  -D Trilinos_ENABLE_STK:BOOL=ON \
  -D Trilinos_ENABLE_Stokhos:BOOL=ON \
  -D Trilinos_ENABLE_Stratimikos:BOOL=ON \
  -D Trilinos_ENABLE_Teko:BOOL=ON \
  -D Trilinos_ENABLE_Teuchos:BOOL=ON \
  -D Trilinos_ENABLE_TriKota:BOOL=ON \
  -D Trilinos_ENABLE_Zoltan:BOOL=ON \
  \
  ${TRILINOS_LOCATION}/trilinos-${VERSION} \
  | tee /admin/build/rpms/SPECS/trilinos-${VERSION}-cmake.log 2>&1

# /bin/true \
#   \
#   -D CMAKE_PYTHON_INCLUDE_DIR:PATH="${TACC_PYTHON_INC}" \
#   -D CMAKE_PYTHON_LIBRARIES:STRING="${TACC_PYTHON_LIB}" \
#   -D Trilinos_ENABLE_PyTrilinos:Bool=ON \
#   \
#   -D SWIG_EXECUTABLE:FILEPATH=${TACC_SWIG_DIR}/bin/swig \
#   notrue
