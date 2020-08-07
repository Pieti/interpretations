"""Test by interpreting a program."""

from interpretations.interpreter import Interpreter
from interpretations.lexer import Lexer
from interpretations.parser import Parser
from interpretations.symbol import SymbolTableBuilder, BuiltinTypeSymbol, VarSymbol

text = """
PROGRAM myprog;
VAR
    number : INTEGER;
    a, b   : INTEGER;
    y      : REAL;

BEGIN {myprog}
    number := 2;
    a := number;
    b := 10 * a + 10 * number DIV 4;
    y := 20 / 7 + 3.14
END. {myprog}
"""

def test_interpreter():
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    assert interpreter.GLOBAL_SCOPE['a'] == 2
    assert interpreter.GLOBAL_SCOPE['b'] == 25
    assert interpreter.GLOBAL_SCOPE['y'] == 5.997142857142857
