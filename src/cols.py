import re
from typing import List
from _basecol import Col
from sym import Sym
from num import Num
from row import Row


class Cols:
    def __init__(self, t: List):
        self.names: List = t
        self.all: List[Col] = []
        self.x: List[Col] = []
        self.y: List[Col] = []

        self.klass = None

        for n, s in enumerate(t):
            s = s.strip()
            col = Num(n, s) if re.findall("^[A-Z]+", s) else Sym(n, s)
            self.all.append(col)

            if not re.findall("X$", s):
                if re.findall("!$", s):
                    self.klass = col
                self.y.append(col) if re.findall("[!+-]$", s) else self.x.append(col)

    def add(self, row: Row) -> None:
        for _, t in enumerate([self.x, self.y]):
            for _, col in enumerate(t):
                col.add(row.cells[col.at])
