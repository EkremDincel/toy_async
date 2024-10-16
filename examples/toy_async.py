# This isn't an example.
# This is just a proxy module used by the example scripts.

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
del sys, os

from src.prelude import *
