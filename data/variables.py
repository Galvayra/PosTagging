import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("-corpus", "--corpus", help="load corpus\n"
                                                    "(default is 'corpus')\n")
    parser.add_argument("-dict", "--dict", help="set dictionary file name\n"
                                                "(default is 'dict')\n")
    parser.add_argument("-test", "--test", help="test option\n"
                                                "(default is 0)\n")
    _args = parser.parse_args()

    return _args


args = get_arguments()

if not args.dict:
    SAVE_DICT = "dict"
else:
    SAVE_DICT = args.dict

if not args.corpus:
    SAVE_CORPUS = "corpus"
else:
    SAVE_CORPUS = args.corpus

if not args.test:
    IS_TEST = False
else:
    try:
        IS_TEST = int(args.test)
    except ValueError:
        print("\nPlease input a test option corrected!\n")
        exit(-1)
    else:
        if IS_TEST == 1:
            IS_TEST = True
        elif IS_TEST == 0:
            IS_TEST = False
        else:
            print("\nPlease input a test option corrected!\n")
            exit(-1)

PATH_CORPUS = "corpus/"
PATH_TEST = "test"
PATH_SAVE = "data/dict/"

START_FLAG = "<s>"
END_FLAG = "</s>"
