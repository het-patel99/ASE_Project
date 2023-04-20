from typing import List

class Row:
    def __init__(self, t: List):
        self.cells = t
        self.x = None
        self.y = None
        self.rank = -1
