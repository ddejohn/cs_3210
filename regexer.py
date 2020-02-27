# def is_id(lex:str):
#     if bool(re.match("^[a-zA-Z]+\\d*[a-zA-Z]*$", lex)):
#         return tkd.TOKEN.IDENTIFIER
#     return None


# def is_int(lex:str):
#     if bool(re.match("^[-]?[1-9]+0*$|^0$", lex)):
#         return tkd.TOKEN.INT_LITERAL


# def is_flt(lex:str):
#     if bool(re.match("-?[1-9]+\\.\\d+|-?0?\\.\\d+", lex)):
#         return tkd.TOKEN.FLOAT_LITERAL


# def is_chr(lex:str):
#     if bool(re.match("'[a-zA-Z]'", lex)):
#         return tkd.TOKEN.CHAR_LITERAL
#     return None

import re


def match(lex):
    regexes = {
        re.compile("^[a-zA-Z]+\\d*[a-zA-Z]*$"): "ID",
        re.compile("^[-]?[1-9]+0*$|^0$"): "INT",
        re.compile("-?[1-9]+\\.\\d+|-?0?\\.\\d+"): "FLOAT",
        re.compile("'[a-zA-Z]'"): "CHAR"
    }

    for k, v in regexes.items():
        if k.match(lex):
            return v
    return "NO MATCH"
#

tests = ["a", "'a'", "a.a", "'aaa'", "12", "a2", ".14", "a1a", "-0.2"]

for t in tests:
    print(f"{t}:\t\t{match(t)}")