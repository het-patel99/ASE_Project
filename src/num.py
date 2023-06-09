import math
from typing import Union
from options import options
from utils import rint, rand, per, norm
from _basecol import Col

class Num(Col):
    def __init__(self, at: int = 0, txt: str = "", t=None):
        super().__init__(at=at, txt=txt)
        self.has_ = {}
        self.ok = True
        self.lo = math.inf
        self.hi = -math.inf
        self.w = -1 if self.txt.endswith("-") else 1
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        if t:
            for x in t:
                self.add(x)

    def add(self, x: Union[str, float, int], n: int = 1) -> None:
        if x != "?":
            self.n += n
            self.lo, self.hi = min(x, self.lo), max(x, self.hi)
            all_ = len(self.has_)
            if all_ < options["Max"]:
                pos = all_ + 1
                self.has_[pos] = x
                self.ok = False
            else:
                rand_prob = rand() < options["Max"] / self.n
                if rand_prob:
                    pos = rint(1, all_)
                    self.has_[pos] = x
                    self.ok = False
            d = x - self.mu
            self.mu = self.mu + d / self.n
            self.m2 = self.m2 + d * (x - self.mu)
            self.sd = 0 if self.n < 2 else (self.m2 / (self.n - 1)) ** .5

    def mid(self) -> float:
        return per(self.has(), .5)

    def div(self) -> float:
        return (per(self.has(), .9) - per(self.has(), .1)) / 2.58

    def has(self):
        ret = dict(sorted(self.has_.items(), key=lambda x: x[1]))
        self.ok = True
        return list(ret.values())

    def dist(self, data1, data2):
        data1, data2 = norm(self, data1), norm(self, data2)
        if data1 == "?" and data2 == "?":
            return 1
        if data1 == "?":
            data1 = 1 if data2 < 0.5 else 1
        if data2 == "?":
            data2 = 1 if data1 < 0.5 else 1
        return abs(data1 - data2)
