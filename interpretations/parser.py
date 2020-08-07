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


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class ProcedureDecl(AST):
    def __init__(self, proc_name, block_node):
        self.proc_name = proc_name
        self.block_node = block_node


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg=None):
        if msg:
            raise Exception(f"{msg}, {self.lexer.pos}")
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Token {self.current_token} is not of type {token_type}")

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER_CONST
                  | REAL_CONST
                  | LPAREN expr RPAREN
                  | variable
        """
        token = self.current_token
        if token.type in (tokens.PLUS, tokens.MINUS):
            self.eat(token.type)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type in (tokens.INTEGER_CONST, tokens.REAL_CONST):
            self.eat(token.type)
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
        """
            term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (tokens.MUL, tokens.INTEGER_DIV, tokens.FLOAT_DIV):
            token = self.current_token
            self.eat(token.type)

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

    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        """declarations : VAR (variable_declaration SEMI)+
                        | (PROCEDURE ID SEMI block SEMI)*
                        | empty
        """
        declarations = []

        if self.current_token.type == tokens.VAR:
            self.eat(tokens.VAR)
            while self.current_token.type == tokens.ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(tokens.SEMI)

        while self.current_token.type == tokens.PROCEDURE:
            self.eat(tokens.PROCEDURE)
            proc_name = self.current_token.value
            self.eat(tokens.ID)
            self.eat(tokens.SEMI)
            block_node = self.block()
            proc_decl = ProcedureDecl(proc_name, block_node)
            declarations.append(proc_decl)
            self.eat(tokens.SEMI)

        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]
        self.eat(tokens.ID)

        while self.current_token.type == tokens.COMMA:
            self.eat(tokens.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(tokens.ID)

        self.eat(tokens.COLON)

        type_node = self.type_spec()
        return [VarDecl(var_node, type_node) for var_node in var_nodes]

    def type_spec(self):
        """type_spec : INTEGER
                     | REAL
        """
        token = self.current_token
        if self.current_token.type == tokens.INTEGER:
            self.eat(tokens.INTEGER)
        else:
            self.eat(tokens.REAL)
        node = Type(token)
        return node

    def program(self):
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(tokens.PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(tokens.SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(tokens.DOT)
        return program_node

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
