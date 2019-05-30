import sys
from tatsu.util.testing import generic_main
from ..filepath_test import test_filepath


def main():
    generic_main(test_filepath)


if __name__ == '__main__':
    sys.setrecursionlimit(64 * sys.getrecursionlimit())
    print(sys.getrecursionlimit(), 'recursionlimit', file=sys.stderr)
    main()
