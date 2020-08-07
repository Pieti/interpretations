"""Test by interpreting a program."""

from interpretations.interpreter import Interpreter
from interpretations.lexer import Lexer
from interpretations.parser import Parser
from interpretations.symbol import SymbolTableBuilder, BuiltinTypeSymbol, VarSymbol

text = """
PROGRAM myprog;
VAR
    a : INTEGER;

PROCEDURE P1;
VAR
    a : REAL;
    k : INTEGER;

    PROCEDURE P2;
    VAR
        a, z : INTEGER;
    BEGIN {P2}
        z := 777;
    END; {P2}

BEGIN {P1}
END; {P1}

BEGIN {myprog}
    a := 10;
END. {myprog}
"""

def test_interpreter():
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    assert interpreter.GLOBAL_SCOPE['a'] == 10
