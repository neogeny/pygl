import os
from .global_settings import *  # noqa


__version__ = '0.1.0a2'


try:
    from .local_settings import *  # noqa
except ImportError:
    pass

DEBUG = bool(os.environ.get('DEBUG', False))
