#/bin/bash

corpus=0

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1

if [ $corpus -eq 0 ]; then
	corpus="corpus"
fi

echo
echo "making corpus named $corpus which is consist of sentences in all of corpus"
echo "It is in the data/dict/ directory"
echo

python construct.py >> data/dict/$corpus


