import csv, update, math
from utils import *
from cols import Cols
import row
from main import the

def csv_content(src):
    res = []
    with open(src, mode='r') as file:
        csvFile = csv.reader(file)
        for row in csvFile:
            res.append(row)
    return res


def readCSV(sFilename, fun):
  
    with open(sFilename, mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            fun(line)

class Data():

    ## constructor created for data.py class
    def __init__(self):
        self.rows = []
        self.cols =  None
        
       
    def add(self, t):

        if(self.cols is None):
            self.cols = Cols(t)
        else:
            new_row = row.Rows(t)
            self.rows.append(new_row)
            self.cols.add(new_row)

    def clone(self, data, ts=None):
        new_data = update.row(Data(), data.cols.names)
        for t in ts or []:
            update.row(new_data, t)
        return new_data
    
    def read_file(self, content):
        data = Data()
        callback_function = lambda t: update.row(data, t)
        readCSV(content, callback_function)
        return data


    def better(self, row1, row2):
        s1,s2,ys = 0,0,self.cols.y
        for _,col in enumerate(ys):
            x = col.norm(row1.cells[col.at])
            y = col.norm[row2.cells[col.at]]
            s1 = s1 - math.exp(col.w*(x-y)/len(ys))
            s2 = s2 - math.exp(col.w*(y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)

    def around(self, rows):
        return map(sorted(map(rows)))


    def cluster(self, rows, min, cols, above):
        rows = rows or self.rows
        min = min or len(rows)^min
        cols = cols or self.cols.x
        node = data = self.clone()
        if len(rows)>2*min:
            left, right, node.A, node.B, node.mid = self.half(rows,cols,above)
            node.left = self.cluster(left,min,cols,node.A)
            node.right = self.cluster(right,min,cols,node.B)
        return node


    def sway(self,rows,min,cols,above):
        rows = rows or self.rows
        min = min or len(rows)^min
        cols = cols or self.cols.x
        node = data = self.clone()
        if len(rows)>2*min:
            left, right, node.A, node.B, node.mid = self.half(rows,cols,above)
            if self.better(node.B,node.A):
                left,right,node.A,node.B = right,left,node.B,node.A
            else:
                node.left = self.sway(left,min,cols,node.A)
        return node
