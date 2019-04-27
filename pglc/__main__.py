import sys
import json

import tatsu
from tatsu.util import asjson
from tatsu.exceptions import ParseException
from tatsu.codegen.python import codegen as pythoncg

from . import grammars


def main(trace=False):
    python_grammar = grammars.load_python_grammar()
    pglc_grammar = grammars.load_plg_grammar()

    try:
        parser = tatsu.compile(pglc_grammar)
        ast = parser.parse(python_grammar, trace=trace, colorize=True)
    except ParseException as e:
        print(e)
        sys.exit(1)

    print(json.dumps(asjson(ast), indent=2))
    print(pythoncg(parser))


if __name__ == '__main__':
    main()
