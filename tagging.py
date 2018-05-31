from PosTagging.data.dataHandler import DataHandler
from collections import OrderedDict


class PosTagging(DataHandler):
    def __init__(self):
        super().__init__()
        self.__transition_prob = OrderedDict()
        self.__emission_prob = OrderedDict()
        self.__tags = list()

    @property
    def transition_prob(self):
        return self.__transition_prob

    @property
    def emission_prob(self):
        return self.__emission_prob

    @property
    def tags(self):
        return self.__tags

    # set dictionary for POS Tagging
    def set_dict4tag(self):
        corpus = self.read_corpus()

        for line in corpus:
            for word in line.split():
                word_tag = self.get_key_value(word)
                print(word_tag)
