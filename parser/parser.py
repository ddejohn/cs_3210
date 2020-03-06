"""Lexical and syntax analyzer (LR parser) for a C-lite language,
written for CS-3210 Principles of Programming Languages by Devon DeJohn"""

from utilities import tokens_patterns as util


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
        proto_lexemes = util.reader(self.source)
        for lex in proto_lexemes:
            new_lex = Lexeme(lex)
            self.lexemes.append(new_lex)

    def parser(self):
        """Basic LR parser (shift-reduce)"""
# end


# main
# if __name__ == "__main__":

#     # checks if source file was passed and if it exists
#     if len(sys.argv) != 2:
#         raise ValueError("Missing source file")
#     source = open(sys.argv[1], "rt")
#     if not source:
#         raise IOError("Couldn't open source file")
#     input = source.read()
#     source.close()
#     output = []

#     # main loop
#     while True:
#         input, lexeme, token = lex(input)
#         if lexeme == None:
#             break
#         output.append((lexeme, token))

#     # prints the output
#     for (lexeme, token) in output:
#         print(lexeme, token)
# end

