import sys
from dataclasses import dataclass, field
from typing import List

from tatsu.exceptions import FailedSemantics


def debug(*args, **kwargs):
    file = kwargs.pop('file', sys.stderr)
    print(*args, file=file, **kwargs)


@dataclass()
class PythonSemantics:
    indent_levels: List[int] = field(default_factory=list, init=False)

    def error(self, msg):
        raise FailedSemantics(msg)

    def current_indent(self):
        return self.indent_levels[-1] if self.indent_levels else 0  # pylint: disable=E1136

    def INDENT(self, ast):
        # debug('INDENT', self.indent_levels, '"%s"' % ast)
        indent = len(ast.strip('\r\n'))
        prev = self.current_indent()
        if not indent or indent <= prev:
            return self.error('Expecting INDENT')
        self.indent_levels.append(indent)

    def DEDENT(self, ast):
        # debug('DEDENT', self.indent_levels, '"%s"' % ast)
        indent = len(ast.strip('\r\n'))
        while self.indent_levels and self.indent_levels[-1] > indent:
            self.indent_levels.pop()

    def EQDENT(self, ast):
        indent = len(ast.strip('\r\n'))
        prev = self.current_indent()
        if indent != prev:
            return self.error('Unexpected change of INDENT')
