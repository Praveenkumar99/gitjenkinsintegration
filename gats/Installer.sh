#!/bin/bash
#
# INSTALL - Package installation and build setup script for GATS

cd "$( dirname "${BASH_SOURCE[0]}" )"
current_working_dir=$(pwd)
project_name="/GATS"
gats_path=$current_working_dir

echo "gats_path: $gats_path"
current_platform="$(uname -s)"


_install_python_dependencies()
{
   sudo apt-get install libffi-dev
   sudo apt-get install default-jdk
   sudo -H python3 -m pip install --ignore-installed -r Configuration-FW.txt | tee -a pip_package_installer.log

}

_linux_packages_installation()
{

  var=$(apt list "$1" | grep -w "installed" | grep -w "$2")
  if [[ $var == ""  ]];
  then
  echo "$1 NOT INSTALLED"
  sudo apt-get install -y "$1=$2" | tee -a apt_package_installer.log

  else
  echo "$1 ALREADY INSTALLED.. SKIPPING INSTALLING"
  fi
}

_install_linux_packages()
{
  _linux_packages_installation "python3-pip" "8.1.1-2ubuntu0.4"
  _linux_packages_installation "libpython2.7-dev" "2.7.12-1ubuntu0~16.04.3"
  _linux_packages_installation "python3-tk" "3.5.1-1"
  _linux_packages_installation "python3-xlib" "0.14+20091101-5"
  _linux_packages_installation "xsel" "1.2.0-2"

}

_remove_linux_packages()
{
  sudo apt remove -y "$1=$2" | tee -a apt_packages_uninstaller.log
}

_uninstall_linux_packages()
{
  _remove_linux_packages "xsel" "1.2.0-2"
  _remove_linux_packages "python3-xlib" "0.14+20091101-5"
  _remove_linux_packages "python3-tk" "3.5.1-1"

}

_check_bash()
{
    echo "Checking bash requirements"
    if [ -z "$BASH" ] ; then
	echo "Requires bash"
	exit 1
    fi
    bashrc_file_loc="$HOME/.bashrc"
    bash_profile_file_loc="$HOME/.bash_profile"
    use_bash_file=""
    if [ -f $bashrc_file_loc ] ; then
	use_bash_file=$bashrc_file_loc
    elif [ -f $bash_profile_file_loc ] ; then
	use_bash_file=$bash_profile_file_loc
    else
	echo "Please check to see if you have either a .bashrc or .bash_profile in your HOME directory then rerun this installer."
	exit 1
    fi
    echo "Using bash file for environment configuration: $use_bash_file"
    if grep -q "$gats_path/automation/scripts/libraries" "$use_bash_file" ; then
	echo "Found required environment variables"
    else
	echo "Adding required environment variables"
	echo "" >> $use_bash_file
	echo "# # # Adding QuizUI to python path # # #" >> $use_bash_file
	echo "export PYTHONPATH=$gats_path/automation/scripts/libraries:\$PYTHONPATH" >> $use_bash_file
	echo "export TC_TEST=$gats_path" >> $use_bash_file
	source $use_bash_file
	echo "If this is your first time, please exit the shell or source your bash configuration file before continuing."
    fi
}

_check_python()
{
    echo "Checking python version"
    sys_python_version=$( python -c 'import sys; print "".join([str(v) for v in sys.version_info[:3]])' )
    if [[ $sys_python_version -lt "273" ]] ; then
	echo "Requires python version 2.7.3+."
    fi
    echo "done"
}

build_setup()
{
   _check_python
   _check_bash
   if [ "$current_platform" == "Linux" ] ; then
	echo "Current build platform is Linux"
	_install_linux_packages
	_install_python_dependencies
   else
	echo "Unknown Platform"
	exit 1
   fi
}

_clean_linux_environment()
{
   sudo pip3 uninstall -y -r Configuration-FW.txt | tee -a pip_packages_uninstaller.log
   _uninstall_linux_packages

}


if [ "$1" = "clean" ]; then
   if [ "$current_platform" == "Linux" ] ; then
   	_clean_linux_environment
   fi
else
   build_setup
fi

exit 0
