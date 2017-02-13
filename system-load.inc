# Support for the lmod system in tacc_world
if [ -f /etc/tacc/tacc_functions ]; then
  . /etc/tacc/tacc_functions
  module purge
  clearMT
  export MODULEPATH=/opt/apps/tools/modulefiles:/opt/apps/modulefiles
  module load TACC
fi
