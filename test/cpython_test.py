from pathlib import Path

import pytest

from pglc.pythonc import parse
from pglc.settings import CPYTHON_PATH


def _get_cpython_python_source():
    for pathname in CPYTHON_PATH.glob('**/*.py'):
        yield pathname
        break


cpython_python_sources = _get_cpython_python_source()


def _stem(value):
    if isinstance(value, Path):
        return str(value.relative_to(CPYTHON_PATH))


@pytest.mark.parametrize("filepath", cpython_python_sources, ids=_stem)
def test_filepath(filepath):
    assert filepath is not None
    try:
        with filepath.open('r') as f:
            source = f.read()
    except UnicodeDecodeError:
        pytest.skip('unsupported encoding')

    assert source is not None
    try:
        parse(source, start='file_input', trace=True, colorize=True)
    except Exception as e:
        raise e from None
    pytest.fail('wanna see trace')
