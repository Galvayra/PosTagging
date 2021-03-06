from PosTagging.data.fileHandler import FileHandler
from PosTagging.variables import END_FLAG, START_FLAG, FILE_TRAIN, UNKNOWN_KEY
from collections import OrderedDict
import copy
import re
import math

NUM_OF_SMOOTH = 0.01


class DictConstructor(FileHandler):
    def __init__(self):
        super().__init__()
        self.__transition_map = OrderedDict()
        self.__transition_reverse_map = OrderedDict()
        self.__emission_map = OrderedDict()
        self.__tags = OrderedDict()
        self.__name = {
            "tags": "tags",
            "emission": "emission_map",
            "transition": "transition_map",
            "reverse": "transition_reverse_map"
        }

    @property
    def transition_map(self):
        return self.__transition_map

    @transition_map.setter
    def transition_map(self, _dict):
        self.__transition_map = _dict

    @property
    def transition_reverse_map(self):
        return self.__transition_reverse_map

    @transition_reverse_map.setter
    def transition_reverse_map(self, _dict):
        self.__transition_reverse_map = _dict

    @property
    def emission_map(self):
        return self.__emission_map

    @emission_map.setter
    def emission_map(self, _dict):
        self.__emission_map = _dict

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        self.__tags = tags

    @staticmethod
    def get_key_value(word):
        if word == START_FLAG or word == END_FLAG:
            return word

        p = re.compile("[\S]+/[A-Z]+")

        # if the word has WSJ tag
        if p.findall(word):
            word = word.split('/')

            key = ''.join(word[0:-1]).lower()
            value = word[-1].upper()
        # normal word
        else:
            key = word
            value = str()

        return key, value

    @property
    def name(self):
        return self.__name

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

    # if the word can not find in the dictionary, set zero
    def __init_none_emission(self):
        for _, _map in self.emission_map.items():
            _map[UNKNOWN_KEY] = 0

    @staticmethod
    def __sorted_map(_map):
        _map_copied = copy.deepcopy(_map)

        # initialize ordered dict for tag key
        _map = OrderedDict()

        # copy emission map of tag key for sorting
        for tag in sorted(_map_copied):
            word_dict = _map_copied[tag]

            # initialize ordered dict for word key
            _map[tag] = OrderedDict()

            # copy emission map of word key for sorting
            for word in sorted(word_dict):
                _map[tag][word] = word_dict[word]

        return _map

    # initialize transition map
    # Matrix size == (COUNT(tags) + START_FLAG) X ((COUNT(tags) + END_FLAG))
    def __init_transition(self, _map, is_reverse=False):
        # initialize a columns of transition map
        def __init_columns__():
            if is_reverse:
                return {_tag: int() for _tag in tags + [END_FLAG]}
            else:
                return {_tag: int() for _tag in tags + [START_FLAG]}

        tags = sorted(self.tags)

        # initialize a rows of transition map
        _map.update({tag: __init_columns__() for tag in tags})

        if is_reverse:
            _map[START_FLAG] = __init_columns__()
        else:
            _map[END_FLAG] = __init_columns__()

    # calculate maps for getting probability
    def __calculate_map(self, name=""):
        # get total number of frequency
        def __get_total__():
            return sum(_map[_k] for _k in _map)

        # get probability using smoothing
        def __get_probability__():
            prob = float(_map[k] + NUM_OF_SMOOTH) / (total + (len(_map) * NUM_OF_SMOOTH))

            return math.fabs(math.log(prob))

        target_map = dict()

        if name == "transition":
            target_map = self.transition_map
        elif name == "transition_reverse":
            target_map = self.transition_reverse_map
        elif name == "emission":
            target_map = self.emission_map

        # calculate transition map
        for _, _map in target_map.items():
            total = __get_total__()

            for k in _map:
                _map[k] = __get_probability__()

    def __set_transition(self, corpus):
        def __get_tag(word):
            key_tag = self.get_key_value(word)

            if type(key_tag) is tuple:
                return key_tag[1]
            else:
                return key_tag

        def __set_map__(_map, _line):
            tag_given = __get_tag(_line[0].strip())

            for i in range(1, len(_line)):
                tag = __get_tag(_line[i].strip())

                _map[tag][tag_given] += 1
                tag_given = tag

        self.__init_transition(self.transition_map)
        self.__init_transition(self.transition_reverse_map, is_reverse=True)

        # set transition map by reading a corpus
        for line in corpus:
            __set_map__(self.transition_map, self.__get_line(line))
            __set_map__(self.transition_reverse_map, self.__get_line(line, is_reverse=True))

    @staticmethod
    def __get_line(line, is_reverse=False):
        line = START_FLAG + " " + line.strip() + " " + END_FLAG
        line = line.split()

        if is_reverse:
            return list(reversed(line))
        else:
            return line

    # set dictionary for POS Tagging
    def set_dict4tagging(self):
        corpus = self.read_corpus(FILE_TRAIN)

        if corpus:
            for line in corpus:
                # <s> line </s>
                line = self.__get_line(line)

                for i in range(len(line)):
                    key_tag = self.get_key_value(line[i].strip())

                    # set tags
                    self.__set_tags(key_tag)

                    # set emission map
                    self.__set_emission(key_tag)

            self.__init_none_emission()

            # set transition map
            self.__set_transition(corpus)

            # sorted data
            self.tags = OrderedDict({tag: self.tags[tag] for tag in sorted(self.tags)})
            self.emission_map = self.__sorted_map(self.emission_map)
            self.transition_map = self.__sorted_map(self.transition_map)
            self.transition_reverse_map = self.__sorted_map(self.transition_reverse_map)

            # get probability in the maps
            self.__calculate_map(name="emission")
            self.__calculate_map(name="transition")
            self.__calculate_map(name="transition_reverse")

            # dump data
            self.dump(self.tags, dump_name=self.name["tags"])
            self.dump(self.emission_map, dump_name=self.name["emission"])
            self.dump(self.transition_map, dump_name=self.name["transition"])
            self.dump(self.transition_reverse_map, dump_name=self.name["reverse"])
