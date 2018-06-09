from PosTagging.data.dictConstructor import DictConstructor
from PosTagging.data.variables import FILE_TEST, START_FLAG, END_FLAG
from PosTagging.tagger.model import Hmm


class PosTagger(DictConstructor):
    def __init__(self):
        super().__init__()

        # load data
        self.tags = self.load(self.name["tags"])
        self.emission_map = self.load(self.name["emission"])
        self.transition_map = self.load(self.name["transition"])

        # action for system
        self.__action = {
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
        print("1. Input sentence what you want")
        print("   UseAge: print I am a boy\n")
        print("2. Test performance in the system")
        print("   UseAge: test [file]\n")
        print("3. Show manual")
        print("   UseAge: show\n")
        print("4. Exit Program")
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
        hmm = Hmm(self.tags, self.transition_map, self.emission_map)

        while not self.action["exit"]:
            action = self.__input_command()

            if not action:
                print("Error] Please make sure command\n")
            else:
                if action == "print":
                    observations = [self.__get_observation(self.command[1:])]
                    hmm.viterbi(observations)

                elif action == "test":
                    observations = self.__get_observations_from_set()
                    hmm.viterbi(observations)

                elif action == "show":
                    self.__print()

    # get observations
    def __get_observation(self, observation):
        observation = [self.get_key_value(word) for word in observation]

        # if the observation is inputted by user
        # <s> sentence </s>
        if type(observation[0]) is tuple:
            observation.insert(0, START_FLAG)
            observation.append(END_FLAG)

        return observation

    # get observations from test set
    def __get_observations_from_set(self):

        if len(self.command) == 2:
            file_name = self.command[1]
        elif len(self.command) < 2:
            file_name = FILE_TEST
        else:
            print("Error] Please make sure 'test' command\n")
            return

        corpus = self.read_corpus(file_name)

        if corpus:
            return [self.__get_observation(line.split()) for line in corpus]
        else:
            return list()
