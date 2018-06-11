from PosTagging.variables import START_FLAG, END_FLAG, UNKNOWN_KEY
import numpy as np

INDEX_OF_FIRST_WORD = 1


class Hmm:
    def __init__(self, tags, transition_map, emission_map):
        self.__tags = [tag for tag in tags]
        self.__transition_map = transition_map
        self.__transition_reverse_map = None
        self.__emission_map = emission_map
        self.__sentence_list = list()
        self.__predict_list = list()
        self.__answer_list = list()

    @property
    def tags(self):
        return self.__tags

    @property
    def transition_map(self):
        return self.__transition_map

    @property
    def transition_reverse_map(self):
        return self.__transition_reverse_map

    @transition_reverse_map.setter
    def transition_reverse_map(self, transition_reverse_map):
        self.__transition_reverse_map = transition_reverse_map

    @property
    def emission_map(self):
        return self.__emission_map

    @property
    def sentence_list(self):
        return self.__sentence_list

    @sentence_list.setter
    def sentence_list(self, sentence_list):
        self.__sentence_list = sentence_list

    @property
    def predict_list(self):
        return self.__predict_list

    @predict_list.setter
    def predict_list(self, predict_list):
        self.__sentence_list = predict_list

    @property
    def answer_list(self):
        return self.__answer_list

    @answer_list.setter
    def answer_list(self, answer_list):
        self.__sentence_list = answer_list

    # get emission probability == P(word|tag)
    def __get_emission_prob(self, tag, word):
        if word in self.emission_map[tag]:
            return self.emission_map[tag][word]
        else:
            return self.emission_map[tag][UNKNOWN_KEY]

    # when the tag is given, get node of weights as adding emission probability and previous node
    # [word_1, ... , word_N]
    # (from t to N) sigma(P(tag(t)|tag(t-1)) * P(word(t)|tag(t)))
    def __get_weight_node(self, tag, pre_node, _emission_prob=0):
        transition_map = self.__get_transition_map(tag)

        node = np.array([weight + transition_map[tag_given] for tag_given, weight in pre_node.items()])
        node += _emission_prob

        return node

    # get transition map only tag
    def __get_transition_map(self, tag, is_reverse=False):
        if is_reverse:
            return {key: value for key, value in self.transition_map[tag].items() if not key == END_FLAG}
        else:
            return {key: value for key, value in self.transition_map[tag].items() if not key == START_FLAG}

    # initialize lists
    def __init_lists(self):
        self.sentence_list = list()
        self.predict_list = list()
        self.answer_list = list()

    # append lists
    def __append_lists(self, sentence, predict, answer):
        self.sentence_list.append(sentence)
        self.predict_list.append(predict)
        self.answer_list.append(answer)

    # return lists
    def get_result(self):
        return self.sentence_list, self.answer_list, self.predict_list

    # dynamic programming using viterbi
    def viterbi(self, observations):

        # node == [{tag: prob, .... , tag: prob}, min_tag]
        def __append_node__(_word, is_flag=False):
            if is_flag:
                words.append(_word)
            else:
                answer.append(_word[1])
                words.append(_word[0])
                node.append([{tag: float() for tag in self.tags}, {tag: str() for tag in self.tags}])

        # calculate node during forward process
        def __calculate_node__(_index):
            target_word = words[_index - 1]

            # process of END FLAG
            if target_word == END_FLAG:
                current_network = self.__get_weight_node(target_word, node[_index - 2][0])
                node.append(self.tags[int(np.argmin(current_network))])
            else:
                target_node = node[_index - 1]
                for tag in target_node[0]:
                    emission_prob = self.__get_emission_prob(tag, target_word)

                    # if the word is occur first
                    # process of start word (word_1)
                    if _index == INDEX_OF_FIRST_WORD:
                        transition_prob = self.transition_map[tag][START_FLAG]
                        target_node[0][tag] = emission_prob + transition_prob

                    # process of words (word_2, ... , word_N)
                    else:
                        current_network = self.__get_weight_node(tag, node[_index - 2][0], emission_prob)
                        target_node[0][tag] = np.min(current_network)
                        target_node[1][tag] = self.tags[int(np.argmin(current_network))]

        def __forward__():
            # for word_1, word_2, ... , word_N, END_FLAG
            for index in range(1, len(observation)):
                word = observation[index]

                # process of word
                if type(word) is tuple:
                    __append_node__(word)
                    __calculate_node__(index)

                # process of END FLAG
                elif type(word) is str and word == END_FLAG:
                    __append_node__(word, is_flag=True)
                    __calculate_node__(index)

        # predict tags by back tracking
        def __back_tracking__():
            predict.insert(0, node.pop())

            for target_node in reversed(node):
                tag = predict[-1]
                predict.insert(0, target_node[1][tag])

            predict.pop(0)

        self.__init_lists()

        # forward
        for observation in observations:
            if not observation:
                self.predict_list.append(False)
            else:
                node = list()
                answer = list()
                words = list()
                predict = list()

                __forward__()
                __back_tracking__()

                self.__append_lists(sentence=words[:-1], predict=predict, answer=answer)

    def forward_backward(self, observations):
        def __forward__():
            pass

        self.__init_lists()

        # forward
        for observation in observations:
            if not observation:
                self.predict_list.append(False)
            else:
                node = list()
                answer = list()
                words = list()
                predict = list()

                # for START_FLAG, word_1, word_2, ... , word_N, END_FLAG
                for index in range(len(observation)):
                    word = observation[index]

                #     # process of word
                #     if type(word) is tuple:
                #         __append_node__(word)
                #         __calculate_node__()
                #
                #     # process of END FLAG
                #     elif type(word) is str and word == END_FLAG:
                #         __append_node__(word, is_flag=True)
                #         __calculate_node__()
                #
                # __back_tracking__()

    def __forward(self):
        pass

    def __backward(self):
        pass
