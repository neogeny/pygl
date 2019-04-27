import sys
import json

from . import grammars
from .parser import pgl_parser
from .util import asjson


def main(trace=False):
    python_grammar = grammars.load_python_grammar()
    try:
        model = pgl_parser().parse(python_grammar, trace=trace)
    except Exception as e:
        print(e)
        sys.exit(1)

    print(json.dumps(asjson(model), indent=2))


if __name__ == '__main__':
    main()
