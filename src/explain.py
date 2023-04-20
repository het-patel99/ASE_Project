from typing import List, Dict, Tuple
from data import Data
from discretization import value, bins, Range
from utils import kap

def show_rule(rule):
    def pretty_range(range_):
        if range_["lo"] == range_["hi"]:
            return range_["lo"]
        else:
            return [range_["lo"], range_["hi"]]

    def merge_ranges(attr, ranges):
        sorted_ranges = sorted(ranges, key=lambda x: x["lo"])
        merged_ranges = []
        for i in range(len(sorted_ranges)):
            left = sorted_ranges[i]
            right = None if i + 1 >= len(sorted_ranges) else sorted_ranges[i + 1]
            if right and left["hi"] == right["lo"]:
                left["hi"] = right["hi"]
            else:
                merged_ranges.append({"lo": left["lo"], "hi": left["hi"]})
        return merged_ranges, attr

    return kap(rule, merge_ranges)

class Explain:
    def __init__(self, best_data: Data, rest_data: Data):
        self.best_data = best_data
        self.rest_data = rest_data
        self.tmp = []
        self.max_sizes = {}

    def score(self, ranges):
        rule = self.rule(ranges, self.max_sizes)
        if rule:
            bestr = select_rows(rule, self.best_data.rows)
            restr = select_rows(rule, self.rest_data.rows)
            if len(bestr) + len(restr) > 0:
                return value({"best": len(bestr), "rest": len(restr)}, len(self.best_data.rows), len(self.rest_data.rows),
                             "best"), rule
        return None, None

    def xpln(self, data, best_data, rest_data):
        def value_counts(value_counts):
            return value(value_counts, len(best_data.rows), len(rest_data.rows), "best")

        self.max_sizes = {}
        for i, ranges in enumerate(bins(data.cols.x, {"best": best_data.rows, "rest": rest_data.rows})):
            self.max_sizes[ranges[0].txt] = len(ranges)
            for j, range_ in enumerate(ranges):
                self.tmp.append({"range": range_, "max": len(ranges), "val": value_counts(range_.y.value_counts)})
        rule, most = self.first_n(sorted(self.tmp, key=lambda x: x["val"], reverse=True), self.score)

        return rule, most

    def first_n(self, sorted_ranges, score_func):
        first = sorted_ranges[0]['val']

        def is_useful(range_):
            return range_['val'] > 0.05 and range_['val'] > first / 10

        sorted_ranges = [s for s in sorted_ranges if is_useful(s)]
        most = -1
        out = -1
        for n in range(len(sorted_ranges)):
            tmp, rule = score_func([r['range'] for r in sorted_ranges[:n + 1]])

            if tmp is not None and tmp > most:
                out, most = rule, tmp

        return out, most

    def rule(self, ranges, max_size):
        t = {}
        for i, range_ in enumerate(ranges):
            t[range_.txt] = t.get(range_.txt, [])
            t[range_.txt].append({"lo": range_.lo, "hi": range_.hi, "at": range_.at})
        return self.prune(t, max_size)

    def prune(self, rule, max_size):
        n = 0
        new_rule = {}
        for txt, ranges in rule.items():
            n += 1
            if len(ranges) == max_size[txt]:
                n -= 1
                rule[txt] = None
            else:
                new_rule[txt] = ranges
        if n > 0:
            return new_rule
        return None


def select_rows(rule, rows):
    def check_disjunction(ranges, row):
        for range_ in ranges:
            x = row.cells[range_['at']]
            if x == '?' or (range_['lo'] == range_['hi'] and range_['lo'] == x) or (range_['lo'] <= x < range_['hi']):
                return True
        return False

    def check_conjunction(row):
        for _, ranges in rule.items():
            if not check_disjunction(ranges, row):
                return False
        return True

    result = list(filter(check_conjunction, rows))
    return result
