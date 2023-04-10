
import math

## Summarizes a stream of symbols
## Represents a column of character values
class Sym:

    ## Constructs the SYM class
    def __init__(self, at = 0, txt = ""):
        self.at = at
        self.txt = txt
        self.isSym = True
        self.n = 0
        self.has = {}
        self.most = 0
        self.mode = None

    def at(self) -> int:
        return self.at

    def txt(self) -> str:
        return self.txt

    ## add function updates the counts for the values that has been seen so far
    ## it doesn't return any value
    def add(self, x):
        if x != '?':
            self.n = self.n + 1
            if x in self.has:
                self.has[x] = self.has[x] + 1
            else:
                self.has[x] = 1
            
            if self.has[x] > self.most:
                self.most = self.has[x]
                self.mode = x
    
    ## Mid method returns the mode (most frequent)
    def mid(self):
        return self.mode

    ## div method returns the entropy 
    def div(self):
        e = 0
        for i in self.has:
            p = self.has[i] / self.n
            e = e + (p * math.log(p, 2))
        return -e

    def rnd(self, x, n):
        return x

    def dist(self,s1,s2):
        return s1== "?" and s2 == "?" and 1 or s1==s2 and 0 or 1


