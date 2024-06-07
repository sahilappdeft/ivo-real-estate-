import os

# Determine the environment based on whether HTTPS is enabled
# if 'HTTPS' in os.environ and os.environ['HTTPS'] == 'on':
#     # Production environment
#     from .production import *
# else:
#     # Staging environment
from .staging import *
