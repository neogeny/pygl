import sys
from pathlib import Path

import docopt

from tatsu.exceptions import FailedParse
from tatsu.codegen.python import PythonCodeGenerator

from .bootstrap import bootstrap_python_peg_grammar
from .parser import python_parser, model_python_parser
from .parser import parse
from .peg.packcc import PackCCCodeGenerator
from .peg.leg import LEGCodeGenerator
from . import settings

USAGE = """\
{name} - Python Grammar Language Compiler

Usage:
    {name} [options] <file.py>
    {name} --gen
    {name} --leg
    {name} --peg

Options:
    -g --gen       generate Python parser
    -p --peg       generate a peg/PackCC grammar
    -l --leg       generate a leg grammar
    -t --trace     enable tracing
    -h --help      print this help text
""".format(name=__package__)


def print_python_peg_grammar():
    parser = bootstrap_python_peg_grammar(trace=False)
    print(parser)


def generate_python_parser():
    parser = model_python_parser()
    grammar = PythonCodeGenerator().render(parser)
    print(grammar)


def generate_packcc_grammar():
    parser = python_parser()
    grammar = PackCCCodeGenerator().render(parser)
    print(grammar)


def generate_leg_grammar():
    parser = python_parser()
    grammar = LEGCodeGenerator().render(parser)
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

    if args['--gen']:
        generate_python_parser()
        sys.exit()
    if args['--leg']:
        generate_leg_grammar()
        sys.exit()
    if args['--peg']:
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
