from tokens import *
from visitor import NodeVisitor

class SemanticAnalyser(NodeVisitor):
    """
    The semantic analyser checks types and populates the symbol table before the AST is passed to the interpreter to be run.\n
    The methods in the semantic analyser are mostly concerned with types.\n
    """
    def __init__(self):
        self.symtab = SymbolTable()
        self.integer_type = self.symtab.lookup(INTEGER)
        self.real_type = self.symtab.lookup(REAL)
        self.boolean_type = self.symtab.lookup(BOOLEAN)

    def _is_numeric(self, type_symbol):
        return type_symbol in (self.integer_type, self.real_type)

    def _assignment_compatible(self, left_type, right_type):
        # Allow widening assignment: INTEGER expression into REAL variable.
        if left_type == right_type:
            return True
        if left_type == self.real_type and right_type == self.integer_type:
            return True
        return False

    def visit_VarDecl(self, node):
        type_symbol = self.visit(node.type_node)
        var_name = node.var_node.name
        if self.symtab.lookup(var_name) is not None:
            raise SemanticError(f"Duplicate declaration of variable {var_name}")
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)
        return var_symbol

    def visit_Type(self, node):
        type_symbol = self.symtab.lookup(node.value)
        if type_symbol is None:
            raise SemanticError(f"Unknown type {node.value}")
        return type_symbol

    def visit_IntegerNode(self,node):
        return self.integer_type

    def visit_RealNode(self,node):
        return self.real_type
    
    def visit_BooleanNode(self,node):
        return self.boolean_type

    def visit_BinaryOperation(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        arithmetic_ops = (PLUS, MINUS, MUL, FLOAT_DIV, INTEGER_DIV)
        comparison_ops = (
            EQUAL,
            NOT_EQUAL,
            LESS_THAN,
            LESS_EQUAL,
            GREATER_THAN,
            GREATER_EQUAL,
        )

        if node.value in arithmetic_ops:
            if not (self._is_numeric(left_type) and self._is_numeric(right_type)):
                raise SemanticError(f"Type Error: invalid operands for {node.value}: {left_type}, {right_type}")

            if node.value == INTEGER_DIV:
                if left_type != self.integer_type or right_type != self.integer_type:
                    raise SemanticError("Type Error: DIV requires INTEGER operands")
                return self.integer_type

            if node.value == FLOAT_DIV:
                return self.real_type

            if left_type == self.integer_type and right_type == self.integer_type:
                return self.integer_type
            return self.real_type

        if node.value in comparison_ops:
            if not (self._is_numeric(left_type) and self._is_numeric(right_type)):
                raise SemanticError(f"Type Error: invalid operands for {node.value}: {left_type}, {right_type}")
            return self.boolean_type

        raise SemanticError(f"Unknown binary operator {node.value}")

    def visit_UnaryOperation(self, node):
        child_type = self.visit(node.child)
        if not self._is_numeric(child_type):
            raise SemanticError(f"Type Error: invalid unary operand type {child_type}")
        return child_type
    
    def visit_Assign(self, node):
        var_name = node.left.name
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise SemanticError(f"Variable {var_name} is not defined")
        right_type = self.visit(node.right)
        if not self._assignment_compatible(var_symbol.type, right_type):
            raise SemanticError(f"Type Error: cannot assign {right_type} to {var_symbol.type} ({var_name})")
        return None
    
    def visit_If(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != self.boolean_type:
            raise SemanticError("Type Error: IF condition must evaluate to BOOLEAN")

        self.visit(node.true_statement)

        if node.false_statement is not None:
            self.visit(node.false_statement)

    def visit_While(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != self.boolean_type:
            raise SemanticError("Type Error: WHILE condition must evaluate to BOOLEAN")
        
        self.visit(node.statement)

    def visit_Var(self,node):
        var_name = node.name
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise SemanticError(f"Variable {var_name} is not defined")
        return var_symbol.type
