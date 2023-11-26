import importlib.resources


PYTHON_GRAMMAR = 'Grammar'
PYGL_GRAMMAR = 'pygl.ebnf'
PYTHON_PEG_GRAMMAR = 'python.ebnf'


def load_grammar(name):
    package = f'{__package__}'
    filepath = importlib.resources.files() / name
    with filepath.open() as stream:
        return stream.read()


def load_python_grammar():
    return load_grammar(PYTHON_GRAMMAR)


def load_plg_grammar():
    return load_grammar(PYGL_GRAMMAR)


def load_python_peg_grammar():
    return load_grammar(PYTHON_PEG_GRAMMAR)
