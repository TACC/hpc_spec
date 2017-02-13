# Support for the lmod system in tacc_world
if [ -f "$BASH_ENV" ]; then
  . $BASH_ENV
  module purge
  clearMT
  export MODULEPATH=/opt/apps/tools/modulefiles:/opt/apps/modulefiles
  module load TACC-largemem
fi
