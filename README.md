### POS Tagging ###

First) build dictionary

	you can build it easy to use build shell script

	Options:
		train - set name of training set
		test  - set name of test set
		ratio - set ratio of training and test
		dir   - set name of directory which has dictionary for tagging
		new   - whether making new dataset or not 
	
	UseAge: ./build.sh --train "train_name" --test "test_name" --ratio x --dir "dir_name" --new "1 or 0"


	merge.py is making dataset of train and test which is in corpus dir
	Plus, please make sure saving them in the 'data/data' dir
	UseAge: python merge.py > data/data/"train"

	construct.py is building dictionary in order to POS tagging
	the saving location is 'data/dict/"dir"'
	UseAge: python construct.py -train "train" -dir "dict_1"


Second) run

	main.py is running of POS Tagging
	must use -dir option to know directory where dictionary is in data/dict/"dir"
	UseAge: python main.py -dir train (data/dict/train)

