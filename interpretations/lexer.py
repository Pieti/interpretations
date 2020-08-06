#!/usr/bin/env python

from .token import Token, IntegerToken, EofToken, OperatorToken, ParenToken, BeginToken, EndToken, AssignToken, SemiToken, DotToken
from .token import OPERATORS, PARENS, ID

RESERVED_KEYWORDS = {
    'BEGIN': BeginToken(),
    'END': EndToken()
}

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return IntegerToken(self.integer())

            if self.current_char in OPERATORS:
                operator = self.current_char
                self.advance()
                return OperatorToken(operator)

            if self.current_char in PARENS:
                paren = self.current_char
                self.advance()
                return ParenToken(paren)

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return AssignToken()

            if self.current_char == ';':
                self.advance()
                return SemiToken()

            if self.current_char == '.':
                self.advance()
                return DotToken()

            self.error()

        return EofToken()
