import re

import tatsu
from tatsu.buffering import Buffer

from ..grammars import load_python_peg_grammar
from .semantics import PythonSemantics


__parser = None


def python_parser():
    global __parser
    if __parser is None:
        grammar = load_python_peg_grammar()
        __parser = tatsu.compile(grammar)
    return __parser


def parse(source, **kwargs):
    if isinstance(source, bytes):
        m = re.search(rb'^\s*#.*coding:\s(\S*)', source)
        encoding = m.group(1) if m else 'utf-8'
        source = source.decode(encoding=encoding)

    semantics = kwargs.pop('semantics', None)
    parser = python_parser()
    if semantics is None:
        semantics = PythonSemantics()
    return parser.parse(source, semantics=semantics, **kwargs)


python_parser()
