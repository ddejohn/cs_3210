from prg01_data import token_data as tkd


class Lexeme:
    def __init__(self, label:str):
        self.label = label
        self.token = tkd.lookup(self.label)
        if not self.token:
            self.token = tkd.regexer(self.label)
# end


class Tree:
    def __init__(self):
        self.branch = None
        self.leaf = Lexeme
# end


class Source:
    def __init__(self, source:str):
        self.source = source
        self.lexemes = []
        self.parse_tree = Tree

    def lexer(self):
        proto_lexemes = self.source.split()
        for lex in proto_lexemes:
            new_lex = Lexeme(lex)
            self.lexemes.append(new_lex)

    def parser(self):
        pass
# end