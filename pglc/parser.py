import tatsu

from .grammars import load_plg_grammar
from .semantics import PGLSemantics


def pgl_parser(trace=False):
    pglc_grammar = load_plg_grammar()
    return tatsu.compile(
        pglc_grammar,
        semantics=PGLSemantics(),
        parseinfo=True,
        colorize=True,
        trace=trace,
    )
