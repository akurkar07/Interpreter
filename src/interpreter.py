from tokens import *
from visitor import NodeVisitor


class Interpreter(NodeVisitor):
    """Executes the program after it has been type-checked by the SemAnalyser"""
    def __init__(self):
        self.scopes = [{}]  # first empty dict is GLOBAL
        self.procedures = {}
        self.functions = {}

    def runtime_error(self, message, node):
        raise InterpreterError(message, node.line, node.column)

    def visit_Assign(self, node):
        var_name = node.left.name
        val = self.visit(node.right)
        self.scopes[-1][var_name] = val
        return val

    def visit_ProcedureCall(self, node):
        proc_decl = self.procedures[node.name]

        call_scope = {}

        for param_node, arg_node in zip(proc_decl.params, node.params): # zips into (param, argument)
            arg_value = self.visit(arg_node)
            param_name = param_node.var_node.name
            call_scope[param_name] = arg_value

        self.scopes.append(call_scope)
        self.visit(proc_decl.block)
        self.scopes.pop()

    def visit_FunctionCall(self, node):
        func_decl = self.functions[node.name]

        call_scope = {}

        for param_node, arg_node in zip(func_decl.params, node.params): # zips into (param, argument)
            arg_value = self.visit(arg_node)
            param_name = param_node.var_node.name
            call_scope[param_name] = arg_value

        self.scopes.append(call_scope)
        self.visit(func_decl.block)
        result = self.scopes[-1][func_decl.name]
        self.scopes.pop()
        return result

    def visit_If(self, node):
        condition = self.visit(node.condition)
        if condition:
            self.visit(node.true_statement)
        elif node.false_statement is not None:
            self.visit(node.false_statement)

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.statement)

    def visit_For(self, node):
        start_value = self.visit(node.start_expr)
        self.scopes[-1][node.var.name] = start_value
        end_value = self.visit(node.end_expr)
        direction = 1 if node.direction == TO else -1
        for i in range(start_value, end_value + direction, direction): # start_val TO end_val inclusive on TO, exclusive on DOWNTO 
            self.scopes[-1][node.var.name] = i
            self.visit(node.statement)

    def visit_WriteLn(self, node):
        print(self.visit(node.expression))

    def visit_Write(self, node):
        print(self.visit(node.expression), end='')

    def visit_ProcDecl(self, node):
        self.procedures[node.name] = node
        return None
    
    def visit_FuncDecl(self, node):
        self.functions[node.name] = node
        return None

    def visit_BinaryOperation(self, node):
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

    def visit_UnaryOperation(self, node):
        childvalue = self.visit(node.child) if node.child is not None else None
        if node.value == PLUS:
            return childvalue
        if node.value == MINUS:
            return -childvalue
        return None

    def visit_Var(self, node):
        for scope in reversed(self.scopes):
            if node.name in scope:
                return scope[node.name]

        self.runtime_error(f"Variable {node.name} is not defined", node)
