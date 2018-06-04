from PosTagging.data.dataHandler import DataHandler
from collections import OrderedDict
from PosTagging.data.variables import END_FLAG, START_FLAG
import copy


class DataTagger(DataHandler):
    def __init__(self):
        super().__init__()
        self.__transition_prob = OrderedDict()
        self.__emission_prob = OrderedDict()
        self.__tags = dict()

    @property
    def transition_prob(self):
        return self.__transition_prob

    @property
    def emission_prob(self):
        return self.__emission_prob

    @emission_prob.setter
    def emission_prob(self, value):
        self.__emission_prob = value

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

    # set P(word|tag)
    def __set_emission(self, key_tag):
        if type(key_tag) is tuple:
            word = key_tag[0]
            tag = key_tag[1]

            if tag not in self.emission_prob:
                self.emission_prob[tag] = dict()

            if word not in self.emission_prob[tag]:
                self.emission_prob[tag][word] = 1
            else:
                self.emission_prob[tag][word] += 1

    # sort emission_prob
    def __sorted_emission(self):
        emission_prob = copy.deepcopy(self.emission_prob)
        self.emission_prob = OrderedDict()

        for tag in sorted(emission_prob):
            word_dict = emission_prob[tag]

            self.emission_prob[tag] = OrderedDict({word: word_dict[word] for word in sorted(word_dict)})

    # init P(tag(t)|tag(t-1))
    def __init_transition(self):
        tags = sorted(self.tags)

        transition_dict = OrderedDict({tag: dict() for tag in tags})
        self.transition_prob.update({tag: transition_dict for tag in tags})
        self.transition_prob[START_FLAG] = transition_dict

    # set dictionary for POS Tagging
    def set_dict4tagging(self):
        corpus = self.read_corpus()

        for line in corpus:
            line = line.split()

            for i in range(len(line)):
                key_tag = self.get_key_value(line[i].strip())

                self.__set_emission(key_tag)
                self.__set_tags(key_tag)

        # self.__init_transition()
        # print(self.tags)
        # print(self.transition_prob)

        self.__sorted_emission()

        # print(self.emission_prob)
        self.dump(self.emission_prob, dump_name="emission_prob")
