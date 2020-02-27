from dataclasses import dataclass
from typing import List
from prg01_data import token_data as tkd


class Lexeme:
    def __init__(self, label:str):
        self.label = label
        self.token = tkd.lookup(self.label)
        if not self.token:
            self.token = regexer(self.label)
# end


@dataclass
class Source:
    src: str
    lexemes: List[Lexeme]
    tokens: List[tkd.TOKEN]
# end


def regexer(lex):
    for k, v in tkd.PATTERNS.items():
        if k.match(lex):
            return v
    # else return lex_error(lex)
# end


def lexer(source:Source):
    proto_lexemes = source.src.split()
    for lex in proto_lexemes:
        new_lex = Lexeme(lex)
        source.lexemes.append(new_lex)
# end
