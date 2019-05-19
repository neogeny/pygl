import re
from pathlib import Path

import pytest

from pglc.pythonc import parse
from pglc.settings import CPYTHON_PATH


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
    try:
        with filepath.open('rt') as f:
            return f.read()
    except UnicodeDecodeError:
        with filepath.open('rb') as f:
            return f.read()


@pytest.mark.parametrize("filepath", cpython_python_sources, ids=_stem)
def test_filepath(filepath):
    source = load_filepath(filepath)
    assert source is not None

    try:
        parse(source, start='file_input', trace=True, colorize=True)
    except Exception as e:
        raise e from None
