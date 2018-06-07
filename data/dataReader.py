from PosTagging.data.variables import PATH_DICT, PATH_DATA
import os
import json


class DataReader:
    @staticmethod
    def read_corpus(file_name):
        try:
            with open(PATH_DATA + file_name, 'r') as r_file:
                print("\nSuccess read file -", "'" + file_name + "'", '\n')
                return r_file.readlines()
        except FileNotFoundError:
            try:
                with open(file_name, 'r') as r_file:
                    print("\nSuccess read file -", "'" + file_name + "'", '\n')
                    return r_file.readlines()
            except FileNotFoundError:
                print("\nCan not find to read data -", "'" + file_name + "'", "\n")
                return False

    @staticmethod
    def dump(data, dump_name):
        if not os.path.isdir(PATH_DICT):
            os.mkdir(PATH_DICT)

        try:
            with open(PATH_DICT + dump_name + '.json', 'w') as w_file:
                json.dump(data, w_file, indent=4)
                print("\nSuccess Save File !!")
                print("File name is", "'" + dump_name + "'", "in the", "'" + PATH_DICT[:-1] + "'", "directory", "\n")
        except FileNotFoundError:
            print("\nCan not save dump file!\n")

    @staticmethod
    def load(file_name):
        try:
            with open(PATH_DICT + file_name + '.json') as r_file:
                return json.load(r_file)
        except FileNotFoundError:
            print("\nCan not load data -", "'" + file_name + "'", "\n")
            exit(-1)
