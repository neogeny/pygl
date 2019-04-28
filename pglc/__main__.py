import sys
import json

from . import parser
from .util import asjson


def main(trace=False):
    try:
        model = parser.python_grammar_model(trace=trace)
    except Exception as e:
        print(e)
        sys.exit(1)

    # print(json.dumps(asjson(model), indent=2))
    # print(model.genpython())
    print(parser.python_grammar_model())


if __name__ == '__main__':
    main()
