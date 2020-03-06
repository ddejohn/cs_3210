"""Token data and regex pattern matchers for a C-lite language,
written for CS-3210 Principles of Programming Languages by Devon DeJohn"""

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


ERRORS = Enum(
    "ERRORS", [
        "source file missing",
        "couldn't open source file",
        "lexical error",
        "digit expected",
        "symbol missing",
        "EOF expected",
        "'}' expected",
        "'{' expected",
        "')' expected",
        "'(' expected",
        "main expected",
        "int type expected",
        "']' expected",
        "int literal expected",
        "'[' expected",
        "identifier expected",
        "';' expected",
        "'=' expected",
        "identifier, 'if', or 'while' expected",
        "syntax error"
    ]
)


PATTERNS = {
    re.compile(r"^[a-zA-Z]+[a-zA-Z0-9]*$"): TOKEN.IDENTIFIER,
    re.compile(r"^-?[1-9]+\d*$|^0$"): TOKEN.INT_LITERAL,
    re.compile(r"^-?0?\.\d+$|^[1-9]+\d*\.\d+$"): TOKEN.FLOAT_LITERAL,
    re.compile(r"'[a-zA-Z]'"): TOKEN.CHAR_LITERAL
}


def lookup(data:str):
    """Match against keywords, symbols, operators"""
    return TYPES.get(data, OPERATORS.get(data, SYMBOLS.get(data, None)))
# end


def regexer(lex):
    """Match against literal patterns"""
    tkn = None
    for k, v in PATTERNS.items():
        if k.match(lex):
            tkn = v
            break
    if not tkn:
        raise_error(3, lex)
    return tkn
# end


def reader(data:str):
    """Separate source file into proto-lexemes"""
    symbol_match = re.split(r"\s+|([\(\)\[\]\{\};,])", data)
    return list(filter(None, symbol_match))
# end


def raise_error(err_code, offender=""):
    err = ERRORS(err_code).name
    got = ""
    if "expected" in err:
        got = f" -- got '{offender}' instead"
    if err == "lexical error":
        lexy = f"{err.upper()}\n    > Unrecognized symbol"
        raise Exception(f"{lexy} '{offender}' found.")
    raise Exception(f"PARSER ERROR {err_code}\n    > {err}{got}")
# end
