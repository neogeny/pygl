import os
from .global_settings import *  # noqa
__version__ = '0.1.0'
try:
    from .local_settings import *  # noqa
except ImportError:
    pass

DEBUG = os.environ.get('DEBUG', False)
