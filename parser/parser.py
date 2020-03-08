"""Lexical and syntax analyzer (LR parser) for a C-lite language,
written for CS-3210 Principles of Programming Languages by Devon DeJohn"""

import sys
from utilities import tokens_patterns as util
from utilities import grammar_reader as grmmr


class Lexeme:
    """Lexeme object which holds its label and corresponding token"""
    def __init__(self, label: str):
        self.label = label
        self.token = util.lookup(self.label)
        if not self.token:
            self.token = util.regexer(self.label)
# end


class Tree:
    """Generic tree-like structure for generating the parse tree"""
    def __init__(self):
        self.branch = None
        self.leaf = Lexeme

    def sprout(self, new_branch):
        """Add a subtree"""
        self.branch = new_branch
# end


class Grammar:
    """Loads the grammar files stored at parent directory 'dir'"""
    def __init__(self, dir: str):
        self.actions, self.goto = grmmr.get_slr(f"{dir}/grammar.csv")
        self.productions = grmmr.get_prods(f"{dir}/grammar.txt")
# end


class Source:
    """Source object which holds the source file, lexemes, and parse tree"""
    def __init__(self, source: str):
        self.source = source
        self.lexemes = []
        self.grammar = Grammar("grammar")
        self.parse_tree = Tree

    def lexer(self):
        """Split source at whitespace, instatiate lexeme, add to list"""
        proto_lexemes = util.reader(self.source)
        for lex in proto_lexemes:
            new_lex = Lexeme(lex)
            self.lexemes.append(new_lex)

    def parser(self):
        """Basic LR parser (shift-reduce)"""
# end


# main
if __name__ == "__main__":
    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        util.raise_error(1)

    with open(sys.argv[1], "rt") as f:
        source = f.read()
    if not source:
        util.raise_error(2)
    source = Source(source)
    source.lexer()
    for lex in source.lexemes:
        print(f"lexeme: {lex.label}\ttoken: {lex.token.value} {lex.token}")
# end
