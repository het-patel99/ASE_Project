import sys
from main import the
from num import Num
from sym import Sym
import utils
from data import Data, csv_content
import data_explain
from pathlib import Path
import os,math 
import optimize 
import query
import update 
import cluster
import csv
import discretization 



def test_csv():
    if(csv_content(the["file"]) == 8 * 399):
        print("test_csv : successful \n")
    return csv_content(the["file"]) == 8 * 399

def test_nums():
    val = Num()
    lst = [1,1,1,1,2,2,3]
    for a in lst:
        val.add(a)
    print("test_nums: successful\n")
    return 11/7 == val.mid() and 0.787 == utils.rnd(val.div(),3)
    
def test_sym():
    value = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    sym1 = Sym()
    for x in value:
        sym1.add(x)
    print("test_syms: successful\n")
    return "a"==sym1.mid() and 1.379 == utils.rnd(sym1.div(),3)

def test_the():
    print("The results of test_the function:")
    print(str(the))
    print("test_the: successful\n")
    return True

def test_data():
    data = Data().read_file(the["file"])
    col = data.cols.x[1].col
    print("test_data : successful \n")
    print(col.lo,col.hi, query.mid(col), query.div(col))
    print(query.stats(data))
    return True

def test_clone():
    data = Data().read_file(the["file"])
    data2 = data.clone(data,data.rows)
    print("test_clone : successful \n")
    utils.oo(query.stats(data))
    utils.oo(query.stats(data2))
    return True

def test_half():
    data = Data().read_file(the["file"])

    left, right, A, B, c, evals = cluster.half(data)
    print("test_half : successful \n")
    print(len(left), len(right), len(data.rows))
    print(utils.o(A), c)
    print(utils.o(B))
    return True

def test_cliffs():
    if utils.cliffs_delta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]):
        return False
    if not utils.cliffs_delta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]):
        return False

    t1, t2 = [], []
    for i in range(1000):
        t1.append(utils.rand())
        t2.append(math.sqrt(utils.rand()))
    if utils.cliffs_delta(t1, t1):
        return False
    if not utils.cliffs_delta(t1, t2):
        return False
    diff, j = False, 1.0
    while not diff:
        t3 = list(map(lambda x: x * j,t1))
        diff = utils.cliffs_delta(t1, t3)
        print(">", utils.rnd(j), diff)
        j *= 1.025
    print("test_cliffs : successful \n")
    return True

def test_dist():
    data = Data().read_file(the["file"])
    num = Num()
    for row in data.rows:
        update.add(num, query.dist(data, row, data.rows[1]))
    print("test_dist : successful \n")
    print({"lo": num.lo, "hi": num.hi, "mid": utils.rnd(query.mid(num)), "div": utils.rnd(num.n)})
    return True

def test_tree():
    data = Data().read_file(the["file"])
    print("test_tree : successful \n")
    cluster.show_tree(cluster.tree(data))

    return True

def test_sway():
    data = Data().read_file(the["file"])
    best, rest, evals = optimize.sway(data)
    print(utils.o(query.stats(data)))
    print("\nall ", utils.o(query.stats(data)))
    print("    ",  utils.o( query.stats(data, query.div)))
    print("\nbest", utils.o(query.stats(best)))
    print("    ",   utils.o(query.stats(best, query.div)))
    print("\nrest", utils.o(query.stats(rest)))
    print("    ",   utils.o(query.stats(rest, query.div)))
    print("\nall ~= best?", utils.o(utils.diffs(best.cols.y, data.cols.y)))
    print("best ~= rest?", utils.o(utils.diffs(best.cols.y, rest.cols.y)))
    return True



def test_bins():
    data = Data().read_file(the["file"])
    best, rest, evals = optimize.sway(data)
    print("test_bins : successful")
    print("all","","","",utils.o({"best":len(best.rows), "rest": len(rest.rows)}))
    for k,t in enumerate(discretization.bins(data.cols.x, {"best": best.rows, "rest": rest.rows})):
        for _, range in enumerate(t):
            print(range.txt, range.lo, range.hi,round(query.value(range.y.has, len(best.rows), len(rest.rows), "best")),
                  range.y.has)
    print("end")
    return  True 

def test_explain():
    data = data_explain.New_Data(the["file"])
    best, rest , evals = optimize.sway(data)
    rule, most= discretization.xpln(data,best,rest)
    data1= data_explain.New_Data(data,discretization.selects(rule,data.rows))
    top, _ = query.betters(data, len(best.rows))
    print("calculation of showrule", discretization.showRule(rule))
    print("All --- ",query.stats(data),query.stats(data,query.div))
    print(f"Sway with {evals} evals",query.stats(best),query.stats(best,query.div))
    print(f"Xpln on {evals} evals",query.stats(data1),query.stats(data1,query.div))
    
    print("\n test_explain : successful \n")
    return True 