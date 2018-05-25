#/bin/bash

prep=0
ngram=2

. utils/parse_options.sh || echo "Can't find parse_options.sh" | exit 1


dict="dict_$ngram"

if [ $prep -eq 1 ]; then
	echo
	echo
	echo "Start preprocessing for making dictionary!"
	python preprocessing.py -ngram $ngram -dict $dict
	echo "=========================================="
fi
python main.py -ngram $ngram -dict $dict

