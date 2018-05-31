import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("-ngram", "--ngram", help="set n-gram (default is 2(bi-gram))\n"
                                                  "UseAge : python construct_dict.py -ngram 2\n"
                                                  "UseAge : python main.py -ngram 2\n\n")
    parser.add_argument("-corpus", "--corpus", help="load corpus\n"
                                                    "(default is 'corpus')\n")
    parser.add_argument("-dict", "--dict", help="set dictionary file name\n"
                                                "(default is 'dict')\n")
    _args = parser.parse_args()

    return _args


args = get_arguments()

if not args.ngram:
    N_GRAM = 2
else:
    try:
        N_GRAM = int(args.ngram)
    except ValueError:
        print("\nInput Error type of ngram option!\n")
        exit(-1)
    else:
        if N_GRAM < 2 or N_GRAM > 6:
            print("\nInput Error ngram option! (boundary is 2~5)\n")
            exit(-1)

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
