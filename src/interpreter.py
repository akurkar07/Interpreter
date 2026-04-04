from tokens import *
from visitor import NodeVisitor


class Interpreter(NodeVisitor):
    """Base visitor class, not used directly but can be inherited from for more complex visitors"""
    def __init__(self):
        self.GLOBAL_SCOPE = {}

    def runtime_error(self, message, node):
        raise InterpreterError(message, node.line, node.column)
        
    def visit_Assign(self,node):
        var_name = node.left.name
        val = self.visit(node.right)
        self.GLOBAL_SCOPE[var_name] = val
        return val
    
    def visit_If(self,node):
        condition = self.visit(node.condition)
        if condition: 
            self.visit(node.true_statement)
        elif node.false_statement is not None:
            self.visit(node.false_statement)

    def visit_While(self, node):
        while self.visit(node.condition):
           self.visit(node.statement)

    def visit_WriteLn(self, node):
        print(self.visit(node.expression))

    def visit_Var(self,node):
        if node.name not in self.GLOBAL_SCOPE:
            self.runtime_error(f"Variable {node.name} is not defined", node)
        return self.GLOBAL_SCOPE[node.name]

    def visit_BinaryOperation(self,node):
        leftvalue = self.visit(node.left)
        rightvalue = self.visit(node.right)
        if node.value == PLUS:
            return leftvalue + rightvalue
        if node.value == MINUS:
            return leftvalue - rightvalue
        if node.value == MUL:
            return leftvalue * rightvalue
        if node.value == FLOAT_DIV:
            try:
                return leftvalue / rightvalue
            except ZeroDivisionError:
                self.runtime_error("Division by zero", node)
        if node.value == INTEGER_DIV:
            try:
                return leftvalue // rightvalue
            except ZeroDivisionError:
                self.runtime_error("Division by zero", node)
        if node.value == EQUAL:
            return leftvalue == rightvalue
        if node.value == NOT_EQUAL:
            return leftvalue != rightvalue
        if node.value == LESS_THAN:
            return leftvalue < rightvalue
        if node.value == LESS_EQUAL:
            return leftvalue <= rightvalue
        if node.value == GREATER_THAN:
            return leftvalue > rightvalue
        if node.value == GREATER_EQUAL:
            return leftvalue >= rightvalue
        return None

    def visit_UnaryOperation(self,node):
        childvalue = self.visit(node.child) if node.child is not None else None
        if node.value == PLUS:
            return childvalue
        elif node.value == MINUS:
            return -childvalue
        return None
