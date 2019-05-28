from dataclasses import dataclass
import token

from tatsu.exceptions import FailedSemantics

from .tokenizing import PythonTokenizer


@dataclass()
class PythonSemantics:
    tokenizer: PythonTokenizer

    def set_tokenizer(self, tokenizer):
        self.tokenizer = tokenizer

    def error(self, msg):
        raise FailedSemantics(msg)

    def _match_type(self, type):
        if not self.tokenizer.matchtype(type):
            self.error(f'Expecting {type}')
        return True

    def _(self, _):
        self.tokenizer.eat_comments()

    def NEWLINE(self, ast):
        return self._match_type(token.NEWLINE)

    def INDENT(self, ast):
        return self._match_type(token.INDENT)

    def DEDENT(self, ast):
        return self._match_type(token.DEDENT)

    def EQDENT(self, ast):
        if self.tokenizer.token.type in (token.INDENT, token.DEDENT):
            self.error('INDENT/DEDENT')
