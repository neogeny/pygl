import sys

from pglc.bootstrap import parser


def bootstrap_python_peg_grammar(trace=False):
    try:
        model = parser.python_grammar_model(trace=trace)
    except Exception as e:
        print(e)
        sys.exit(1)

    print(model)
