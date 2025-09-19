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
        GLOBAL_SCOPE[var_name] = var_type
        return var_type
    
class Type():
    def __init__(self, token):
        self.token = token
        self.value = token.value

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
    "Represents an assignment statement. Its left variable is for storing a Var node and its right variable is for storing a node returned by the expr parser method"
    def __init__(self, value = None, left = None, right = None):
        self.left = left
        self.token = self.value = value
        self.right = right
    
    def visit(self):
        var_name = self.left.name         # get identifier string
        val = self.right.visit()          # evaluate RHS
        GLOBAL_SCOPE[var_name] = val      # store in global env
        return val

class Var:
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def visit(self):
        if self.name not in GLOBAL_SCOPE:
            raise NameError(f"Variable {self.name} is not defined")
        return GLOBAL_SCOPE[self.name]

class NoOp():
    def visit(self):
        pass

class BinaryOperation():
    """
    Holds the arithmetic operations, that have two children, whether they are integers or other binary operations.\n
    Returns the result of the operation on visit.
    """
    def __init__(self, value = None,left = None, right = None):
        self.value = value
        if left in ('+', '-', '*', '/'):
            self.left = BinaryOperation(left)
        elif type(left) == int:
            self.left = IntegerNode(left)
        else:
            self.left = left

        if right in ('+', '-', '*', '/'):
            self.right = BinaryOperation(right)
        elif type(right) == int:
            self.right = IntegerNode(right)
        else:
            self.right = right

    def visit(self):
        """
        Returns the result of the operation upon postorder visit
        """
        #preorder
        if self.left is not None:
            leftvalue = self.left.visit()
        #in-order
        if self.right is not None:
            rightvalue = self.right.visit()
        #postorder
        if self.value == "+":
            return leftvalue + rightvalue
        elif self.value == "-":
            return leftvalue - rightvalue
        elif self.value == "*":
            return leftvalue * rightvalue
        # evaluator
        elif self.value == '/':
            return leftvalue / rightvalue
        elif self.value == 'div':
            return leftvalue // rightvalue
        else:
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
    def __init__(self, value):
        self.value = int(value)
    
    def visit(self):
        return self.value
    
    def __str__(self):
        return f"IntegerNode | Value: {self.value}"
    
    def __repr__(self):
        return self.__str__()
    
class RealNode():
    def __init__(self, value):
        self.value = float(value)
    
    def visit(self):
        return self.value
    
    def __str__(self):
        return f"RealNode | Value: {self.value}"
    
    def __repr__(self):
        return self.__str__()