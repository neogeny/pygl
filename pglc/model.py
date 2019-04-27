from dataclasses import dataclass
from typing import List

from .util import asjson, trim, indent


@dataclass(repr=True)
class _Node:
    pos: int
    endpos: int

    @property
    def _type_name(self):
        return type(self).__name__

    def genpython(self):
        return self._type_name

    def asjson(self):
        self.__json__()

    def __json__(self):
        return {
            **{'type': self._type_name},
            **{
                name: asjson(value)
                for name, value in vars(self).items()
                if not name.startswith('_')
            }
        }


@dataclass
class Error(_Node):
    msg : str

    def __bool__(self):
        return False


@dataclass
class Void(_Node):
    def __bool__(self):
        return True

@dataclass
class Indent(_Node):
    level: int


@dataclass
class Dedent(_Node):
    level: int


@dataclass
class Comment(_Node):
    comment: str


@dataclass
class Exp(_Node):
    pass


@dataclass
class _HasExp(_Node):
    exp: Exp


@dataclass
class _Name(_Node):
    name: str


@dataclass
class Token(_Node):
    token: str

    def genpython(self):
        return f'self.match("{self.token}")'


@dataclass
class Ref(_Name):
    def genpython(self):
        return f'self.parse_{self.name}()'


@dataclass
class Seq(_Node):
    seq: List[Exp]

    def genpython(self):
        seq = ',\n'.join(f'lambda: {e.genpython()}' for e in self.seq)
        return trim('''
            self.allof(
            {seq}
            )''').format(seq=indent(seq))


@dataclass
class Choice(_Node):
    options: List[Exp]

    def genpython(self):
        options = ',\n'.join(f'lambda: {o.genpython()}' for o in self.options)
        return trim('''
            self.oneof(
            {options},
            )
            ''').format(options=indent(options))


@dataclass
class Optional(_HasExp):
    def genpython(self):
        return trim(f'{self.exp.genpython()} or self.void()')


@dataclass
class Closure(_HasExp):
    def genpython(self):
        return trim('''
            self.closure(
                lambda: (
            {exp}
                )
            )''').format(exp=indent(self.exp.genpython(), 2))


@dataclass
class PositiveClosure(_HasExp):
    def genpython(self):
        return trim('''
            self.closureplus(
                lambda: (
            {exp}
                )
            )''').format(exp=indent(self.exp.genpython(), 2))


@dataclass
class Rule(_HasExp):
    name: str

    def genpython(self):
        return trim('''
            def parse_{name}(self):
                print('{name}', '>>>', '"%s"' % self.text[self.pos: self.pos + 20])
                self.spaces()
            {exp}
                print('{name}', result, '"%s"' % self.text[self.pos: self.pos + 20])
                return result
        ''').format(
            name=self.name,
            exp=indent(f'result = {self.exp.genpython()}')
        )


@dataclass
class Grammar(_Node):
    rules: List[Rule]

    def genpython(self):
        rules = '\n\n'.join(trim(r.genpython()) for r in self.rules)
        result = trim('''
            import argparse
            from pglc.context import ParseContext
            
            class PythonParser(ParseContext):
            {rules}
                
                
            if __name__ == '__main__':
                argp = argparse.ArgumentParser(description="Simple parser for Python")
                addarg = argp.add_argument
                
                addarg('file',
                       metavar="FILE",
                       help="the input file to parse or '-' for standard input",
                       nargs='?',
                       # default='-',
                )
                addarg('startrule',
                       metavar="STARTRULE",
                       nargs='?',
                       help="the start rule for parsing",
                       default=None,
                )
                args = argp.parse_args()
               
                if args.file:
                    with open(args.file) as f:
                        text = f.read()
                    
                    parser = PythonParser(text)    
                    ast = parser.parse(args.startrule)
                    print(type(ast), ast)
                
            
        ''').format(rules=indent(rules))

        # compile(result, '<text>', mode='exec')
        return result
