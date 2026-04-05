from tokens import *
from visitor import NodeVisitor

class SemanticAnalyser(NodeVisitor):
    """
    The semantic analyser checks types and populates the symbol table before the AST is passed to the interpreter to be run.\n
    The methods in the semantic analyser are mostly concerned with types.\n
    """
    def __init__(self):
        self.current_scope = SymbolTable()
        self.integer_type = self.current_scope.lookup(INTEGER)
        self.real_type = self.current_scope.lookup(REAL)
        self.boolean_type = self.current_scope.lookup(BOOLEAN)

    def semantic_error(self, message, node):
        raise SemanticError(message, node.line, node.column)

    def _is_numeric(self, type_symbol):
        return type_symbol in (self.integer_type, self.real_type)

    def _assignment_compatible(self, left_type, right_type):
        # Allow widening assignment: INTEGER expression into REAL variable.
        if left_type == right_type:
            return True
        if left_type == self.real_type and right_type == self.integer_type:
            return True
        return False

    def visit_Type(self, node):
        type_symbol = self.current_scope.lookup(node.value)
        if type_symbol is None:
            self.semantic_error(f"Unknown type {node.value}", node)
        return type_symbol

    def visit_VarDecl(self, node):
        type_symbol = self.visit(node.type_node)
        var_name = node.var_node.name
        if self.current_scope.lookup(var_name,current_scope_only=True) is not None:
            self.semantic_error(f"Duplicate declaration of variable {var_name}", node.var_node)
        var_symbol = VarSymbol(var_name, type_symbol)
        self.current_scope.define(var_symbol)
        return var_symbol
    
    def visit_ProcDecl(self, node):
        proc_name = node.name
        if self.current_scope.lookup(proc_name) is not None:
            self.semantic_error(f"Duplicate declaration of procedure {proc_name}", node.token)
        
        params = node.params
        proc_symbol = ProcSymbol(proc_name, params)
        self.current_scope.define(proc_symbol)

        outer_scope = self.current_scope
        self.current_scope = SymbolTable(proc_name, outer_scope) # Here we switch the current scope which persists through visiting AST children
        for param in node.params:
            self.visit(param)

        self.visit(node.block)
        self.current_scope = outer_scope
        return proc_symbol

    def visit_Param(self, node):
        type_symbol = self.visit(node.type_node)
        var_name = node.var_node.name
        if self.current_scope.lookup(var_name, current_scope_only=True) is not None:
            self.semantic_error(f"Duplicate declaration of parameter {var_name}", node.var_node)
        var_symbol = VarSymbol(var_name, type_symbol)
        self.current_scope.define(var_symbol)
        return var_symbol
    
    def visit_Assign(self, node):
        var_name = node.left.name
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.semantic_error(f"Variable {var_name} is not defined", node.left)
        right_type = self.visit(node.right)
        if not self._assignment_compatible(var_symbol.type, right_type):
            self.semantic_error(f"Type Error: cannot assign {right_type} to {var_symbol.type} ({var_name})", node)
        return None

    def visit_ProcedureCall(self, node):
        proc_symbol = self.current_scope.lookup(node.name)
        if proc_symbol is None:
            self.semantic_error(f"Procedure {node.name} is not defined", node)

        if len(proc_symbol.params) != len(node.params):
            self.semantic_error(
                f"Procedure {node.name} expected {len(proc_symbol.params)} arguments, got {len(node.params)}",
                node
            )

        for arg_node in node.params:
            self.visit(arg_node)

        return None

    def visit_If(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != self.boolean_type:
            self.semantic_error("Type Error: IF condition must evaluate to BOOLEAN", node)

        self.visit(node.true_statement)

        if node.false_statement is not None:
            self.visit(node.false_statement)

    def visit_While(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != self.boolean_type:
            self.semantic_error("Type Error: WHILE condition must evaluate to BOOLEAN", node)

        self.visit(node.statement)

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
                self.semantic_error(f"Type Error: invalid operands for {node.value}: {left_type}, {right_type}", node)

            if node.value == INTEGER_DIV:
                if left_type != self.integer_type or right_type != self.integer_type:
                    self.semantic_error("Type Error: DIV requires INTEGER operands", node)
                return self.integer_type

            if node.value == FLOAT_DIV:
                return self.real_type

            if left_type == self.integer_type and right_type == self.integer_type:
                return self.integer_type
            return self.real_type

        if node.value in comparison_ops:
            if not (self._is_numeric(left_type) and self._is_numeric(right_type)):
                self.semantic_error(f"Type Error: invalid operands for {node.value}: {left_type}, {right_type}", node)
            return self.boolean_type

        self.semantic_error(f"Unknown binary operator {node.value}", node)

    def visit_UnaryOperation(self, node):
        child_type = self.visit(node.child)
        if not self._is_numeric(child_type):
            self.semantic_error(f"Type Error: invalid unary operand type {child_type}", node)
        return child_type

    def visit_IntegerNode(self,node):
        return self.integer_type

    def visit_RealNode(self,node):
        return self.real_type

    def visit_BooleanNode(self,node):
        return self.boolean_type

    def visit_Var(self,node):
        var_name = node.name
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.semantic_error(f"Variable {var_name} is not defined", node)
        return var_symbol.type
