import re
from prg01_data import token_data as tkd


class Lexeme:
    def __init__(self, label:str):
        self.label = label
        self.token = tkd.lookup(self.label)
        if not self.token:
            self.token = is_other(self.label)


class Source:
    def __init__(self, src):
        self.src = str
        self.lexemes = list     # of Lexeme
        self.tokens = list      # of TOKEN

    def src_print(self):
        return


def is_other(lex:str):
    # starts with alpha
        # isalnum() -> is_id
        # error
    # starts with digit
        # isdigit() -> is_int
        # split(".") == 2
            # [0], [1] is_int -> is_flt
        # error
    # starts with '
        # single alpha
            # ends with ' -> is_chr
        # error
    # error
    return ""


def is_id(lex:str):
    if lex.isalnum():
        return tkd.TOKEN.IDENTIFIER
    return None


def is_int(lex:str):
    if lex.isdigit():
        return tkd.TOKEN.INT_LITERAL
    elif len(lex.split(".")) == 2:
        return is_flt(lex)
    return None


def is_flt(lex:str):
    integral, fractional = lex.split(".")
    if integral.isdigit() and fractional.isdigit():
        return tkd.TOKEN.FLOAT_LITERAL
    return None


def is_chr(lex:str):
    if bool(re.match("('[a-zA-Z]')", lex)):
        return tkd.TOKEN.CHAR_LITERAL
    return None


def go_to(char):
    return {
        "abcdefghijklmnopqrstuvwxyz": is_id,
        "0123456789": is_int,
        "'": is_chr
    }.get(char, None)


def lexer(source:Source):
    proto_lexemes = source.src.split()
    for lex in proto_lexemes:
        new_lex = Lexeme(lex)
        source.lexemes.append(new_lex)
