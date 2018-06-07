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
    def read_corpus(file_name):
        try:
            with open(PATH_CORPUS + file_name, 'r') as r_file:
                return r_file.readlines()
        except FileNotFoundError:
            print("\nCan not find to read corpus!\n\n")
            exit(-1)
