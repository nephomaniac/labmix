#!/bin/bash
 venvname='labmix_venv'
 sudo apt install python3 python3-setuptools python3-pip -y
 sudo apt install python3-venv -y
 sudo apt install gcc -y
 git clone git@bitbucket.org:smartrg/labmix.git
 cd labmix
 python3 -m venv $venvname
 source $venvname/bin/activate
#pip install -U pip setuptools
 python setup.py install
 pip install ipython
 echo "all done"
 echo "Run: ipython"
 echo "then try:"
 echo "from lab_utils.net_utils.sshconnection import SshConnection"
