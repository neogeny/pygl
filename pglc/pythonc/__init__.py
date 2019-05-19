import tatsu

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
    semantics = kwargs.pop('semantics', None)
    if semantics is None:
        semantics = PythonSemantics()
    return python_parser().parse(source, semantics=semantics, **kwargs)
