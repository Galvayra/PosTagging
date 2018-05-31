import sys
from os import path

try:
    import PosTagging
except ImportError:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from PosTagging.data.dataHandler import DataHandler

if __name__ == '__main__':
    data_handler = DataHandler()
    data_handler.set_dict4tag()
