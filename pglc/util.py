from collections import OrderedDict
from collections.abc import Mapping, Iterable

def asjson(obj, seen=None):
    if isinstance(obj, (Mapping, Iterable)):
        # prevent traversal of recursive structures
        if seen is None:
            seen = set()
        elif id(obj) in seen:
            return '__RECURSIVE__'
        seen.add(id(obj))

    if hasattr(obj, '__json__') and type(obj) is not type:
        return obj.__json__()
    elif isinstance(obj, Mapping):
        result = OrderedDict()
        for k, v in obj.items():
            try:
                result[asjson(k, seen)] = asjson(v, seen)
            except TypeError:
                raise
        return result
    elif isinstance(obj, Iterable):
        return [asjson(e, seen) for e in obj]
    else:
        return obj
