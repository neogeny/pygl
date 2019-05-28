import tatsu

from ..grammars import load_python_peg_grammar
from .semantics import PythonSemantics
from .tokenizing import PythonTokenizer


__parser = None


def python_parser():
    global __parser
    if __parser is None:
        grammar = load_python_peg_grammar()
        __parser = tatsu.compile(grammar)
    return __parser


def parse(source, filename='<unknown>', **kwargs):
    # if isinstance(source, bytes):
    #     m = re.search(rb'^\s*#.*coding:\s(\S*)', source)
    #     encoding = m.group(1) if m else 'utf-8'
    #     source = source.decode(encoding=encoding)

    tokenizer = PythonTokenizer(source, filename=filename)
    semantics = kwargs.pop('semantics', None)
    if semantics is None:
        semantics = PythonSemantics()

    parser = python_parser()
    return parser.parse(tokenizer, semantics=semantics, **kwargs)


python_parser()
