import csv


def get_slr(path):
    """Read a grammar table as csv, return separate ACTION and GOTO tables"""
    with open(path) as g:
        reader = csv.reader(g)
        next(reader)
        grammar = list(reader)

    _, grammar = _col_split(grammar, 1)
    eof = grammar[0][:].index("$")
    return _col_split(grammar, eof+1)


def get_productions(path):
    """Parse a production list for the grammar at 'path'"""
    with open(path) as p:
        productions = p.read()
    


def _col_split(mat, col):
    """Split a 2D array into left and right 2D arrays at column 'col'"""
    left_mat = []
    right_mat = []
    for row in mat:
        left_mat.append(row[:col])
        right_mat.append(row[col:])
    return left_mat, right_mat
