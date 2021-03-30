#!/bin/bash
### Use eutesters virtual environment
if [ ! -d virtualenv ];then
  rsync -va /share/eutester-base/ virtualenv/ > eutester-install.log 2>&1
fi

source virtualenv/bin/activate
if [ ! -d adminapi ]; then
  git clone --depth 1 https://github.com/bigschwan/adminapi.git
fi
pushd adminapi
git pull origin master
../virtualenv/bin/python setup.py install
popd
if [ ! -d nephoria ]; then
  git clone --depth 1 https://github.com/bigschwan/nephoria.git
fi
pushd nephoria
git pull origin master
../virtualenv/bin/python setup.py install
popd

# Create a script to dump the config_data from a CLC via adminapi tool...
cat > stress_test.py <<  EOF
$python_script
EOF
virtualenv/bin/python dump_config_data.py -u $user_count -v $vm_count -l $log_level
exit $?