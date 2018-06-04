from .variables import *
from PosTagging.data.dataReader import DataReader
import re
import os


class DataHandler(DataReader):
    def __init__(self):
        super().__init__()
        self.__sentence = str()

    @property
    def sentence(self):
        return self.__sentence

    @sentence.setter
    def sentence(self, sentence):
        self.__sentence = sentence

    def init_sentence(self, word=str()):
        self.sentence = word

    @staticmethod
    def __corpus_generator():
        target_path = os.path.normpath(PATH_CORPUS)

        for path, _, files in os.walk(target_path):
            if files:
                for file in files:
                    # making test corpus
                    if IS_TEST and path == PATH_CORPUS + PATH_TEST:
                        yield path + '/' + file
                    # making train corpus
                    elif not IS_TEST and not path == PATH_CORPUS + PATH_TEST:
                        yield path + '/' + file

    @staticmethod
    def __read_corpus(path):
        try:
            with open(path, 'r') as r_file:
                lines = r_file.readlines()
                return lines
        except FileNotFoundError:
            print("Can not find read file -", path, "\n\n")
            return list()

    def print_sent_in_corpus(self):
        corpus_gen = self.__corpus_generator()

        # A-Za-z.,? / A-Za-z.,?     all of words
        # A-Za-z.,? / A-Z           for only word
        p = re.compile("[\S]+/[\S]+")
        p_end = re.compile("[\S]+/\.")

        for corpus in corpus_gen:
            for line in self.__read_corpus(corpus):

                p_list = p.findall(line)

                if p_list:
                    p_end_list = p_end.findall(' '.join(p_list))
                    self.sentence += ' '.join(p_list) + ' '

                    if p_end_list:
                        self.__set_sentence()

                if line[0] is "=":
                    self.__set_sentence()

    # get original sentence
    def __set_sentence(self):
        p = re.compile("[\S]+/[A-Z]+")

        # making sentence of words not including special character
        self.sentence = ' '.join(p.findall(self.sentence))

        if len(self.sentence.split()) > 1:
            # <s> sentence </s>
            self.sentence = START_FLAG + " " + self.sentence + " " + END_FLAG
            print(self.sentence)

        self.sentence = str()
