from PosTagging.data.dataHandler import DataHandler
from collections import OrderedDict
from PosTagging.data.variables import END_FLAG, START_FLAG
import copy


class DataTagger(DataHandler):
    def __init__(self):
        super().__init__()
        self.__transition_map = OrderedDict()
        self.__emission_map = OrderedDict()
        self.__tags = dict()

    @property
    def transition_map(self):
        return self.__transition_map

    @property
    def emission_map(self):
        return self.__emission_map

    @emission_map.setter
    def emission_map(self, value):
        self.__emission_map = value

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

    # set emission probability = P(word(t)|tag(t))
    def __set_emission(self, key_tag):
        if type(key_tag) is tuple:
            word = key_tag[0]
            tag = key_tag[1]

            if tag not in self.emission_map:
                self.emission_map[tag] = dict()

            if word not in self.emission_map[tag]:
                self.emission_map[tag][word] = 1
            else:
                self.emission_map[tag][word] += 1

    # sort emission map
    def __sorted_emission(self):
        emission_map = copy.deepcopy(self.emission_map)
        self.emission_map = OrderedDict()

        # copy emission map for sorting
        for tag in sorted(emission_map):
            word_dict = emission_map[tag]

            self.emission_map[tag] = OrderedDict({word: word_dict[word] for word in sorted(word_dict)})

    # initialize transition map
    # Matrix size == (COUNT(tags) + START_FLAG) X ((COUNT(tags) + END_FLAG))
    def __init_transition(self):
        # initialize a columns of transition map
        def __init_columns(_tags):
            return OrderedDict({_tag: int() for _tag in _tags + [END_FLAG]})

        tags = sorted(self.tags)

        # initialize a rows of transition map
        self.transition_map.update({tag: __init_columns(tags) for tag in tags})
        self.transition_map[START_FLAG] = __init_columns(tags)

    def __calculate(self):
        self.__sorted_emission()

    def __set_transition(self, corpus):
        def __get_tag(word):
            key_tag = self.get_key_value(word)

            if type(key_tag) is tuple:
                return key_tag[1]
            else:
                return key_tag

        self.__init_transition()

        for line in corpus:
            line = line.split()

            # print(line)
            pre_tag = __get_tag(line[0].strip())

            for i in range(1, len(line)):
                tag = __get_tag(line[i].strip())

                self.transition_map[pre_tag][tag] += 1

                pre_tag = tag

    # set dictionary for POS Tagging
    def set_dict4tagging(self):
        corpus = self.read_corpus()

        for line in corpus:
            line = line.split()

            for i in range(len(line)):
                key_tag = self.get_key_value(line[i].strip())

                self.__set_emission(key_tag)
                self.__set_tags(key_tag)

        self.__set_transition(corpus)

        # for k, v in self.transition_map.items():
        #     print(k, v)

        # self.__calculate()
        # self.dump(self.emission_map, dump_name="emission_map")
