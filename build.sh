#/bin/bash

train=train
test=test
path=data/data
dir=$train
ratio=10
new=0

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1

if ! [ -d $path ]; then
    echo "Making $path directory"
    mkdir $path
fi

if [ $new -eq 1 ]; then
    if [ -f $path/$train ]; then
        echo
        echo "Remove $train"
        rm -r $path/$train
    fi

    if [ -f $path/$test ]; then
        echo
        echo "Remove $test"
        rm -r $path/$test
    fi
fi

if ! [ -f $path/$train ]; then
    echo
    echo "============= making train corpus ==============="
    echo
    echo "Cut Ratio - $ratio"
    echo "making corpus named $train for train (default name is train)"
    echo "It is in the $path directory"
    echo
    python merge.py -cut $ratio >> $path/$train
fi

if ! [ -f $path/$test ]; then
    echo
    echo "============= making test corpus ================"
    echo
    echo "Cut Ratio - $ratio"
    echo "making corpus named $test for test (default name is test)"
    echo "It is in the $path directory"
    echo
    python merge.py -cut $ratio -set 1 >> $path/$test

    echo "================================================="
    echo
    echo
fi


echo
echo "the directory name - $dir for dictionary"
echo
echo "============= construct dictionary =============="
python construct.py -dir $dir -train $train
echo "================================================="

