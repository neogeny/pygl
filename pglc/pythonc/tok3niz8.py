import re
from itertools import takewhile, repeat
from collections import namedtuple
from tokenize import TokenInfo
import token

from tatsu.util import identity

def group(*choices):
    return '(?:' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*?'


def maybe(*choices):
    return group(*choices) + '?'


NL = r'\r?\n|\r'
WHITESPACE = r'(?:(?![^\r\n])\s)+'
COMMENT = r'#.*?' + NL
STRING_PREFIX = r'(?i)(b|r|u|f|br|fr)'
NAME = r'[\w_]+'
STRING = STRING_PREFIX + group(
    r"'''(?:[^']|\\\'|\\\"\\\n|\\.)'''"
    r"'(?:[^']|\\\'|\\\"\\\n|\\.)'"
    r'"""(?:[^"]|\\\'|\\\"\\\n|\\.)"""'
    r'"(?:[^"]|\\\'|\\\"\\\n|\\.)"'
)
ENCODING = br'''(?x)
    (?:\s|#.*?(?:\r?\n|\r))*
    #.*?coding:\s*(\S*)
'''

OPS = dict(sorted(
    [(type, re.escape(op)) for op, type in token.EXACT_TOKEN_TYPES.items()],
    key=lambda pair: -len(pair[1]),
))


SYMBOLS = {
    token.NL: NL,
    token.NAME: NAME,
    token.STRING: STRING,
    **OPS,
}

TOKENS = {
    **SYMBOLS,
}


class PosInfo(namedtuple('PosInfo', ['line', 'col'])):
    pass


class Tok3nize8:
    def __init__(self, readline):
        self.encoding = 'utf-8'
        self.text = ''
        self.lines = []
        self.index = []
        self.pos = 0

    def _index(self, readline):
        btext = b''.join(l for l in readline)

        m = re.match(ENCODING, btext)
        if m:
            self.encoding = m.group(1).decode('ascii')
        text = btext.decode(self.encoding)
        text += chr(0)

        for n, line in text.splitlines(True):
            self.lines.append(line)
            for col in range(len(line)):
                self.index.append(PosInfo(n, col))

    def _goto(self, pos):
        self._pos = max(0, min(len(self.text), pos))

    def _next(self):
        self._goto(self.pos + 1)

    def _move(self, n):
        self._goto(self.pos + n)

    def _scanre(self, pattern, offset=0):
        return re.match(pattern, self.text, self.pos + offset)

    def _matchre(self, pattern)
        matched = self._scanre(pattern)
        if matched:
            token = matched.group()
            self._move(len(token))
            return token

    def _eat_regex(self, regex):
        return all(takewhile(identity, map(self._matchre, repeat(regex))))

    def atend(self):
        return self.pos >= len(self.text)

    def eat_whitespace(self):
        return self._eat_regex(WHITESPACE)

    def eat_comments(self):
        return self._eat_regex(COMMENT)

    def next_token(self):
        p = None
        while self._pos != p:
            p = self._pos
            self.eat_comments()
            self.eat_whitespace()

    def _token(self, type):
        i = self.pos
        line = self.index[i].line
        start = self.index[i].col

        pattern = TOKENS[type]
        string = self._matchre(pattern)
        if not string:
            return
        e = self.pos
        end = self.index[e].col
        return TokenInfo(type, string, start, end, line)

    def token(self):
        self.next_token()
        for type in SYMBOLS:
            t = self._token(type)
            if t:
                return t

    def tokenize(self):
        last = None
        while True:
            t = self.token()
            if t.type == token.NL:
                if last.type not in (token.NL, token.NEWLINE):
                    t = TokenInfo(token.NEWLINE, t.string, t.start, t.end, t.line)
            elif last.type in (token.NL, token.NEWLINE):
                pass
            yield t
            last = t
            if not t: break
