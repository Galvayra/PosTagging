from PosTagging.variables import START_FLAG, END_FLAG, UNKNOWN_KEY
import numpy as np

INDEX_OF_FIRST_WORD = 1
ALPHA = 0.5
BETA = 1 - ALPHA


class Hmm:
    def __init__(self, tags, transition_map, transition_reverse_map, emission_map):
        self.__tags = [tag for tag in tags]
        self.__transition_map = transition_map
        self.__transition_reverse_map = transition_reverse_map
        self.__emission_map = emission_map
        self.__sentence_list = list()
        self.__predict_list = list()
        self.__answer_list = list()
        self.method = 1

    @property
    def tags(self):
        return self.__tags

    @property
    def transition_map(self):
        return self.__transition_map

    @property
    def transition_reverse_map(self):
        return self.__transition_reverse_map

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
    def __get_weight_node(self, previous_node, transition_map, _emission_prob=0):
        # node = previous node + transition probability + emission probability
        node = self.__get_np_array(previous_node) + self.__get_np_array(transition_map)
        node += _emission_prob

        return node

    # return 1 by (# of tags) matrix
    @staticmethod
    def __get_np_array(target_node):
        return np.array([weight for weight in target_node.values()])

    # get transition map only tag
    def __get_transition_map(self, tag, is_reverse=False):
        if is_reverse:
            return {key: value for key, value in self.transition_reverse_map[tag].items() if not key == END_FLAG}
        else:
            return {key: value for key, value in self.transition_map[tag].items() if not key == START_FLAG}

    def __get_arg_min_tag(self, node):
        return self.tags[int(np.argmin(node))]

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

    # node == [{tag: prob, .... , tag: prob}, min_tag]
    def __init_node(self, dynamic_program=True):
        if dynamic_program:
            return [{tag: float() for tag in self.tags}, {tag: str() for tag in self.tags}]
        else:
            return {tag: float() for tag in self.tags}

    def tagging(self, observations):
        if self.method == 1:
            self.__viterbi(observations)
        elif self.method == 0:
            self.__forward_backward(observations)

    # dynamic programming using viterbi
    def __viterbi(self, observations):

        # node == [{tag: prob, .... , tag: prob}, min_tag]
        def __append_node__(_word, is_flag=False):
            if is_flag:
                words.append(_word)
            else:
                answer.append(_word[1])
                words.append(_word[0])
                node.append(self.__init_node())

        # calculate node during forward process
        def __compute_node__(_index):
            target_word = words[_index - 1]

            # process of END FLAG
            if target_word == END_FLAG:
                transition_map = self.__get_transition_map(target_word)

                current_node = self.__get_weight_node(node[_index - 2][0], transition_map)
                node.append(self.tags[int(np.argmin(current_node))])

            # process of middle words
            else:
                target_node = node[_index - 1]
                for tag in target_node[0]:
                    emission_prob = self.__get_emission_prob(tag, target_word)
                    transition_map = self.__get_transition_map(tag)

                    # if the word is occur first
                    # process of start word (word_1)
                    if _index == INDEX_OF_FIRST_WORD:
                        transition_prob = self.transition_map[tag][START_FLAG]
                        target_node[0][tag] = emission_prob + transition_prob

                    # process of words (word_2, ... , word_N)
                    else:
                        current_node = self.__get_weight_node(node[_index - 2][0], transition_map, emission_prob)
                        target_node[0][tag] = np.min(current_node)
                        target_node[1][tag] = self.__get_arg_min_tag(current_node)

        def __forward__():
            # for word_1, word_2, ... , word_N, END_FLAG
            for index in range(1, len(observation)):
                word = observation[index]

                # process of word
                if type(word) is tuple:
                    __append_node__(word)
                    __compute_node__(index)

                # process of END FLAG
                elif type(word) is str and word == END_FLAG:
                    __append_node__(word, is_flag=True)
                    __compute_node__(index)

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

    def __forward_backward(self, observations):
        # append node
        def __append_node__(key, word):
            node[key].append(self.__init_node(dynamic_program=False))
            answer[key].append(word[1])
            words[key].append(word[0])

        # transpose weight to probability in the node
        def __trans_probability__(target_node):
            weight_total = sum(weight for weight in target_node.values())

            for tag in target_node:
                target_node[tag] = target_node[tag] / weight_total

        def __compute_node__(method, is_init=False):
            target_word = words[method][-1]
            target_node = node[method][-1]

            # compute initialize transition and emission probability to the first node
            if is_init:

                for tag in target_node:
                    emission_prob = self.__get_emission_prob(tag, target_word)

                    if method == "forward":
                        transition_prob = self.transition_map[tag][START_FLAG]
                        target_node[tag] = transition_prob + emission_prob
                    elif method == "backward":
                        transition_prob = self.transition_reverse_map[tag][END_FLAG]
                        target_node[tag] = transition_prob + emission_prob

            # compute transition and emission probability to the node
            else:
                previous_node = node[method][-2]

                for tag in target_node:
                    emission_prob = self.__get_emission_prob(tag, target_word)

                    # forward
                    if method == "forward":
                        transition_map = self.__get_transition_map(tag)
                        current_node = self.__get_weight_node(previous_node, transition_map, emission_prob)
                        target_node[tag] = np.sum(current_node)
                    # backward
                    elif method == "backward":
                        transition_map = self.__get_transition_map(tag, is_reverse=True)
                        current_node = self.__get_weight_node(previous_node, transition_map, emission_prob)
                        target_node[tag] = np.sum(current_node)

            __trans_probability__(target_node)

        # train node for getting tag using forward and backward
        def __train__(keys):
            # for word_1, word_2, ... , word_N
            for word, word_reverse in zip(observation, list(reversed(observation))):

                # if the word is existed
                if type(word) is tuple:
                    __append_node__("forward", word)
                    __append_node__("backward", word_reverse)

                    for method in keys:
                        if len(node[method]) == INDEX_OF_FIRST_WORD:
                            __compute_node__(method, is_init=True)
                        else:
                            __compute_node__(method)

        # set predict
        def __predict__(keys):
            for node_fwd, node_bkw in zip(node[keys[0]], list(reversed(node[keys[1]]))):
                fwd_node = self.__get_np_array(node_fwd)
                bkw_node = self.__get_np_array(node_bkw)
                current_node = __fwd_bkw_expression__(fwd_node, bkw_node)

                predict[keys[0]].append(self.__get_arg_min_tag(fwd_node))
                predict[keys[1]].append(self.__get_arg_min_tag(bkw_node))
                predict[keys[2]].append(self.__get_arg_min_tag(current_node))

        # expression of forward and backward
        def __fwd_bkw_expression__(node_fwd, node_bkw):
            return node_fwd*ALPHA + node_bkw*BETA

        self.__init_lists()

        for observation in observations:
            if not observation:
                self.predict_list.append(False)
            else:
                node = {"forward": list(), "backward": list()}
                answer = {"forward": list(), "backward": list()}
                words = {"forward": list(), "backward": list()}
                predict = {"forward": list(), "backward": list(), "fwd_bkw": list()}

                __train__(["forward", "backward"])
                __predict__(["forward", "backward", "fwd_bkw"])

                self.__append_lists(sentence=words["forward"], predict=predict["fwd_bkw"], answer=answer["forward"])
