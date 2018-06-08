### POS Tagging ###

First) build dictionary

	you can build it easy to use build shell script
	UseAge: ./build.sh --train "train" --test "test"

	merge.py is making dataset of train and test which is in corpus dir
	Plus, please make sure saving them in the 'data/data' dir
	UseAge: python merge.py > data/data/"train"
		python merge.py set -1 > data/data/"test"

	construct.py is building dictionary in order to POS tagging
	UseAge: python construct.py -train "train"

