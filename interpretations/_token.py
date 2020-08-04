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
