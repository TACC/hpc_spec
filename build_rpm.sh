#!/bin/bash
# -*- shell-script -*-

#  This script is designed to handle building rpm files.
#  It is probably too fancy by half but then I had fun putting it together.
#  Nobody told you that you had to use it. (;->)

#  Robert McLay 2/5/2012

ECHO()
{
  builtin echo "$@"
  if [ -n "$log" ]; then
    builtin echo "$@" >> $logName.log
  fi
}
    
# This script needs lua but should not require that a working module
# system be in place.  So we search for lua the old fashion way.

for i in /usr/bin /opt/apps/lua/lua/bin /opt/local/bin /usr/local/bin; do
  if [ -x $i/lua ]; then
    luaPath=$i
    break
  fi
done

PATH=$luaPath:$PATH



PATH=/opt/apps/tacc_build_rpm/0.9.5/bin:$PATH

Name="build_rpm.sh"
Version="unknown"
if [ -f /opt/apps/tacc_build_rpm/0.9.5/bin/.version ]; then
  Version=$(cat /opt/apps/tacc_build_rpm/0.9.5/bin/.version)
fi


# Defaults:
force=0
gccV="unknown"
intelV="unknown"
pgiV="unknown"
impiV="unknown"
mvapich2V="unknown"
cmpich="unknown"
openmpiV="unknown"
debug="%{nil}"
comp="none"
mpi="none"
mpiV="%{nil}"
build=b

TEMP=`getopt -o hb:fdlg:i:j:p:m:o:c:v --long help,build:,debug,log,gcc:,intel:,pgi:,impi:,,mvapich2:,openmpi:,cmpich:,force,show,version \
     -n 'build' -- "$@"`
if [ $? != 0 ] ; then
  echo "For usage of $0 do: $0 --help"
  echo "Terminating..." >&2 ;
  exit 1 ;
fi

# Note the quotes around `$TEMP': they are essential!
eval set -- "$TEMP"


while true ; do
  case "$1" in
    -v|--version)  version=1;                      shift   ;;
    -f|--force)    force=1;                        shift   ;;
    -h|--help)     help=1;                         shift   ;;
    -b|--build)    build=$2;                       shift 2 ;;
    -d|--debug)    debug=1;                        shift   ;;
    -l|--log)      log=1;                          shift   ;;           
    -g|--gcc)      comp="gcc";     gccV="$2";      shift 2 ;;
    -i|--intel)    comp="intel";   intelV="$2";    shift 2 ;;
    -p|--pgi)      comp="pgi";     pgiV="$2";      shift 2 ;;
    -m|--mvapich2) mpi="mvapich2"; mvapich2V="$2"; shift 2 ;;
    -j|--impi)     mpi="impi";     impiV="$2";     shift 2 ;;
    -c|--cmpich)   mpi="cmpich";   cmpichV="$2";   shift 2 ;;
    -o|--openmpi)  mpi="openmpi";  openmpiV="$2";  shift 2 ;;
    --show)        show=1;                                                  shift   ;;
    --) shift; break;;
    *) break;;
  esac
done

if [ "$version" == 1 ]; then
  echo $NAME $Version
  exit
fi


if [ -n "$help" ]; then
  echo ""
  echo $NAME $Version
  echo ""
  echo "Usage: $0 [-options] name.spec"
  echo "  -h  | --help       : This message "
  echo "  -d  | --debug      : turn on 'is_debug 1'"
  echo "  -l  | --log        : write build to a log file"
  echo "  --show             : print command WITHOUT running it."
  echo ""
  echo "Options to control how the rpm file is built:"
  echo "  -bL | --build L    : rpmbuild build command p prep, c compile, b build all ..."
  echo "                     : (Default is: -bb)"
  echo "  -gV | --gcc=V      : build with gcc         with version V"
  echo "  -iV | --intel=V    : build with intel       with version V"
  echo "  -pV | --pgi=V      : build with pgi         with version V"
  echo "  -jV | --impi=V     : build with impi        with version V"
  echo "  -mV | --mvapich2=V : build with mvapich2    with version V"
  echo "  -cV | --cmpich=V   : build with cray-mpich  with version V"
  echo "  -oV | --openmpi=V  : build with openmpi     with version V"
  echo ""
  echo "To specify a version of a compiler or MPI stack do:"
  echo "     $0 -i15 -m2_1 name.spec"
  echo "OR"
  echo "     $0 --intel=15 --mvapich2=2_1 name.spec"
  echo "will use intel 15 and mvapich2 version 2.1"
  echo ""
  exit
fi


eval "compV=\$${comp}V"
eval "mpiV=\$${mpi}V"

mpiV=$(echo $mpiV | sed -e 's/\./_/g')
compV=$(echo $compV | sed -e 's/\./_/g')

# Build command line:

argA=("-b$build")
logA=("")
pSargA=("")


# Compiler
if [ "$comp" != "none" ]; then
  argA=(${argA[@]}          "--define 'is_$comp$compV 1'" "--define 'compV $compV'")
  pSargA=(${pSargA[@]} "-c" "--define 'is_$comp$compV 1'" "--define 'compV $compV'")
  logA=(${logA[@]} "$comp$compV")
fi

# MPI
if [ "$mpi" != "none" ]; then
   argA=(${argA[@]}          "--define 'is_$mpi 1'" "--define 'mpiV $mpiV'") 
   pSargA=(${pSargA[@]} "-m" "--define 'is_$mpi 1'" "--define 'mpiV $mpiV'")
   logA=(${logA[@]} "${mpi}_$mpiV")
fi

# Debug
if [ "$debug" == 1 ]; then
   logA=(${logA[@]} "debug")
   argA=(${argA[@]}     "--define 'is_debug 1'")
   pSargA=(${pSargA[@]} "--define 'is_debug 1'")
fi

if [ "x$1" = x ]; then
  echo ""
  echo "Quitting:  No spec file specified.  Mind reading in a future release (;->)"
  echo ""
  exit
fi

argA=(${argA[@]}     "${1%%.spec}.spec")
pSargA=(${pSargA[@]} "${1%%.spec}.spec")

if [ -n "$log" ]; then
  logName="${1%%.spec} ${logA[@]}"
  logName=`echo "$logName" | sed -e 's/  */_/g'`
  logName=`echo "$logName" | sed -e 's/_$//g'`
  argA=(${argA[@]} "2>&1 | tee -a $logName.log")
fi
  
# eval parseSpec "${pSargA[@]}"
# if [ "$?" != 0 ]; then
#   if [ "$force" == 0 ]; then
#     echo ""
#     echo "Quitting:  If you wish to build it anyway add \"--force\" to the command line"
#     echo ""
#     exit
#   fi
# fi

if [ -n "$show" ]; then
  echo "rpmbuild  ${argA[@]} "
  exit
fi

if [ -n "$log" ]; then
  rm -f $logName.log
fi

ECHO "rpmbuild  ${argA[@]}"
ECHO "Build Start time: $(date)"

if [ `id -u` = 0 -a -n "$log" ]; then
  chown build: $logName.log
  chmod 644    $logName.log
fi


t1=`date +%s`
eval  rpmbuild "${argA[@]}" 
t2=`date +%s`
numSec=`echo "$t2 - $t1" | bc -q`
runTime=`date -ud @$numSec +%T`
ECHO "Time to build: $runTime ($numSec seconds)"
