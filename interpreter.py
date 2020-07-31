from parser import Parser

from token import INTEGER, OPERATOR, EOF, PLUS, MINUS, MULTIPLICATION, DIVISION

class Interpreter:
    def expr(self, text):
        parser = Parser(text)
        tokens = parser.parse()

        result = tokens[0].value
        operation = None
        for token in tokens[1:]:
            if token.type == EOF:
                return result
            if token.type == OPERATOR:
                operation = token.value
            else:
                if operation == PLUS:
                    result = result + token.value
                elif operation == MINUS:
                    result = result - token.value

        return result


