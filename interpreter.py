from token import INTEGER, OPERATOR, EOF, PLUS, MINUS, MUL, DIV


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
        result = self.factor()
        while self.current_token.type == OPERATOR and self.current_token.value in (MUL, DIV):
            token = self.current_token
            self.eat(OPERATOR)
            if token.value == MUL:
                result = result * self.factor()
            elif token.value == DIV:
                result = int(result / self.factor())
        return result

    def expr(self, text):
        """Aritchmetic expression parser / interpreter.

        expr    : term ((PLUS | MINUS) term)*
        term    : factor ((MUL | DIV) factor)*
        factor  : INTEGER
        """
        result = self.term()
        while self.current_token.type == OPERATOR and self.current_token.value in (PLUS, MINUS):
            token = self.current_token
            self.eat(OPERATOR)
            if token.value == PLUS:
                result = result + self.term()
            elif token.value == MINUS:
                result = result - self.term()

        return result


