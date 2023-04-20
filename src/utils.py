import copy as cpy
import io
import math
import re
import sys


class Random:
    def __init__(self):
        self.seed = 937162211

    def set_seed(self, value: int):
        self.seed = value

    def get_seed(self):
        return self.seed

    def rand(self, lo=0, hi=1):
        self.seed = (16807 * self.seed) % 2147483647
        return lo + (hi - lo) * self.seed / 2147483647

    def rint(self, lo=0, hi=1):
        return math.floor(0.5 + self.rand(lo, hi))

_inst = Random()
rand = _inst.rand
rint = _inst.rint
get_seed = _inst.get_seed
set_seed = _inst.set_seed

def rnd(n: float, n_places: int = 2) -> float:
    mult = math.pow(10, n_places)
    return math.floor(n * mult + 0.5) / mult

def coerce(v):
    types = [int, float]
    for t in types:
        try:
            return t(v)
        except ValueError:
            pass
    bool_vals = ["true", "false"]
    if v.lower() in bool_vals:
        return v.lower() == "true"
    return v

def csv(filename, func):
    with io.open(filename) as f:
        while True:
            s = f.readline().rstrip()
            if s:
                t = []
                for s1 in re.findall("([^,]+)", s):
                    t.append(coerce(s1))
                func(t)
            else:
                f.close()
                break

def many(t, n):
    return [any(t) for _ in range(n)]

def any(t):
    return t[rint(len(t)) - 1]

def copy(t):
    return cpy.deepcopy(t)

def norm(num, n):
    return n if n == "?" else (n - num.lo) / (num.hi - num.lo + sys.float_info.min)

def per(t, p):
    p = math.floor(((p or 0.5) * len(t)) + 0.5)
    return t[max(0, min(len(t), p) - 1)]

def kap(t, func, u={}):
    u = {}
    what = enumerate(t)
    if isinstance(t, dict):
        what = t.items()
    for k, v in what:
        v, k = func(k, v)
        if not k:
            u[len(u)] = v
        else:
            u[k] = v
    return u
