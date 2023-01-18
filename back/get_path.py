from inspect import getsourcefile
from os.path import abspath

def get_path():
    return abspath(getsourcefile(lambda:0))[:-16]
