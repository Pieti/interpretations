#!/usr/bin/env python

from lexer import Lexer
from token import INTEGER, OPERATOR, EOF


class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.tokens = []

    def error(self):
        raise Exception("Parser error")

    def eat(self, token_types):
        token = self.lexer.get_next_token()
        if token.type in token_types:
            return token
        self.error()

    def parse(self):
        self.lexer.reset()

        self.tokens.append(self.eat(INTEGER))

        while True:
            token = self.eat([OPERATOR, EOF])
            self.tokens.append(token)
            if token.type == EOF:
                break

            token = self.eat([INTEGER])
            self.tokens.append(token)

        return self.tokens


        
