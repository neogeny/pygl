from pathlib import Path

import pytest

from pglc.settings import CPYTHON_PATH


def _get_cpython_python_source():
    yield from CPYTHON_PATH.glob('**/*.py')


cpython_python_sources = _get_cpython_python_source()


def _stem(value):
    if isinstance(value, Path):
        return str(value.relative_to(CPYTHON_PATH))


@pytest.mark.parametrize("filepath", cpython_python_sources, ids=_stem)
def test_here(filepath):
    assert filepath is not None
    try:
        with filepath.open('r') as f:
            source = f.read()
    except UnicodeDecodeError:
        pytest.skip('unsupported encoding')
