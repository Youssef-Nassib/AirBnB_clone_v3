from importlib import import_module
import sys


try:
    mode_to_check = import_module(sys.argv[1])
    print(mode_to_check.__doc__)
except ModuleNotFoundError as e:
    print(e)
    pass