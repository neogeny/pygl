import re
from dataclasses import dataclass, field
from typing import List

from .model import Error, Comment, Indent, Dedent


@dataclass(frozen=True)
class PosInfo:
    line: int
    col: int

    @staticmethod
    def pos_index(text):
        return [
            PosInfo(i, col)
            for i, line in enumerate(text.splitlines(True))
            for col, _ in enumerate(line)
        ]


@dataclass(eq=False)
class ParseContext:
    text: str
    pos: int = 0
    indent_levels: List[int] = field(default_factory=list, init=False)

    def parse(self, startrule):
        start = getattr(self, f'parse_{startrule}')
        return start()

    def curr(self):
        if self.pos < len(self.text):
            return self.text[self.pos]

    def current_indent(self):
        return self.indent_levels[-1] if self.indent_levels else 0

    def parse_ASYNC(self):
        return self.match('async')

    def parse_NAME(self):
        return self.matchre(r'\w[\w\d]*')

    def parse_NEWLINE(self):
        return self.parse_ENDMARKER() or self.matchre(r'\s*(?:\n|$)')

    def parse_ENDMARKER(self):
        return self.atend()

    def parse_SPACE(self):
        return self.matchre(r'\s*')

    def parse_TYPE_COMMENT(self):
        self.matchre(r'\s*')
        comment = self.matchre(r'#.*$')
        if comment:
            self.parse_NEWLINE()
            return Comment(comment=comment)

    def parse_AWAIT(self):
        return self.match('await')

    def parse_INDENT(self):
        if not self.atbol():
            return self.error('Expecting INDENT')

        ind = self.indent()
        prev = self.current_indent()
        if ind and ind > prev:
            self.indent_levels.append(ind)
            return Indent(level=ind, pos=self.pos, endpos=self.pos)
        else:
            return self.error('Expecting INDENT')

    def parse_DEDENT(self):
        if not self.atbol():
            return self.error('Expecting DEDENT')

        ind = self.indent()
        if ind >= self.current_indent():
            return self.error('Expecting DEDENT')

        self.indent_levels.pop()
        prev = self.current_indent()
        if ind == prev:
            return Dedent(level=ind, pos=self.pos, endpos=self.pos)
        else:
            return self.error('Expecting DEDENT')

    def error(self, msg):
        return Error(msg=msg, pos=self.pos, endpos=self.pos)

    def is_error(self, e):
        return e and isinstance(e, Error)

    def is_not_error(self, e):
        return not self.is_error(e)

    def atend(self):
        return self.pos >= len(self.text)

    def atbol(self):
        return self.pos == 0 or self.atend() or self.text[self.pos - 1] == '\n'

    def move(self, n):
        self.pos += n

    def spaces(self):
        return self.matchre(r'(?:(?!\n)\s)*')

    def indent(self):
        return len(self.spaces())

    def match(self, token):
        p = self.pos
        e = p + len(token)

        if token != self.text[p:e]:
            return self.error(f'expecting {token}')

        self.pos = e
        return token

    def matchre(self, pattern, offset=0):
        matched = self._scanre(pattern, offset=offset)
        if matched:
            token = matched.group()
            self.move(len(token))
            return token

    def _scanre(self, pattern, offset=0):
        p = re.compile(pattern)
        return p.match(self.text, self.pos + offset)

    def closure(self, f):
        result = []
        while True:
            e = f()
            if self.is_error(e):
                return e
            elif e:
                result.append(e)
            else:
                break
        return result

    def closureplus(self, f):
        e = f()
        if self.is_error(e):
            return e
        else:
            return [e] + self.closure(f)

    def gather(self, *args):
        result = []
        for f in args:
            e = f()
            if self.is_error(e):
                return e
            elif e:
                result.append(e)
            else:
                break
        return result
