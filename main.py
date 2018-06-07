import sys
from os import path

try:
    import PosTagging
except ImportError:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from PosTagging.posTagging import PosTagging

if __name__ == '__main__':
    tagger = PosTagging()
    tagger.run()
