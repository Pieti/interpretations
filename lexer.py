#!/usr/bin/env python

from token import IntegerToken, EofToken, OperatorToken, ParenToken, OPERATORS, PARENS

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

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

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


            self.error()

        return EofToken()
