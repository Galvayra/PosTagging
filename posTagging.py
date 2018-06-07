from PosTagging.data.dataTagger import DataTagger
from PosTagging.data.variables import FILE_TEST


class PosTagging(DataTagger):
    def __init__(self):
        super().__init__()

    def tagging(self):
        corpus = self.read_corpus(FILE_TEST)

        for line in corpus:
            print(line)
            # for word in line.split():
            #     word_tag = self.get_key_value(word)
            #     print(word_tag)
