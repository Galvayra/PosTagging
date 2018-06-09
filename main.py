import sys
from os import path

try:
    import PosTagging
except ImportError:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from PosTagging.tagger.posTagger import PosTagger

if __name__ == '__main__':
    tagger = PosTagger()
    tagger.run()
