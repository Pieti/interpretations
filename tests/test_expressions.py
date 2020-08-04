"""Test by evaluating some expressions."""

from interpretations.calculator import calculate

expressions = (
        ("1+1", 2),
        ("2-1", 1),
        ("2*2", 4),
        ("10/2", 5),
        ("9-5+3+11", 18),
        ("10+1+2-3+4+6-15", 5),
        ("2+7*4", 30),
        ("100-50/2", 75),
        ("7*(2+2)", 28),
        ("8/2/2", 2),
        ("2*(2*3-6/2)", 6),
        ("7+(((3+2)))", 12),
        ("7+3*(10/(12/(3+1)-1))/(2+3)-5-3+(8)", 10)
)

def test_expressions():
    for text, result in expressions:
        assert calculate(text) == result


def test_whitespace():
    assert calculate(" 1 + 2 ") == 3

