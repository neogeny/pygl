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


def trim(text, tabwidth=4):
    """
    Trim text of common, leading whitespace.

    Based on the trim algorithm of PEP 257:
        http://www.python.org/dev/peps/pep-0257/
    """
    if not text:
        return ''
    lines = text.expandtabs(tabwidth).splitlines()
    lines = [x.rstrip() for x in lines]
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    lines = lines[i:]
    maxindent = len(text)
    indent = maxindent
    f = 0
    for line in lines:
        if not line.strip():
           continue
        stripped = line.lstrip()
        indent = min(indent, len(line) - len(stripped))
    trimmed = (
            [line[indent:].rstrip() for line in lines[f:]]
    )
    i = 0
    while i < len(trimmed) and not trimmed[i].strip():
        i += 1
    return '\n'.join(trimmed[i:])


def indent(text, indentation=1, multiplier=4):
    """ Indent the given block of text by indent*4 spaces
    """
    if text is None:
        return ''
    text = str(text)
    if indentation >= 0:
        sindent = ' ' * multiplier * indentation
        text = '\n'.join((sindent + t).rstrip() for t in text.splitlines())
    return text


def trimind(text, depth):
    return indent(trim(text), indentation=depth)
