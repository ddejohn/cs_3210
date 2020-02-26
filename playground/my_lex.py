""" A very stripped down implementation of a lexical analyzer for a very basic grammar. """

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


class Lexeme:
    def __init__(self):
        self.label = str
        self.token = TOKEN


class Source:
    def __init__(self, src):
        self.src = str
        self.lexemes = list     # of Lexeme
        self.tokens = list      # of TOKEN

    def src_print(self):
        return


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
                lex_error("alpha")
            else:
                new_token = TOKEN_LOOKUP.get(lexeme, None)
                if not new_token:
                    lex_error("no token", lexeme)
                return input_str, lexeme, new_token

    if char_type == CHARTYPE.ID_START:
        input_str, lexeme = add_char(input_str, lexeme)
        while True:
            char_type = get_char(input_str)
            if char_type == CHARTYPE.LETTER:
                input_str, lexeme = add_char(input_str, lexeme)
            elif char_type == CHARTYPE.OTHER:
                lex_error("alpha")
            else:
                return input_str, lexeme, TOKEN.IDENTIFIER

    if char_type == CHARTYPE.OTHER:
        lex_error("unrecognized", char_type)
# end


def lex_error(err_type, offender=""):
    """ Return meaningful error messages. """
    msg = {
        "alpha": f"non-alphabet character '{offender}' found in identifier.",
        "no token": f"'{offender}' token not found!",
        "unrecognized": f"unrecognized symbol '{offender}' found.",
        "no src": "no source file provided.",
        "no open": "unable to open source file."
    }.get(err_type, "unknown error.")

    raise Exception(f"Lexical analyzer error: {msg}")
# end


# TODO: rewrite using source and lexeme classes
if __name__ == "__main__":
    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        lex_error("no src")

    SOURCE = open(sys.argv[1])
    if not SOURCE:
        lex_error("no open")

    INPUT_STR = SOURCE.read()
    SOURCE.close()
    OUTPUT = []

    source = Source(INPUT_STR)
    


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



def lexer(source):
    next_char = get_char(source)
    # if next_char
    lexify = {
        CHARTYPE.EOF: "",
        CHARTYPE.LETTER: "",
        CHARTYPE.ID_START: "",
        CHARTYPE.BLANK: "",
        CHARTYPE.OTHER: ""
    }



def lexeme_builder(source):
    new_lexeme = Lexeme()








def lexer(source):
    proto_lexemes = source.split()
    for lex in proto_lexemes:
        