from tokens import *

class Node():
    "A node is anything in the grammar that is capitalised"
    @property
    def line(self):
        token = getattr(self, "token", None)
        return getattr(token, "line", None)

    @property
    def column(self):
        token = getattr(self, "token", None)
        return getattr(token, "column", None)

    def __repr__(self):
        return self.__str__()

class Program(Node):
    """The root node of the AST, which holds a block node"""
    def __init__(self, name, block):
        self.name = name
        self.block = block

    def __str__(self):
        return f"Program(name={getattr(self.name, 'name', None)}, block={type(self.block).__name__})"

class Block(Node):
    """Holds a list of declarations and a compound statement"""
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

    def __str__(self):
        return f"Block(declarations={len(self.declarations)}, compound_statement={type(self.compound_statement).__name__})"

class VarDecl(Node):
    """Holds a variable node and a type node"""
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def __str__(self):
        return f"VarDecl(var_name={getattr(self.var_node, 'name', None)}, type={getattr(self.type_node, 'value', None)})"

class ProcDecl(Node):
    def __init__(self, token, name, params, block):
        self.token = token
        self.name = name
        self.params = params
        self.block = block

    def __str__(self):
        return f"ProcDecl(name={self.name}, params={len(self.params)}, block={type(self.block).__name__})"

class ProcedureCall(Node):
    def __init__(self, token, name, params):
        self.token = token
        self.name = name
        self.params = params

    def __str__(self):
        return f"ProcedureCall(name={self.name}, params={len(self.params)})"

class Param(Node):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def __str__(self):
        return f"Param(var_name={getattr(self.var_node, 'name', None)}, type={getattr(self.type_node, 'value', None)})"

class Type(Node):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f"Type(value={self.value})"

class Compound(Node):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []

    def __str__(self):
        return f"Compound(children={len(self.children)})"

class Assign(Node):
    """Represents an assignment statement.\n 
    Left variable is for storing a Var node,\n
    its right variable is for storing a node returned by the expr parser method\n
    """
    def __init__(self, value = None, left = None, right = None):
        self.left = left
        self.token = value
        self.right = right
    
    def __str__(self):
        op = self.token.type if self.token is not None else None
        right_type = type(self.right).__name__ if self.right is not None else None
        return f"Assign(left={getattr(self.left, 'name', None)}, op={op}, right={right_type})"
    
class Var(Node):
    """
    Defined with the variable name whose value is to be returned\n
    When visited returns the value associated with the variable name in GLOBAL_SCOPE
    Raises InterpreterError if the variable isn't found in GLOBAL_SCOPE
    """
    def __init__(self, token):
        self.token = token
        self.name = token.value
    
    def __str__(self):
        return f"Var(name={self.name})"
    
class NoOp(Node):
    "Just doesn't do anything on visit, equivalent to ε in compiler theory"
    def __str__(self):
        return "NoOp()"

class If(Node):
    "Represents an IF ... THEN ... ELSE statement. No ELSE by default"
    def __init__(self, token, condition, true_statement, false_statement = None):
        self.token = token
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement
    
    def __str__(self):
        false_type = type(self.false_statement).__name__ if self.false_statement is not None else None
        return f"If(condition={type(self.condition).__name__}, true={type(self.true_statement).__name__}, false={false_type})"

class While(Node):
    "Represents a WHILE ... DO statement"
    def __init__(self, token, condition, statement):
        self.token = token
        self.condition = condition
        self.statement = statement

    def __str__(self):
        return f"While(condition={type(self.condition).__name__}, statement={type(self.statement).__name__})"
  
class WriteLn(Node):
    "Represents a WRITELN statement"
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def __str__(self):
        return f"WriteLn(expression={type(self.expression).__name__})"

class BinaryOperation(Node):
    """
    Returns the result of the operation upon postorder visit\n
    Handles arithmetic and comparison operators such as
    +, -, *, /, DIV, =, <>, <, <=, >, >=
    """
    def __init__(self, token, left, right):
        self.token = token
        self.value = token.type
        self.left = left
        self.right = right
    
    def __str__(self):
        left_type = type(self.left).__name__ if self.left is not None else None
        right_type = type(self.right).__name__ if self.right is not None else None
        return f"BinaryOperation(op={self.value}, left={left_type}, right={right_type})"

class UnaryOperation(Node):
    def __init__(self, token = None,child = None):
        self.token = token
        self.value = token.type if token is not None else None
        self.child = child

    def __str__(self):
        child_type = type(self.child).__name__ if self.child is not None else None
        return f"UnaryOperation(op={self.value}, child={child_type})"

class IntegerNode(Node):
    "Represents an integer and returns its value"
    def __init__(self, token):
        self.token = token
        value = token.value
        self.value = int(value)
        self.type = INTEGER
    
    def __str__(self):
        return f"IntegerNode(value={self.value})"
    
class RealNode(Node):
    "Represents a real and returns its value"
    def __init__(self, token):
        self.token = token
        value = token.value
        self.value = float(value)
        self.type = REAL
    
    def __str__(self):
        return f"RealNode(value={self.value})"
    
class BooleanNode(Node):
    "Represents a bool and returns its value"
    def __init__(self, token):
        self.token = token
        value = token.value
        self.value = bool(value)
        self.type = BOOLEAN
    
    def __str__(self):
        return f"BooleanNode(value={self.value})"
