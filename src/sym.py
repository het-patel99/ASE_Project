import collections
import math
from _basecol import Col

class Sym(Col):
    def __init__(self, at: int = 0, txt: str = ""):
        super().__init__(at=at, txt=txt)
        self.value_counts = collections.defaultdict(int)
        self.mode = None
        self.most_frequent_count = 0

    def add(self, value: str, count: int = 1):
        if value != "?":
            self.n += count
            self.value_counts[value] += count
            value_count = self.value_counts[value]
            if value_count > self.most_frequent_count:
                self.most_frequent_count = value_count
                self.mode = value
        return value

    def mid(self):
        return self.mode

    def div(self):
        def entropy(p):
            return p * math.log2(p)

        total_entropy = 0
        for value_count in self.value_counts.values():
            p = value_count / self.n
            total_entropy -= entropy(p)

        return total_entropy

    def dist(self, data1, data2):
        if data1 == "?" and data2 == "?":
            return 1
        elif data1 == data2:
            return 0
        else:
            return 1
