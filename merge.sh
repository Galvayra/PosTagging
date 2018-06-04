#/bin/bash

train=0
test=0

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1

if [ $train -eq 0 ]; then
	train="train"
fi

echo
echo "making corpus named $train for train (default name is train)"
echo "It is in the data/dict/ directory"
echo

python merge.py >> data/dict/$train


if [ $test -eq 0 ]; then
	test="test"
fi

echo
echo "making corpus named $test for test (default name is test)"
echo "It is in the data/dict/ directory"
echo
python merge.py -test 1 >> data/dict/$test

echo "=========================="
