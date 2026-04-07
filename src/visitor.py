from nodes import *


class NodeVisitor():
    """Base visitor class, not used directly but can be inherited from for more complex visitors"""

    def visit_Program(self, node):
        "visits root node"
        return self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        return self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        return self.visit(node.type_node)

    def visit_ProcDecl(self, node):
        for param in node.params:
            self.visit(param)
        return self.visit(node.block)
    
    def visit_FuncDecl(self, node):
        for param in node.params:
            self.visit(param)
        return self.visit(node.block)
    
    def visit_Param(self, node):
        return self.visit(node.type_node)

    def visit_Type(self, node):
        return node.value

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        self.visit(node.right)

    def visit_ProcedureCall(self, node):
        return None
    
    def visit_FunctionCall(self, node):
        return None

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.true_statement)
        if node.false_statement is not None:
            self.visit(node.false_statement)

    def visit_While(self, node):
        self.visit(node.condition)
        self.visit(node.statement)

    def visit_For(self, node):
        self.visit(node.var)
        self.visit(node.start_expr)
        self.visit(node.end_expr)
        self.visit(node.statement)

    def visit_Write(self, node):
        self.visit(node.expression)

    def visit_WriteLn(self, node):
        self.visit(node.expression)

    def visit_NoOp(self, node):
        return None

    def visit_BinaryOperation(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOperation(self, node):
        return self.visit(node.child)

    def visit_IntegerNode(self, node):
        return node.value

    def visit_RealNode(self, node):
        return node.value

    def visit_BooleanNode(self, node):
        return node.value
    
    def visit_StringNode(self, node):
        return node.value

    def visit_Var(self, node):
        return None

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
