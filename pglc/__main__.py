import sys
from pathlib import Path

import docopt

from tatsu.exceptions import FailedParse

from .bootstrap import bootstrap_python_peg_grammar
from .pythonc import python_parser
from .pythonc import parse
from .packcc.codegen import PackCCCodeGenerator
from . import settings

USAGE = """\
{name} - Python Grammar Language Compiler

Usage:
    {name} [options] <file.py>
    {name} --packcc

Options:
    -c --packcc   generate  PackCC grammar
    -t --trace    enable tracing
    -h --help     print this help text
""".format(name=__package__)


def print_python_peg_grammar():
    parser = bootstrap_python_peg_grammar(trace=False)
    print(parser)


def generate_packcc_grammar():
    parser = python_parser()
    grammar = PackCCCodeGenerator().render(parser)
    print(grammar)


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

    if args['--packcc']:
        generate_packcc_grammar()
        sys.exit()

    filename = args['<file.py>']
    trace = args['--trace']

    with Path(filename).open('rb') as f:
        source = f.read()

    sys.setrecursionlimit(4 * sys.getrecursionlimit())
    try:
        parse(source, trace=trace, colorize=True)
    except FailedParse as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
