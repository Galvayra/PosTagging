from PosTagging.data.variables import *
from collections import OrderedDict
import json


class DataReader:
    def __init__(self):
        pass

    @staticmethod
    def dump(data, dump_name):
        def __sorted(_dict):
            dump_dict = OrderedDict()

            for key in sorted(_dict.keys()):

                # if value is dictionary, do sort for readability
                if type(_dict[key]) is dict:
                    dump_sub_dict = OrderedDict()
                    for sub_key in sorted(_dict[key].keys()):
                        dump_sub_dict[sub_key] = _dict[key][sub_key]

                    dump_dict[key] = dump_sub_dict
                else:
                    dump_dict[key] = _dict[key]

            return dump_dict

        try:
            with open(PATH_SAVE + dump_name, 'w') as w_file:
                json.dump(__sorted(data), w_file, indent=4)
                print("\n\nSuccess Save File !! \n")
                print("File name is", "'" + dump_name + "'", "in the", "'" + PATH_SAVE[:-1] + "'", "directory", "\n\n")
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
