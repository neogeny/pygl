from .global_settings import *  # noqa
try:
    from .local_settings import *  # noqa
except ImportError:
    pass
