from dataclasses import dataclass, field
from typing import List


@dataclass()
class PythonSemantics:
    indent_levels: List[int] = field(default_factory=list, init=False)
