from PosTagging.data.variables import *
from collections import OrderedDict
import json


class DataReader:
    def __init__(self):
        pass

    @staticmethod
    def dump(vocab_dict):
        def __sorted(_vocab_dict):
            dump_dict = OrderedDict()

            for key in sorted(_vocab_dict.keys()):
                dump_dict[key] = _vocab_dict[key]

            return dump_dict

        try:
            with open(PATH_SAVE + SAVE_DICT, 'w') as w_file:
                json.dump(__sorted(vocab_dict), w_file, indent=4)
                print("\n\nSuccess Save File !! \n")
                print("File name is", "'" + SAVE_DICT + "'", "in the", "'" + PATH_SAVE[:-1] + "'", "directory", "\n\n")
        except FileNotFoundError:
            print("Can not save dump file!\n\n")

    @staticmethod
    def read_corpus():
        try:
            with open(PATH_SAVE + SAVE_CORPUS, 'r') as r_file:
                return r_file.readlines()
        except FileNotFoundError:
            print("\nCan not find to read corpus!\n\n")
            exit(-1)

    # @staticmethod
    # def can_load():
    #     def __load(vocab_dict):
    #         for k in sorted(vocab_dict.keys()):
    #             vocab_dict[k] = vocab_dict[k]
    #
    #     try:
    #         with open(PATH_SAVE + SAVE_DICT, 'r') as r_file:
    #             __load(json.load(r_file))
    #             print("\nSuccess loading from", "'" + SAVE_DICT + "'", "!!\n\n")
    #             return True
    #     except FileNotFoundError:
    #         print("\nCan not find to load file!\n\n")
    #         return False
