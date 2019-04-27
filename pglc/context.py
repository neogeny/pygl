import re
from itertools import takewhile
from dataclasses import dataclass


@dataclass(eq=False)
class ParseContext:
    text: str
    pos: int = 0

    def parse_ASYNC(self):
        return self.match('async')

    def parse_NAME(self):
        return self.matchre(r'\w[\w\d]*')

    def parse_NEWLINE(self):
        return self.matchre(r'\s*\n')

    def parse_ENDMARKER(self):
        return self.atend()

    def atend(self):
        return self.pos >= len(self.text)

    def move(self, n):
        self.pos += n

    def match(self, token):
        p = self.pos
        e = p + len(token)

        if token != self.text[p:e]:
            return

        self.pos = e
        return token

    def matchre(self, pattern, offset=0):
        matched = self._scanre(pattern, offset=offset)
        if matched:
            token = matched.group()
            self.move(len(token))
            return token

    def _scanre(self, pattern, offset=0):
        return re.match(pattern, self.text, self.pos + offset)

    def closure(self, f):
        return list(takewhile(lambda e: e, f))

    def closureplus(self, f):
        e = f()
        if e:
            return [e] + list(takewhile(lambda e: e, f))
