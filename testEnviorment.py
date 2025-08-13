import random
import sys
import runpy
from freezegun import freeze_time

random.seed(4000)
with freeze_time("2024-01-01"): 
    runpy.run_path(sys.argv[1], run_name="__main__")