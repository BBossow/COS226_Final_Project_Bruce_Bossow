# This is where the csv file will be loaded and put into dataItem

import csv
from data_item import DataItem

def load_csv(filename):
    records = []
    with open(filename, 'r', newline = '', encoding = "utf8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            records.append(DataItem(row))
    return records 