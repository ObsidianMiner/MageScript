import random
import sys
import runpy

random.seed(4000)
runpy.run_path(sys.argv[1], run_name="__main__")