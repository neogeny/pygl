import tatsu

from ..grammars import load_python_peg_grammar
from .semantics import PythonSemantics
from .tokenizing import PythonTokenizer


__parser = None


def python_parser():
    parser = generated_python_parser()
    if parser:
        return parser

    global __parser
    if __parser is None:
        __parser = model_python_parser()
    return __parser


def generated_python_parser():
    try:
        from .generated import PythonParser
        return PythonParser(tokenizercls=PythonTokenizer, semantics=PythonSemantics())
    except ImportError:
        pass


def model_python_parser():
    grammar = load_python_peg_grammar()
    return tatsu.compile(grammar)


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
