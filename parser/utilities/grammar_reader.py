"""Generate action, goto, and productions for a given grammar"""

import csv


def get_slr(path) -> list:
    """Read a grammar table as csv, return separate ACTION and GOTO tables"""
    with open(path, "rt") as g:
        reader = csv.reader(g)
        next(reader)
        grammar = list(reader)

    _, grammar = _col_split(grammar, 1)
    eof = grammar[0][:].index("$")
    return _col_split(grammar, eof+1)
# end


def get_prods(path) -> dict:
    """Parse a production list for the grammar at 'path'"""
    with open(path) as p:
        productions = p.read()
    productions = filter(None, productions.split("\n"))
    productions = [row.split(" -> ") for row in productions]
    return {i: v for i,v in enumerate(productions)}
# end


def _col_split(mat, col) -> list:
    """Split a 2D array into left and right 2D arrays at column 'col'"""
    left_mat = []
    right_mat = []
    for row in mat:
        left_mat.append(row[:col])
        right_mat.append(row[col:])
    return left_mat, right_mat
# end
