from PosTagging.data.dataHandler import DataHandler
from collections import OrderedDict
from PosTagging.data.variables import END_FLAG, START_FLAG


class DataTagger(DataHandler):
    def __init__(self):
        super().__init__()
        self.__transition_prob = dict()
        self.__emission_prob = dict()
        self.__tags = dict()

    @property
    def transition_prob(self):
        return self.__transition_prob

    @property
    def emission_prob(self):
        return self.__emission_prob

    @property
    def tags(self):
        return self.__tags

    @staticmethod
    def get_key_value(word):
        if word == START_FLAG or word == END_FLAG:
            return word

        word = word.split('/')

        key = ''.join(word[0:-1]).lower()
        value = word[-1].upper()

        return key, value

    # set tag
    def __set_tags(self, key_tag):
        if type(key_tag) is tuple:
            tag = key_tag[1]

            if tag not in self.tags:
                self.tags[tag] = 0

            self.tags[tag] += 1

    # set P(tag|word)
    def __set_emission(self, key_tag):
        if type(key_tag) is tuple:
            key = key_tag[0]
            tag = key_tag[1]

            if key not in self.emission_prob:
                self.emission_prob[key] = dict()

            if tag not in self.emission_prob[key]:
                self.emission_prob[key][tag] = 1
            else:
                self.emission_prob[key][tag] += 1

    # set dictionary for POS Tagging
    def set_dict4tag(self):
        corpus = self.read_corpus()

        for line in corpus:
            line = line.split()

            for i in range(len(line)):
                key_tag = self.get_key_value(line[i].strip())

                self.__set_emission(key_tag)
                self.__set_tags(key_tag)

        print(self.tags)
        # self.dump(self.emission_prob, dump_name="emission_prob")
