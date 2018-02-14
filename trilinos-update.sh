#!/bin/bash

if [ $# -eq 1 ] ; then
  today=$1
else
  today=`date +%Y%m%d`
fi

set -x
cd ../SOURCES

rm -rf trilinos-git*
git clone https://github.com/trilinos/Trilinos.git trilinos-git
tar fcz trilinos-git${today}.tar.gz trilinos-git
