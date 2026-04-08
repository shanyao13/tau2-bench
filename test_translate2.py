import sys
import os
sys.path.insert(0, os.path.abspath("src"))
import litellm
print(litellm.__version__)
