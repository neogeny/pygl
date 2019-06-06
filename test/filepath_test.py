import sys
from pathlib import Path

import pytest

from pygl.parser import parse
from pygl.settings import CPYTHON_PATH


@pytest.fixture(scope="session")
def increase_python_stack():
    sys.setrecursionlimit(4 * sys.getrecursionlimit())


def _get_cpython_python_source():
    def filesize(p):
        return p.stat().st_size

    return sorted(
        (
            f for f in CPYTHON_PATH.glob('**/*.py')
            if '/test' not in str(f)
        ),
        key=filesize
    )


cpython_python_sources = _get_cpython_python_source()


def _stem(value):
    if isinstance(value, Path):
        return str(value.relative_to(CPYTHON_PATH))


def load_filepath(filepath):
    with filepath.open('rb') as f:
        return f.read()


@pytest.mark.parametrize("filepath", cpython_python_sources, ids=_stem)
def test_filepath(filepath, trace=False):
    source = load_filepath(filepath)
    assert source is not None

    _ = parse(source, start='file_input', trace=trace, colorize=True)
    return True
