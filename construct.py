import sys
from os import path

try:
    import PosTagging
except ImportError:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from PosTagging.data.dictConstructor import DictConstructor

if __name__ == '__main__':
    data_tagger = DictConstructor()
    data_tagger.set_dict4tagging()
