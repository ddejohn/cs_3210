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
    tab = "    "
    
    def __init__(self, leaf: Lexeme):
        self.leaf = leaf
        self.branches = []

    def sprout(self, new_branch):
        """Add a subtree"""
        self.branches.append(new_branch)
    
    def prnt(self, tabs=1):
        if self.branches:
            print(f"{tabs*Tree.tab}{self.leaf}")
            tabs += 1
            for branch in self.branches:
                if isinstance(branch, Tree):
                    branch.prnt(tabs)
                else:
                    print(f"{tabs}{branch}")
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
            new_header.append(symbol)

        self.actions = {
            st: {
                v: acts[i] for i, v in enumerate(new_header) if acts[i]
            } for st, acts in enumerate(self.actions[1:])
        }

        # print(self.goto[0],)

        self.goto = {
            st: {
                v: int(gotos[i]) for i,v in enumerate(self.goto[0]) if gotos[i]
            } for st, gotos in enumerate(self.goto[1:]) if any(gotos)
        }

        # print(self.goto,)
        # self.actions = actions
        # self.goto = goto
# end


class Source:
    """Source object which holds the source file, lexemes, and parse tree"""
    def __init__(self, source: str):
        self.source = source
        self.grammar = Grammar("grammar")
        self.lexemes = self.lexer()
        self.parse_tree = self.parser()

    def lexer(self):
        """Split source at whitespace, instatiate lexeme, add to list"""
        lexemes = []
        proto_lexemes = util.reader(self.source)
        for lex in proto_lexemes:
            new_lex = Lexeme(lex)
            lexemes.append(new_lex)
        return lexemes

    def parser(self):
        """Basic LR parser (shift-reduce)"""
        state = 0
        counter = 0
        ungrafted_trees = []
        tkn = self.lexemes[counter].token
        stack = [state, tkn.name]
        while True:
            action = self.grammar.actions[state][tkn]
            # print(f"stack: {stack}")
            # print(f"state: {state}\ntkn: {tkn.name}")
            # print(f"action: {action}")
            if not action:
                util.raise_error(19)
            elif action[0] == "s":
                state = int(action[1:])
                ungrafted_trees.append(Tree(tkn.name))
                counter += 1
                tkn = self.lexemes[counter].token
                stack.append(state)
                stack.append(tkn.name)
            elif action[0] == "r":
                prod = self.grammar.productions.get(int(action[1:]))
                lhs, rhs = prod
                pop_num = len(rhs.split())
                # print(f"LHS: {lhs}\tRHS: {rhs}")
                for _ in range(pop_num*2):
                    stack.pop()
                state = stack[-2]
                stack.append(self.grammar.goto[state][lhs])
                state = stack[-1]
                stack.append(lhs)
                new_tree = Tree(lhs)
                for tree in ungrafted_trees[-pop_num:]:
                    new_tree.sprout(tree)
                ungrafted_trees = ungrafted_trees[:pop_num]
                ungrafted_trees.append(new_tree)
            else:
                prod = self.grammar.productions[0]
                lhs, rhs = prod
                new_tree = Tree(lhs)
                for tree in ungrafted_trees:
                    new_tree.sprout(tree)
                return new_tree
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
    source.parse_tree.prnt()
# end
