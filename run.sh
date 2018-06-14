#/bin/bash

path=data/dict
train=train
dir=$train

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1

echo
echo "access directory - $dir in $path"
echo
python main.py -dir $dir

