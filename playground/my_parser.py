# CS3210 - Principles of Programming Languages - Spring 2020
# A recursive-descent parser for an expression
# written by Dr. Thyago Mota, modified by Devon DeJohn
from enum import IntEnum
import sys


# all char classes
class CharClass(IntEnum):
    EOF = -1
    LETTER = 1
    DIGIT = 2
    OPERATOR = 3
    PUNCTUATOR = 4
    QUOTE = 5
    BLANK = 6
    DELIMITER = 7
    OTHER = 8


# all tokens
class Token(IntEnum):
    EOF = -1
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    IDENTIFIER = 5
    LITERAL = 6


# lexeme to token conversion map
TOKEN_LOOKUP = {
    "$" : Token.EOF,
    "+" : Token.ADDITION,
    "-" : Token.SUBTRACTION,
    "*" : Token.MULTIPLICATION,
    "/" : Token.DIVISION
}


# a tree-like data structure
class Tree:
    TAB = "   "

    def __init__(self, data=None):
        self.data = data
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab=""):
        if not self.data:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)


# Raise an exception
def error_msg(err_type, offender=""):
    msg = {
        "no source":        "source file missing.",
        "source open":      "couldn't open source file.",
        "lex error":        f"'{offender}' symbol unrecognized.",
        "grammar open":     "couldn't open grammar file.",
        "SLR open":         "couldn't open SLR table file.",
        "eof":              f"EOF expected, got '{offender}'.",
        "id":               f"identifier expected, got '{offender}'.",
        "special word":     "special word missing.",
        "symbol":           "symbol missing",
        "data type":        f"data type expected, got '{offender}'.",
        "id or lit":        f"identifier or literal expected, got '{offender}'."
    }.get(err_type, "whoa! Unknown error! You've really done it!")

    raise Exception(f"Syntax analyzer error: {msg}")
# end


# reads the next char from input_str and returns its class
def get_char(input_str):
    if len(input_str) == 0:
        return (None, CharClass.EOF)
    char = input_str[0].lower()
    if char.isalpha():
        return (char, CharClass.LETTER)
    if char.isdigit():
        return (char, CharClass.DIGIT)
    if char == '"':
        return (char, CharClass.QUOTE)
    if char in ['+', '-', '*', '/']:
        return (char, CharClass.OPERATOR)
    if char in ['.', ';']:
        return (char, CharClass.PUNCTUATOR)
    if char in [' ', '\n', '\t']:
        return (char, CharClass.BLANK)
    if char in ['(', ')']:
        return (char, CharClass.DELIMITER)
    return (char, CharClass.OTHER)


# calls get_char and add_char until it returns a non-blank
def get_non_blank(input_str):
    ignore = ""
    while True:
        _, char_type = get_char(input_str)
        if char_type == CharClass.BLANK:
            input_str, ignore = add_char(input_str, ignore)
        else:
            return input_str
# end


# adds the next char from input_str to lexeme, advancing the input_str by one char
def add_char(input_str, lexeme):
    if len(input_str) > 0:
        lexeme += input_str[0]
        input_str = input_str[1:]
    return (input_str, lexeme)
# end


# returns the next (lexeme, token) pair or ("", EOF) if EOF is reached
def lex(input_str):
    input_str = get_non_blank(input_str)

    char, char_type = get_char(input_str)
    lexeme = ""

    if char_type == CharClass.EOF:
        return (input_str, lexeme, Token.EOF)

    if char_type == CharClass.LETTER:
        input_str, lexeme = add_char(input_str, lexeme)
        while True:
            char, char_type = get_char(input_str)
            if char_type in [CharClass.LETTER, CharClass.DIGIT]:
                input_str, lexeme = add_char(input_str, lexeme)
            else:
                return (input_str, lexeme, Token.IDENTIFIER)

    if char_type == CharClass.DIGIT:
        input_str, lexeme = add_char(input_str, lexeme)
        while True:
            char, char_type = get_char(input_str)
            if char_type == CharClass.DIGIT:
                input_str, lexeme = add_char(input_str, lexeme)
            else:
                return (input_str, lexeme, Token.LITERAL)

    if char_type == CharClass.OPERATOR:
        input_str, lexeme = add_char(input_str, lexeme)
        if lexeme in TOKEN_LOOKUP:
            return (input_str, lexeme, TOKEN_LOOKUP[lexeme])

    if char_type == CharClass.DELIMITER:
        if char in ["(", ")"]:
            input_str, lexeme = add_char(input_str, lexeme)
            return (input_str, lexeme, TOKEN_LOOKUP[lexeme])

    error_msg("lex error", char)
# end


# parse the input_str file
def parse(input_str):
    """ start parsing a new input"""
    tree = Tree()
    parse_expr(input_str, tree)
    return tree
# end


# <expression>  -> <term> <expression’>
# <expression'> -> (+|-) <term> <expression'>
# <expression'> -> epsilon
def parse_expr(input_str, tree):
    """ parse the current expression """
    tree.data = "<expression>"
    input_str, lexeme, token = parse_term(input_str, tree)

    # parse more terms
    while True:
        if token in [Token.ADDITION, Token.SUBTRACTION]:
            tree.add(lexeme)
            input_str, lexeme, token = parse_term(input_str, tree)
        elif token == Token.EOF:
            break
        else:
            error_msg("eof")

    return tree
# end


# <term> -> <factor> <term’>
# <term'> -> (*|/) <factor> <term'>
# <term'> -> epsilon
def parse_term(input_str, tree):
    """ parse the current lexeme """
    subtree = Tree(data="<term>")
    tree.add(subtree)
    input_str, lexeme, token = parse_factor(input_str, subtree)

    # parse more factors
    while True:
        if token in [Token.MULTIPLICATION, Token.DIVISION]:
            subtree.add(lexeme)
            input_str, lexeme, token = parse_factor(input_str, subtree)
        else:
            break

    return input_str, lexeme, token
# end


# <factor> -> <identifier> | <literal>
def parse_factor(input_str, tree):
    """ parse the current lexeme """
    subtree = Tree(data="<factor>")
    tree.add(subtree)
    input_str, lexeme, token = lex(input_str)

    if token in [Token.IDENTIFIER, Token.LITERAL]:
        subtree.add(lexeme)
        input_str, lexeme, token = lex(input_str)
    else:
        error_msg("id or lit")

    return input_str, lexeme, token
# end


# main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        error_msg("no source")
    SOURCE = open(sys.argv[1], "rt")
    if not SOURCE:
        error_msg("source open")
    FILE_CONTENTS = SOURCE.read()
    SOURCE.close()
    OUTPUT = []

    # calls the parser function
    PARSE_TREE = parse(FILE_CONTENTS)

    # prints the tree if the code is syntactically correct
    if PARSE_TREE:
        print("Input_str is syntactically correct!")
        print("Parse Tree:")
        PARSE_TREE.print()
    else:
        # prints error message otherwise
        print("Code has syntax errors!")
#end
