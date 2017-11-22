#!/bin/bash
#
# W. Cyrus Proctor
# 2017-09-19

rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'suf avx2'              boost-vec.spec 2>&1 | tee -a boost-vec_intel17.log
rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'suf avx2-novec-nosimd' boost-vec.spec 2>&1 | tee -a boost-vec_intel17.log
rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'suf common-avx512'     boost-vec.spec 2>&1 | tee -a boost-vec_intel17.log
rpmbuild  -bb --define 'is_intel17 1' --define 'compV 17' --define 'suf core-avx512'       boost-vec.spec 2>&1 | tee -a boost-vec_intel17.log

rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'suf avx2'              boost-vec.spec 2>&1 | tee -a boost-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'suf avx2-novec-nosimd' boost-vec.spec 2>&1 | tee -a boost-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'suf common-avx512'     boost-vec.spec 2>&1 | tee -a boost-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'suf common-avx512-zmm' boost-vec.spec 2>&1 | tee -a boost-vec_intel18.log
rpmbuild  -bb --define 'is_intel18 1' --define 'compV 18' --define 'suf core-avx512-zmm'   boost-vec.spec 2>&1 | tee -a boost-vec_intel18.log

rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71'   --define 'suf avx2'              boost-vec.spec 2>&1 | tee -a boost-vec_gcc71.log
rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71'   --define 'suf avx2-novec-nosimd' boost-vec.spec 2>&1 | tee -a boost-vec_gcc71.log
rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71'   --define 'suf common-avx512'     boost-vec.spec 2>&1 | tee -a boost-vec_gcc71.log
rpmbuild  -bb --define 'is_gcc71 1' --define 'compV 71'   --define 'suf core-avx512'       boost-vec.spec 2>&1 | tee -a boost-vec_gcc71.log
