#!/bin/bash
#
# W. Cyrus Proctor
# 2017-09-19

rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf avx2'              fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel17.log
rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf avx2-novec-nosimd' fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel17.log
rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf common-avx512'     fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel17.log
rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf core-avx512'       fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel17.log

rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf avx2'              fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf avx2-novec-nosimd' fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf common-avx512'     fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf common-avx512-zmm' fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf core-avx512-zmm'   fftw3-vec.spec 2>&1 | tee -a fftw3-vec_intel18.log

rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf avx2'                fftw3-vec.spec 2>&1 | tee -a fftw3-vec_gcc71_impi_17_0.log
rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf avx2-novec-nosimd'   fftw3-vec.spec 2>&1 | tee -a fftw3-vec_gcc71_impi_17_0.log
rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf common-avx512'       fftw3-vec.spec 2>&1 | tee -a fftw3-vec_gcc71_impi_17_0.log
rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71' --define 'is_impi 1' --define 'mpiV 17_0' --define 'suf core-avx512'         fftw3-vec.spec 2>&1 | tee -a fftw3-vec_gcc71_impi_17_0.log
