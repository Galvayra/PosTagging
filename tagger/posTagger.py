from PosTagging.data.dictConstructor import DictConstructor
from PosTagging.variables import FILE_TEST, START_FLAG, END_FLAG
from PosTagging.tagger.model import Hmm


class PosTagger(DictConstructor):
    def __init__(self):
        super().__init__()

        if self.can_load():
            # load data
            self.tags = self.load(self.name["tags"])
            self.emission_map = self.load(self.name["emission"])
            self.transition_map = self.load(self.name["transition"])
            self.transition_reverse_map = self.load(self.name["reverse"])
        else:
            self.load_exception()

        # action for system
        self.__action = {
            'set': False,
            'print': False,
            'test': False,
            'show': False,
            'exit': False
        }

        # command will be inputted by user
        self.__command = list()

    @property
    def action(self):
        return self.__action

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, command):
        self.__command = command

    @staticmethod
    def __print():
        print("\n========== POS Tagging ==========\n")
        print("1. Set algorithm for tagging (Default is 1)")
        print("   UseAge: set 1 (vitrebi)")
        print("   UseAge: set 0 (forward-backward)\n")
        print("2. Input sentence what you want")
        print("   UseAge: print I am a boy\n")
        print("3. Test performance in the system")
        print("   UseAge: test [file]\n")
        print("4. Show manual")
        print("   UseAge: show\n")
        print("5. Exit Program")
        print("   UseAge: exit\n")
        print("=================================\n")

    # initialize action
    def __init_action(self):
        for action in self.action:
            self.action[action] = False

    # input command
    def __input_command(self):
        self.__init_action()
        self.command = input("POS Tagging > ").split()

        action = self.command[0].lower()

        if action in self.action:
            self.action[action] = True
            return action
        else:
            return None

    # run the system
    def run(self):
        self.__print()
        hmm = Hmm(self.tags, self.transition_map, self.transition_reverse_map, self.emission_map)

        while not self.action["exit"]:
            action = self.__input_command()

            if not action:
                print("\n[Error] Please make sure command\n")
            else:
                if action == "set":
                    self.__set_method(hmm)

                elif action == "print":
                    observations = [self.__get_observation(self.command[1:])]
                    # hmm.viterbi(observations)
                    # hmm.forward_backward(observations)
                    hmm.tagging(observations)
                    self.__result(hmm.get_result())

                elif action == "test":
                    observations = self.__get_observations_from_set()
                    self.init_write_result(self.file_name + "_Result")

                    # hmm.viterbi(observations)
                    # hmm.forward_backward(observations)
                    hmm.tagging(observations)
                    self.__print_accuracy(self.__result(hmm.get_result()))

                elif action == "show":
                    self.__print()

    def __set_method(self, hmm):
        if len(self.command) == 2:
            try:
                command = int(self.command[1])
            except ValueError:
                print("\n[Error] Please make sure 1 (viterb) or 0 (forward-backward)\n")
            else:
                if command == 1:
                    hmm.method = 1
                    print("\nSuccess set viterbi\n")
                elif command == 0:
                    hmm.method = 0
                    print("\nSuccess set forward-backward\n")
                else:
                    print("\n[Error] Please make sure 1 (viterb) or 0 (forward-backward)\n")
        else:
            print("\n[Error] Please make sure 1 (viterb) or 0 (forward-backward)\n")

    # get observations
    def __get_observation(self, observation):
        if observation:
            observation = [self.get_key_value(word) for word in observation]
            observation = [word for word in observation if type(word) is tuple]

            # if the observation is inputted by user
            # <s> sentence </s>
            observation.insert(0, START_FLAG)
            observation.append(END_FLAG)

            return observation
        else:
            return False

    # get observations from test set
    def __get_observations_from_set(self):

        if len(self.command) == 2:
            self.file_name = self.command[1]
        elif len(self.command) < 2:
            self.file_name = FILE_TEST
        else:
            print("\n[Error] Please make sure 'test' command\n")
            return

        corpus = self.read_corpus(self.file_name)

        if corpus:
            return [self.__get_observation(line.split()) for line in corpus]
        else:
            return list()

    def __result(self, *result):
        # counting for get accuracy
        def __counting__():
            nonlocal match, total

            for _answer, _predict in zip(answer, predict):
                if _answer == _predict:
                    match += 1
                total += 1

        length = int()
        total = int()
        match = int()

        for s, a, p in result:
            for sentence, answer, predict in zip(s, a, p):
                length += 1

                __counting__()
                self.__write_sentence(sentence, answer, predict)

        return length, total, match

    # show the predicted sentence and original sentence in the result file
    def __write_sentence(self, sentence, answer, predict):
        sentence_answer = list()
        sentence_predict = list()

        for word, tag_answer, tag_predict in zip(sentence, answer, predict):
            if tag_answer:
                sentence_answer.append(word + "/" + tag_answer)
            else:
                sentence_answer.append(word)

            sentence_predict.append(word + "/" + tag_predict)

        sentence_original = " ".join(sentence)
        sentence_answer = " ".join(sentence_answer)
        sentence_predict = " ".join(sentence_predict)

        if self.action["print"]:
            print()
            print("Sentence :", sentence_original)
            print("Predict  :", sentence_predict + "\n")
        elif self.action["test"]:
            self.write_sentence("Sentence : " + sentence_original + "\n")
            self.write_sentence("Predict  : " + sentence_predict + "\n")
            self.write_sentence("Answer   : " + sentence_answer + "\n\n")

    # show accuracy in the test set
    @staticmethod
    def __print_accuracy(count):
        length = count[0]
        total = count[1]
        match = count[2]

        print("# of sentences -", length)
        print("# of words     -", total)
        if total:
            print("Accuracy       - %.2f" % ((float(match)/total)*100))
        else:
            print("Accuracy       - 0.00")
        print("\n==============================\n")
