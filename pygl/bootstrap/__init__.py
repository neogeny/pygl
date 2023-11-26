import sys

from pygl.bootstrap import parser


def bootstrap_python_peg_grammar(trace=False):
    return parser.python_grammar_model(trace=trace)
