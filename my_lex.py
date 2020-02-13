""" A very stripped down implementation of a lexical analyzer for a very basic grammar. """

from enum import Enum
import sys


TOKEN = Enum(
    "TOKEN", [
        "DECLARE",
        "IDENTIFIER",
        "REAL",
        "COMPLEX",
        "FIXED",
        "FLOATING",
        "SINGLE",
        "DOUBLE",
        "BINARY",
        "DECIMAL"
    ]
)


CHARTYPE = Enum(
    "CHARTYPE", [
        "EOF",
        "LETTER",
        "ID_START",
        "BLANK",
        "OTHER"
    ]
)


TOKEN_LOOKUP = {
    "declare":      TOKEN.DECLARE,
    "identifier":   TOKEN.IDENTIFIER,
    "real":         TOKEN.REAL,
    "complex":      TOKEN.COMPLEX,
    "fixed":        TOKEN.FIXED,
    "floating":     TOKEN.FLOATING,
    "single":       TOKEN.SINGLE,
    "double":       TOKEN.DOUBLE,
    "binary":       TOKEN.BINARY,
    "decimal":      TOKEN.DECIMAL
}


CHAR_LOOKUP = {
    "abcdefghijklmnopqrstuvwxyz": CHARTYPE.LETTER,
    "$": CHARTYPE.ID_START,
    " \n\t": CHARTYPE.BLANK
}


def get_char(input_str):
    """ Reads a single character from the input and classifies its type. """
    if not input_str:
        return CHARTYPE.EOF

    for k in CHAR_LOOKUP.keys():
        if input_str[0].casefold() in k:
            return CHAR_LOOKUP[k]
    return CHARTYPE.OTHER
# end


def get_non_blank(input_str):
    """ Scrubs through the input until a non-blank character is found. """
    ignore = ""
    while True:
        char_type = get_char(input_str)
        if char_type == CHARTYPE.BLANK:
            input_str, ignore = add_char(input_str, ignore)
        else:
            return input_str
# end


def add_char(input_str, lexeme):
    """ Adds the current character from the input to the lexeme. """
    if input_str:
        lexeme += input_str[0]
    return input_str[1:], lexeme
# end


# TODO: DE-UGLIFY
def lex(input_str):
    """ Build a lexeme and then determine its corresponding token. """
    lexeme = ""
    input_str = get_non_blank(input_str)
    char_type = get_char(input_str)

    if char_type == CHARTYPE.EOF:
        return input_str, None, None

    if char_type == CHARTYPE.LETTER:
        input_str, lexeme = add_char(input_str, lexeme)
        while True:
            char_type = get_char(input_str)
            if char_type == CHARTYPE.LETTER:
                input_str, lexeme = add_char(input_str, lexeme)
            elif char_type == CHARTYPE.OTHER:
                lex_error("non_alpha")
            else:
                new_token = TOKEN_LOOKUP.get(lexeme, None)
                if not new_token:
                    lex_error("no_token", lexeme)
                return input_str, lexeme, new_token

    if char_type == CHARTYPE.ID_START:
        input_str, lexeme = add_char(input_str, lexeme)
        while True:
            char_type = get_char(input_str)
            if char_type == CHARTYPE.LETTER:
                input_str, lexeme = add_char(input_str, lexeme)
            elif char_type == CHARTYPE.OTHER:
                lex_error("non_alpha")
            else:
                return input_str, lexeme, TOKEN.IDENTIFIER

    if char_type == CHARTYPE.OTHER:
        lex_error("unrecognized")
# end


def lex_error(err_type, token=""):
    """ Return meaningful error messages. """
    msg = {
        "non_alpha": "non-alphabet character found in identifier!",
        "no_token": f"'{token}' token not found!",
        "unrecognized": "unrecognized symbol found!"
    }.get(err_type, "unknown error! You've really done it!")

    raise Exception(f"Lexical analyzer error: {msg}")
# end


# NOT MY CODE
if __name__ == "__main__":
    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    SOURCE = open(sys.argv[1], "rt")
    if not SOURCE:
        raise IOError("Couldn't open source file")
    INPUT_STR = SOURCE.read()
    SOURCE.close()
    OUTPUT = []

    # main loop
    while True:
        INPUT_STR, LEXEME, TOKEN = lex(INPUT_STR)
        if not LEXEME:
            break
        OUTPUT.append((LEXEME, TOKEN))

    # prints the output
    for (LEXEME, TOKEN) in OUTPUT:
        print(LEXEME, TOKEN)
# end
