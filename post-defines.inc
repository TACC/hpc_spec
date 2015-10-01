#
# W. Cyrus Proctor
# John Fonner
#
# 2015-10-01 Updated for verbose print
# 2015-08-25

function vprintf () {
    if [ ${VERBOSE:=0} = 1 ]; then
        printf "$@"
    fi
}
function vcat() {
    if [ ${VERBOSE:=0} = 1 ]; then
        cat "$@"
    fi
}



R='\033[1;31m' # Red
G='\033[1;32m' # Green
B='\033[1;34m' # Blue
NC='\033[0m'   # No Color
W=${NC}        # White    (set to NC for compatability)
F=${NC}        # Flashing (set to NC for compatability)

if [ ${PACKAGE_POST:=0} = 0 ] && [ ${MODULEFILE_POST:=0} = 0 ]; then
  printf "${R}ERROR: Neither \${PACKAGE_POST} nor \${MODULEFILE_POST} are set\n"
  printf "${R}ERROR: Did you modify your spec file post sections?\n"
  printf "${R}Exiting!${NC}\n"
  exit -1
elif [ ${PACKAGE_POST:=0} = 1 ] && [ ${MODULEFILE_POST:=0} = 1 ]; then
  printf "${R}ERROR: Both \${PACKAGE_POST} and \${MODULEFILE_POST} are set\n"
  printf "${R}ERROR: Did you modify your spec file post sections?\n"
  printf "${R}Exiting!${NC}\n"
  exit -1
fi 


vprintf "${F}======================================================================${NC}\n"
vprintf "${F}||${B} TTTTTTTTTTTTTTT     AAAAA      ${W}    /@@@@@@@\        /@@@@@@@\    ${F}||${NC}\n"
vprintf "${F}||${B} TTTTTTTTTTTTTTT    /AAAAA\     ${W}  @@@@@@@@@@@@\    @@@@@@@@@@@@\  ${F}||${NC}\n"
vprintf "${F}||${B}      TTTTT        /AA/${W}A${B}\AA\    ${W} @@@@@/   \@@@@|  @@@@@/   \@@@@| ${F}||${NC}\n"
vprintf "${F}||${B}      TTTTT       /AA/${W}A@A${B}\AA\   ${W}|@@@@/      '''' |@@@@/      '''' ${F}||${NC}\n"
vprintf "${F}||${B}      TTTTT      ,${W}^V@@@@@@@V^${B},  ${R}|CCCC            |CCCC            ${F}||${NC}\n"
vprintf "${F}||${B}      TTTTT      AAAV${W}@@@@@${B}VAAA  ${R} CCCCC    ,CCCC|  CCCCC    ,CCCC| ${F}||${NC}\n"
vprintf "${F}||${B}      TTTTT     /AAV${W}|@/^\@|${B}VAA\ ${R}  CCCCCCCCCCCCC    CCCCCCCCCCCCC  ${F}||${NC}\n"
vprintf "${F}||${B}      TTTTT    /AAA|${W}/     \\\\${B}|AAA\\\\${R}    ^CCCCCCC^        ^CCCCCCC^    ${F}||${NC}\n"
vprintf "${F}======================================================================${NC}\n"
if [ ${PACKAGE_POST:=0} = 1 ]; then
  vprintf "This is the %{RPM_PACKAGE_NAME} subpackage postinstall script\n"
fi
if [ ${MODULEFILE_POST:=0} = 1 ]; then
  vprintf "This is the %{RPM_MODULEFILE_NAME} subpackage postinstall script\n"
fi
# Query rpm after installation for location of canary files -----------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                         # |
  export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                      # |
  export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                       # |
  vprintf "Using default RPM database path:                             %{_dbpath}\n"                                                # |
else                                                                                                                            # |
  export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)               # |
  export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                # |
  vprintf "Using user-specified RPM database path:                      ${RPM_DBPATH}\n"                                             # |
fi                                                                                                                              # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")                # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                  # |
# ---------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
vprintf "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       \n"                        # |
vprintf "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      \n"                        # |
vprintf "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          \n"                        # |
vprintf "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         \n"                        # |
if [ ${PACKAGE_POST:=0} = 1 ]; then                                                                                             # |
  if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                    # |
    echo -e "${R}ERROR: POST_INSTALL_PREFIX is currently set but null or unset"                                    # |
    echo -e "${R}ERROR: tacc_install_canary was not found"                                                         # |
    echo -e "${R}ERROR: Something is not right. Exiting!${NC}"                                                     # |
    exit -1                                                                                                                     # |
  else                                                                                                                          # |
    vprintf "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} \n"                    # |
    vprintf "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}\n"   # |
  fi                                                                                                                            # |
  if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                     # |
    vprintf "${G}POST_MODULE_PREFIX set but null or unset${NC}\n"                                                    # |
    vprintf "${G}Has %{RPM_MODULEFILE_NAME} been installed in this rpm database yet?${NC}\n"                         # |
    vprintf "${G}Install %{RPM_MODULEFILE_NAME} to automatically update %{MODULE_SUFFIX}/%{MODULE_FILENAME}${NC}\n"  # |
  else                                                                                                                          # |
    vprintf "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  \n"                    # |
    vprintf "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  \n"   # |
  fi                                                                                                                            # |
fi                                                                                                                              # |
if [ ${MODULEFILE_POST:=0} = 1 ]; then                                                                                          # |
  if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                    # |
    vprintf "${G}POST_INSTALL_PREFIX is set but null or unset${NC}\n"                                                # |
    vprintf "${G}Has %{RPM_PACKAGE_NAME} been installed in this rpm database yet?${NC}\n"                            # |
    vprintf "${G}Install %{RPM_PACKAGE_NAME} to automatically update %{MODULE_SUFFIX}/%{MODULE_FILENAME}${NC}\n"     # |
  else                                                                                                                          # |
    vprintf "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} \n"                    # |
    vprintf "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}\n"   # |
  fi                                                                                                                            # |
  if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                     # |
    echo -e "${R}ERROR: POST_MODULE_PREFIX is currently set but null or unset"                                     # |
    echo -e "${R}ERROR: tacc_module_canary was not found"                                                          # |
    echo -e "${R}ERROR: Something is not right. Exiting!${NC}"                                                     # |
    exit -1                                                                                                                     # |
  else                                                                                                                          # |
    vprintf "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  \n"                    # |
    vprintf "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  \n"   # |
  fi                                                                                                                            # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
  vprintf "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       \n"                      # |
  vprintf "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         \n"                      # |
  sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}               # |
  sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}                 # |
  vprintf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
  vcat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}            | \
      GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
      GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                          # |
  vprintf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------

