from PosTagging.data.variables import *
import os
import json


class DataReader:
    @staticmethod
    def dump(data, dump_name):
        if not os.path.isdir(PATH_DICT):
            os.mkdir(PATH_DICT)

        try:
            with open(PATH_DICT + dump_name, 'w') as w_file:
                json.dump(data, w_file, indent=4)
                print("\n\nSuccess Save File !! \n")
                print("File name is", "'" + dump_name + "'", "in the", "'" + PATH_DICT[:-1] + "'", "directory", "\n\n")
        except FileNotFoundError:
            print("Can not save dump file!\n\n")

    @staticmethod
    def read_corpus():
        try:
            with open(PATH_CORPUS + FILE_TRAIN, 'r') as r_file:
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
