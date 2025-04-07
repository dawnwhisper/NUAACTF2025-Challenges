import sys
if sys.version_info[:2] != (3, 10):
    print("Python 3.10 is required")
    print("Your Python version is: ", sys.version)
    sys.exit(1)

from secret import *

vm = VM()
vm.run()