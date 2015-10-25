# Support for the lmod system
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles:~cproctor/apps/modulefiles
  module load TACC
fi
