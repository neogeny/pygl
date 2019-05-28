import re
import io
import token
from tokenize import tokenize

from tatsu.infos import PosLine, LineInfo
from tatsu.tokenizing import Tokenizer


class PythonTokenizer(Tokenizer):
    def __init__(self, text, filename=None):
        self._filename = filename
        self.text = text
        self.lines = text.splitlines(False)

        # namedtuple(type string start end line)
        with io.BytesIO(text) as f:
            self.tokens = list(tokenize(f.readline))
        self._pos = 0

    @property
    def filename(self):
        return self._filename

    @property
    def ignorecase(self):
        return False

    @property
    def pos(self):
        return self._pos

    def at(self, pos):
        return self.tokens[min(pos, len(self.tokens) - 1)]

    def goto(self, pos):
        self._pos = min(pos, len(self.tokens) - 1)
        return self.token

    def atend(self):
        return (
            self.token.type == token.ENDMARKER or
            self.pos >= len(self.tokens)
        )

    def ateol(self):
        raise NotImplementedError

    @property
    def token(self):
        return self.tokens[self.pos]

    def _next(self):
        if self.atend():
            return None
        self.goto(self.pos + 1)
        return self.token

    def next(self):
        self._next()
        self.eat_comments()

    def eat_comments(self):
        while self.token.type in (token.COMMENT, token.NL,):
            self._next()

    def next_token(self):
        self.eat_comments()

    def match(self, word, ignorecase=False):
        if self.token.type in (token.INDENT, token.DEDENT, token.COMMENT):
            return False
        if word == self.token.string:
            t = self.token.string
            self.next()
            return t

    def matchre(self, pattern, ignorecase=False):
        m = re.match(pattern, self.token.string)
        if not m:
            return

        t = m.group()
        if t:
            t = self.token.string
            self.next()
        return t

    def matchtype(self, type):
        if self.token.type != type:
            return
        self.next()
        return True

    def posline(self, pos):
        t = self.at(pos)
        return PosLine(
            t.start[1],
            t.line,
            t.end[1] - t.start[1],
        )

    def line_info(self, pos=None):
        if pos is None:
            pos = self._pos

        pos = min(pos, len(self.tokens))
        t = self.tokens[pos]

        line = t.start[0]
        start = t.start[1]
        end = t.end[1]
        col = start
        text = t.line or t.string

        return LineInfo(self.filename, line, col, start, end, text)

    def get_lines(self, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = len(self.lines)
        return self.lines[start:end + 1]

    def lookahead(self):
        if self.atend():
            return ''
        info = self.line_info()
        text = info.text[info.col:info.col + 1 + 80]
        if text:
            return text.splitlines(False)[0].rstrip()
        else:
            return ''
