#!/bin/bash


./build_rpm.sh -l --intel=18                           boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --gcc=71                             boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --intel=18 --impi=18_0               boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --gcc=71   --impi=18_0               boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --intel=18 --python=2_7              boost_python.spec; umount `df | grep boost | awk '{print $6}'`
#./build_rpm.sh -l --gcc=71   --python=2_7              boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --intel=18 --impi=18_0 --python=2_7  boost_python.spec; umount `df | grep boost | awk '{print $6}'`
#./build_rpm.sh -l --gcc=71   --impi=18_0 --python=2_7  boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --intel=18 --python=3_7              boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --gcc=71   --python=3_6              boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --intel=18 --impi=18_0 --python=3_7  boost_python.spec; umount `df | grep boost | awk '{print $6}'`
./build_rpm.sh -l --gcc=71   --impi=18_0 --python=3_6  boost_python.spec; umount `df | grep boost | awk '{print $6}'`
