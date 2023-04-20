from data import Data
from utils import set_seed, Random, get_seed


class BaseOptimizer:
    def __init__(self, seed: int = None):
        self.random = Random()

        if seed:
            self.random.set_seed(seed)

    def run(self, data: Data):
        set_seed(self.random.seed)
        best, rest, eval = self._run(data=data)
        self.random.set_seed(get_seed())

        return best, rest, eval

    def _run(self, data: Data):
        raise NotImplementedError("Cannot create an object of BaseOptimizer")

    @property
    def seed(self):
        return self.random.seed

    @seed.setter
    def seed(self, value):
        self.random.set_seed(value)