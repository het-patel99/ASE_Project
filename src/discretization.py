from math import inf, floor
from typing import Union, Optional, List
from sym import Sym
from num import Num
from options import options
from utils import copy
from collections import defaultdict


class Range:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.lo = lo
        self.hi = lo or hi or lo
        self.y = Sym()

    def extend(self, n: int, s: str):
        self.lo = min(n, self.lo)
        self.hi = max(n, self.hi)
        self.y.add(s)


def merge(col1: Union[Sym, Num], col2: Union[Sym, Num]) -> Union[Sym, Num]:
    new = copy(col1)

    if isinstance(col1, Sym):
        for x, n in col2.value_counts.items():
            new.add(x, n)
    else:
        for _, n in col2.value_counts.items():
            new.add(n)

        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)

    return new

def merge2(col1: Union[Sym, Num], col2: Union[Sym, Num]) -> Optional[Union[Sym, Num]]:
    new = merge(col1, col2)

    col1_div = col1.div()
    col2_div = col2.div()
    col1_n = col1.n
    col2_n = col2.n
    new_n = new.n

    if new_div := new.div() <= ((col1_div * col1_n) + (col2_div * col2_n)) / new_n:
        return new


def merge_any(ranges0: List[Range]) -> List[Range]:
    def no_gaps(t: List[Range]):
        if not t:
            return t

        last_hi = -inf
        return [Range(r.lo if r.lo != -inf else last_hi, r.hi) for r in t]

    n = len(ranges0)

    for i, left in enumerate(ranges0):
        right = None if i == n - 1 else ranges0[i + 1]

        if right is not None:
            y = merge2(left.y, right.y)

            if y is not None:
                left.hi, left.y = right.hi, y
                del ranges0[i + 1]

    return no_gaps(ranges0) if n == len(ranges0) else merge_any(ranges0)

def extend(range_, n, s):
    range_.lo = min(n, range_.lo)
    range_.hi = max(n, range_.hi)
    range_.y.add(s)


def bins(cols, rowss):
    def with_one_col(col):
        n, ranges = with_all_rows(col)
        ranges = [x for x in ranges.values()]
        ranges.sort(key=lambda x: x.lo)
        if isinstance(col, Sym):
            return ranges
        else:
            return merges(ranges, n / options["bins"], options["D"] * col.div())

    def with_all_rows(col):
        def xy(x, y):
            nonlocal n
            if x != "?":
                n = n + 1
                k = bin_(col, x)
                if k not in ranges:
                    ranges[k] = Range(col.at, col.txt, x)
                extend(ranges[k], x, y)

        n, ranges = 0, {}
        for y, rows in rowss.items():
            for _, row in enumerate(rows):
                xy(row.cells[col.at], y)
        return n, ranges

    ret = list(map(with_one_col, cols))
    return ret

def bin_(col, x):
    if x == "?" or isinstance(col, Sym):
        return x
    tmp = (col.hi - col.lo) / (options["bins"] - 1)
    return col.hi == col.lo and 1 or floor(x / tmp + .5) * tmp

def value(has, n_b: int = 1, n_r: int = 1, s_goal: str = None) -> float:
    b, r = 0, 0
    for x, n in has.items():
        if x == s_goal:
            b += n
        else:
            r += n
    b, r = b / (n_b + 1 / inf), r / (n_r + 1 / inf)
    return b ** 2 / (b + r)

def merges(ranges0, n_small, n_far):
    def no_gaps(t):
        if not t:
            return t
        for j in range(1, len(t)):
            t[j].lo = t[j - 1].hi
        t[0].lo = -inf
        t[len(t) - 1].hi = inf
        return t

    def try2_merge(left, right, j):
        y = merged(left.y, right.y, n_small, n_far)
        if y:
            j += 1
            left.hi, left.y = right.hi, y
        return j, left

    ranges1, j, here = [], 0, None
    while j < len(ranges0):
        here = ranges0[j]
        if j < len(ranges0) - 1:
            j, here = try2_merge(here, ranges0[j + 1], j)
        j += 1
        ranges1.append(here)
    return no_gaps(ranges0) if len(ranges0) == len(ranges1) else merges(ranges1, n_small, n_far)

def merged(col1, col2, n_small, n_far):
    new = merge(col1, col2)
    if n_small and col1.n < n_small or col2.n < n_small:
        return new
    if n_far and not isinstance(col1, Sym) and abs(col1.div() - col2.div()) < n_far:
        return new
    if new.div() <= (col1.div() * col1.n + col2.div() * col2.n) / new.n:
        return new