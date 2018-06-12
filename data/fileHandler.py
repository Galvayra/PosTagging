from PosTagging.variables import PATH_DICT, PATH_DATA, PATH_RESULT, DIR_DICT
import os
import json


class FileHandler:
    def __init__(self):
        self.__write_file = None

    @property
    def write_file(self):
        return self.__write_file

    @write_file.setter
    def write_file(self, write_file):
        self.__write_file = write_file

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

    def dump(self, data, dump_name):
        self.__make_dir(PATH_DICT)
        self.__make_dir(PATH_DICT + DIR_DICT)

        try:
            with open(PATH_DICT + DIR_DICT + dump_name + '.json', 'w') as w_file:
                json.dump(data, w_file, indent=4)
                print("\nSuccess Save File !!")
                print("File name is", "'" + dump_name + "'", "in the", "'" + PATH_DICT[:-1] + "'", "directory", "\n")
        except FileNotFoundError:
            print("\nCan not save dump file!\n")

    @staticmethod
    def load(file_name):
        try:
            with open(PATH_DICT + DIR_DICT + file_name + '.json') as r_file:
                return json.load(r_file)
        except FileNotFoundError:
            print("\nCan not load data -", "'" + file_name + "'", "\n")
            exit(-1)

    def init_write_result(self, file_name):
        self.__make_dir(PATH_RESULT)
        self.__make_dir(PATH_RESULT + DIR_DICT)

        try:
            self.write_file = open(PATH_RESULT + DIR_DICT + file_name, 'w')
        except FileNotFoundError:
            print("\nCan not write result -", "'" + file_name + "'", "\n")
            self.write_file = False

    def write_sentence(self, sentence):
        if self.write_file:
            self.write_file.write(sentence)

    @staticmethod
    def can_load():
        return os.path.isdir(PATH_DICT + DIR_DICT)

    @staticmethod
    def load_exception():
        print("\nThere is no dir having dictionary !")
        print("dir path -", PATH_DICT + DIR_DICT, "\n")
        exit(-1)

    @staticmethod
    def __make_dir(_path):
        if not os.path.isdir(_path):
            os.mkdir(_path)
