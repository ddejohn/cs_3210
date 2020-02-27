"""Token data for C-lite language"""

from enum import Enum
import re


TOKEN = Enum(
    "TOKEN", [
        "EOF",
        "INT_TYPE",
        "MAIN",
        "OPEN_PAR",
        "CLOSE_PAR",
        "OPEN_CURLY",
        "CLOSE_CURLY",
        "OPEN_BRACKET",
        "CLOSE_BRACKET",
        "COMMA",
        "ASSIGNMENT",
        "SEMICOLON",
        "IF",
        "ELSE",
        "WHILE",
        "OR",
        "AND",
        "EQUALITY",
        "INEQUALITY",
        "LESS",
        "LESS_EQUAL",
        "GREATER",
        "GREATER_EQUAL",
        "ADD",
        "SUBTRACT",
        "MULTIPLY",
        "DIVIDE",
        "BOOL_TYPE",
        "FLOAT_TYPE",
        "CHAR_TYPE",
        "IDENTIFIER",
        "INT_LITERAL",
        "TRUE",
        "FALSE",
        "FLOAT_LITERAL",
        "CHAR_LITERAL",
        "DECIMAL",
        "QUOTATION"
    ]
)


TYPES = {
    "main": TOKEN.MAIN,
    "int": TOKEN.INT_TYPE,
    "bool": TOKEN.BOOL_TYPE,
    "float": TOKEN.FLOAT_TYPE,
    "char": TOKEN.CHAR_TYPE
}


OPERATORS = {
    "if": TOKEN.IF,
    "else": TOKEN.ELSE,
    "while": TOKEN.WHILE,
    "||": TOKEN.OR,
    "&&": TOKEN.AND,
    "==": TOKEN.EQUALITY,
    "!=": TOKEN.INEQUALITY,
    "<": TOKEN.LESS,
    "<=": TOKEN.LESS_EQUAL,
    ">": TOKEN.GREATER,
    ">=": TOKEN.GREATER_EQUAL,
}


SYMBOLS = {
    "true": TOKEN.TRUE,
    "false": TOKEN.FALSE,
    ";": TOKEN.SEMICOLON,
    "+": TOKEN.ADD,
    ",": TOKEN.COMMA,
    "=": TOKEN.ASSIGNMENT,
    "-": TOKEN.SUBTRACT,
    "*": TOKEN.MULTIPLY,
    "/": TOKEN.DIVIDE,
    "(": TOKEN.OPEN_PAR,
    ")": TOKEN.CLOSE_PAR,
    "{": TOKEN.OPEN_CURLY,
    "}": TOKEN.CLOSE_CURLY,
    "[": TOKEN.OPEN_BRACKET,
    "]": TOKEN.CLOSE_BRACKET,
}


PATTERNS = {
    re.compile("^[a-zA-Z]+\\d*[a-zA-Z]*$"): TOKEN.IDENTIFIER,
    re.compile("^[-]?[1-9]+0*$|^0$"): TOKEN.INT_LITERAL,
    re.compile("-?[1-9]+\\.\\d+|-?0?\\.\\d+"): TOKEN.FLOAT_LITERAL,
    re.compile("'[a-zA-Z]'"): TOKEN.CHAR_LITERAL
}


def lookup(data:str):
    return TYPES.get(data, OPERATORS.get(data, SYMBOLS.get(data, None)))
#
