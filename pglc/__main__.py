import sys
import json

from .parser import python_grammar_model
from .util import asjson


def main(trace=False):
    try:
        model = python_grammar_model(trace=trace)
    except Exception as e:
        print(e)
        sys.exit(1)

    print(json.dumps(asjson(model), indent=2))


if __name__ == '__main__':
    main()
