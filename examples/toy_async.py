# This isn't an example
# This is just a proxy module

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src import *

del sys, os