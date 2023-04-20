import math
from typing import List, Union
from _basecol import Col
from row import Row
from utils import norm
from options import options


class ZitzlerPredicate:
    @staticmethod
    def better(cols: List[Union[Col]], row1: Row, row2: Row, s1=0, s2=0, x=0, y=0):
        for col in cols:
            x = norm(col, row1.cells[col.at])
            y = norm(col, row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(cols))
            s2 = s2 - math.exp(col.w * (y - x) / len(cols))
        return s1 / len(cols) < s2 / len(cols)

class HyperparameterPredicate:
    @staticmethod
    def better(cols: List[Union[Col]], row1: Row, row2: Row, data=None, opt=None):
        def get_options(row):
            opt = options.t.copy()
            for item, col_name in zip(row.cells, cols.names):
                opt[col_name] = item
            return opt

        option1 = get_options(row1)
        reuse=option1["reuse"]
        rest=option1["rest"]
        far=option1["Far"]
        halves=option1["halves"]
        i_min=option1["min_cluster"]
        best1, rest1, evals1 = opt(reuse=reuse,far=far,halves=halves,rest=rest,i_min=i_min).run(data)

        row_best1 = [0 for _ in data.cols.names]
        for key, val in best1.stats().items():
            for ys in data.cols.y:
                if ys.txt == key:
                    row_best1[ys.at] = val

        option2 = get_options(row1)
        reuse=option2["reuse"]
        rest=option2["rest"]
        far=option2["Far"]
        halves=option2["halves"]
        i_min=option2["min_cluster"]
        best2, rest2, evals2 = opt(reuse=reuse,far=far,halves=halves,rest=rest,i_min=i_min).run(data)
        row_best2 = [0 for _ in data.cols.names]
        for key, val in best2.stats().items():
            for ys in data.cols.y:
                if ys.txt == key:
                    row_best2[ys.at] = val
        res = ZitzlerPredicate.better(data.cols.y, Row(row_best1), Row(row_best2))
        total_evals = evals1 + evals2
        return [res, total_evals]
