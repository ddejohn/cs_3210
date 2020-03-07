import csv

with open("grammar/grammar.csv") as f:
    reader = csv.reader(f)
    next(reader)
    grammar_list = list(reader)


for row in grammar_list:
    print(row, )
