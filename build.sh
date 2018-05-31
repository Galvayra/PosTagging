#/bin/bash

dict=0

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1

if [ $dict -eq 0 ]; then
	dict="dict"
fi

echo
echo "making dictionary named $dict in the data/dict/ directory !!"
echo

python construct.py >> data/dict/$dict


