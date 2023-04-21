from typing import Optional, List
from dataclasses import dataclass
from data import Data
from _basecol import Col
from row import Row
from distance import PDist, cosine_similarity
from predicate import ZitzlerPredicate
from utils import many, any
from _baseoptimizer import BaseOptimizer

@dataclass
class Projection:
    row: Row
    x: float

class SwayOptimizer(BaseOptimizer):
    def __init__(
        self,
        p: float = 2,
        reuse: bool = True,
        far: float = 0.95,
        halves: int = 512,
        rest: int = 10,
        i_min: float = 0.5,
        seed: Optional[int] = None
    ):
        super().__init__(seed)
        self.data = None
        self.distance_class = PDist(p=2)
        self.reuse = reuse
        self.far = far
        self.halves = halves
        self.rest = rest
        self.i_min = i_min

    def run(self, data: Data):
        self.data = data
        return self._sway(self.data.cols.x)

    def _project(self, cols: List[Col], row: Row, a: Row, b: Row, c: float) -> Projection:
        return Projection(
            row=row,
            x=cosine_similarity(
                a=self.distance_class.dist(cols, row, a),
                b=self.distance_class.dist(cols, row, b),
                c=c
            )
        )

    def _half(self, cols: List[Col], rows: List[Row], above=None):
        some = many(rows, self.halves)
        a = above if above is not None and self.reuse else any(some)
        tmp = sorted(
            [
                {"row": r, "d": self.distance_class.dist(cols, r, a)} 
                for r in some
            ], 
            key=lambda x: x["d"]
        )
        far = tmp[int((len(tmp) - 1) * self.far)]
        b, c = far["row"], far["d"]
        sorted_rows = sorted(
            [self._project(cols, row, a, b, c) for row in rows], 
            key=lambda x: x.x
        )
        left, right = [], []
        for n, two in enumerate(sorted_rows):
            if (n + 1) <= (len(rows) / 2):
                left.append(two.row)
            else:
                right.append(two.row)
        evals = 1 if above is not None and self.reuse else 2
        return left, right, a, b, c, evals

    def _sway(self, cols: List[Col]):
        def worker(rows: List[Row], worse, evals0=None, above=None):
            if len(rows) <= len(self.data.rows) ** self.i_min:
                return rows, many(worse, self.rest * len(rows)), evals0
            l, r, a, b, c, evals_ = self._half(cols, rows, above)
            if ZitzlerPredicate.better(self.data.cols.y, b, a):
                l, r, a, b = r, l, b, a
            worse.extend(r)
            return worker(l, worse, evals_ + evals0, a)

        best, rest, evals = worker(self.data.rows, [], 0)
        return Data.clone(self.data, best), Data.clone(self.data,rest), evals
