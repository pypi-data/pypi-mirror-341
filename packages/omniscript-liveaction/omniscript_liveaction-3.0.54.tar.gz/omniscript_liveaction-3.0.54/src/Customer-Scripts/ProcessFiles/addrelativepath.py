# addrelativepath.py

# Add the parent path to Python's search path.

import os
import sys

_file_path = os.path.abspath(os.path.dirname(__file__))
_src_path = os.path.abspath(os.path.join(_file_path, '../..'))
sys.path.insert(0, _src_path)


def do_addrelative_path():
    return
