#!/bin/bash 

set -x

cd ../SOURCES
rm -rf petsc4py*
git clone https://VictorEijkhout@bitbucket.org/petsc/petsc4py.git
( cd petsc4py && git checkout maint )

if [ $# -gt 0 ]  ; then
  cp -r petsc4py petsc4py-$1
  tar fcz petsc4py-$1.tgz petsc4py-$1
else
  tar fcz petsc4py.tgz petsc4py
fi
