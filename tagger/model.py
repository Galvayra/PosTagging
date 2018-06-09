from PosTagging.data.variables import END_FLAG


class Hmm:
    def __init__(self, tags, transition_map, emission_map):
        self.__tags = tags
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

    # dynamic programming using viterbi
    def viterbi(self, observations):
        def __append_network__(_word, is_flag=False):
            if is_flag:
                network.append({_word: float()})
                answer.append(_word)
            else:
                answer.append(_word[1])
                _word = _word[0]
                network.append({tag: float() for tag in self.tags})

        def __calculate_network__():
            for tag_given in network[i-1]:
                _map = self.transition_map[tag_given]

                for tag in _map:
                    if not tag == END_FLAG:
                        print(tag_given, tag, _map[tag])

        network = list()
        answer = list()
        predict = list()

        for observation in observations:
            for i in range(len(observation)):
                word = observation[i]

                # process of word
                if type(word) is tuple:
                    __append_network__(word)
                    __calculate_network__()

                # process of FLAGS (START, END)
                elif type(word) is str:

                    # process of START FLAG == <s>
                    if word in self.transition_map:
                        __append_network__(word, is_flag=True)

                    # process of END FLAG == </s>
                    else:
                        __append_network__(word, is_flag=True)

        for i in network:
            print(i)



    def forward(self):
        pass

    def backward(self):
        pass
