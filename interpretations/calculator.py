#!/usr/bin/env python

from ._interpreter import Interpreter
from ._parser import Parser
from ._lexer import Lexer


def calculate(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    return interpreter.interpret()


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue

        print(calculate(text))

if __name__ == '__main__':
    main()
