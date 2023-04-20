from functools import cmp_to_key
from typing import Union, List, Dict, Optional
from predicate import ZitzlerPredicate
from utils import csv, rnd
from sym import Sym
from num import Num
from cols import Cols
from row import Row


class Data:
    def __init__(self, src: Union[str, List] = None, rows: Union[List, Row] = None):
        self.rows: List[Row] = []
        self.cols: Optional[Cols] = None

        if src or rows:
            self.read(src, rows)

    def read(self, src: Union[str, List], rows: Union[List, Row] = None):
        def add_to_data(t):
            self.add(t)

        if isinstance(src, str):
            csv(src, add_to_data)
        else:
            self.cols = Cols(src.cols.names)

            for row in rows:
                self.add(row)

    def add(self, res: Union[List, Row]):
        if self.cols:
            res = res if isinstance(res, Row) else Row(res)

            self.rows.append(res)
            self.cols.add(res)
        else:
            self.cols = Cols(res)

    @staticmethod
    def clone(data: 'Data', ls: List = None) -> 'Data':
        if ls is None:
            ls = []

        data1 = Data()
        data1.add(data.cols.names)

        for _, t in enumerate(ls):
            data1.add(t)

        return data1

    def stats(self, cols: List[Union[Sym, Num]] = None, nplaces: int = 2, what: str = "mid") -> Dict:
        cols = cols or self.cols.y
        result = {col.txt: rnd(getattr(col, what)(), nplaces) for col in cols}
        result["N"] = len(self.rows)

        return result

    def betters(self, i: int = None, predicate=None):
        if predicate is None:
            predicate = ZitzlerPredicate

        tmp = sorted(
            self.rows,
            key=cmp_to_key(lambda row1, row2: -1 if predicate.better(self.cols.y, row1, row2) else 1)
        )

        return tmp[1:i], tmp[i + 1:] if i is not None else tmp
