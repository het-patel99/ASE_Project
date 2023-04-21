from typing import Optional
from data import Data
from sym import Sym
from _baseoptimizer import BaseOptimizer
from sklearn import preprocessing, tree

class DtreeOptimizer(BaseOptimizer):
    def __init__(self, best=None, rest=None, seed=None):
        super().__init__(seed)
        self._data: Optional[Data] = None
        self._best = best
        self._rest = rest

    def _run(self, data: Data):
        self._data: Data = data
        self._clf = self._dtree()
        return self._classify_dtree()

    def _dtree(self):
        best_rows = [[r.cells[c.at] for c in self._best.cols.x] + ["best"] for r in self._best.rows]
        rest_rows = [[r.cells[c.at] for c in self._rest.cols.x] + ["rest"] for r in self._rest.rows]
        X = best_rows + rest_rows

        LabelEncoder = preprocessing.LabelEncoder()
        for i, col in enumerate(self._rest.cols.x):
            if isinstance(col, Sym):
                new_cols = LabelEncoder.fit_transform([x[i] for x in X])
                for j, x in zip(new_cols, X):
                    x[i] = j

        X = list(filter(self._remove_missing, X))
        X_data = [i[:-1] for i in X]
        y = [j[-1] for j in X]
        
        clf = tree.DecisionTreeClassifier(random_state=0).fit(X_data, y)
        return clf
    
    def _remove_missing(self, X):
        return "?" not in X

    def _classify_dtree(self):
        X = [[row.cells[col.at] for col in self._data.cols.x] for row in self._data.rows]
        LabelEncoder = preprocessing.LabelEncoder()
        for i, col in enumerate(self._data.cols.x):
            if isinstance(col, Sym):
                new_cols = LabelEncoder.fit_transform([x[i] for x in X])
                for j, x in zip(new_cols, X):
                    x[i] = j
        best = []
        other = []
        for i, x in enumerate(X):
            if self._remove_missing(x):
                result = self._clf.predict([x])
                if result == "best":
                    best.append(self._data.rows[i])
                else:
                    other.append(self._data.rows[i])

        return best, other, 0
