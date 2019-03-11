#
#
#-------------------------------
# Python Stack Family Definitions
#-------------------------------

# see rpm-dir.inc for the definition of "undefined"

%if %{undefined python_fam}
  %define python_fam error
%endif

%if %{undefined python_label}
  %define python_label error
%endif

########################################################################
##  The idea is to make all decisions in the here then python-load.inc 
##  is simple.
########################################################################

%if "%{is_python}" == "1"
  %if %{undefined pythonV}
    %define python_label 3_7
    %define python_module_version 3.7.0
    %define python_major_version 3
    %define python_minor_version 7
  %endif
  %if "%{pythonV}" == "3_6"
    %define python_label 3_6
    %define python_module_version 3.6.1
    %define python_major_version 3
    %define python_minor_version 6
  %endif
  %if "%{pythonV}" == "3_7"
    %define python_label 3_7
    %define python_module_version 3.7.0
    %define python_major_version 3
    %define python_minor_version 7
  %endif
  %if "%{pythonV}" == "2_7"
    %define python_label 2_7
    %define python_module_version 2.7.15
    %define python_major_version 2
    %define python_minor_version 7
  %endif
  %define python_fam     python
  %define python_fam_ver %{python_fam}%{python_label}
  %define python_module  %{python_fam}%{python_major_version}/%{python_module_version}
  %define python_exec    python%{python_major_version}
  %define pip_exec       pip%{python_major_version}
%endif

%if "%{python_fam}" == "error"
  %{error: You must define which Python you are using!}
  exit
%endif

%if "%{python_label}" == "error"
  %{error: Illegal Python version syntax! Use e.g. --python=3_7}
  exit
%endif
