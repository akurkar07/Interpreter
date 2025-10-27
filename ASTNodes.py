from tokens import *

class Program():
    """The root node of the AST, which holds a block node"""
    def __init__(self, name, block):
        self.name = name
        self.block = block
    
    def visit(self):
        return self.block.visit()
    
class Block():
    """Holds a list of declarations and a compound statement"""
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement
    
    def visit(self):
        for declaration in self.declarations:
            declaration.visit()
        return self.compound_statement.visit()
    
class VarDecl():
    """Holds a variable node and a type node"""
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node
    
    def visit(self):
        var_name = self.var_node.name
        var_type = self.type_node.visit()
        SYMBOL_TABLE[var_name] = var_type
        return var_type
    
class Type():
    def __init__(self, token):
        self.token = token
        self.value = token.value
    
    def visit(self):
        return self.value

class Compound():
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []
    
    def visit(self):
        last = None
        for child in self.children:
            last = child.visit()
        return last

class Assign():
    """Represents an assignment statement.\n 
    Left variable is for storing a Var node,\n
    its right variable is for storing a node returned by the expr parser method\n
    When visited it checks type is correct (TEMPORARY) and adds the value to global scope
    """
    def __init__(self, value = None, left = None, right = None):
        self.left = left
        self.token = self.value = value
        self.right = right
    
    def visit(self):
        var_name = self.left.name         # get identifier string
        val = self.right.visit()          # evaluate RHS
        if SYMBOL_TABLE[var_name] != typechecker(val):
            raise InterpreterError(f"Variable {var_name} ({SYMBOL_TABLE[var_name]}) cannot hold value {val} ({typechecker(val)}).")
        GLOBAL_SCOPE[var_name] = val      # store in global env
        return val
    
    def __str__(self):
        return f"Assign | {self.left.name} := {self.right.visit()}"
    
    def __repr__(self):
        return self.__str__()

class Var:
    """
    Defined with the variable name whose value is to be returned\n
    When visited returns the value associated with the variable name in GLOBAL_SCOPE
    Raises InterpreterError if the variable isn't found in GLOBAL_SCOPE
    """
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def visit(self):
        if self.name not in GLOBAL_SCOPE:
            # Use the project's custom runtime exception so callers can
            # distinguish interpreter runtime errors from other NameError uses.
            raise InterpreterError(f"Variable {self.name} is not defined")
        return GLOBAL_SCOPE[self.name]
    
    def __str__(self):
        return f"Var | Name: {self.name} | Value: {self.token}"
    
    def __repr__(self): 
        return self.__str__()
    

class NoOp():
    "Just doesn't do anything on visit, equivalent to ε in compiler theory"
    def visit(self):
        pass
  
class BinaryOperation():
    """
    Returns the result of the operation upon postorder visit\n
    Handles +, -, *, /, div
    """
    def __init__(self, op, left, right):
        self.value = op
        self.left = left
        self.right = right

    def visit(self):
        #preorder
        leftvalue = self.left.visit()
        #inorder
        rightvalue = self.right.visit()
        #postorder
        if self.value == '+':
            return leftvalue + rightvalue
        elif self.value == '-':
            return leftvalue - rightvalue
        elif self.value == '*':
            return leftvalue * rightvalue
        elif self.value == '/':
            return leftvalue / rightvalue
        elif self.value == 'div':
            return leftvalue // rightvalue
        return None
    
    def __str__(self):
        return f"BinaryOperation | Value: {self.value} | Left: {self.left} | Right: {self.right}"

    def __repr__(self):
        return self.__str__()

class UnaryOperation():
    def __init__(self, value = None,child = None):
        self.value = value
        self.child = child

    def visit(self):
        """
        Returns the result of the operation upon postorder visit
        Handles +child, -child
        """
        #preorder
        if self.child is not None:
            childvalue = self.child.visit()
        #postorder
        if self.value == "+":
            return childvalue
        elif self.value == "-":
            return -childvalue

    def __str__(self):
        return f"UnaryOperation | Value: {self.value} | Child: {self.child}"

    def __repr__(self):
        return self.__str__()

class IntegerNode():
    "Represents an integer and returns its value"
    def __init__(self, value):
        self.value = int(value)
        self.type = INTEGER
    
    def visit(self):
        return self.value
    
    def __str__(self):
        return f"IntegerNode | Value: {self.value}"
    
    def __repr__(self):
        return self.__str__()
    
class RealNode():
    "Represents a real and returns its value"
    def __init__(self, value):
        self.value = float(value)
        self.type = REAL
    
    def visit(self):
        return self.value
    
    def __str__(self):
        return f"RealNode | Value: {self.value}"
    
    def __repr__(self):
        return self.__str__()