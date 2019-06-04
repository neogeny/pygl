from dataclasses import dataclass

from tatsu.contexts import ParseContext
from tatsu.exceptions import FailedSemantics

from .tokenizing import (
    PythonTokenizer,
    token,
    ENCODING, TYPE_COMMENT,
)


@dataclass()
class PythonSemantics:
    ctx: ParseContext = None
    tokenizer: PythonTokenizer = None

    def set_context(self, ctx):
        self.ctx = ctx
        self.tokenizer = ctx.tokenizer

    def error(self, msg):
        raise FailedSemantics(msg)

    def _match_type(self, type):
        t = self.tokenizer.matchtype(type)
        if not t:
            name = token.tok_name.get(type)
            other = token.tok_name.get(self.tokenizer.current.type)
            if name:
                self.error(f'Expecting {name} (not {other})')
            else:
                self.error('Syntax error')
        self.ctx.last_node = t
        return t

    def _(self, _):
        self.tokenizer.eat_comments()

    def name(self, ast):
        self.ctx._check_name(ast)
        return ast

    def NUMBER(self, ast):
        return self._match_type(token.NUMBER)

    def STRING(self, ast):
        return self._match_type(token.STRING)

    def NAME(self, ast):
        return self._match_type(token.NAME)

    def NEWLINE(self, ast):
        return self._match_type(token.NEWLINE)

    def INDENT(self, ast):
        return self._match_type(token.INDENT)

    def DEDENT(self, ast):
        return self._match_type(token.DEDENT)

    def EQDENT(self, ast):
        if self.tokenizer.token.type in (token.INDENT, token.DEDENT):
            self.error('INDENT/DEDENT')

    def ENCODING(self, ast):
        return self._match_type(ENCODING)

    def TYPE_COMMENT(self, ast):
        return self._match_type(TYPE_COMMENT)
