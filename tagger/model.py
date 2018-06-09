from PosTagging.data.variables import START_FLAG, END_FLAG, UNKNOWN_KEY
import numpy as np

INDEX_OF_FIRST_WORD = 1


class Hmm:
    def __init__(self, tags, transition_map, emission_map):
        self.__tags = [tag for tag in tags]
        self.__transition_map = transition_map
        self.__emission_map = emission_map

    @property
    def tags(self):
        return self.__tags

    @property
    def transition_map(self):
        return self.__transition_map

    @property
    def emission_map(self):
        return self.__emission_map

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
        def __calculate_node__():
            target_word = words[index - 1]

            # process of END FLAG
            if target_word == END_FLAG:
                current_network = self.__get_weight_node(target_word, node[index - 2][0])
                node.append(self.tags[int(np.argmin(current_network))])
            else:
                target_node = node[index - 1]
                for tag in target_node[0]:
                    emission_prob = self.__get_emission_prob(tag, target_word)

                    # if the word is occur first
                    # process of start word (word_1)
                    if index == INDEX_OF_FIRST_WORD:
                        transition_prob = self.transition_map[tag][START_FLAG]
                        target_node[0][tag] = emission_prob + transition_prob

                    # process of words (word_2, ... , word_N)
                    else:
                        current_network = self.__get_weight_node(tag, node[index - 2][0], emission_prob)
                        target_node[0][tag] = np.min(current_network)
                        target_node[1][tag] = self.tags[int(np.argmin(current_network))]

        # predict tags by back tracking
        def __back_tracking__():
            predict.insert(0, node.pop())

            for target_node in reversed(node):
                tag = predict[-1]
                predict.insert(0, target_node[1][tag])

            predict.pop(0)

        # forward
        for observation in observations:
            if not observation:
                print("\nThere is no observation!\n")
            else:
                node = list()
                answer = list()
                words = list()
                predict = list()

                # for word_1, word_2, ... , word_N, END_FLAG
                for index in range(1, len(observation)):
                    word = observation[index]

                    # process of word
                    if type(word) is tuple:
                        __append_node__(word)
                        __calculate_node__()

                    # process of END FLAG
                    elif type(word) is str and word == END_FLAG:
                        __append_node__(word, is_flag=True)
                        __calculate_node__()

                __back_tracking__()
                print()
                print(predict)
                print(answer)
                print()

    def forward(self):
        pass

    def backward(self):
        pass
