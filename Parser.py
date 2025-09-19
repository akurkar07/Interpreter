from tokens import *
from ASTNodes import *

class Parser(object):
    """
    The grammar is represented in the Parser's methods. The Parser turns text into an AST for the tree visit to evaluate\n
    Syntax errors come from here
    """
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParserError(f'Invalid syntax at token {self.current_token}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        "program : PROGRAM variable SEMI block DOT"
        self.eat(PROGRAM)
        program_name = self.variable()
        self.eat(SEMI)
        result = self.block()
        self.eat(DOT)
        return result

    def block(self):
        "block : declarations compound_statement"
        vars = self.declarations()
        cmpd_nodes = self.compound_statement()
        return Block(vars, cmpd_nodes)

    def declarations(self):
        """declarations : VAR (variable_declaration SEMI)+
                        | empty
        """
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)
        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]  # first ID
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return var_declarations
    
    def type_spec(self):
        """type_spec : INTEGER
                    | REAL
        """
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        node = Type(token)
        return node

    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root


    def statement_list(self):
        """
        statement_list : statement
                    | statement SEMI statement_list
        """
        nodes = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            if self.current_token.type == END:
                break
            nodes.append(self.statement())
        return nodes

    def statement(self):
        """
        statement : compound_statement
                | assignment_statement
                | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
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
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(token, left, right)
        return node
    
    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        "empty :"
        return NoOp()

    def expr(self):
        """
        Returns an value from the result of the +/- arithmetic expressions

        expr: term((PLUS/MINUS)term)*"""
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                right = self.term()
                node = BinaryOperation("+", node, right)
            elif op.type == MINUS:
                self.eat(MINUS)
                right = self.term()
                node = BinaryOperation("-", node, right)
        return node
    
    # parser term precedence
    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, FLOAT_DIV, INTEGER_DIV):
            op = self.current_token
            if op.type == MUL:
                self.eat(MUL); right = self.factor()
                node = BinaryOperation('*', node, right)
            elif op.type == FLOAT_DIV:
                self.eat(FLOAT_DIV); right = self.factor()
                node = BinaryOperation('/', node, right)
            elif op.type == INTEGER_DIV:
                self.eat(INTEGER_DIV); right = self.factor()
                node = BinaryOperation('div', node, right)
        return node

    
    def factor(self):
        """
        Returns an integer value for the current token and then eats it

        OR

        Returns the integer value of the expression in the parentheses and eats the parentheses

        factor: (PLUS|MINUS) factor | INTEGER_CONST | LPAREN expr RPAREN | variable
        """
        token = self.current_token
        if token.type in (PLUS, MINUS):
            self.eat(token.type)                       # consume the unary operator
            child = self.factor()                      # then parse the operand
            return UnaryOperation(token.value, child)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
        elif token.type == INTEGER_CONST:
            node = IntegerNode(token.value)
            self.eat(INTEGER_CONST)
        elif token.type == REAL_CONST:
            node = RealNode(token.value)
        else:
            node = self.variable()
        return node
    
    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node