# Support for the lmod system
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/modulefiles:/opt/cray/modulefiles:/opt/cray/ari/modulefiles:/opt/cray/craype/default/modulefiles:/opt/modulefiles
  module load TACC
fi
