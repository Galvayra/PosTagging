
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
        network = list()
        answer = list()
        predict = list()

        for observation in observations:
            for i in range(len(observation)):
                word = observation[i]

                # process of word
                if type(word) is tuple:
                    answer.append(word[1])
                    word = word[0]
                    network.append({tag: float() for tag in self.tags})
                    print(word)

                # process of FLAGS (START, END)
                elif type(word) is str:

                    # process of START FLAG == <s>
                    if word in self.transition_map:
                        print(word)
                        # print(word, self.transition_map[word])
                    # process of END FLAG == </s>
                    else:
                        print(word)

    def forward(self):
        pass

    def backward(self):
        pass
