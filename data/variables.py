import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("-save", "--save", help="set dictionary file name\n"
                                                "(default is 'dict')\n")
    _args = parser.parse_args()

    return _args


args = get_arguments()

if not args.save:
    NAME_SAVE = "dict"
else:
    NAME_SAVE = args.dict

PATH_CORPUS = "corpus/"
PATH_SAVE = "data/dict/"
START_FLAG = "<s>"
END_FLAG = "</s>"
