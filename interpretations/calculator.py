#!/usr/bin/env python

from .interpreter import Interpreter
from .parser import Parser
from .lexer import Lexer


def calculate(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    return interpreter.interpret()
