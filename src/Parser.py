from tokens import *
from nodes import *

class Parser(object):
    """
    The parser operates at the token level.\n
    The grammar is represented in the Parser's methods. The Parser turns text into an AST for the semantic analyser visit\n
    Each method in the parser is responsible for turning a sequence of tokens into a node in the AST\n
    Syntax errors come from here
    """
    def __init__(self,lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def __str__(self):
        return f"Parser | Current Token: {self.current_token}"
    
    def __repr__(self):
        return self.__str__()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ParserError(
                                f"Invalid token at line {self.lexer.line}, position {self.lexer.column}. "
                                f"Expected {token_type}, got {self.current_token.type}"
                             )


    def program(self):
        "program : PROGRAM variable SEMI block DOT"
        self.eat(PROGRAM)
        program_name = self.variable()
        self.eat(SEMI)
        block_node = self.block()
        self.eat(DOT)
        return Program(program_name, block_node)

    def block(self):
        "block : declarations compound_statement"
        vars = self.declarations()
        cmpd_nodes = self.compound_statement()
        return Block(vars, cmpd_nodes)

    def declarations(self):
        """declarations : VAR (variable_declaration SEMI)+
                        \\| empty
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

        while self.current_token.type == COMMA: # keeps receiving variables with commas
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec() # We determine their type
        var_declarations = [
            VarDecl(var_node, type_node) for var_node in var_nodes
        ]
        return var_declarations # then return the list of var declarations with that type
    
    def type_spec(self):
        """
        Returns the type bsed on the INTEGER or REAL after the colon

        type_spec : INTEGER
                    \\| REAL
                    \\| BOOLEAN
        """
        token = self.current_token 
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        elif self.current_token.type == REAL:
            self.eat(REAL)
        elif self.current_token.type == BOOLEAN:
            self.eat(BOOLEAN)
        else:
            self.error()
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
                    \\| statement SEMI statement_list
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
                | if_statement
                | while_statement
                | writeln_statement
                | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == IF:
            node = self.if_statement()
        elif self.current_token.type == WHILE:
            node = self.while_statement()
        elif self.current_token.type == WRITELN:
            node = self.writeln_statement()        
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expression
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expression()
        node = Assign(token, left, right)
        return node
    
    def if_statement(self):
        self.eat(IF)
        condition = self.expression()
        self.eat(THEN)
        true_statement = self.statement()
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            false_statement = self.statement()
        else:
            false_statement = None
        node = If(condition,true_statement,false_statement)
        return node
    
    def while_statement(self):
        self.eat(WHILE)
        condition = self.expression()
        self.eat(DO)
        statement = self.statement()
        node = While(condition,statement)
        return node
    
    def writeln_statement(self):
        self.eat(WRITELN)
        self.eat(LPAREN)
        expression = self.expression()
        self.eat(RPAREN)
        node = WriteLn(expression)
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

    def expression(self):
        """
        Returns the value of either a plain arithmetic expression or
        a comparison between two arithmetic expressions

        expression : arithmetic_expr ((EQUAL
                                     | NOT_EQUAL
                                     | LESS_THAN
                                     | LESS_EQUAL
                                     | GREATER_THAN
                                     | GREATER_EQUAL) arithmetic_expr)?
        """
        node = self.arithmetic_expr()
        if self.current_token.type in (
            EQUAL,
            NOT_EQUAL,
            LESS_THAN,
            LESS_EQUAL,
            GREATER_THAN,
            GREATER_EQUAL,
        ):
            op = self.current_token
            self.eat(op.type)
            right = self.arithmetic_expr()
            node = BinaryOperation(op.type, node, right)
        return node

    def arithmetic_expr(self):
        """
        Returns an value from the result of the +/- arithmetic expressions

        arithmetic_expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)

            right = self.term()
            node = BinaryOperation(op.type, node, right)
        return node
    
    # parser term precedence
    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, FLOAT_DIV, INTEGER_DIV):
            op = self.current_token
            if op.type == MUL:
                self.eat(MUL) 
            elif op.type == FLOAT_DIV:
                self.eat(FLOAT_DIV) 
            elif op.type == INTEGER_DIV:
                self.eat(INTEGER_DIV) 

            right = self.factor()
            node = BinaryOperation(op.type, node, right)
        return node

    
    def factor(self):
        """
        Returns an integer value for the current token and then eats it

        OR

        Returns the integer value of the expression in the parentheses and eats the parentheses

        factor : (PLUS | MINUS) factor
               | INTEGER_CONST
               | REAL_CONST
               | BOOLEAN_CONST
               | LPAREN expression RPAREN
               | variable
        """
        token = self.current_token
        if token.type in (PLUS, MINUS):
            self.eat(token.type)                       # consume the unary operator
            child = self.factor()                      # then parse the operand
            return UnaryOperation(token.type, child)
        
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expression()
            self.eat(RPAREN)
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            node = IntegerNode(token.value)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            node = RealNode(token.value)
        elif token.type == BOOLEAN_CONST:
            self.eat(BOOLEAN_CONST)
            node = BooleanNode(token.value)
        else:
            node = self.variable()
        return node
    
    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node
