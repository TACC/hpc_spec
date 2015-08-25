#
# W. Cyrus Proctor
# John Fonner
# 2015-08-25


R='\033[1;31m' # Red
G='\033[1;32m' # Green
B='\033[1;34m' # Blue
NC='\033[0m'   # No Color
W=${NC}        # White    (set to NC for compatability)
F=${NC}        # Flashing (set to NC for compatability)
printf "${F}======================================================================${NC}\n"
printf "${F}||${B} TTTTTTTTTTTTTTT     AAAAA      ${W}    /@@@@@@@\        /@@@@@@@\    ${F}||${NC}\n"
printf "${F}||${B} TTTTTTTTTTTTTTT    /AAAAA\     ${W}  @@@@@@@@@@@@\    @@@@@@@@@@@@\  ${F}||${NC}\n"
printf "${F}||${B}      TTTTT        /AA/${W}A${B}\AA\    ${W} @@@@@/   \@@@@|  @@@@@/   \@@@@| ${F}||${NC}\n"
printf "${F}||${B}      TTTTT       /AA/${W}A@A${B}\AA\   ${W}|@@@@/      '''' |@@@@/      '''' ${F}||${NC}\n"
printf "${F}||${B}      TTTTT      ,${W}^V@@@@@@@V^${B},  ${R}|CCCC            |CCCC            ${F}||${NC}\n"
printf "${F}||${B}      TTTTT      AAAV${W}@@@@@${B}VAAA  ${R} CCCCC    ,CCCC|  CCCCC    ,CCCC| ${F}||${NC}\n"
printf "${F}||${B}      TTTTT     /AAV${W}|@/^\@|${B}VAA\ ${R}  CCCCCCCCCCCCC    CCCCCCCCCCCCC  ${F}||${NC}\n"
printf "${F}||${B}      TTTTT    /AAA|${W}/     \\\\${B}|AAA\\\\${R}    ^CCCCCCC^        ^CCCCCCC^    ${F}||${NC}\n"
printf "${F}======================================================================${NC}\n"
echo "This is the %{RPM_PACKAGE_NAME} subpackage postinstall script"
# Query rpm after installation for location of canary files ---------------------------------------------------------------------
if [ ${RPM_DBPATH:=/var/lib/rpm} = /var/lib/rpm ]; then                                                                       # |
  export install_canary_path=$(rpm -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)                                    # |
  export  module_canary_path=$(rpm -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)                                     # |
  echo "Using default RPM database path:                             %{_dbpath}"                                              # |
else                                                                                                                          # |
  export install_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_PACKAGE_NAME}    | grep .tacc_install_canary)             # |
  export  module_canary_path=$(rpm --dbpath ${RPM_DBPATH} -ql %{RPM_MODULEFILE_NAME} | grep .tacc_module_canary)              # |
  echo "Using user-specified RPM database path:                      ${RPM_DBPATH}"                                           # |
fi                                                                                                                            # |
export POST_INSTALL_PREFIX=$(echo "${install_canary_path}" | sed "s:/%{INSTALL_SUFFIX}/.tacc_install_canary$::")              # |
export  POST_MODULE_PREFIX=$(echo "${module_canary_path}"  | sed "s:/%{MODULE_SUFFIX}/.tacc_module_canary$::")                # |
# -------------------------------------------------------------------------------------------------------------------------------

# Update modulefile with correct prefixes when "--relocate" flag(s) was specified at install time ---------------------------------
echo "rpm build-time macro module prefix:                          %{MODULE_PREFIX}       "                       > /dev/stderr # |
echo "rpm build-time macro install prefix:                         %{INSTALL_PREFIX}      "                       > /dev/stderr # |
echo "rpm build-time macro MODULE_DIR:                             %{MODULE_DIR}          "                       > /dev/stderr # |
echo "rpm build-time macro INSTALL_DIR:                            %{INSTALL_DIR}         "                       > /dev/stderr # |
if [ ${POST_INSTALL_PREFIX:-x} = x ]; then                                                                                      # |
  echo -e "${R}ERROR: POST_INSTALL_PREFIX is currently set but null or unset"                                     > /dev/stderr # |
  echo -e "${R}ERROR: tacc_install_canary was not found"                                                          > /dev/stderr # |
  echo -e "${R}ERROR: Something is not right. Exiting!"                                                           > /dev/stderr # |
  exit -1                                                                                                                       # |
else                                                                                                                            # |
  echo "rpm post-install install prefix:                             ${POST_INSTALL_PREFIX} "                     > /dev/stderr # |
  echo "rpm package install location:                                ${POST_INSTALL_PREFIX}/%{INSTALL_SUFFIX}"    > /dev/stderr # |
fi                                                                                                                              # |
if [ ${POST_MODULE_PREFIX:-x} = x ]; then                                                                                       # |
  echo -e "${G}POST_MODULE_PREFIX set but null or unset${NC}"                                                     > /dev/stderr # |
  echo -e "${G}Has %{RPM_MODULEFILE_NAME} been installed in this rpm database yet?${NC}"                          > /dev/stderr # |
  echo -e "${G}Install %{RPM_MODULEFILE_NAME} to automatically update %{MODULE_SUFFIX}/%{MODULE_FILENAME}${NC}"   > /dev/stderr # |
else                                                                                                                            # |
  echo "rpm post-install module prefix:                              ${POST_MODULE_PREFIX}  "                     > /dev/stderr # |
  echo "rpm modulefile install location:                             ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}  "    > /dev/stderr # |
fi                                                                                                                              # |
if [ ! ${POST_INSTALL_PREFIX:-x} = x ] && [ ! ${POST_MODULE_PREFIX:-x} = x ]; then                                              # |
  echo "Replacing \"%{INSTALL_PREFIX}\" with \"${POST_INSTALL_PREFIX}\" in modulefile       "                     > /dev/stderr # |
  echo "Replacing \"%{MODULE_PREFIX}\" with \"${POST_MODULE_PREFIX}\" in modulefile         "                     > /dev/stderr # |
  sed -i "s:%{INSTALL_PREFIX}:${POST_INSTALL_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}               # |
  sed -i "s:%{MODULE_PREFIX}:${POST_MODULE_PREFIX}:g" ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}                 # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
  cat ${POST_MODULE_PREFIX}/%{MODULE_SUFFIX}/%{MODULE_FILENAME}            | \
      GREP_COLOR='01;91' grep -E --color=always "$|${POST_INSTALL_PREFIX}" | \
      GREP_COLOR='01;92' grep -E --color=always "$|${POST_MODULE_PREFIX}"                                         > /dev/stderr # |
  printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' - # Print fancy lines                                                   # |
fi                                                                                                                              # |
#----------------------------------------------------------------------------------------------------------------------------------

