import tatsu

from . import grammars
from .semantics import PGLSemantics


def pgl_parser(trace=False):
    pgl_grammar = grammars.load_plg_grammar()
    return tatsu.compile(
        pgl_grammar,
        semantics=PGLSemantics(),
        parseinfo=True,
        colorize=True,
        trace=trace,
    )


def python_grammar_model(trace=False):
    python_grammar = grammars.load_python_grammar()
    return pgl_parser().parse(python_grammar, trace=trace)
