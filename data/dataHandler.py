from .variables import *
import re
import json
import os
from collections import OrderedDict


class MyDataHandler:
    def __init__(self):
        self.__vocab_dict = OrderedDict()
        self.__sent_list = list()
        self.__sentence = str()
        self.__is_sent = False
        self.end_flag = END_FLAG

    @property
    def vocab_dict(self):
        return self.__vocab_dict

    @property
    def sent_list(self):
        return self.__sent_list

    @sent_list.setter
    def sent_list(self, sentence):
        self.__sent_list.append(sentence)

    @property
    def sentence(self):
        return self.__sentence

    @sentence.setter
    def sentence(self, sentence):
        self.__sentence = sentence

    @property
    def is_sent(self):
        return self.__is_sent

    @is_sent.setter
    def is_sent(self, is_sent):
        self.__is_sent = is_sent

    def init_sentence(self, word=str()):
        self.sentence = word

    @staticmethod
    def __corpus_generator():
        target_path = os.path.normpath(PATH_CORPUS)

        for path, _, files in os.walk(target_path):
            if files:
                for file in files:
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

    def construct_dict(self):
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

    def get_key(self, word, tagging=True):
        if word == self.end_flag:
            return word

        word = word.split('/')

        if len(word) > 1:
            if tagging:
                key = word[0].lower() + "/" + word[1].upper()
            else:
                key = word[0].lower()
        else:
            key = word[0].lower()

        return key

    def get_key_from_sent(self):
        sent_list = self.sentence.split()
        key = sent_list[len(sent_list):]

        return " ".join(key)

    # initialize vocab using count
    def __init_vocab_dict(self, n_gram):
        for sentence in self.sent_list:
            sentence = sentence.split()
            for i in range(len(sentence) + 1 - n_gram):
                keys = [self.get_key(sentence[j], tagging=False) for j in range(i, i + n_gram)]
                key = ' '.join(keys[0:-1])

                # vocab = { key: [ num of key, { given key: num of given key, ... , } ],
                #                   ... ,
                #         }
                if key not in self.vocab_dict:
                    self.vocab_dict[key] = [1, OrderedDict()]
                else:
                    self.vocab_dict[key][0] += 1

    def __extend_vocab_dict(self, n_gram):
        for sentence in self.sent_list:
            sentence = sentence.split()
            for i in range(len(sentence) + 1 - n_gram):
                keys = list()

                for j in range(i, i + n_gram):
                    if j == i + n_gram - 1:
                        keys.append(self.get_key(sentence[j], tagging=True))
                    else:
                        keys.append(self.get_key(sentence[j], tagging=False))

                key = ' '.join(keys[0:-1])
                target_key = keys[-1]
                prob_dict = self.vocab_dict[key][1]

                if target_key not in prob_dict:
                    prob_dict[target_key] = 1
                else:
                    prob_dict[target_key] += 1

    def __set_probability(self):
        for value in self.vocab_dict.values():
            total = value[0]
            prob_dict = value[1]

            for key in prob_dict:
                prob_dict[key] = prob_dict[key] / total

    # set vocab for counting
    def __set_vocab_dict(self):
        self.__init_vocab_dict()
        self.__extend_vocab_dict()
        self.__set_probability()

    def print_dict(self):
        keys = sorted(self.vocab_dict.keys())

        print("\n===============================\n")
        print("Vocab Size -", len(keys), "\n\n")
        for key in keys:
            print(key.ljust(30), self.vocab_dict[key])

    def dump(self):
        def __sorted(vocab_dict):
            dump_dict = OrderedDict()

            for key in sorted(vocab_dict.keys()):
                dump_dict[key] = vocab_dict[key]

            return dump_dict

        try:
            with open(PATH_SAVE + NAME_SAVE, 'w') as w_file:
                json.dump(__sorted(self.vocab_dict), w_file, indent=4)
                print("\n\nSuccess Save File !! \n")
                print("File name is", "'" + NAME_SAVE + "'", "in the", "'" + PATH_SAVE[:-1] + "'", "directory", "\n\n")
        except FileNotFoundError:
            print("Can not save dump file!\n\n")

    def can_load(self):
        def __load(vocab_dict):
            for k in sorted(vocab_dict.keys()):
                self.vocab_dict[k] = vocab_dict[k]
        try:
            with open(PATH_SAVE + NAME_SAVE, 'r') as r_file:
                __load(json.load(r_file))
                print("\nSuccess loading from", "'" + NAME_SAVE + "'", "!!\n\n")
                return True
        except FileNotFoundError:
            print("\nCan not find to load file!\n\n")
            return False
