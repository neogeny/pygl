from dataclasses import dataclass
from typing import List

from tatsu.util import asjson

@dataclass
class _Node:
    pos: int
    endpos: int

    def asjson(self):
        self.__json__()

    def __json__(self):
        return {
            **{'type': type(self).__name__},
            **{
                name: asjson(value)
                for name, value in vars(self).items()
                if not name.startswith('_')
            }
        }


@dataclass
class Exp(_Node):
    pass


@dataclass
class _HasExp(_Node):
    exp: Exp


@dataclass
class Name(_Node):
    name: str


@dataclass
class Token(Name):
    pass


@dataclass
class Ref(Name):
    pass


@dataclass
class Seq(_Node):
    seq: List[Exp]


@dataclass
class Choice(_Node):
    options: List[Exp]


@dataclass
class Optional(_HasExp):
    pass


@dataclass
class Closure(_HasExp):
    pass


@dataclass
class PositiveClosure(_HasExp):
    pass


@dataclass
class Rule(_HasExp):
    name: str


@dataclass
class Grammar(_Node):
    rules: List[Rule]
