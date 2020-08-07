"""Test by interpreting a program."""

from interpretations.interpreter import Interpreter
from interpretations.lexer import Lexer
from interpretations.parser import Parser

text = """
PROGRAM Part10AST;
VAR
   a, b : INTEGER;
   y    : REAL;

BEGIN {Part10AST}
   a := 2;
   b := 10 * a + 10 * a DIV 4;
   y := 20 / 7 + 3.14;
END.  {Part10AST}
"""

def test_expressions():
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    assert interpreter.GLOBAL_SCOPE['a'] == 2
    assert interpreter.GLOBAL_SCOPE['b'] == 25
    assert interpreter.GLOBAL_SCOPE['y'] == 5.997142857142857
