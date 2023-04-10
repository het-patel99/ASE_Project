from cols import Cols
import csv, tests, update, data

def csv_content(src):
    res = []
    with open(src, mode='r') as file:
        csvFile = csv.reader(file)
        for row in csvFile:
            res.append(row)
    return res



class New_Data:
    def __init__(self, src, rows = None):
        self.cols = None
        self.rows = []
        add = lambda t: update.row(self, t)
        if isinstance(src, str):
            data.readCSV(src, add)
        else:
            self.cols = Cols(src.cols.names)
            if rows:
                for row in rows:
                    add(row)


    def read_file(self, content):
        data = data()
        callback_function = lambda t: update.row(data, t)
        tests.readCSV(content, callback_function)
        return data

    def clone(self, ndata, ts=None):
        new_data = update.row(data.Data(), ndata.cols.names)
        for t in ts or []:
            update.row(new_data, t)
        return new_data

