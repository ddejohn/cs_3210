"""Lexical and syntax analyzer (LR parser) for a C-lite language,
written for CS-3210 Principles of Programming Languages by Devon DeJohn"""

from data import token_data as tkd


class Lexeme:
    """Lexeme object which holds its label and corresponding token"""
    def __init__(self, label: str):
        self.label = label
        self.token = tkd.lookup(self.label)
        if not self.token:
            self.token = tkd.regexer(self.label)
# end


class Tree:
    """Generic tree-like structure for generating the parse tree"""
    def __init__(self):
        self.branch = None
        self.leaf = Lexeme

    def sprout(self, new_branch: Tree):
        """Add a subtree"""
        self.branch = new_branch
# end


class Source:
    """Source object which holds the source file, lexemes, and parse tree"""
    def __init__(self, source: str):
        self.source = source
        self.lexemes = []
        self.parse_tree = Tree

    def lexer(self):
        """Split source at whitespace, instatiate lexeme, add to list"""
        proto_lexemes = self.source.split()
        for lex in proto_lexemes:
            new_lex = Lexeme(lex)
            self.lexemes.append(new_lex)

    def parser(self):
        """Basic LR parser (shift-reduce)"""
# end