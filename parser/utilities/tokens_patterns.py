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
    ], start=0
)


TOKEN_LOOKUP = {
    "main": TOKEN.MAIN,
    "int": TOKEN.INT_TYPE,
    "bool": TOKEN.BOOL_TYPE,
    "float": TOKEN.FLOAT_TYPE,
    "char": TOKEN.CHAR_TYPE,
    "id": TOKEN.IDENTIFIER,
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
    "": TOKEN.EOF,
    "$": TOKEN.EOF
}


ERRORS = {
    1 : "source file missing",
    2 : "couldn't open source file",
    3 : "lexical error",
    4 : "digit expected",
    5 : "symbol missing",
    6 : "EOF expected",
    7 : "'}' expected",
    8: "'{' expected",
    9: "')' expected",
    10: "'(' expected",
    11: "main expected",
    12: "int type expected",
    13: "']' expected",
    14: "int literal expected",
    15: "'[' expected",
    16: "identifier expected",
    17: "';' expected",
    18: "'=' expected",
    19: "identifier, 'if', or 'while' expected",
    99: "syntax error"
}


EXPECTED_ERRORS = {
    TOKEN.EOF: 6,
    TOKEN.INT_TYPE: 12,
    TOKEN.MAIN: 11,
    TOKEN.OPEN_PAR: 10,
    TOKEN.CLOSE_PAR: 9,
    TOKEN.OPEN_CURLY: 8,
    TOKEN.CLOSE_CURLY: 7,
    TOKEN.IDENTIFIER: 16,
    TOKEN.SEMICOLON: 17,
    TOKEN.ASSIGNMENT: 1
}


PATTERNS = {
    re.compile(r"^[a-zA-Z]+[a-zA-Z0-9]*$"): TOKEN.IDENTIFIER,
    re.compile(r"^-?[1-9]+\d*$|^0$"): TOKEN.INT_LITERAL,
    re.compile(r"^-?0?\.\d+$|^[1-9]+\d*\.\d+$"): TOKEN.FLOAT_LITERAL,
    re.compile(r"'[a-zA-Z]'"): TOKEN.CHAR_LITERAL
}


def lookup(lex: str):
    """Match against keywords, symbols, operators"""
    tkn = TOKEN_LOOKUP.get(lex)
    if not tkn:
        return regexer(lex)
    return tkn
# end


def regexer(lex: str):
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


def reader(source: str):
    """Separate source file into proto-lexemes"""
    parsed_source = re.split(r"\s+|([\(\)\[\]\{\};,])", source)
    eof = parsed_source[-1]
    parsed_source = list(filter(None, parsed_source))
    parsed_source.append(eof)
    return parsed_source
# end


def raise_error(err_code, offender=""):
    err = ERRORS.get(err_code)
    if err == "lexical error":
        lexy = f"{err.upper()}\n    > Unrecognized symbol"
        raise Exception(f"{lexy} '{offender}' found.")
    raise Exception(f"PARSER ERROR {err_code}\n    > {err}")
# end


def read_error(state: dict):
    if len(state) == 1:
        key = next(iter(state.keys()))
    err_code = EXPECTED_ERRORS.get(key, 99)
    raise_error(err_code)
# end
