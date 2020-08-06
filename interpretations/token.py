from dataclasses import dataclass
from typing import Any

# Token types
# EOF token is used to indicate that
# there is no more input left for lexical analysis

INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
BEGIN = 'BEGIN'
END = 'END'
DOT = '.'
ASSIGN = ':='
SEMI = ';'
ID = 'ID'

OPERATORS = {'+': PLUS, '-': MINUS, '*': MUL, '/': DIV}
PARENS = {'(': LPAREN, ')': RPAREN}


@dataclass
class Token:
    type: str
    value: Any


class IntegerToken(Token):
    def __init__(self, value):
        value = int(value)
        super().__init__(INTEGER, value)


class OperatorToken(Token):
    def __init__(self, value):
        assert value in OPERATORS
        super().__init__(OPERATORS[value], value)


class ParenToken(Token):
    def __init__(self, value):
        assert value in PARENS
        super().__init__(PARENS[value], value)


class EofToken(Token):
    def __init__(self):
        super().__init__(EOF, None)


class BeginToken(Token):
    def __init__(self):
        super().__init__(BEGIN, BEGIN)


class EndToken(Token):
    def __init__(self):
        super().__init__(END, END)


class DotToken(Token):
    def __init__(self):
        super().__init__(DOT, DOT)


class AssignToken(Token):
    def __init__(self):
        super().__init__(ASSIGN, ASSIGN)


class SemiToken(Token):
    def __init__(self):
        super().__init__(SEMI, SEMI)


class IdToken(Token):
    def __init__(self, value):
        super().__init__(ID, value)
