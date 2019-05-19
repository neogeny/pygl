import sys

from .bootstrap import bootstrap_python_peg_grammar
from .pythonc import python_parser


def _pending_cmdline_options():
    bootstrap_python_peg_grammar(trace=False)


def main():
    try:
        parser = python_parser()
    except Exception as e:
        print(e)
        sys.exit(-1)
    print(parser)


if __name__ == '__main__':
    main()
