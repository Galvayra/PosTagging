#/bin/bash

train=train
test=test
path=data/data

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1

if ! [ -d $path ]; then
    echo "Making $path directory"
    mkdir $path
fi

if ! [ -f $path/$train ]; then
    echo
    echo "============= making train corpus ==============="
    echo
    echo "making corpus named $train for train (default name is train)"
    echo "It is in the $path directory"
    echo
    python merge.py >> $path/$train
fi

if ! [ -f $path/$test ]; then
    echo
    echo "============= making test corpus ================"
    echo
    echo "making corpus named $test for test (default name is test)"
    echo "It is in the $path directory"
    echo
    python merge.py -set 1 >> $path/$test

    echo "================================================="
    echo
    echo
fi

echo
echo "============= construct dictionary =============="
python construct.py -train $train
echo "================================================="

