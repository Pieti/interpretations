# Token types
# EOF token is used to indicate that
# there is no more input left for lexical analysis

INTEGER = 'INTEGER'
EOF = 'EOF'
OPERATOR = 'OPERATOR'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'

OPERATORS = {'+': PLUS, '-': MINUS, '*': MUL, '/': DIV}


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()


class IntegerToken(Token):
    def __init__(self, value):
        value = int(value)
        super().__init__(INTEGER, value)


class OperatorToken(Token):
    def __init__(self, value):
        super().__init__(OPERATOR, OPERATORS[value])


class EofToken(Token):
    def __init__(self):
        super().__init__(EOF, None)
