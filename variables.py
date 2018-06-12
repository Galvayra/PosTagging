import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


def get_arguments():
    parser.add_argument("-train", "--train", help="load train corpus\n"
                                                  "(default is 'train')\n")
    parser.add_argument("-test", "--test", help="load test corpus\n"
                                                "(default is 'test')\n")
    parser.add_argument("-set", "--set", help="set option whether make test set or not\n"
                                              "(default is 0 (False))\n")
    parser.add_argument("-cut", "--cut", help="set ratio to make test set by cutting train set\n"
                                              "(default is 10)\n")
    parser.add_argument("-dir", "--dir", help="set directory name of saving dictionary\n"
                                              "(default is '$train')\n")
    _args = parser.parse_args()

    return _args


args = get_arguments()

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

if not args.cut:
    CUT_RATIO = 10
else:
    try:
        CUT_RATIO = int(args.cut)
    except ValueError:
        print("\nValueError!\nPlease input a cut option corrected! (2~100) \n")
        exit(-1)
    else:
        if CUT_RATIO < 2 or CUT_RATIO > 100:
            print("\nValueBoundaryError!\nPlease input a cut option (2~100) \n")
            exit(-1)

if not args.dir:
    DIR_DICT = FILE_TRAIN + "/"
else:
    DIR_DICT = args.dir

    if DIR_DICT[-1] != "/":
        DIR_DICT += "/"

PATH_CORPUS = "corpus/"
PATH_RESULT = "Result/"
PATH_DICT = "data/dict/"
PATH_DATA = "data/data/"

START_FLAG = "<s>"
END_FLAG = "</s>"

UNKNOWN_KEY = "#"
