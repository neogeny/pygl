from dataclasses import dataclass, field
from typing import List

from tatsu.tokenizing import Tokenizer
from tatsu.exceptions import FailedSemantics
from tatsu.util import debug

from ..settings import DEBUG


@dataclass()
class PythonSemantics:
    indent_levels: List[int] = field(default_factory=list, init=False)
    tokenizer: Tokenizer = None

    def set_tokenizer(self, tokenizer):
        self.tokenizer = tokenizer

    def error(self, msg):
        raise FailedSemantics(msg)

    def current_indent(self):
        return self.indent_levels[-1] if self.indent_levels else 0  # pylint: disable=E1136

    def INDENT(self, ast):
        if DEBUG:
            debug('INDENT', self.indent_levels, '"%s"' % ast)
        indent = len(ast.strip('\r\n'))
        prev = self.current_indent()
        if not indent or indent <= prev:
            self.error('Expecting INDENT')
        self.indent_levels.append(indent)

    def DEDENT(self, ast):
        if self.tokenizer.atend():
            return
        if DEBUG:
            debug('DEDENT', self.indent_levels, '"%s"' % ast)
        indent = len(ast.strip('\r\n'))
        prev = self.current_indent()
        if indent < prev:
            self.indent_levels.pop()
        elif not self.tokenizer.atend():
            self.error('Expecting DEDENT')

    def EQDENT(self, ast):
        if DEBUG:
            debug('EQDENT', self.indent_levels, '"%s"' % ast)
        indent = len(ast.strip('\r\n'))
        prev = self.current_indent()
        if not self.tokenizer.atend() and indent != prev:
            self.error('Unexpected change of INDENT')
