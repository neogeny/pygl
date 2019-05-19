import sys

from pglc.bootstrap import parser


def main(trace=False):
    try:
        model = parser.python_grammar_model(trace=trace)
    except Exception as e:
        print(e)
        sys.exit(1)

    print(model)


if __name__ == '__main__':
    main()
