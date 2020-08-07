from interpretations import tokens


class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser:
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
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | LPAREN expr RPAREN
                  | variable
        """
        token = self.current_token
        if token.type == tokens.PLUS:
            self.eat(tokens.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == tokens.MINUS:
            self.eat(tokens.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == tokens.INTEGER:
            self.eat(tokens.INTEGER)
            return Num(token)
        elif token.type == tokens.LPAREN:
            self.eat(tokens.LPAREN)
            node = self.expr()
            self.eat(tokens.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (tokens.MUL, tokens.DIV):
            token = self.current_token
            if token.type == tokens.MUL:
                self.eat(tokens.MUL)
            elif token.type == tokens.DIV:
                self.eat(tokens.DIV)
            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """Aritchmetic expression parser / interpreter.

        expr    : term ((PLUS | MINUS) term)*
        term    : factor ((MUL | DIV) factor)*
        factor  : (PLUS|MINUS) factor | INTEGER | LPAREN expr RPAREN
        """
        node = self.term()
        while self.current_token.type in (tokens.PLUS, tokens.MINUS):
            token = self.current_token
            if token.type == tokens.PLUS:
                self.eat(tokens.PLUS)
            elif token.type == tokens.MINUS:
                self.eat(tokens.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def program(self):
        """program : compound_statement DOT"""
        node = self.compound_statement()
        self.eat(tokens.DOT)
        return node

    def compound_statement(self):
        """compound_statement : BEGIN statment_list END"""
        self.eat(tokens.BEGIN)
        nodes = self.statement_list()
        self.eat(tokens.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statment_list : statment
                      | statement SEMI statment_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == tokens.SEMI:
            self.eat(tokens.SEMI)
            results.append(self.statement())

        if self.current_token.type == tokens.ID:
            self.error()

        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == tokens.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == tokens.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(tokens.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable: ID
        """
        node = Var(self.current_token)
        self.eat(tokens.ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def parse(self):
        node = self.program()
        if self.current_token.type != tokens.EOF:
            self.error()

        return node
