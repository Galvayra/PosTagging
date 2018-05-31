import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("-corpus", "--corpus", help="load corpus\n"
                                                    "(default is 'corpus')\n")
    parser.add_argument("-dict", "--dict", help="set dictionary file name\n"
                                                "(default is 'dict')\n")
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

PATH_CORPUS = "corpus/"
PATH_SAVE = "data/dict/"

START_FLAG = "<s>"
END_FLAG = "</s>"
