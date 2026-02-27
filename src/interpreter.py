from nodes import *

class NodeVisitor():
    """Base visitor class, not used directly but can be inherited from for more complex visitors"""

    def visit_Program(self,node):
        "visits root node"
        return self.visit(node.block)
    
    def visit_Block(self,node):
        for declaration in node.declarations:
            self.visit(declaration)
        return self.visit(node.compound_statement)
    
    def visit_VarDecl(self,node):
        var_name = node.var_node.name
        var_type = self.visit(node.type_node)
        return var_type
    
    def visit_Type(self,node):
        return node.value
    
    def visit_Compound(self,node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self,node):
        self.visit(node.right)

    def visit_Var(self,node):
        return None
    
    def visit_NoOp(self, node):
        return None
    
    def visit_BinaryOperation(self,node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOperation(self,node):
        return self.visit(node.child)
    
    def visit_IntegerNode(self,node):
        return node.value

    def visit_RealNode(self,node):
        return node.value
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)    
    
class Interpreter(NodeVisitor):
    """Base visitor class, not used directly but can be inherited from for more complex visitors"""
    def __init__(self):
        self.GLOBAL_SCOPE = {}
        
    def visit_Assign(self,node):
        var_name = node.left.name
        val = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = val
        return val

    def visit_Var(self,node):
        if node.name not in self.GLOBAL_SCOPE:
            raise InterpreterError(f"Variable {node.name} is not defined")
        return self.GLOBAL_SCOPE[node.name]

    def visit_BinaryOperation(self,node):
        leftvalue = self.visit(node.left)
        rightvalue = self.visit(node.right)
        if node.value == PLUS:
            return leftvalue + rightvalue
        elif node.value == MINUS:
            return leftvalue - rightvalue
        elif node.value == MUL:
            return leftvalue * rightvalue
        elif node.value == FLOAT_DIV:
            return leftvalue / rightvalue
        elif node.value == INTEGER_DIV:
            return leftvalue // rightvalue
        return None

    def visit_UnaryOperation(self,node):
        childvalue = self.visit(node.child) if node.child is not None else None
        if node.value == PLUS:
            return childvalue
        elif node.value == MINUS:
            return -childvalue
        return None