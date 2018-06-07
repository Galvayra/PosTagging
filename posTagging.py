from PosTagging.data.dataTagger import DataTagger
from PosTagging.data.variables import FILE_TEST


class PosTagging(DataTagger):
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

        while not self.action["exit"]:
            action = self.__input_command()

            if not action:
                print("Error] Please make sure command\n")
            else:
                if action == "print":
                    self.__tagging_sent(self.command[1:])
                elif action == "test":
                    self.__test()
                elif action == "show":
                    self.__print()

    # test the system by getting performance
    def __test(self):

        if len(self.command) == 2:
            file_name = self.command[1]
        elif len(self.command) < 2:
            file_name = FILE_TEST
        else:
            print("Error] Please make sure 'test' command\n")
            return

        corpus = self.read_corpus(file_name)

        if corpus:
            for line in corpus:
                self.__tagging_sent(line.split())

    # tagging sentence
    def __tagging_sent(self, line):
        line = [self.get_key_value(word) for word in line]

        self.__dynamic(line)

    # dynamic programming using viterbi
    def __dynamic(self, line):
        for word in line:
            pass

    # forward, backward
    def __forward_backward(self, line):
        pass
