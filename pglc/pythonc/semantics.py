from dataclasses import dataclass

from tatsu.exceptions import FailedSemantics

from .tokenizing import (
    PythonTokenizer,
    token,
    ENCODING, TYPE_COMMENT,
)


@dataclass()
class PythonSemantics:
    tokenizer: PythonTokenizer = None

    def set_tokenizer(self, tokenizer):
        self.tokenizer = tokenizer

    def error(self, msg):
        raise FailedSemantics(msg)

    def _match_type(self, type):
        t = self.tokenizer.matchtype(type)
        if not t:
            name = token.tok_name.get(type)
            if name:
                self.error(f'Expecting {name}')
            else:
                self.error('Syntax error')
        return t

    def _(self, _):
        self.tokenizer.eat_comments()

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
