#!/bin/bash
#!/bin/bash -xe

ls -alF


if [ -z "$JOB_ID" ]; then
    export JOB_ID=${ENV,var="BUILD_USER_ID"}-${BUILD_NUMBER}
fi

if [ -z "$TOPOLOGY" ]; then
    export TOPOLOGY=$topology
fi

if [ -z "$PUBLIC_IPS" ]; then
    export PUBLIC_IPS=$public_ips
fi

if [ -z "$OVERRIDES" ]; then
    if [ -z "$overrides" ]; then
        export OVERRIDES=$overrides
    fi
fi


if [[ $machines ]]; then
cat > machine_list << EOF
$machines
EOF
fi


# IF THERE IS A MACHINE LIST THEN USE THAT TO BUILD THE ENV FILE
if [ -f machine_list ]; then
    echo "GOT A MACHINE LIST..."

    if [ "X$eucalele_branch" == "X" ]; then
        eucalele_branch = $branch
    fi

    if [ ! -d "eucalele" ]; then
        echo "EUCALELE NOT FOUND SO CLONING IT NOW..."
        git clone --depth 1 http://git.qa1.eucalyptus-systems.com/qa-repos/eucalele.git -b $eucalele_branch
    else
        pushd eucalele
        echo "UPDATING EXISTING EUCALELE REPO..."
        git checkout $eucalele_branch
        git pull origin $eucalele_branch
        popd
    fi

    echo 'Got a machine list, sourcing it now...'
    cat machine_list
    source ./machine_list

    pushd eucalele/deploy-helpers


    python environment_builder.py -n $network -d $build_type -p $PUBLIC_IPS -b $block_storage_type -o $object_storage_type
    echo "DONE WITH ENVIRONMENT BUILDER"
    pwd
    ls -la
    mv environment.yml ../..
    clc="$(cat config_data | grep -i clc| awk '{print $1}')"
    mv config_data ../..
    popd

# NO MACHINE LIST FOUND THEN USE THE ENV INSTEAD...
else
    echo "NO MACHINES PROVIDED SO ATTEMPTING TO USE THE PROVIDED ENV ATTRIBUTE...."
    if [ -f archive.zip ]; then
        unzip -o archive.zip -d .
        mv archive/* .
    else
cat > environment.yml << EOF
$environment
EOF
    fi

fi

if [ $branch = "master" ]; then
  branch='master'
elif [ $branch = "maint-4.1" ]; then
  branch='euca-4.1'
elif [ $branch = "maint-4.0" ]; then
  branch='euca-4.0'
fi

echo "Using cookbook version $branch"

export PYTHONPATH=.:$PYTHONPATH

### Use eutesters virtual environment to install adminapi
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


virtualenv/bin/python adminapi/cloud_admin/cloudview/remote_calyptos.py $clc -b $branch --debug -p foobar  -l environment.yml
#./bin/euca-deploy prepare -b $branch -e environment.yml --debug
#./bin/euca-deploy bootstrap -b $branch -e environment.yml --debug
#./bin/euca-deploy provision -b $branch -e environ