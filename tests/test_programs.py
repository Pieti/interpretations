"""Test by interpreting a program."""

from interpretations.interpreter import Interpreter
from interpretations.lexer import Lexer
from interpretations.parser import Parser

text = """\
BEGIN

    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - - b
    END;

    x := 11;
END.
"""

def test_expressions():
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    assert interpreter.GLOBAL_SCOPE == {'a': 2, 'x': 11, 'c': 27, 'b': 25, 'number': 2}
