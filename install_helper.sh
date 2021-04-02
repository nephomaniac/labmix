#!/bin/bash
[[ $_ != $0 ]] || { 
	 echo "Error, file must be sourced."
	 echo " Usage:"
	 echo " source $(basename $0)"
	exit 1
}
venvname='labmix_venv'
sudo apt install python3 python3-setuptools python3-pip -y
sudo apt install python3-venv -y
sudo apt install gcc -y
git remote -v | grep labmix > /dev/null
[ $? -ne 0 ] && {
	git clone git@bitbucket.org:smartrg/labmix.git
	cd labmix
}
[ -n "$venvname" ] && {
	echo "virtual env '$venvname' already exists, replace it?"
	read ans
	rep=$(echo $ans | tr '[:upper:]' '[:lower:]')
	[[ "$rep" == "y" ]] && rm -rf $venvname 	
}
python3 -m venv $venvname
source $venvname/bin/activate
#pip install -U pip setuptools
python setup.py install
pip install ipython
python test.py
echo "all done, try the following to test your install:"
[[ "$VIRTUAL_ENV" == "" ]] && echo "source $venvname/bin/activate"
echo "ipython"
echo "Then try:"
echo "	from lab_utils.net_utils.sshconnection import SshConnection"
