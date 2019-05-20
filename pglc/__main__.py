import sys
from pathlib import Path

import docopt

from tatsu.exceptions import FailedParse

from .bootstrap import bootstrap_python_peg_grammar
from .pythonc import python_parser
from .pythonc import parse
from . import settings

USAGE = """\
{name} - Python Grammar Language Compiler

Usage:
    {name} [options] <file.py>

Options:
    -t --trace  enable tracing
    -h --help   print this help text
""".format(name=__package__)


def print_python_peg_grammar():
    parser = bootstrap_python_peg_grammar(trace=False)
    print(parser)


def _pending_cmdline_options():
    bootstrap_python_peg_grammar(trace=False)
    print_python_peg_grammar()
    try:
        parser = python_parser()
        print(parser)
    except Exception as e:
        print(e)


def main():
    args = docopt.docopt(str(USAGE), version=settings.__version__)
    filename = args['<file.py>']
    trace = args['--trace']

    with Path(filename).open() as f:
        source = f.read()

    try:
        parse(source, trace=trace, colorize=True)
    except FailedParse as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
