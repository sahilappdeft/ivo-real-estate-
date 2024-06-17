import os

# Determine the environment based on whether HTTPS is enabled
# if os.getcwd() == "/home/ubuntu/IVO":
#     # Production environment
#     from .production import *
# else:
# Staging environment
from .staging import *
