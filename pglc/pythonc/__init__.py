import tatsu

from ..grammars import load_python_peg_grammar


def python_parser():
    grammar = load_python_peg_grammar()
    return tatsu.compile(grammar)
