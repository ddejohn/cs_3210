"""Lexical and syntax analyzer (LR parser) for a C-lite language,
written for CS-3210 Principles of Programming Languages by Devon DeJohn"""

import sys
import numpy as np
from utilities import tokens_patterns as util
from utilities import grammar_reader as grmmr


class Lexeme:
    """Lexeme object which holds its label and corresponding token"""
    def __init__(self, label: str):
        self.label = label
        self.token = util.lookup(self.label)
# end


class Tree:
    """Generic tree-like structure for generating the parse tree"""
    def __init__(self, leaf: Lexeme):
        self.leaf = leaf
        self.branch = None

    def sprout(self, new_branch):
        """Add a subtree"""
        self.branch = new_branch
# end


# THIS IS SO AWFUL
# NEED TO MAKE MY OWN SLR TABLE GENERATOR
class Grammar:
    """Loads the grammar files stored at parent directory 'dir'"""
    def __init__(self, dir: str):
        self.actions, self.goto = grmmr.get_slr(f"{dir}/grammar.csv")
        self.productions = grmmr.get_prods(f"{dir}/grammar.txt")
        new_header = []
        for symbol in self.actions[0]:
            symbol = util.lookup(symbol)
            new_header.append(symbol.value)
        self.actions[0] = new_header
        self.actions = np.asarray(self.actions)
        self.actions = self.actions[:, self.actions[0].argsort()]
        self.actions = self.actions[1:, :]
# end


class Source:
    """Source object which holds the source file, lexemes, and parse tree"""
    def __init__(self, source: str):
        self.source = source
        self.grammar = Grammar("grammar")
        self.lexemes = []
        self.parse_tree = Tree
        self.stack = []

    def lexer(self):
        """Split source at whitespace, instatiate lexeme, add to list"""
        proto_lexemes = util.reader(self.source)
        for lex in proto_lexemes:
            new_lex = Lexeme(lex)
            self.lexemes.append(new_lex)

    def parser(self):
        """Basic LR parser (shift-reduce)"""
        state = 0
        ungrafted_trees = []
        self.stack.append(state)
        for tkn in self.lexemes:
            action = self.grammar.actions[(state, tkn.value)]
            if not action:
                raise_error(19)
            elif action[0] == "s":
                self.stack.append(tkn.label)
                self.stack.append(int(action[1:]))
                ungrafted_trees.append(Tree(tkn))
            elif action[0] == "r":
                pass
            else:
                # graft trees
                pass


        # for tkn in self.lexemes:


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
    # for lex in source.lexemes:
    #     print(f"lexeme: {lex.label}\ttoken: {lex.token.value} {lex.token}")
    for g in source.grammar.actions:
        print(g,)
    # stack = [0, ]

# end
