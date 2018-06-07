#/bin/bash

train=0
test=0
path="data/corpus"

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1

if ! [ -d $path ]; then
    echo "Making $path directory"
    mkdir $path
fi

if [ $train -eq 0 ]; then
	train="train"
fi

echo
echo "making corpus named $train for train (default name is train)"
echo "It is in the $path directory"
echo

python merge.py >> $path/$train

if [ $test -eq 0 ]; then
	test="test"
fi

echo
echo "making corpus named $test for test (default name is test)"
echo "It is in the $path directory"
echo
python merge.py -set 1 >> $path/$test

echo "=========================="
