import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("-train", "--train", help="load train corpus\n"
                                                  "(default is 'train')\n")
    parser.add_argument("-test", "--test", help="load test corpus\n"
                                                "(default is 'test')\n")
    parser.add_argument("-set", "--set", help="set test option\n"
                                              "(default is 0)\n")
    parser.add_argument("-dict", "--dict", help="set dictionary file name\n"
                                                "(default is 'dict')\n")
    _args = parser.parse_args()

    return _args


args = get_arguments()

if not args.dict:
    FILE_DICT = "dict"
else:
    FILE_DICT = args.dict

if not args.train:
    FILE_TRAIN = "train"
else:
    FILE_TRAIN = args.train

if not args.test:
    FILE_TEST = "test"
else:
    FILE_TEST = args.test

if not args.set:
    IS_TEST = False
else:
    try:
        IS_TEST = int(args.set)
    except ValueError:
        print("\nValueError!\nPlease input a set option corrected! (1 or 0)\n")
        exit(-1)
    else:
        if IS_TEST == 1:
            IS_TEST = True
        elif IS_TEST == 0:
            IS_TEST = False
        else:
            print("\nPlease input a set option corrected! (1 or 0)\n")
            exit(-1)

PATH_CORPUS = "corpus/"
CORPUS_TEST = "test"
PATH_DICT = "data/dict/"
PATH_DATA = "data/data/"

START_FLAG = "<s>"
END_FLAG = "</s>"
