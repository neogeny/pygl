import pkg_resources
from functools import lru_cache


PYTHON_GRAMMAR = 'Grammar'
PGLC_GRAMMAR = 'pglc.ebnf'

@lru_cache()
def load_grammar(name):
    package = f'{__package__}'
    with pkg_resources.resource_stream(package, name) as stream:
        return str(stream.read(), encoding='utf-8')


def load_python_grammar():
    return load_grammar(PYTHON_GRAMMAR)


def load_plg_grammar():
    return load_grammar(PGLC_GRAMMAR)
