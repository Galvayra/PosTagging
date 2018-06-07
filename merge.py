import sys
from os import path

try:
    import PosTagging
except ImportError:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from PosTagging.data.corpusReader import CorpusReader

if __name__ == '__main__':
    corpus_reader = CorpusReader()
    corpus_reader.print_sent_in_corpus()
