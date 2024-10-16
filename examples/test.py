# This isn't an example, it just tests all of the examples.
# It doesn't check their output, only whether they raise any exceptions.

from importlib.machinery import SourceFileLoader
import os
import sys
from io import StringIO

out = StringIO()
stdout, sys.stdout = sys.stdout, out

current_dir = os.path.dirname(os.path.realpath(__file__))
for module in os.listdir(current_dir):
	if os.path.join(current_dir, module) == os.path.realpath(__file__):
		continue  # don't import self
	if module.endswith(".py"):
		print("Running:", module, file=stdout)
		try:
			SourceFileLoader(module.split(".", 1)[0], os.path.join(current_dir, module)).load_module()
		except BaseException as e:
			raise e
		print("Tested:", module, file=stdout, end="\n\n")

print("\nNo error in the examples.", file=stdout)
